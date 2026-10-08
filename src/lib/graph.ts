import { collectPublications } from "./publications";
import { institutionSlug } from "./inst";
import type {
  Person,
  Concept,
  Connection,
  GraphNode,
  GraphLink,
  GraphData,
  ConnectionType,
  Difficulty,
  LifeDateFact,
  ConceptRelationType,
} from "./types";

// ===== Color constants =====

const COLORS = {
  person: "#f59e0b",
  concept: "#6366f1",
  paper: "#10b981",
  institution: "#8b5cf6",
  ghost: "rgba(255, 255, 255, 0.2)",
} as const;

const EDGE_COLORS: Record<ConnectionType, string> = {
  "advisor-student": "#f59e0b",
  "postdoc-mentor": "#fbbf24",
  "postdoc-group": "#fcd34d",
  coauthor: "#6366f1",
  institutional: "#8b5cf6",
  "co-student": "#10b981",
  grant: "#ec4899",
  acknowledgement: "#a8a29e",
};

const EDGE_DASH: Record<ConnectionType, number[] | undefined> = {
  "advisor-student": undefined,
  "postdoc-mentor": [6, 2],
  "postdoc-group": [2, 4],
  coauthor: [5, 5],
  institutional: [2, 4],
  "co-student": [8, 3],
  grant: [3, 3],
  acknowledgement: [1, 3],
};

/** Force-graph mutates node coordinates and replaces link IDs with objects.
 * Give it an owned copy and rebind links after every filter/search update. */
export function simulationGraph(data: GraphData, previous?: GraphData): GraphData {
  const positions = new Map(previous?.nodes.map((node) => [node.id, node]));
  const endpoint = (value: string | { id?: string }) => typeof value === "string" ? value : value.id ?? "";
  const nodes = data.nodes.map((node) => ({ ...node,
    x: node.x ?? positions.get(node.id)?.x, y: node.y ?? positions.get(node.id)?.y,
  }));
  const ids = new Set(nodes.map((node) => node.id));
  const links = data.links.map((link) => ({ ...link,
    source: endpoint(link.source), target: endpoint(link.target),
  })).filter((link) => ids.has(link.source) && ids.has(link.target));
  return { nodes, links };
}

// ===== Adaptive force parameters =====

export function getForceParams(nodeCount: number) {
  // Stronger repulsion + larger base distance so weakly-connected nodes
  // don't crowd into unreadable clusters. Strong collaborations still pull
  // each other close via link strength.
  if (nodeCount < 20) {
    return { chargeStrength: -500, linkDistance: 160 };
  }
  if (nodeCount <= 50) {
    return { chargeStrength: -380, linkDistance: 120 };
  }
  if (nodeCount <= 100) {
    return { chargeStrength: -260, linkDistance: 95 };
  }
  return { chargeStrength: -180, linkDistance: 80 };
}

// Node size shows catalog coverage, never inferred prestige or seniority.
function personRadius(p: Person): number {
  return Math.min(18, 4 + Math.sqrt(collectPublications([p]).length));
}

function yearFromDateValue(value?: number | string | null): number | null {
  if (typeof value === "number") return value;
  if (typeof value !== "string") return null;
  const match = value.match(/\b(1[6-9]\d{2}|20\d{2}|21\d{2})\b/);
  return match ? parseInt(match[1], 10) : null;
}

function yearFromLifeDate(fact?: LifeDateFact, fallback?: number | string | null) {
  return yearFromDateValue(fact?.date) ?? yearFromDateValue(fallback);
}

function personColor(p: Person): string {
  return yearFromLifeDate(p.death, p.died) ? "#777788" : COLORS.person;
}

// ===== Build people graph =====

