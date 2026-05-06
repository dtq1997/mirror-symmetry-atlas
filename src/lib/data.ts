import fs from "fs";
import path from "path";
import yaml from "js-yaml";
import type {
  Person,
  Concept,
  Paper,
  TimelineEvent,
  ConferenceSeries,
  ConferenceEvent,
  Connection,
  Institution,
  OpenProblem,
  Seminar,
  DataStore,
  AckMention,
} from "./types";
import { canonicalPaperId } from "./paper-identity";

const DATA_DIR = path.join(process.cwd(), "data");

// ===== Generic YAML loader =====

function readYaml<T>(filePath: string): T {
  const content = fs.readFileSync(filePath, "utf-8");
  return yaml.load(content) as T;
}

function readYamlDir<T>(dirPath: string): T[] {
  const fullDir = path.join(DATA_DIR, dirPath);
  if (!fs.existsSync(fullDir)) return [];
  return fs
    .readdirSync(fullDir)
    // Skip auxiliary/index files (e.g. _faculty_urls.yaml, _review_queue.yaml)
    .filter((f) => !f.startsWith("_"))
    .filter((f) => f.endsWith(".yaml") || f.endsWith(".yml"))
    .map((f) => readYaml<T>(path.join(fullDir, f)));
}

// ===== People =====

export function getAllPeople(): Person[] {
  return readYamlDir<Person>("people").map((p) => ({
    ...p,
    career_timeline: p.career_timeline || [],
    research_areas: p.research_areas || [],
    students: p.students || [],
    key_collaborators: p.key_collaborators || [],
    activity: p.activity || {},
    external_ids: p.external_ids || {},
    links: p.links || {},
    tags: p.tags || [],
  }));
}

export function getPeopleMap(): Map<string, Person> {
  const map = new Map<string, Person>();
  for (const p of getAllPeople()) {
    map.set(p.slug, p);
  }
  return map;
}

export function getPerson(slug: string): Person | undefined {
  return getPeopleMap().get(slug);
}

// ===== Concepts =====

export function getAllConcepts(): Concept[] {
  return readYamlDir<Concept>("concepts").map((c) => ({
    ...c,
    introduced_by: c.introduced_by || [],
    prerequisites: c.prerequisites || [],
    leads_to: c.leads_to || [],
    related: c.related || [],
    key_people: c.key_people || [],
    key_papers: c.key_papers || [],
  }));
}

export function getConceptsMap(): Map<string, Concept> {
  const map = new Map<string, Concept>();
  for (const c of getAllConcepts()) {
    map.set(c.slug, c);
  }
  return map;
}

// ===== Papers =====

export function getAllPapers(): Paper[] {
  const papers: Paper[] = [];
  const papersDir = path.join(DATA_DIR, "papers");
  if (!fs.existsSync(papersDir)) return papers;

  for (const f of fs.readdirSync(papersDir).filter((f) => f.endsWith(".yaml"))) {
    const data = readYaml<{ papers?: Paper[] }>(path.join(papersDir, f));
    if (data.papers) {
      papers.push(
        ...data.papers.map((p) => ({
          ...p,
          authors: p.authors || [],
          authors_raw: p.authors_raw || [],
        }))
      );
    }
  }
  return papers;
}

// ===== Timeline =====

export function getAllTimelineEvents(): TimelineEvent[] {
  const eventsFile = path.join(DATA_DIR, "timeline", "events.yaml");
  if (!fs.existsSync(eventsFile)) return [];
  const data = readYaml<{ events?: TimelineEvent[] }>(eventsFile);
  return (data.events || []).map((e) => ({
    ...e,
    people: e.people || [],
    concepts: e.concepts || [],
    papers: e.papers || [],
  }));
}

// ===== Conferences =====

export function getAllConferenceSeries(): ConferenceSeries[] {
  const recurringFile = path.join(DATA_DIR, "conferences", "recurring.yaml");
  if (!fs.existsSync(recurringFile)) return [];
  const data = readYaml<{ series?: ConferenceSeries[] }>(recurringFile);
  return data.series || [];
}

