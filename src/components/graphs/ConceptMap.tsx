"use client";

import { useState, useMemo, useCallback } from "react";
import ForceGraph from "./ForceGraph";
import DetailSidebar from "../shared/DetailSidebar";
import type { GraphData, GraphNode, Concept } from "@/lib/types";
import { getPrerequisiteChain } from "@/lib/graph";
import Link from "next/link";
import MathText from "../shared/MathText";

interface ConceptMapProps {
  graphData: GraphData;
  concepts: Concept[];
}

const DIFFICULTY_LABELS: Record<string, { label: string; color: string }> = {
  introductory: { label: "入门", color: "#22c55e" },
  intermediate: { label: "中级", color: "#3b82f6" },
  advanced: { label: "进阶", color: "#a855f7" },
  "research-frontier": { label: "前沿", color: "#ef4444" },
};

export default function ConceptMap({ graphData, concepts }: ConceptMapProps) {
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [learningPathTarget, setLearningPathTarget] = useState<string | null>(
    null
  );

  // Compute learning path chain
  const pathChain = useMemo(() => {
    if (!learningPathTarget) return null;
    return getPrerequisiteChain(learningPathTarget, concepts);
  }, [learningPathTarget, concepts]);

  // Highlight learning path
  const displayData = useMemo(() => {
    if (!pathChain) return graphData;

    const highlightedNodes = graphData.nodes.map((n) => ({
      ...n,
      opacity: pathChain.has(n.id) ? 1 : 0.15,
    }));
    const highlightedLinks = graphData.links.map((l) => ({
      ...l,
      opacity:
        pathChain.has(l.source as string) && pathChain.has(l.target as string)
          ? 0.8
          : 0.05,
    }));
    return { nodes: highlightedNodes, links: highlightedLinks };
  }, [graphData, pathChain]);

  const handleNodeClick = useCallback(
    (node: GraphNode) => {
      if (learningPathTarget === node.id) {
        setLearningPathTarget(null);
      } else {
        setLearningPathTarget(node.id);
      }
      setSelectedNode((prev) => (prev?.id === node.id ? null : node));
    },
    [learningPathTarget]
  );

  return (
    <div className="relative w-full h-full">
      <ForceGraph
        data={displayData}
        onNodeClick={handleNodeClick}
        selectedNodeId={selectedNode?.id}
      />

      {/* Legend */}
      <div className="absolute bottom-4 left-4 z-10 bg-[#14141f]/90 backdrop-blur-sm rounded-lg border border-[#2a2a3a] p-3 text-xs">
        <div className="text-[#8888a0] mb-2 font-medium">图例（难度）</div>
        <div className="space-y-1 mb-3">
          {Object.entries(DIFFICULTY_LABELS).map(([key, { label, color }]) => (
            <div key={key} className="flex items-center gap-2">
              <span
                className="w-3 h-3 rounded-full inline-block shrink-0"
                style={{ backgroundColor: color }}
              />
              <span className="text-[#e8e8f0]">{label}</span>
            </div>
          ))}
        </div>
        <div className="h-px bg-[#2a2a3a] mb-2" />
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="w-6 h-0.5 bg-[#ef4444] inline-block" />
            <span className="text-[#e8e8f0]">前置依赖（有向）</span>
          </div>
          <div className="flex items-center gap-2">
            <span
              className="w-6 h-0.5 inline-block"
              style={{
                backgroundImage:
                  "repeating-linear-gradient(90deg, #8888a0 0, #8888a0 2px, transparent 2px, transparent 5px)",
              }}
            />
            <span className="text-[#e8e8f0]">相关</span>
          </div>
        </div>
        <div className="h-px bg-[#2a2a3a] my-2" />
        <div className="text-[#8888a0]">点击节点 → 显示学习路径</div>
      </div>

      {/* Learning path indicator */}
      {learningPathTarget && (
        <div className="absolute top-4 left-1/2 -translate-x-1/2 z-10 bg-[#14141f]/90 backdrop-blur-sm rounded-lg border border-[#ef4444]/50 px-4 py-2 text-sm flex items-center gap-3">
          <span className="text-[#ef4444]">学习路径：</span>
          <span className="text-[#e8e8f0] font-medium">
            {learningPathTarget}
          </span>
          <span className="text-[#8888a0]">
            （{pathChain?.size ?? 0} 个前置概念）
          </span>
          <button
            onClick={() => setLearningPathTarget(null)}
            className="text-[#8888a0] hover:text-[#e8e8f0] ml-2"
          >
            清除
          </button>
        </div>
      )}

      {/* Sidebar */}
      {selectedNode && selectedNode.data && !selectedNode.isGhost && (
        <div
          className="fixed top-[56px] right-0 w-[400px] h-[calc(100vh-56px)] bg-[#14141f] border-l border-[#2a2a3a] overflow-y-auto z-20 shadow-2xl"
          style={{ animation: "slideIn 0.2s ease-out" }}
        >
          <style jsx>{`
            @keyframes slideIn {
              from {
                transform: translateX(100%);
              }
              to {
                transform: translateX(0);
              }
            }
          `}</style>
          <button
            onClick={() => {
              setSelectedNode(null);
              setLearningPathTarget(null);
            }}
            className="absolute top-3 right-3 w-8 h-8 flex items-center justify-center text-[#8888a0] hover:text-[#e8e8f0] hover:bg-[#2a2a3a] rounded z-10"
          >
            ×
          </button>
          <ConceptSidebar concept={selectedNode.data as Concept} />
        </div>
      )}
    </div>
  );
}