export function buildPeopleGraph(
  people: Person[],
  connections: Connection[]
): GraphData {
  connections = connections.filter((c) => c.type !== "coauthor" || c.coauthored_papers);
  const nodes: GraphNode[] = [];
  const nodeIds = new Set<string>();

  // Add person nodes
  for (const p of people) {
    nodes.push({
      id: p.slug,
      label: p.name.zh || p.name.en,
      type: "person",
      radius: personRadius(p),
      color: personColor(p),
      opacity: 1,
      isGhost: false,
      data: p,
    });
    nodeIds.add(p.slug);
  }

  // Collect all referenced person slugs from connections
  const referencedSlugs = new Set<string>();
  for (const conn of connections) {
    referencedSlugs.add(conn.source);
    referencedSlugs.add(conn.target);
  }

  // Add ghost nodes for referenced but missing people
  for (const slug of referencedSlugs) {
    if (!nodeIds.has(slug)) {
      nodes.push({
        id: slug,
        label: `${slug}（未建档）`,
        type: "person",
        radius: 3,
        color: COLORS.ghost,
        opacity: 0.4,
        isGhost: true,
      });
      nodeIds.add(slug);
    }
  }

  // Build links
  const links: GraphLink[] = [];
  for (const conn of connections) {
    if (!nodeIds.has(conn.source) || !nodeIds.has(conn.target)) continue;

    const weight = conn.weight ?? 1;
    links.push({
      source: conn.source,
      target: conn.target,
      type: conn.type,
      weight,
      color: EDGE_COLORS[conn.type] || "#555",
      dash: EDGE_DASH[conn.type],
      opacity: conn.type === "institutional" ? 0.3 : 0.7,
      label: conn.type === "coauthor" && weight > 1 ? `${weight}` : undefined,
      data: conn,
    });
  }

  return { nodes, links };
}

// ===== Acknowledgement graph: coauthor + acknowledgement only =====

export function buildAckGraph(
  people: Person[],
  connections: Connection[]
): GraphData {
  // Filter relevant connections
  const relevantLinks = connections.filter(
    (c) => (c.type === "coauthor" && !!c.coauthored_papers) || c.type === "acknowledgement"
  );

  // Compute ack-weighted importance per person (in + out)
  const ackDegree = new Map<string, { inW: number; outW: number }>();
  for (const c of connections) {
    if (c.type !== "acknowledgement") continue;
    const w = c.weight ?? 1;
    const src = ackDegree.get(c.source) ?? { inW: 0, outW: 0 };
    src.outW += w;
    ackDegree.set(c.source, src);
    const tgt = ackDegree.get(c.target) ?? { inW: 0, outW: 0 };
    tgt.inW += w;
    ackDegree.set(c.target, tgt);
  }

  // Keep only nodes appearing in coauthor or ack edges, plus all people with any ack degree
  const kept = new Set<string>();
  for (const l of relevantLinks) {
    kept.add(l.source);
    kept.add(l.target);
  }

  const nodes: GraphNode[] = [];
  for (const p of people) {
    if (!kept.has(p.slug)) continue;
    const d = ackDegree.get(p.slug) ?? { inW: 0, outW: 0 };
    // Radius encodes extracted mentions only; it does not measure influence.
    const score = d.inW * 2 + d.outW;
    const r = score > 0 ? Math.min(4 + Math.log2(score + 1) * 1.4, 14) : 4;
    nodes.push({
      id: p.slug,
      label: p.name.zh || p.name.en,
      type: "person",
      radius: r,
      color: personColor(p),
      opacity: 1,
      isGhost: false,
      data: p,
    });
  }

  const nodeIds = new Set(nodes.map((n) => n.id));
  const links: GraphLink[] = [];
  for (const c of relevantLinks) {
    if (!nodeIds.has(c.source) || !nodeIds.has(c.target)) continue;
    const w = c.weight ?? 1;
    links.push({
      source: c.source,
      target: c.target,
      type: c.type,
      weight: w,
      color: EDGE_COLORS[c.type],
      dash: EDGE_DASH[c.type],
      opacity: c.type === "acknowledgement" ? Math.min(0.6 + w * 0.1, 0.9) : 0.6,
      label: c.type === "acknowledgement" && w > 1 ? `${w}` : undefined,
      data: c,
    });
  }

  return { nodes, links };
}

// ===== Time filter =====

