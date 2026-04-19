"use client";

import { useState } from "react";
import type { ConnectionType } from "@/lib/types";

interface GraphControlsProps {
  onZoomIn?: () => void;
  onZoomOut?: () => void;
  onReset?: () => void;
  edgeFilters: Record<ConnectionType, boolean>;
  onEdgeFilterChange: (type: ConnectionType, enabled: boolean) => void;
  showGhosts: boolean;
  onShowGhostsChange: (show: boolean) => void;
}

const EDGE_LABELS: Record<ConnectionType, { label: string; color: string }> = {
  "advisor-student": { label: "师承", color: "#f59e0b" },
  "postdoc-mentor": { label: "博后合作导师", color: "#fbbf24" },
  "postdoc-group": { label: "博后所在组", color: "#fcd34d" },
  coauthor: { label: "合著", color: "#6366f1" },
  institutional: { label: "同机构", color: "#8b5cf6" },
  "co-student": { label: "同门", color: "#10b981" },
  grant: { label: "基金", color: "#ec4899" },
  acknowledgement: { label: "致谢", color: "#a8a29e" },
};

export default function GraphControls({
  onZoomIn,
  onZoomOut,
  onReset,
  edgeFilters,
  onEdgeFilterChange,
  showGhosts,
  onShowGhostsChange,
}: GraphControlsProps) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="absolute top-4 left-4 z-10 flex flex-col gap-2">
      {/* Zoom controls */}
      <div className="flex flex-col gap-1 bg-[#14141f]/90 backdrop-blur-sm rounded-lg border border-[#2a2a3a] p-1">
        <button
          onClick={onZoomIn}
          className="w-8 h-8 flex items-center justify-center text-[#e8e8f0] hover:bg-[#2a2a3a] rounded transition-colors text-lg"
          title="放大"
        >
          +
        </button>
        <div className="w-full h-px bg-[#2a2a3a]" />
        <button
          onClick={onZoomOut}
          className="w-8 h-8 flex items-center justify-center text-[#e8e8f0] hover:bg-[#2a2a3a] rounded transition-colors text-lg"
          title="缩小"
        >
          -
        </button>
        <div className="w-full h-px bg-[#2a2a3a]" />
        <button
          onClick={onReset}
          className="w-8 h-8 flex items-center justify-center text-[#8888a0] hover:bg-[#2a2a3a] hover:text-[#e8e8f0] rounded transition-colors text-xs"
          title="重置视图"
        >
          ⟳
        </button>
      </div>

      {/* Filter panel */}
      <div className="bg-[#14141f]/90 backdrop-blur-sm rounded-lg border border-[#2a2a3a]">
        <button
          onClick={() => setExpanded(!expanded)}
          className="w-full px-3 py-2 text-left text-xs text-[#8888a0] hover:text-[#e8e8f0] transition-colors flex items-center gap-1"
        >
          <span>{expanded ? "▼" : "▶"}</span>
          <span>筛选</span>
        </button>
        {expanded && (
          <div className="px-3 pb-3 space-y-2">
            {(Object.entries(EDGE_LABELS) as [ConnectionType, { label: string; color: string }][]).map(
              ([type, { label, color }]) => (
                <label key={type} className="flex items-center gap-2 text-xs cursor-pointer">
                  <input
                    type="checkbox"
                    checked={edgeFilters[type]}
                    onChange={(e) => onEdgeFilterChange(type, e.target.checked)}
                    className="rounded accent-[#6366f1]"
                  />
                  <span
                    className="w-3 h-0.5 inline-block rounded"
                    style={{ backgroundColor: color }}
                  />
                  <span className="text-[#e8e8f0]">{label}</span>
                </label>
              )
            )}
            <div className="h-px bg-[#2a2a3a]" />
            <label className="flex items-center gap-2 text-xs cursor-pointer">
              <input
                type="checkbox"
                checked={showGhosts}
                onChange={(e) => onShowGhostsChange(e.target.checked)}
                className="rounded accent-[#6366f1]"
              />
              <span className="text-[#e8e8f0]">未记录节点</span>
            </label>
          </div>
        )}
      </div>
    </div>
  );
}
