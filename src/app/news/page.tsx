import fs from "fs";
import path from "path";
import yaml from "js-yaml";
import Link from "next/link";
import MathText from "@/components/shared/MathText";

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

export default function PapersPage() {
  const entries = loadAllEntries();

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

                  {/* Summary */}
                  <MathText className="text-xs text-[#e8e8f0]/80 leading-relaxed mb-3">
                    {entry.summary_zh}
                  </MathText>

                  {/* Tags */}
                  <div className="flex flex-wrap gap-1">
                    {entry.matched_people?.map((p) => (
                      <Link
                        key={p}
                        href={`/people/${p}`}
                        className="text-[10px] px-1.5 py-0.5 rounded bg-[#f59e0b]/15 text-[#fbbf24] hover:bg-[#f59e0b]/25"
                      >
                        {p}
                      </Link>
                    ))}
                    {entry.matched_concepts?.map((c) => (
                      <Link
                        key={c}
                        href={`/concepts/${c}`}
                        className="text-[10px] px-1.5 py-0.5 rounded bg-[#6366f1]/15 text-[#818cf8] hover:bg-[#6366f1]/25"
                      >
                        {c}
                      </Link>
                    ))}
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-[#2a2a3a] text-[#8888a0]">
                      {entry.category}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
