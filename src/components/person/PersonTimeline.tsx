"use client";

import type { CareerEntry } from "@/lib/types";

const TYPE_COLORS: Record<string, string> = {
  education: "#3b82f6",
  position: "#10b981",
  visit: "#8b5cf6",
  award: "#f59e0b",
  event: "#ef4444",
};

const TYPE_LABELS: Record<string, string> = {
  education: "求学",
  position: "职位",
  visit: "访问",
  award: "荣誉",
  event: "事件",
};

interface PersonTimelineProps {
  timeline: CareerEntry[];
}

export default function PersonTimeline({ timeline }: PersonTimelineProps) {
  if (!timeline?.length) return null;

  return (
    <div className="relative">
      {/* Vertical line */}
      <div className="absolute left-[7px] top-2 bottom-2 w-0.5 bg-[#2a2a3a]" />

      <div className="space-y-3">
        {timeline.map((entry, i) => {
          const color = TYPE_COLORS[entry.type] || "#8888a0";
          return (
            <div key={i} className="flex gap-4 relative">
              {/* Dot */}
              <div
                className="w-[15px] h-[15px] rounded-full border-2 shrink-0 mt-0.5 z-10"
                style={{
                  borderColor: color,
                  backgroundColor: "#14141f",
                }}
              />
              {/* Content */}
              <div className="min-w-0">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="text-sm font-mono text-[#6366f1]">
                    {entry.period}
                  </span>
                  <span
                    className="text-[10px] px-1.5 py-0.5 rounded-full"
                    style={{
                      backgroundColor: `${color}20`,
                      color,
                    }}
                  >
                    {TYPE_LABELS[entry.type]}
                  </span>
                </div>
                {(entry.role || entry.title) && (
                  <div className="text-sm text-[#e8e8f0] mt-0.5">
                    {entry.title || entry.role}
                  </div>
                )}
                {entry.institution && (
                  <div className="text-xs text-[#8888a0]">{entry.institution}</div>
                )}
                {entry.advisor && (
                  <div className="text-xs text-[#8888a0]">
                    Advisor: {entry.advisor}
                  </div>
                )}
                {entry.notes && (
                  <div className="text-xs text-[#8888a0] mt-0.5">{entry.notes}</div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
