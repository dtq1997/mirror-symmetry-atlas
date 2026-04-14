"use client";

const AGE_COLORS = [
  { color: "#fcd34d", label: "新锐 (<35)" },
  { color: "#fbbf24", label: "青年 (35-45)" },
  { color: "#f59e0b", label: "中坚 (45-60)" },
  { color: "#d97706", label: "资深 (60-80)" },
  { color: "#b45309", label: "元老 (80+)" },
  { color: "#777788", label: "已故" },
];

export default function GraphLegend() {
  return (
    <div className="absolute bottom-4 left-4 z-10 bg-[#14141f]/90 backdrop-blur-sm rounded-lg border border-[#2a2a3a] p-3 text-xs">
      <div className="text-[#8888a0] mb-2 font-medium">图例</div>

      {/* Person age colors */}
      <div className="space-y-1 mb-3">
        {AGE_COLORS.map(({ color, label }) => (
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
          <span className="text-[#e8e8f0]">合著（宽度 = 论文数）</span>
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
      </div>

      <div className="h-px bg-[#2a2a3a] my-2" />
      <div className="text-[#8888a0]">节点大小 = 论文数/影响力</div>
    </div>
  );
}
