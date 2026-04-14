"use client";

import { useState } from "react";
import ConceptMap from "@/components/graphs/ConceptMap";
import type { GraphData, Concept, Difficulty } from "@/lib/types";
import Link from "next/link";

const DIFFICULTY_COLORS: Record<string, string> = {
  introductory: "#22c55e",
  intermediate: "#3b82f6",
  advanced: "#a855f7",
  "research-frontier": "#ef4444",
};
const DIFFICULTY_LABELS: Record<string, string> = {
  introductory: "入门",
  intermediate: "中级",
  advanced: "进阶",
  "research-frontier": "前沿",
};

interface Props {
  graphData: GraphData;
  concepts: Concept[];
}

export default function ConceptPageClient({ graphData, concepts }: Props) {
  const [viewMode, setViewMode] = useState<"graph" | "list">("graph");

  return (
    <div className="flex-1 flex flex-col">
      <div className="flex items-center justify-between px-6 py-3 border-b border-[#2a2a3a] bg-[#14141f]/50">
        <div>
          <h1 className="text-lg font-semibold text-[#e8e8f0]">
            概念知识图谱
          </h1>
          <p className="text-xs text-[#8888a0]">
            {concepts.length} 个概念 · 点击节点查看学习路径
          </p>
        </div>
        <div className="flex items-center gap-1 bg-[#0a0a0f] rounded-lg p-1 border border-[#2a2a3a]">
          <button
            onClick={() => setViewMode("graph")}
            className={`px-3 py-1 text-xs rounded-md transition-colors ${
              viewMode === "graph"
                ? "bg-[#6366f1] text-white"
                : "text-[#8888a0] hover:text-[#e8e8f0]"
            }`}
          >
            图谱
          </button>
          <button
            onClick={() => setViewMode("list")}
            className={`px-3 py-1 text-xs rounded-md transition-colors ${
              viewMode === "list"
                ? "bg-[#6366f1] text-white"
                : "text-[#8888a0] hover:text-[#e8e8f0]"
            }`}
          >
            列表
          </button>
        </div>
      </div>

      {viewMode === "graph" ? (
        <div
          className="relative"
          style={{ height: "calc(100vh - 56px - 52px)" }}
        >
          <ConceptMap graphData={graphData} concepts={concepts} />
        </div>
      ) : (
        <div className="flex-1 overflow-auto px-6 py-4">
          <div className="space-y-3">
            {concepts
              .sort((a, b) => {
                const order: Difficulty[] = [
                  "introductory",
                  "intermediate",
                  "advanced",
                  "research-frontier",
                ];
                return order.indexOf(a.difficulty) - order.indexOf(b.difficulty);
              })
              .map((c) => (
                <Link
                  key={c.slug}
                  href={`/concepts/${c.slug}`}
                  className="block bg-[#14141f] rounded-lg p-4 border border-[#2a2a3a] hover:border-opacity-50 transition-colors"
                  style={{
                    borderLeftColor:
                      DIFFICULTY_COLORS[c.difficulty] || "#6366f1",
                    borderLeftWidth: 3,
                  }}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <span className="text-sm font-medium text-[#e8e8f0]">
                        {c.name.en}
                      </span>
                      {c.name.zh && (
                        <span className="text-sm text-[#8888a0] ml-2">
                          {c.name.zh}
                        </span>
                      )}
                    </div>
                    <span
                      className="text-[10px] px-2 py-0.5 rounded-full"
                      style={{
                        backgroundColor: `${DIFFICULTY_COLORS[c.difficulty]}20`,
                        color: DIFFICULTY_COLORS[c.difficulty],
                      }}
                    >
                      {DIFFICULTY_LABELS[c.difficulty]}
                    </span>
                  </div>
                  {c.prerequisites?.length > 0 && (
                    <div className="text-xs text-[#8888a0] mt-1">
                      前置：{c.prerequisites.join(", ")}
                    </div>
                  )}
                </Link>
              ))}
          </div>
        </div>
      )}
    </div>
  );
}