export function getAllConferenceEvents(): ConferenceEvent[] {
  const events: ConferenceEvent[] = [];
  const confDir = path.join(DATA_DIR, "conferences");
  if (!fs.existsSync(confDir)) return events;

  for (const f of fs.readdirSync(confDir).filter((f) => f.startsWith("events-"))) {
    const data = readYaml<{ events?: ConferenceEvent[] }>(path.join(confDir, f));
    if (data.events) events.push(...data.events);
  }
  return events;
}

// ===== Connections =====

export function getAllConnections(): Connection[] {
  const connections: Connection[] = [];
  const connDir = path.join(DATA_DIR, "connections");
  if (fs.existsSync(connDir)) {
    for (const f of fs.readdirSync(connDir).filter((f) => f.endsWith(".yaml"))) {
      const data = readYaml<{ edges?: Connection[] }>(path.join(connDir, f));
      if (data.edges) connections.push(...data.edges);
    }
  }

  // Auto-derive coauthor edges from key_collaborators when both endpoints are built.
  // **Publications-derived edges OVERRIDE declared coauthor edges** because the
  // declared yaml had hand-typed weights that drift out of sync with reality.
  // We never trust hand-typed papers_count for the coauthor count.
  const declaredCoauthor = new Set<string>();
  // Build set of pairs declared in connections/coauthorship.yaml (so we
  // can REMOVE them when we have a publications-derived alternative).
  for (const c of connections) {
    if (c.type !== "coauthor") continue;
    const k = [c.source, c.target].sort().join("|");
    declaredCoauthor.add(k);
  }

  const people = getAllPeople();
  const builtSlugs = new Set(people.map((p) => p.slug));
  const derivedSeen = new Set<string>();

  // SSOT for coauthorship: a pair (a, b) shares a paper P **iff** P appears in
  // BOTH a.publications AND b.publications (matched by canonical paper id —
  // doi → arxiv-id → folded title). We do NOT infer slug membership from raw
  // English names in coauthor fields; that produced massive false positives
  // when distinct authors shared a name (e.g. multiple "Ao Li").
  //
  // If a paper is genuinely coauthored but only one side's yaml recorded it,
  // there will be no edge — that's the correct fail-closed behavior. Fix it
  // upstream by adding the paper to the other yaml.
  type CoauthoredPaper = { id: string; title: string; year: number; doi?: string; journal?: string; primary_category?: string };
  type PubRow = { id: string; title: string; year: number; coauthors?: string[]; doi?: string; journal?: string; primary_category?: string };
  // canonical paper id → list of (slug, pub) that own this paper
  const paperOwners = new Map<string, Array<{ slug: string; pub: PubRow }>>();
  for (const p of people) {
    const pubs = (p as unknown as { publications?: PubRow[] }).publications;
    if (!pubs) continue;
    for (const pub of pubs) {
      const cid = canonicalPaperId({ id: pub.id, doi: pub.doi, title: pub.title });
      if (!cid) continue;
      const list = paperOwners.get(cid) ?? [];
      list.push({ slug: p.slug, pub });
      paperOwners.set(cid, list);
    }
  }

  function pickRicher(a: PubRow, b: PubRow): PubRow {
    // Prefer the side that has journal/doi (= "published" version).
    const aPub = !!(a.journal || a.doi);
    const bPub = !!(b.journal || b.doi);
    if (aPub && !bPub) return a;
    if (bPub && !aPub) return b;
    return a;
  }

  const pairPapers = new Map<string, { published: CoauthoredPaper[]; preprint: CoauthoredPaper[] }>();
  for (const owners of paperOwners.values()) {
    if (owners.length < 2) continue; // need both sides
    // Pick the richest record for the canonical view of this paper.
    let canon = owners[0].pub;
    for (let i = 1; i < owners.length; i++) canon = pickRicher(canon, owners[i].pub);
    const isPub = !!(canon.journal || canon.doi);
    const slugs = Array.from(new Set(owners.map((o) => o.slug)));
    for (let i = 0; i < slugs.length; i++) {
      for (let j = i + 1; j < slugs.length; j++) {
        const key = [slugs[i], slugs[j]].sort().join("|");
        const bucket = pairPapers.get(key) ?? { published: [], preprint: [] };
        const existsPub = bucket.published.some((x) => x.id === canon.id);
        const existsPre = bucket.preprint.some((x) => x.id === canon.id);
        if (existsPub || existsPre) continue;
        const row = {
          id: canon.id,
          title: canon.title,
          year: canon.year,
          doi: canon.doi,
          journal: canon.journal,
          primary_category: canon.primary_category,
        };
        if (isPub) bucket.published.push(row);
        else bucket.preprint.push(row);
        pairPapers.set(key, bucket);
      }
    }
  }

  // Emit a coauthor edge per pair with at least one shared paper.
  // These edges OVERRIDE any declared coauthor edges for the same pair,
  // because publications data is authoritative.
  const overriddenDeclared = new Set<string>();
  for (const [key, bucket] of pairPapers) {
    const [a, b] = key.split("|");
    if (derivedSeen.has(key)) continue;
    derivedSeen.add(key);
    const total = bucket.published.length + bucket.preprint.length;
    if (total === 0) continue;
    if (declaredCoauthor.has(key)) overriddenDeclared.add(key);
    const allYears = [...bucket.published, ...bucket.preprint]
      .map((p) => p.year).filter((y): y is number => typeof y === "number")
      .sort((x, y) => x - y);
    connections.push({
      source: a,
      target: b,
      type: "coauthor",
      weight: total,
      period: allYears.length ? `${allYears[0]}-${allYears[allYears.length - 1]}` : undefined,
      derived: true,
      coauthored_papers: bucket,
    } as Connection);
  }

  // Filter out the now-overridden declared coauthor edges to prevent duplicates.
  if (overriddenDeclared.size > 0) {
    for (let i = connections.length - 1; i >= 0; i--) {
      const c = connections[i];
      if (c.type !== "coauthor" || (c as Connection & {derived?: boolean}).derived) continue;
      const k = [c.source, c.target].sort().join("|");
      if (overriddenDeclared.has(k)) {
        connections.splice(i, 1);
      }
    }
  }

  // Also keep declared key_collaborators that didn't show up in publications
  // (rare: e.g. very old joint work pre-arXiv that we know about manually).
  for (const p of people) {
    for (const c of p.key_collaborators || []) {
      const other = c.person;
      if (!other || !builtSlugs.has(other) || other === p.slug) continue;
      const key = [p.slug, other].sort().join("|");
      if (declaredCoauthor.has(key) || derivedSeen.has(key)) continue;
      derivedSeen.add(key);
      connections.push({
        source: p.slug,
        target: other,
        type: "coauthor",
        weight: c.papers_count ?? 1,
        period: c.since ? `${c.since}-present` : undefined,
        notes: c.topic,
        derived: true,
      } as Connection);
    }
  }

  // Load acknowledgement edges (strong, ≥2) from derived/
  const ackFile = path.join(DATA_DIR, "derived", "acknowledgements.yaml");
  if (fs.existsSync(ackFile)) {
    const data = readYaml<{ edges?: Connection[] }>(ackFile);
    if (data.edges) {
      for (const e of data.edges) {
        connections.push({
          source: e.source,
          target: e.target,
          type: "acknowledgement",
          weight: e.weight ?? 1,
          papers: e.papers,
          derived: true,
        } as Connection);
      }
    }
  }

  // Load derived grant edges (去重 source/target pair)
  const grantFile = path.join(DATA_DIR, "derived", "grant-edges.yaml");
  if (fs.existsSync(grantFile)) {
    const data = readYaml<{ edges?: Connection[] }>(grantFile);
    const seen = new Set<string>();
    for (const c of connections) {
      if (c.type === "grant") {
        seen.add([c.source, c.target].sort().join("|"));
      }
    }
    if (data.edges) {
      for (const e of data.edges) {
        const key = [e.source, e.target].sort().join("|");
        if (seen.has(key)) continue;
        seen.add(key);
        connections.push({
          source: e.source,
          target: e.target,
          type: "grant",
          notes: e.notes,
          derived: true,
        } as Connection);
      }
    }
  }

  return connections;
}

