"use client";

import { CONCEPT_RELATIONS } from "@/lib/graph";
import type { ConceptRelationType, GraphData } from "@/lib/types";

export const DIFFICULTY_LABELS: Record<string, { label: string; color: string }> = {
  introductory: { label: "入门", color: "#22c55e" },
  intermediate: { label: "中级", color: "#3b82f6" },
  advanced: { label: "进阶", color: "#a855f7" },
  "research-frontier": { label: "前沿", color: "#ef4444" },
};

interface Props {
  graph: GraphData;
  hidden: Set<ConceptRelationType>;
  onToggle: (type: ConceptRelationType) => void;
  visibleCount: number;
}

export default function ConceptGraphLegend({ graph, hidden, onToggle, visibleCount }: Props) {
  return <details className="absolute bottom-4 left-4 z-10 max-w-[calc(100%_-_2rem)] rounded-lg border border-[#2a2a3a] bg-[#14141f]/95 p-3 text-xs">
    <summary className="cursor-pointer text-[#e8e8f0]">图例与关系筛选</summary>
    <div className="max-h-[45vh] overflow-y-auto mt-3 space-y-3">
      <div className="text-[#8888a0]">难度分级沿用本站记录</div>
      <div className="grid grid-cols-2 gap-2">
        {Object.entries(DIFFICULTY_LABELS).map(([key, { label, color }]) => <div key={key} className="flex gap-2 items-center text-[#e8e8f0]">
          <span className="w-3 h-3 rounded-full" style={{ backgroundColor: color }} />{label}
        </div>)}
      </div>
      <div className="border-t border-[#2a2a3a] pt-2 space-y-2">
        {(Object.keys(CONCEPT_RELATIONS) as ConceptRelationType[]).map((type) => {
          const style = CONCEPT_RELATIONS[type];
          return <label key={type} className="flex items-center gap-2 text-[#e8e8f0] cursor-pointer">
            <input type="checkbox" checked={!hidden.has(type)} onChange={() => onToggle(type)} aria-label={style.label} />
            <svg width="32" height="10" aria-hidden="true">
              <path d="M 0 5 L 30 5" stroke={style.color} strokeDasharray={style.dash?.join(" ")} />
              {type !== "related" && <path d="M 23 1 L 30 5 L 23 9" fill="none" stroke={style.color} />}
            </svg>
            {style.label}（{graph.links.filter((link) => link.type === type).length}）
          </label>;
        })}
      </div>
      <p role="status" className="text-[#c4b5fd]">显示 {visibleCount} 条关系记录</p>
      <p className="max-w-64 text-[#a0a0b8] leading-relaxed">连线来自本站记录，尚未逐项核实。后续方向不等于必需的前置条件；缺档节点仅表示被引用。</p>
    </div>
  </details>;
}
