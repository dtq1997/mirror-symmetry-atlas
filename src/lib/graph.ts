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
// 复合信号: publications 长度 + 奖项等级 + 分区论文 + descendants + senior tag.
// 目标: 大佬 vs 青椒的半径差异应当显著 (例如 18 vs 4),而不是挤在 8-12 区间.

const TOP_AWARD_KEYWORDS = [
  "菲尔兹", "fields medal", "wolf prize", "abel prize",
  "院士", "academician", "national academy",
  "shaw prize", "crafoord", "veblen", "breakthrough prize",
  "national medal of science", "macarthur",
];
const BIG_AWARD_KEYWORDS = [
  "杰出青年", "jieqing", "长江学者", "changjiang",
  "千人", "百千万", "national natural science award",
  "国家自然科学奖", "chern medal", "ramanujan prize",
  "salem prize", "sloan fellow", "packard fellow",
];
const MID_AWARD_KEYWORDS = [
  "青年人才", "优青", "young scientist", "优秀青年",
  "青年学者", "钟家庆", "iccm", "青年长江", "青年拔尖",
  "新世纪人才", "young investigator",
];

function awardTier(p: Person): 0 | 1 | 2 | 3 {
  const timeline = p.career_timeline || [];
  const tags = p.tags || [];
  const collected: string[] = [];
  for (const e of timeline) {
    if (e.type === "award") {
      collected.push(((e.title || "") + " " + ((e as any).notes || "")).toLowerCase());
    }
  }
  const blob = collected.join(" | ") + " " + tags.join(" ").toLowerCase();
  if (TOP_AWARD_KEYWORDS.some((k) => blob.includes(k))) return 3;
  if (BIG_AWARD_KEYWORDS.some((k) => blob.includes(k))) return 2;
  if (MID_AWARD_KEYWORDS.some((k) => blob.includes(k))) return 1;
  return 0;
}

function personRadius(p: Person): number {
  const tags = p.tags || [];

  const a = p.activity ?? {};
  const t1 = (a as any).t1_papers ?? 0;
  const t2 = (a as any).t2_papers ?? 0;
  const t3 = (a as any).t3_papers ?? 0;
  const t4 = (a as any).t4_papers ?? 0;
  const qscore = t1 * 4 + t2 * 2 + t3 * 0.5 + t4 * 0.2;

  const pubs = p.publications?.length ?? 0;
  const desc = a.academic_descendants ?? 0;
  const papersTotal = Math.max(a.total_papers ?? 0, pubs);

  // 始终综合三路信号: 分区论文权重 + descendants + 论文总量
  const rawScore = qscore + desc * 0.8 + papersTotal * 0.6;

  const tier = awardTier(p);
  // 奖项等级直接给基础下限 (tier 3: 院士/菲尔兹级; tier 2: 杰青/长江; tier 1: 优青)
  const awardFloor = tier === 3 ? 15 : tier === 2 ? 11 : tier === 1 ? 8 : 0;

  const scoreRadius = rawScore > 0 ? 4 + Math.sqrt(rawScore) * 0.9 : 4;
  let r = Math.max(scoreRadius, awardFloor);

  // 顶级标签视为绝对优先 (即便数据 stub)
  if (tags.includes("fields-medal")) r = Math.max(r, 18);
  else if (tags.includes("important-person")) r = Math.max(r, 15);

  // stub 只是资料不全,不一定是小人物;仅当无任何信号时压为 3.5
  if (tags.includes("stub") && r <= 4.5 && tier === 0) return 3.5;

  return Math.max(3.5, Math.min(r, 18));
}

// ===== Person color by age/status =====

// 根据 role 文本推断该时间点的大致年龄,用于从 career_timeline 反推出生年
function roleAgeOffset(role: string, type: string): number | null {
  const r = (role || "").toLowerCase();
  if (/本科|undergrad|b\.?s\.?c?\.?|学士/.test(r)) return 20;  // 本科开始约 20 岁前后的均值
  if (/硕士|master|m\.?sc?\.?/.test(r)) return 23;
  if (/博士后|post.?doc/.test(r)) return 29;
  if (/博士|ph\.?d\.?|doctor/.test(r)) return 25;
  if (/教授|professor|讲席|chair/.test(r)) return 38;
  if (/副教授|associate/.test(r)) return 33;
  if (/助理教授|assistant|lecturer|讲师|特聘/.test(r)) return 30;
  if (type === "education") return 22;
  if (type === "position") return 30;
  if (type === "visit") return 30;
  return null;
}

function estimateBirthYear(p: Person): number | null {
  if (p.born) return p.born;
  const timeline = p.career_timeline || [];
  // 取所有能推断年龄的条目,取中位数以稳健
  const estimates: number[] = [];
  for (const entry of timeline) {
    const match = entry.period?.replace(/~/g, "").match(/(\d{4})/);
    if (!match) continue;
    const year = parseInt(match[1]);
    const offset = roleAgeOffset(entry.role || "", entry.type || "");
    if (offset !== null) estimates.push(year - offset);
  }
  if (estimates.length === 0) return null;
  estimates.sort((a, b) => a - b);
  return estimates[Math.floor(estimates.length / 2)];
}

function personColor(p: Person): string {
  if (p.died) return "#777788";

  const birthYear = estimateBirthYear(p);
  if (!birthYear) return "#9ca3af"; // 未知年龄 → 中性灰蓝,避免误导

  const age = 2026 - birthYear;

  if (age >= 75) return "#92400e"; // 深棕 — 元老 (75+)
  if (age >= 60) return "#b45309"; // 深琥珀 — 资深 (60-74)
  if (age >= 50) return "#d97706"; // 中深琥珀 — 中坚 (50-59)
  if (age >= 40) return "#f59e0b"; // 标准琥珀 — 壮年 (40-49)
  if (age >= 32) return "#fbbf24"; // 亮琥珀 — 青年 PI (32-39)
  return "#fde047";                // 亮金 — 新锐 (<32)
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

// ===== Acknowledgement graph: coauthor + acknowledgement only =====

export function buildAckGraph(
  people: Person[],
  connections: Connection[]
): GraphData {
  // Filter relevant connections
  const relevantLinks = connections.filter(
    (c) => c.type === "coauthor" || c.type === "acknowledgement"
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
    // Radius = 4 + log2(1 + inW*2 + outW) * 1.4 (被致谢权重更高,代表影响力)
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
      opacity: c.type === "acknowledgement" ? Math.min(0.3 + w * 0.15, 0.85) : 0.6,
      label: c.type === "acknowledgement" && w > 1 ? `${w}` : undefined,
      data: c,
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