// ===== Acknowledgement mentions (single + strong) for detail sidebar =====

let ackCache: {
  bySource: Map<string, AckMention[]>;
  byTarget: Map<string, AckMention[]>;
} | null = null;

export function getAckMentions(): {
  bySource: Map<string, AckMention[]>;
  byTarget: Map<string, AckMention[]>;
} {
  if (ackCache) return ackCache;
  const bySource = new Map<string, AckMention[]>();
  const byTarget = new Map<string, AckMention[]>();
  const file = path.join(DATA_DIR, "derived", "acknowledgements.yaml");
  if (!fs.existsSync(file)) {
    ackCache = { bySource, byTarget };
    return ackCache;
  }
  const data = readYaml<{
    edges?: Array<{ source: string; target: string; papers: string[] }>;
    single_mentions?: Array<{ source: string; target: string; papers: string[] }>;
  }>(file);
  const all = [...(data.edges || []), ...(data.single_mentions || [])];
  for (const m of all) {
    const mention: AckMention = { source: m.source, target: m.target, papers: m.papers };
    const srcList = bySource.get(m.source) ?? [];
    srcList.push(mention);
    bySource.set(m.source, srcList);
    const tgtList = byTarget.get(m.target) ?? [];
    tgtList.push(mention);
    byTarget.set(m.target, tgtList);
  }
  ackCache = { bySource, byTarget };
  return ackCache;
}

