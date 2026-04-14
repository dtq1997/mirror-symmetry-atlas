"use client";

import type { Activity } from "@/lib/types";

interface PersonStatsProps {
  activity: Activity;
}

const STAT_ITEMS: { key: keyof Activity; label: string; anchor?: string }[] = [
  { key: "total_papers", label: "论文数", anchor: "#publications" },
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

  if (!stats.length) return null;

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
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
          <div className="text-xs text-[#8888a0] mt-1">{label}</div>
        </div>
      ))}
      {activity.active_period && (
        <div className="bg-[#14141f] rounded-lg p-4 border border-[#2a2a3a]">
          <div className="text-sm font-mono text-[#6366f1]">
            {activity.active_period}
          </div>
          <div className="text-xs text-[#8888a0] mt-1">活跃期</div>
        </div>
      )}
      {activity.peak_period && (
        <div className="bg-[#14141f] rounded-lg p-4 border border-[#2a2a3a]">
          <div className="text-sm font-mono text-[#f59e0b]">
            {activity.peak_period}
          </div>
          <div className="text-xs text-[#8888a0] mt-1">高峰期</div>
        </div>
      )}
    </div>
  );
}
