import fs from "fs";
import path from "path";
import yaml from "js-yaml";
import RichSummary from "@/components/shared/RichSummary";
import { canonicalArxivId, publicationUrl } from "@/lib/paper-identity";
import { publicSourceUrl } from "@/lib/source-url";

interface NewsEntry {
  id: string;
  title: string;
  date: string;
  authors_raw?: string[];
  summary_zh?: string;
  source_url?: string;
  source_version?: string;
  review_status?: string;
  reviewed_at?: string;
  updated?: string;
  category?: string;
}

interface NewsFile {
  entries?: NewsEntry[];
  last_success_at?: string;
}

function loadNews() {
  const newsDir = path.join(process.cwd(), "data", "news");
  const byId = new Map<string, NewsEntry>();
  let lastSuccess = "";
  if (fs.existsSync(newsDir)) {
    for (const f of fs.readdirSync(newsDir).filter((f) => f.endsWith(".yaml") && !f.startsWith("_")).sort()) {
      const data = yaml.load(fs.readFileSync(path.join(newsDir, f), "utf-8")) as NewsFile;
      if (data.last_success_at && data.last_success_at > lastSuccess) lastSuccess = data.last_success_at;
      for (const entry of data.entries || []) {
        const key = canonicalArxivId(entry.id) || entry.id;
        const old = byId.get(key);
        // A newer automatic record cannot erase an editorial review.
        if (!old || entry.reviewed_at || (!old.reviewed_at && (entry.updated || "") >= (old.updated || ""))) {
          byId.set(key, entry);
        }
      }
    }
  }
  return { entries: [...byId.values()].sort((a, b) => b.date.localeCompare(a.date)), lastSuccess };
}

export default function NewsPage() {
  const { entries, lastSuccess } = loadNews();
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-10">
      <h1 className="text-2xl font-bold text-[#e8e8f0] mb-2">新闻</h1>
      <p className="text-[#8888a0] mb-3">论文动态与会议记录。每条注明来源和核查范围。</p>
      <div className="text-xs text-[#8888a0] leading-relaxed mb-8 space-y-1">
        <p>{lastSuccess ? `最近完整抓取：${new Date(lastSuccess).toLocaleString("zh-CN", { timeZone: "Asia/Shanghai", hour12: false })}（北京时间）` : "自动抓取尚无可验证的成功记录；下方为已有记录的核查结果。"}</p>
        <p>自动筛选覆盖 math-ph、math.AG、math.QA、hep-th、math.DG、math.SG、nlin.SI 的近期新提交；不代表领域全部论文，也不据姓名自动确认本站人物身份。</p>
        <a className="underline" href="https://github.com/dtq1997/mirror-symmetry-atlas/actions/workflows/arxiv-news.yml" target="_blank" rel="noopener noreferrer">查看更新运行记录</a>
      </div>
      {entries.length === 0 ? <p className="text-[#8888a0]">暂未收录论文动态。</p> : (
        <div className="space-y-5">
          {entries.map((entry) => {
            const source = publicSourceUrl(entry.source_url) || publicationUrl(entry);
            const reviewed = entry.review_status === "abstract-reviewed" || entry.review_status === "source-reviewed";
            return (
              <article key={entry.id} className="min-w-0 bg-[#14141f] rounded-xl p-4 sm:p-5 border border-[#2a2a3a] break-words">
                <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-[#8888a0] mb-2">
                  <time dateTime={entry.date}>{entry.date}</time>
                  <span>{entry.category}</span>
                  <span className={reviewed ? "text-[#a5b4fc]" : "text-[#d4ad68]"}>
                    {entry.review_status === "abstract-reviewed" ? "署名与摘要已对照来源" : entry.review_status === "source-reviewed" ? "已对照官方通知" : "自动收录 · 未人工审读"}
                  </span>
                </div>
                <h2 className="text-base font-medium leading-snug mb-2 text-[#e8e8f0]">
                  {source ? <a href={source} target="_blank" rel="noopener noreferrer" className="hover:text-[#a5b4fc] underline decoration-[#55556b] underline-offset-4">{entry.title}</a> : entry.title}
                </h2>
                {!!entry.authors_raw?.length && <p className="text-sm text-[#b8b8cc] mb-3">作者：{entry.authors_raw.join("；")}</p>}
                {/* No inferred entity links: surnames and shared full names do not prove identity. */}
                {entry.summary_zh && <RichSummary className="text-sm text-[#e8e8f0]/80 leading-relaxed" text={entry.summary_zh} entities={[]} />}
                <p className="text-xs text-[#8888a0] mt-3">
                  {entry.source_version && `来源版本：${entry.source_version}。`}
                  {entry.reviewed_at && ` 核对日期：${entry.reviewed_at}。`}
                  {!reviewed && " 主题由关键词筛选；摘要与全文请查看原始来源。"}
                </p>
              </article>
            );
          })}
        </div>
      )}
    </div>
  );
}
