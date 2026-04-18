"use client";

import { useState } from "react";
import PeopleNetwork from "@/components/graphs/PeopleNetwork";
import type { GraphData, Person } from "@/lib/types";
import Link from "next/link";

interface Props {
  graphData: GraphData;
  people: Person[];
  institutionNames?: Record<string, string>;
}

export default function PeopleNetworkClient({ graphData, people, institutionNames }: Props) {
  const [viewMode, setViewMode] = useState<"graph" | "list">("graph");

  return (
    <div className="flex-1 flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between px-6 py-3 border-b border-[#2a2a3a] bg-[#14141f]/50">
        <div>
          <h1 className="text-lg font-semibold text-[#e8e8f0]">
            人物关系网络
          </h1>
          <p className="text-xs text-[#8888a0]">
            {people.length} 人 · {graphData.links.length} 条关系
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

      {/* Content */}
      {viewMode === "graph" ? (
        <div
          className="relative"
          style={{ height: "calc(100vh - 56px - 52px)" }}
        >
          <PeopleNetwork graphData={graphData} institutionNames={institutionNames} />
        </div>
      ) : (
        <div className="flex-1 overflow-auto px-6 py-4">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-[#8888a0] border-b border-[#2a2a3a]">
                <th className="py-2 pr-4">姓名</th>
                <th className="py-2 pr-4">国籍</th>
                <th className="py-2 pr-4">论文</th>
                <th className="py-2 pr-4">学生</th>
                <th className="py-2">状态</th>
              </tr>
            </thead>
            <tbody>
              {people
                .sort((a, b) => (b.activity?.total_papers ?? 0) - (a.activity?.total_papers ?? 0))
                .map((p) => (
                  <tr
                    key={p.slug}
                    className="border-b border-[#2a2a3a]/50 hover:bg-[#14141f] transition-colors"
                  >
                    <td className="py-2.5 pr-4">
                      <Link
                        href={`/people/${p.slug}`}
                        className="text-[#f59e0b] hover:text-[#fbbf24] transition-colors"
                      >
                        {p.name.en}
                      </Link>
                      {p.name.zh && (
                        <span className="text-[#8888a0] ml-2 text-xs">
                          {p.name.zh}
                        </span>
                      )}
                    </td>
                    <td className="py-2.5 pr-4 text-[#8888a0]">
                      {p.nationality || "—"}
                    </td>
                    <td className="py-2.5 pr-4 text-[#e8e8f0]">
                      {p.activity?.total_papers ?? "—"}
                    </td>
                    <td className="py-2.5 pr-4 text-[#e8e8f0]">
                      {p.students?.length || "—"}
                    </td>
                    <td className="py-2.5">
                      {p.died ? (
                        <span className="text-xs text-[#8888a0]">
                          {p.born}–{p.died}
                        </span>
                      ) : (
                        <span className="text-xs text-[#10b981]">活跃</span>
                      )}
                    </td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
