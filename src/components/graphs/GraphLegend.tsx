"use client";

import { useMobile } from "@/lib/use-mobile";

const PERSON_COLORS = [
  { color: "#f59e0b", label: "已建档人物" },
  { color: "#777788", label: "有逝世记录" },
];

export default function GraphLegend() {
  const mobile = useMobile();
  return (
    <details open={!mobile} className="absolute bottom-32 sm:bottom-4 left-4 z-10 bg-[#14141f]/90 backdrop-blur-sm rounded-lg border border-[#2a2a3a] p-3 text-xs">
      <summary className="text-[#8888a0] mb-2 font-medium cursor-pointer">图例</summary>

      {/* Person record colors */}
      <div className="space-y-1 mb-3">
        {PERSON_COLORS.map(({ color, label }) => (
          <div key={label} className="flex items-center gap-2">
            <span
              className="w-3 h-3 rounded-full inline-block shrink-0"
              style={{ backgroundColor: color }}
            />
            <span className="text-[#e8e8f0]">{label}</span>
          </div>
        ))}
        <div className="flex items-center gap-2">
          <span
            className="w-3 h-3 rounded-full inline-block border border-dashed border-white/30 shrink-0"
            style={{ backgroundColor: "rgba(255,255,255,0.1)" }}
          />
          <span className="text-[#e8e8f0]">未建档</span>
        </div>
      </div>

      <div className="h-px bg-[#2a2a3a] mb-2" />

      {/* Edge types */}
      <div className="space-y-1.5">
        <div className="flex items-center gap-2">
          <span className="w-6 h-0.5 bg-[#f59e0b] inline-block" />
          <span className="text-[#e8e8f0]">导师 → 学生</span>
        </div>
        <div className="flex items-center gap-2">
          <span
            className="w-6 h-0.5 inline-block"
            style={{
              backgroundImage:
                "repeating-linear-gradient(90deg, #6366f1 0, #6366f1 3px, transparent 3px, transparent 6px)",
            }}
          />
          <span className="text-[#e8e8f0]">共同收录论文（线越粗，篇数越多）</span>
        </div>
        <div className="flex items-center gap-2">
          <span
            className="w-6 h-0.5 inline-block"
            style={{
              backgroundImage:
                "repeating-linear-gradient(90deg, #8b5cf6 0, #8b5cf6 2px, transparent 2px, transparent 4px)",
            }}
          />
          <span className="text-[#e8e8f0]">同机构</span>
        </div>
        <div className="flex items-center gap-2">
          <span
            className="w-6 h-0.5 inline-block"
            style={{
              backgroundImage:
                "repeating-linear-gradient(90deg, #10b981 0, #10b981 5px, transparent 5px, transparent 8px)",
            }}
          />
          <span className="text-[#e8e8f0]">同门</span>
        </div>
        <div className="flex items-center gap-2">
          <span
            className="w-6 h-0.5 inline-block"
            style={{
              backgroundImage:
                "repeating-linear-gradient(90deg, #ec4899 0, #ec4899 2px, transparent 2px, transparent 5px)",
            }}
          />
          <span className="text-[#e8e8f0]">同号基金资助（来源见人物资料）</span>
        </div>
      </div>

      <div className="h-px bg-[#2a2a3a] my-2" />
      <div className="text-[#8888a0]">节点越大，本站收录论文越多</div>
      <div className="text-[#8888a0] mt-1 max-w-60">合著线仅据双方相同论文标识；身份仍在逐篇复核。</div>
    </details>
  );
}
