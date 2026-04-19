import type {
  Person,
  Concept,
  Connection,
  GraphNode,
  GraphLink,
  GraphData,
  ConnectionType,
  Difficulty,
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
  friendship: "#ef4444",
  institutional: "#8b5cf6",
  "co-student": "#10b981",
  grant: "#ec4899",
};

const EDGE_DASH: Record<ConnectionType, number[] | undefined> = {
  "advisor-student": undefined,
  "postdoc-mentor": [6, 2],
  "postdoc-group": [2, 4],
  coauthor: [5, 5],
  friendship: [10, 4],
  institutional: [2, 4],
  "co-student": [8, 3],
  grant: [3, 3],
};

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

// ===== Node radius by importance =====

function personRadius(p: Person): number {
  const tags = p.tags || [];
  if (tags.includes("important-person")) return 11;
  if (tags.includes("stub")) return 3.5;

  // Quality-weighted score using 新锐分区表 tiers (from enrich-venues.py).
  // T1 = 4x, T2 = 2x, T3 = 0.5x, T4 = 0.2x (用户要求: 一二区重要, 三区只记录不重要)
  const a = p.activity ?? {};
  const t1 = (a as any).t1_papers ?? 0;
  const t2 = (a as any).t2_papers ?? 0;
  const t3 = (a as any).t3_papers ?? 0;
  const t4 = (a as any).t4_papers ?? 0;
  const qscore = t1 * 4 + t2 * 2 + t3 * 0.5 + t4 * 0.2;

  // Senior tag boost
  const seniorBoost =
    tags.includes("senior-researcher") ||
    tags.includes("fields-medal") ||
    tags.includes("jieqing")
      ? 1
      : 0;

  // qscore-based radius (log scale so outliers don't blow up)
  if (qscore > 0) {
    // qscore 0-200+ range; log2 gives 0..7.6 roughly
    const r = 4 + Math.log2(qscore + 1) * 1.1 + seniorBoost;
    return Math.max(4, Math.min(r, 12));
  }

  // Fallback: descendants or paper count
  const desc = a.academic_descendants ?? 0;
  const papers = a.total_papers ?? 0;
  if (desc > 100 || papers > 150) return 9 + seniorBoost;
  if (desc > 30 || papers > 80) return 7 + seniorBoost;
  if (desc > 10 || papers > 40) return 6 + seniorBoost;
  if (papers > 15) return 5.5 + seniorBoost;
  if (papers > 5) return 5;
  return 4;
}

// ===== Person color by age/status =====

function estimateBirthYear(p: Person): number | null {
  if (p.born) return p.born;
  // Estimate from earliest career entry
  const timeline = p.career_timeline || [];
  for (const entry of timeline) {
    const match = entry.period?.replace(/~/g, "").match(/(\d{4})/);
    if (match) {
      const year = parseInt(match[1]);
      if (entry.type === "education") return year - 18;
      if (entry.type === "position") return year - 28;
    }
  }
  return null;
}

function personColor(p: Person): string {
  // Deceased → gray
  if (p.died) return "#777788";

  const birthYear = estimateBirthYear(p);
  if (!birthYear) return COLORS.person; // fallback amber

  const age = 2026 - birthYear;

  // Color gradient: younger = brighter warm, older = deeper warm
  if (age >= 80) return "#b45309"; // deep amber — 元老
  if (age >= 60) return "#d97706"; // dark amber — 资深
  if (age >= 45) return "#f59e0b"; // standard amber — 中坚
  if (age >= 35) return "#fbbf24"; // bright amber — 活跃青年
  return "#fcd34d";                // light gold — 新锐
}

// ===== Build people graph =====

export function buildPeopleGraph(
  people: Person[],
  connections: Connection[],
  knownSlugs: Set<string>
): GraphData {
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

// ===== Time filter =====

function periodContainsYear(period: string | undefined, year: number): boolean {
  if (!period) return true;
  const clean = period.replace(/~/g, "").replace(/circa /g, "");

  // "present" → current year
  const resolved = clean.replace(/present/gi, "2026");

  // Single year: "1998"
  if (/^\d{4}$/.test(resolved)) {
    return parseInt(resolved) <= year;
  }

  // Range: "1993-2019"
  const rangeMatch = resolved.match(/(\d{4})\s*[-–]\s*(\d{4})/);
  if (rangeMatch) {
    const start = parseInt(rangeMatch[1]);
    const end = parseInt(rangeMatch[2]);
    return start <= year && year <= end;
  }

  // Date: "2019-03-19"
  const dateMatch = resolved.match(/^(\d{4})-/);
  if (dateMatch) {
    return parseInt(dateMatch[1]) <= year;
  }

  return true;
}

export function filterByYear(
  data: GraphData,
  year: number | null
): GraphData {
  if (year === null) return data;

  const filteredNodes = data.nodes.map((node) => {
    if (node.isGhost) return { ...node, opacity: 0.2 };

    const p = node.data as Person | undefined;
    if (!p) return node;

    // Person must be born and alive in that year
    const born = p.born ?? 0;
    const died = p.died ?? 9999;
    const alive = born <= year && year <= died;

    // Check if they had any career activity by that year
    const hasActivity =
      !p.career_timeline?.length ||
      p.career_timeline.some((entry) => {
        const periodStr = entry.period;
        const startMatch = periodStr
          .replace(/~/g, "")
          .match(/^(\d{4})/);
        if (!startMatch) return true;
        return parseInt(startMatch[1]) <= year;
      });

    const visible = alive && hasActivity;
    return { ...node, opacity: visible ? 1 : 0.05 };
  });

  const filteredLinks = data.links.map((link) => {
    const conn = link.data as Connection | undefined;
    if (!conn) return link;

    // Check connection year/period
    if (conn.year && conn.year > year) {
      return { ...link, opacity: 0 };
    }
    if (conn.period && !periodContainsYear(conn.period, year)) {
      return { ...link, opacity: 0 };
    }

    return { ...link, opacity: link.opacity };
  });

  return { nodes: filteredNodes, links: filteredLinks };
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

export function buildConceptGraph(
  concepts: Concept[],
  knownSlugs: Set<string>
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

  // Ghost nodes for referenced but missing concepts
  const referenced = new Set<string>();
  for (const c of concepts) {
    for (const p of c.prerequisites || []) referenced.add(p);
    for (const l of c.leads_to || []) referenced.add(l);
  }
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

  // Directed edges: prerequisites → concept
  const links: GraphLink[] = [];
  for (const c of concepts) {
    for (const prereq of c.prerequisites || []) {
      if (nodeIds.has(prereq)) {
        links.push({
          source: prereq,
          target: c.slug,
          type: "advisor-student", // reuse for arrow rendering
          weight: 1,
          color: "#ef4444",
          opacity: 0.6,
          label: undefined,
        });
      }
    }
    // Also add "related" edges (undirected, dashed)
    for (const rel of c.related || []) {
      if (nodeIds.has(rel) && c.slug < rel) {
        // avoid duplicates
        links.push({
          source: c.slug,
          target: rel,
          type: "coauthor", // reuse for dashed rendering
          weight: 1,
          color: "#8888a0",
          dash: [3, 4],
          opacity: 0.3,
        });
      }
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
