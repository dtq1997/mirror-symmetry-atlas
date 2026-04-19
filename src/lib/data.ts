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
} from "./types";

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
  // Skip if pair already present in declared coauthor edges.
  const declaredCoauthor = new Set<string>();
  for (const c of connections) {
    if (c.type !== "coauthor") continue;
    const k = [c.source, c.target].sort().join("|");
    declaredCoauthor.add(k);
  }

  const people = getAllPeople();
  const builtSlugs = new Set(people.map((p) => p.slug));
  const derivedSeen = new Set<string>();

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

  return connections;
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