/** Read the year actually recorded at the start of a period. Unknown dates
 * stay unknown; no birthday, present-day position or fallback year is inferred. */
export function recordedStartYear(value: unknown): number | null {
  if (typeof value === "number") {
    return Number.isInteger(value) && value >= 1600 && value <= 2199 ? value : null;
  }
  if (typeof value !== "string") return null;
  const match = value.trim().match(/^(?:~|circa\s+|c\.\s*)?((?:1[6-9]|20|21)\d{2})(?=$|[-–—./\s])/i);
  return match ? Number(match[1]) : null;
}

/** Recorded affiliations include education, visits and past positions. They
 * are not a claim about the person's current employer. */
export function recordedInstitutions(person: Person, throughYear: number | null = null): string[] {
  return [...new Set((person.career_timeline ?? []).filter((entry) => {
    if (!entry.institution) return false;
    if (throughYear === null) return true;
    const start = recordedStartYear(entry.period);
    return start !== null && start <= throughYear;
  }).map((entry) => institutionSlug(entry.institution!)))];
}

/** Cumulative dated records through a chosen year, not a historical census.
 * Undated evidence is omitted. Past/deceased people and completed relations
 * remain once recorded; coauthor weights use only papers through the cutoff. */
export function filterByYear(data: GraphData, year: number | null): GraphData {
  if (year === null) return data;
  const byCutoff = (value: unknown) => {
    const start = recordedStartYear(value);
    return start !== null && start <= year;
  };
  const links: GraphLink[] = [];
  for (const link of data.links) {
    const conn = link.data;
    if (!conn) continue;
    if (conn.type === "coauthor") {
      if (!conn.coauthored_papers) continue;
      const published = conn.coauthored_papers.published.filter((p) => byCutoff(p.year));
      const preprint = conn.coauthored_papers.preprint.filter((p) => byCutoff(p.year));
      const weight = published.length + preprint.length;
      if (!weight) continue;
      const years = [...published, ...preprint].map((p) => p.year);
      links.push({ ...link, weight, label: weight > 1 ? String(weight) : undefined,
        data: { ...conn, weight, period: `${Math.min(...years)}-${Math.max(...years)}`,
          coauthored_papers: { published, preprint } } });
    } else {
      const starts = [recordedStartYear(conn.year), recordedStartYear(conn.period)]
        .filter((start): start is number => start !== null);
      if (starts.length && starts.every((start) => start <= year)) links.push({ ...link });
    }
  }
  const endpoint = (value: string | { id?: string }) => typeof value === "string" ? value : value.id ?? "";
  const linked = new Set(links.flatMap((link) => [endpoint(link.source), endpoint(link.target)]));
  const nodes = data.nodes.filter((node) => {
    if (linked.has(node.id)) return true;
    if (!node.data || node.type !== "person") return false;
    const person = node.data as Person;
    return (person.career_timeline ?? []).some((entry) => byCutoff(entry.period)) ||
      (person.publications ?? []).some((paper) => byCutoff(paper.year));
  }).map((node) => {
    if (!node.data || node.type !== "person") return { ...node };
    const person = node.data as Person;
    return { ...node, radius: personRadius({ ...person,
      publications: (person.publications ?? []).filter((paper) => byCutoff(paper.year)) }) };
  });
  const ids = new Set(nodes.map((node) => node.id));
  return { nodes, links: links.filter((link) => ids.has(endpoint(link.source)) && ids.has(endpoint(link.target))) };
}

// ===== Concept graph =====

const DIFFICULTY_COLORS: Record<Difficulty, string> = {
  introductory: "#22c55e",
  intermediate: "#3b82f6",
  advanced: "#a855f7",
  "research-frontier": "#ef4444",
};

function conceptRadius(c: Concept): number {
  const people = (c.key_people?.length ?? 0) + (c.contributions?.length ?? 0);
  const deps =
    (c.prerequisites?.length ?? 0) +
    (c.leads_to?.length ?? 0) +
    (c.related?.length ?? 0);
  if (people + deps > 10) return 10;
  if (people + deps > 5) return 7;
  return 5;
}