function ConceptSidebar({ concept }: { concept: Concept }) {
  const diffInfo = DIFFICULTY_LABELS[concept.difficulty];
  return (
    <div className="p-5 space-y-4">
      <div>
        <h2 className="text-xl font-semibold text-[#e8e8f0]">
          {concept.name.en}
        </h2>
        {concept.name.zh && (
          <p className="text-[#8888a0] text-sm">{concept.name.zh}</p>
        )}
        <div className="flex items-center gap-2 mt-2">
          {diffInfo && (
            <span
              className="px-2 py-0.5 text-xs rounded-full"
              style={{
                backgroundColor: `${diffInfo.color}20`,
                color: diffInfo.color,
              }}
            >
              {diffInfo.label}
            </span>
          )}
          {concept.year_introduced && (
            <span className="text-xs text-[#8888a0]">
              {concept.year_introduced} 年引入
            </span>
          )}
        </div>
      </div>

      {concept.definition && (
        <MathText className="bg-[#0a0a0f] rounded-lg p-3 border border-[#2a2a3a] text-sm text-[#e8e8f0] leading-relaxed">
          {concept.definition}
        </MathText>
      )}

      {concept.prerequisites?.length > 0 && (
        <div>
          <div className="text-xs text-[#8888a0] mb-2">前置概念</div>
          <div className="flex flex-wrap gap-1">
            {concept.prerequisites.map((p) => (
              <Link
                key={p}
                href={`/concepts/${p}`}
                className="px-2 py-0.5 text-xs rounded-full bg-[#ef4444]/15 text-[#f87171] border border-[#ef4444]/30 hover:bg-[#ef4444]/25"
              >
                {p}
              </Link>
            ))}
          </div>
        </div>
      )}

      {concept.leads_to?.length > 0 && (
        <div>
          <div className="text-xs text-[#8888a0] mb-2">后续概念</div>
          <div className="flex flex-wrap gap-1">
            {concept.leads_to.map((l) => (
              <Link
                key={l}
                href={`/concepts/${l}`}
                className="px-2 py-0.5 text-xs rounded-full bg-[#6366f1]/15 text-[#818cf8] border border-[#6366f1]/30 hover:bg-[#6366f1]/25"
              >
                {l}
              </Link>
            ))}
          </div>
        </div>
      )}

      {concept.key_people?.length > 0 && (
        <div>
          <div className="text-xs text-[#8888a0] mb-2">关键人物</div>
          <div className="flex flex-wrap gap-1">
            {concept.key_people.map((p) => (
              <Link
                key={p}
                href={`/people/${p}`}
                className="px-2 py-0.5 text-xs rounded-full bg-[#f59e0b]/15 text-[#fbbf24] border border-[#f59e0b]/30 hover:bg-[#f59e0b]/25"
              >
                {p}
              </Link>
            ))}
          </div>
        </div>
      )}

      {concept.contributions && concept.contributions.length > 0 && (
        <div>
          <div className="text-xs text-[#8888a0] mb-2">贡献者</div>
          <div className="space-y-1.5">
            {concept.contributions.map((ct) => (
              <div
                key={ct.person}
                className="text-xs bg-[#0a0a0f] rounded p-2 border border-[#2a2a3a]"
              >
                <Link
                  href={`/people/${ct.person}`}
                  className="text-[#f59e0b]"
                >
                  {ct.person}
                </Link>
                <span className="text-[#8888a0] ml-2">({ct.role})</span>
                {ct.description && (
                  <div className="text-[#8888a0] mt-0.5">{ct.description}</div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="pt-2 border-t border-[#2a2a3a]">
        <Link
          href={`/concepts/${concept.slug}`}
          className="text-sm text-[#6366f1] hover:text-[#818cf8]"
        >
          查看详情 →
        </Link>
      </div>
    </div>
  );
}
