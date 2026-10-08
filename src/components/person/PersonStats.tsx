"use client";

import type { Activity } from "@/lib/types";

interface PersonStatsProps {
  activity: Activity;
}

const STAT_ITEMS: { key: keyof Activity; label: string; anchor?: string }[] = [
  { key: "h_index", label: "h-index" },
  { key: "mathscinet_citations", label: "MathSciNet 引用" },
  { key: "google_scholar_citations", label: "Google Scholar 引用" },
  { key: "phd_students", label: "博士生" },
  { key: "academic_descendants", label: "学术后代" },
];

export default function PersonStats({ activity }: PersonStatsProps) {
  const stats = STAT_ITEMS.filter(
    (s) => activity[s.key] != null && activity[s.key] !== undefined
  );
  const showPapers = activity.total_papers != null;
  const pub = activity.published_count;
  const pre = activity.preprint_only_count;

  if (!stats.length && !showPapers) return null;

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
      {showPapers && (
        <div className="bg-[#14141f] rounded-lg p-4 border border-[#2a2a3a]">
          <a
            href="#publications"
            className="text-2xl font-bold text-[#e8e8f0] hover:text-[#6366f1] transition-colors"
          >
            {(activity.total_papers as number).toLocaleString()}
          </a>
          <div className="text-xs text-[#8888a0] mt-1">收录论文数</div>
          {(pub != null || pre != null) && (
            <div className="text-[10px] text-[#8888a0] mt-1 font-mono">
              {pub != null && (
                <span className="text-[#22c55e]">{pub} 有出版线索</span>
              )}
              {pub != null && pre != null && <span className="mx-1">/</span>}
              {pre != null && (
                <span className="text-[#f59e0b]">{pre} 待补出版线索</span>
              )}
            </div>
          )}
        </div>
      )}
      {stats.map(({ key, label, anchor }) => (
        <div
          key={key}
          className="bg-[#14141f] rounded-lg p-4 border border-[#2a2a3a]"
        >
          {anchor ? (
            <a href={anchor} className="text-2xl font-bold text-[#e8e8f0] hover:text-[#6366f1] transition-colors">
              {(activity[key] as number).toLocaleString()}
            </a>
          ) : (
            <div className="text-2xl font-bold text-[#e8e8f0]">
              {(activity[key] as number).toLocaleString()}
            </div>
          )}
          <div className="text-xs text-[#8888a0] mt-1">{label}（待核实）</div>
        </div>
      ))}
      {activity.active_period && (
        <div className="bg-[#14141f] rounded-lg p-4 border border-[#2a2a3a]">
          <div className="text-sm font-mono text-[#6366f1]">
            {activity.active_period}
          </div>
          <div className="text-xs text-[#8888a0] mt-1">资料记载活跃期（待核实）</div>
        </div>
      )}
      {activity.peak_period && (
        <div className="bg-[#14141f] rounded-lg p-4 border border-[#2a2a3a]">
          <div className="text-sm font-mono text-[#f59e0b]">
            {activity.peak_period}
          </div>
          <div className="text-xs text-[#8888a0] mt-1">资料记载高峰期（待核实）</div>
        </div>
      )}
    </div>
  );
}