export const CONCEPT_RELATIONS: Record<ConceptRelationType, {
  label: string; color: string; dash?: number[];
}> = {
  prerequisite: { label: "前置记录", color: "#ef4444" },
  "leads-to": { label: "后续方向", color: "#38bdf8", dash: [7, 3] },
  related: { label: "相关记录", color: "#a1a1b8", dash: [3, 4] },
};

function conceptLinks(concepts: Concept[]): GraphLink[] {
  const links = new Map<string, GraphLink>();
  for (const c of concepts) {
    const fields = [
      ["prerequisite", c.prerequisites], ["leads-to", c.leads_to], ["related", c.related],
    ] as const;
    for (const [type, refs] of fields) {
      for (const ref of refs ?? []) {
        if (ref === c.slug) continue;
        let [source, target] = type === "prerequisite" ? [ref, c.slug] : [c.slug, ref];
        if (type === "related") [source, target] = [source, target].sort();
        const style = CONCEPT_RELATIONS[type];
        links.set(JSON.stringify([type, source, target]), {
          source, target, type, weight: 1, ...style,
          dash: style.dash?.slice(), opacity: type === "related" ? 0.4 : 0.65,
        });
      }
    }
  }
  const pairs = new Map<string, GraphLink[]>();
  for (const link of links.values()) {
    const key = JSON.stringify([link.source, link.target].sort());
    const group = pairs.get(key) ?? [];
    group.push(link);
    pairs.set(key, group);
  }
  // Distinct relation types and reverse arrows must not paint over each other.
  for (const group of pairs.values()) {
    group.sort((a, b) => `${a.type}:${a.source}`.localeCompare(`${b.type}:${b.source}`));
    group.forEach((link, index) => {
      const direction = link.source < link.target ? 1 : -1;
      link.curve = direction * 0.24 * (index - (group.length - 1) / 2);
    });
  }
  return [...links.values()];
}

export function highlightConceptPrerequisites(graph: GraphData, chain: Set<string>): GraphData {
  return {
    nodes: graph.nodes.map((node) => ({ ...node, opacity: chain.has(node.id) ? 1 : 0.15 })),
    links: graph.links.map((link) => ({ ...link, opacity:
      link.type === "prerequisite" && chain.has(link.source) && chain.has(link.target) ? 0.85 : 0.06 })),
  };
}

export function buildConceptGraph(
  concepts: Concept[]
): GraphData {
  const nodes: GraphNode[] = [];
  const nodeIds = new Set<string>();

  for (const c of concepts) {
    nodes.push({
      id: c.slug,
      label: c.name.zh || c.name.en,
      type: "concept",
      radius: conceptRadius(c),
      color: DIFFICULTY_COLORS[c.difficulty] || COLORS.concept,
      opacity: 1,
      isGhost: false,
      data: c,
    });
    nodeIds.add(c.slug);
  }

  const links = conceptLinks(concepts);
  // Every relation retains missing targets as explicit, non-clickable records.
  const referenced = new Set(links.flatMap((link) => [link.source, link.target]));
  for (const slug of referenced) {
    if (!nodeIds.has(slug)) {
      nodes.push({
        id: slug,
        label: `${slug}（未记录）`,
        type: "concept",
        radius: 3,
        color: COLORS.ghost,
        opacity: 0.4,
        isGhost: true,
      });
      nodeIds.add(slug);
    }
  }

  return { nodes, links };
}

// ===== Learning path: recursive prerequisite chain =====

export function getPrerequisiteChain(
  conceptSlug: string,
  concepts: Concept[]
): Set<string> {
  const conceptMap = new Map(concepts.map((c) => [c.slug, c]));
  const chain = new Set<string>();

  function walk(slug: string) {
    if (chain.has(slug)) return;
    chain.add(slug);
    const c = conceptMap.get(slug);
    if (c) {
      for (const p of c.prerequisites || []) walk(p);
    }
  }

  walk(conceptSlug);
  return chain;
}
