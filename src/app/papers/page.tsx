import fs from "fs";
import path from "path";
import yaml from "js-yaml";
import Link from "next/link";

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
  fetch_date: string;
  period_days: number;
  total_fetched: number;
  relevant_count: number;
  entries: NewsEntry[];
}

function loadAllNews(): { date: string; data: NewsFile }[] {
  const newsDir = path.join(process.cwd(), "data", "news");
  if (!fs.existsSync(newsDir)) return [];
  return fs
    .readdirSync(newsDir)
    .filter((f) => f.endsWith(".yaml"))
    .sort()
    .reverse()
    .map((f) => ({
      date: f.replace(".yaml", ""),
      data: yaml.load(fs.readFileSync(path.join(newsDir, f), "utf-8")) as NewsFile,
    }));
}

export default function PapersPage() {
  const allNews = loadAllNews();
  const hasNews = allNews.length > 0 && allNews.some((n) => n.data.entries?.length > 0);

  return (
    <div className="max-w-4xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-bold text-[#e8e8f0] mb-2">论文动态</h1>
      <p className="text-[#8888a0] mb-8">
        arXiv 最新论文，自动匹配领域内人物和概念
      </p>

      {!hasNews ? (
        <div className="bg-[#14141f] rounded-xl p-8 border border-[#2a2a3a] text-center">
          <p className="text-[#8888a0] mb-4">暂无论文动态</p>
          <p className="text-xs text-[#8888a0]">
            运行 <code className="text-[#6366f1]">python3 scripts/fetch-arxiv-news.py</code> 获取最新论文
          </p>
        </div>
      ) : (
        <div className="space-y-8">
          {allNews.map(({ date, data }) => {
            if (!data.entries?.length) return null;
            return (
              <section key={date}>
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-lg font-semibold text-[#e8e8f0]">
                    {date}
                  </h2>
                  <span className="text-xs text-[#8888a0]">
                    {data.relevant_count} / {data.total_fetched} 篇相关
                  </span>
                </div>
                <div className="space-y-3">
                  {data.entries.map((entry) => (
                    <div
                      key={entry.id}
                      className="bg-[#14141f] rounded-lg p-4 border border-[#2a2a3a]"
                    >
                      <div className="flex items-start justify-between gap-3">
                        <div className="min-w-0">
                          <a
                            href={`https://arxiv.org/abs/${entry.id}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-sm text-[#e8e8f0] hover:text-[#6366f1] transition-colors leading-snug font-medium"
                          >
                            {entry.title}
                          </a>
                          <p className="text-xs text-[#8888a0] mt-1.5">
                            {entry.summary_zh}
                          </p>
                          <div className="flex flex-wrap gap-1 mt-2">
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
                          </div>
                        </div>
                        <div className="flex flex-col items-end shrink-0 gap-1">
                          <span className="text-[10px] font-mono text-[#8888a0]">
                            {entry.id}
                          </span>
                          <span className="text-[10px] text-[#8888a0]">
                            {entry.category}
                          </span>
                          <span
                            className={`text-[10px] px-1.5 py-0.5 rounded ${
                              entry.relevance_score >= 10
                                ? "bg-[#f59e0b]/20 text-[#fbbf24]"
                                : "bg-[#2a2a3a] text-[#8888a0]"
                            }`}
                          >
                            相关度 {entry.relevance_score}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            );
          })}
        </div>
      )}
    </div>
  );
}