// ===== Institutions =====

export function getAllInstitutions(): Institution[] {
  return readYamlDir<Institution>("institutions").map((i) => ({
    ...i,
    research_groups: i.research_groups || [],
    events: i.events || [],
  }));
}

export function getInstitutionsMap(): Map<string, Institution> {
  const map = new Map<string, Institution>();
  for (const i of getAllInstitutions()) {
    map.set(i.slug, i);
  }
  return map;
}

// ===== Open Problems =====

export function getAllProblems(): OpenProblem[] {
  return readYamlDir<OpenProblem>("problems").map((p) => ({
    ...p,
    proposed_by: p.proposed_by || [],
    prerequisites: p.prerequisites || [],
    related_problems: p.related_problems || [],
    key_people: p.key_people || [],
    progress: p.progress || [],
    current_approaches: p.current_approaches || [],
  }));
}

// ===== Seminars =====

export function getAllSeminars(): Seminar[] {
  const seminarsFile = path.join(DATA_DIR, "seminars", "recurring.yaml");
  if (!fs.existsSync(seminarsFile)) return [];
  const data = readYaml<{ seminars?: Seminar[] }>(seminarsFile);
  return data.seminars || [];
}

// ===== Full DataStore =====

export function loadAllData(): DataStore {
  return {
    people: getPeopleMap(),
    concepts: getConceptsMap(),
    papers: getAllPapers(),
    timeline: getAllTimelineEvents(),
    conferences: {
      series: getAllConferenceSeries(),
      events: getAllConferenceEvents(),
    },
    connections: getAllConnections(),
    institutions: getInstitutionsMap(),
    problems: new Map(getAllProblems().map((p) => [p.slug, p])),
    seminars: getAllSeminars(),
  };
}

// ===== Utility: get all known slugs =====

export function getAllKnownSlugs(): Set<string> {
  const slugs = new Set<string>();
  for (const p of getAllPeople()) slugs.add(p.slug);
  for (const c of getAllConcepts()) slugs.add(c.slug);
  for (const i of getAllInstitutions()) slugs.add(i.slug);
  return slugs;
}

// ===== Utility: find ghost slugs (referenced but not defined) =====

export function findGhostSlugs(): string[] {
  const known = getAllKnownSlugs();
  const referenced = new Set<string>();

  for (const p of getAllPeople()) {
    if (p.advisor) referenced.add(p.advisor);
    for (const s of p.students) referenced.add(s);
    for (const c of p.key_collaborators) referenced.add(c.person);
    for (const r of p.research_areas) referenced.add(r);
    for (const e of p.career_timeline) {
      if (e.institution) referenced.add(e.institution);
      if (e.advisor) referenced.add(e.advisor);
    }
  }

  for (const conn of getAllConnections()) {
    referenced.add(conn.source);
    referenced.add(conn.target);
    if (conn.institution) referenced.add(conn.institution);
  }

  return [...referenced].filter((s) => !known.has(s));
}
