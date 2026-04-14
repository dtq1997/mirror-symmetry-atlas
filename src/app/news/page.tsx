import fs from "fs";
import path from "path";
import yaml from "js-yaml";
import Link from "next/link";
import RichSummary from "@/components/shared/RichSummary";
import { getPeopleMap, getConceptsMap } from "@/lib/data";

interface NewsEntry {
  id: string;
  title: string;
  date: string;
  authors_raw: string[];
  matched_people: string[];
  matched_concepts: string[];
  category: string;
  relevance_score: number;
  summary_zh: string;
}

interface NewsFile {
  entries: NewsEntry[];
}

function loadAllEntries(): NewsEntry[] {
  const newsDir = path.join(process.cwd(), "data", "news");
  if (!fs.existsSync(newsDir)) return [];

  const entries: NewsEntry[] = [];
  for (const f of fs.readdirSync(newsDir).filter((f) => f.endsWith(".yaml"))) {
    const data = yaml.load(
      fs.readFileSync(path.join(newsDir, f), "utf-8")
    ) as NewsFile;
    if (data.entries) entries.push(...data.entries);
  }

  // Deduplicate by id, keep highest relevance_score
  const byId = new Map<string, NewsEntry>();
  for (const e of entries) {
    const existing = byId.get(e.id);
    if (!existing || e.relevance_score > existing.relevance_score) {
      byId.set(e.id, e);
    }
  }

  // Sort by paper date descending
  return [...byId.values()].sort((a, b) => b.date.localeCompare(a.date));
}

function getPersonHover(slug: string, people: Map<string, any>) {
  const p = people.get(slug);
  if (!p) return undefined;
  const name = p.name?.zh || p.name?.en || slug;
  const career = (p.career_timeline || []).filter((e: any) => e.type === "position").pop();
  const details: string[] = [];
  if (career?.role) details.push(career.role);
  if (career?.institution) details.push(career.institution);
  if (p.activity?.total_papers) details.push(`${p.activity.total_papers} 篇论文`);
  return { title: name, subtitle: p.name?.en !== name ? p.name?.en : undefined, details };
}

function getConceptHover(slug: string, concepts: Map<string, any>) {
  const c = concepts.get(slug);
  if (!c) return undefined;
  const name = c.name?.zh || c.name?.en || slug;
  const details: string[] = [];
  if (c.difficulty) details.push(c.difficulty);
  if (c.year_introduced) details.push(`${c.year_introduced} 年引入`);
  return { title: name, subtitle: c.name?.en !== name ? c.name?.en : undefined, details };
}

function buildEntities(
  entry: NewsEntry,
  people: Map<string, any>,
  concepts: Map<string, any>
) {
  const entities: {
    slug: string;
    type: "person" | "concept";
    displayName: string;
    hoverTitle?: string;
    hoverSubtitle?: string;
    hoverDetails?: string[];
  }[] = [];

  const text = entry.summary_zh || "";

  // Check all people — match zh name, en full name, or en last name
  for (const [slug, p] of people) {
    const zh = p.name?.zh;
    const en = p.name?.en;
    // Try: Chinese name, full English name, English last name (surname)
    const enParts = en?.split(" ") || [];
    const lastName = enParts.length > 1 ? enParts[enParts.length - 1] : null;
    const matchName =
      zh && text.includes(zh) ? zh
      : en && text.includes(en) ? en
      : lastName && lastName.length > 3 && text.includes(lastName) ? lastName
      : null;
    if (matchName) {
      const hover = getPersonHover(slug, people);
      entities.push({
        slug,
        type: "person",
        displayName: matchName,
        hoverTitle: hover?.title,
        hoverSubtitle: hover?.subtitle,
        hoverDetails: hover?.details,
      });
    }
  }

  // Check all concepts — match zh name, en name, or aliases
  for (const [slug, c] of concepts) {
    const zh = c.name?.zh;
    const en = c.name?.en;
    const aliases: string[] = c.aliases || [];
    const allNames = [zh, en, ...aliases].filter(Boolean) as string[];
    // Find longest matching name in text
    const sorted = allNames.sort((a, b) => b.length - a.length);
    const matchName = sorted.find((n) => text.includes(n)) || null;
    if (matchName) {
      const hover = getConceptHover(slug, concepts);
      entities.push({
        slug,
        type: "concept",
        displayName: matchName,
        hoverTitle: hover?.title,
        hoverSubtitle: hover?.subtitle,
        hoverDetails: hover?.details,
      });
    }
  }

  return entities;
}

export default function NewsPage() {
  const entries = loadAllEntries();
  const people = getPeopleMap();
  const concepts = getConceptsMap();

  return (
    <div className="max-w-4xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-bold text-[#e8e8f0] mb-2">新闻</h1>
      <p className="text-[#8888a0] mb-8">
        领域动态：核心人物的新论文、学术会议、重要进展
      </p>

      {entries.length === 0 ? (
        <div className="bg-[#14141f] rounded-xl p-8 border border-[#2a2a3a] text-center">
          <p className="text-[#8888a0]">暂无论文动态</p>
        </div>
      ) : (
        <div className="relative">
          {/* Vertical timeline line */}
          <div className="absolute left-[59px] top-0 bottom-0 w-px bg-[#2a2a3a]" />

          <div className="space-y-6">
            {entries.map((entry) => (
              <div key={entry.id} className="flex gap-4">
                {/* Date column */}
                <div className="w-[52px] shrink-0 text-right pt-1">
                  <span className="text-xs font-mono text-[#6366f1] leading-tight">
                    {entry.date}
                  </span>
                </div>

                {/* Dot */}
                <div className="relative pt-2">
                  <div
                    className="w-3 h-3 rounded-full relative z-10"
                    style={{
                      backgroundColor:
                        entry.relevance_score >= 15
                          ? "#f59e0b"
                          : entry.relevance_score >= 10
                            ? "#6366f1"
                            : "#8888a0",
                    }}
                  />
                </div>

                {/* Content */}
                <div className="flex-1 min-w-0 bg-[#14141f] rounded-lg p-4 border border-[#2a2a3a]">
                  <div className="flex items-start justify-between gap-3 mb-2">
                    {entry.id.match(/^\d/) ? (
                      <a
                        href={`https://arxiv.org/abs/${entry.id}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-sm text-[#e8e8f0] hover:text-[#6366f1] transition-colors leading-snug font-medium"
                      >
                        {entry.title}
                      </a>
                    ) : (
                      <span className="text-sm text-[#e8e8f0] font-medium leading-snug">
                        {entry.title}
                      </span>
                    )}
                    <span className="text-[10px] font-mono text-[#8888a0] shrink-0">
                      {entry.id.match(/^\d/) ? entry.id : ""}
                    </span>
                  </div>

                  {/* Rich summary with inline entity links */}
                  <RichSummary
                    className="text-xs text-[#e8e8f0]/80 leading-relaxed"
                    text={entry.summary_zh}
                    entities={buildEntities(entry, people, concepts)}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
