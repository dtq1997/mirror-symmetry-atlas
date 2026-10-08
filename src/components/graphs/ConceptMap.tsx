"use client";

import { useState, useMemo, useCallback } from "react";
import ForceGraph from "./ForceGraph";
import type { GraphData, GraphNode, Concept, ConceptRelationType } from "@/lib/types";
import { getPrerequisiteChain, highlightConceptPrerequisites } from "@/lib/graph";
import Link from "@/components/shared/AtlasLink";
import MathText from "../shared/MathText";
import { displayName } from "@/lib/name";
import ConceptGraphLegend, { DIFFICULTY_LABELS } from "./ConceptGraphLegend";
import { CONCEPT_ROLE_LABELS } from "@/lib/concepts";

interface ConceptMapProps {
  graphData: GraphData;
  concepts: Concept[];
}

export default function ConceptMap({ graphData, concepts }: ConceptMapProps) {
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [learningPathTarget, setLearningPathTarget] = useState<string | null>(
    null
  );

  const [hidden, setHidden] = useState<Set<ConceptRelationType>>(new Set());
  const optionLabels = useMemo(() => {
    const counts = new Map<string, number>();
    for (const node of graphData.nodes) counts.set(node.label, (counts.get(node.label) ?? 0) + 1);
    return new Map(graphData.nodes.map((node) => [node.id,
      (counts.get(node.label) ?? 0) > 1 && node.data && "name" in node.data
        ? `${node.label} · ${node.data.name.en}` : node.label]));
  }, [graphData.nodes]);

  // Trace only literal prerequisite records, not further-study suggestions.
  const pathChain = useMemo(() => {
    if (!learningPathTarget) return null;
    return getPrerequisiteChain(learningPathTarget, concepts);
  }, [learningPathTarget, concepts]);

  // Highlight learning path
  const displayData = useMemo(() => {
    const base = pathChain ? highlightConceptPrerequisites(graphData, pathChain) : graphData;
    return { ...base, links: base.links.filter((link) => !hidden.has(link.type as ConceptRelationType)) };
  }, [graphData, pathChain, hidden]);

  const toggleRelation = (type: ConceptRelationType) => setHidden((old) => {
    const next = new Set(old);
    if (next.has(type)) next.delete(type); else next.add(type);
    return next;
  });

  const handleNodeClick = useCallback(
    (node: GraphNode) => {
      if (node.isGhost || learningPathTarget === node.id) {
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
        focusNodeId={selectedNode?.id}
      />

      <div className="absolute top-4 left-16 right-4 sm:right-auto z-10">
        <select aria-label="选择图中概念" value={selectedNode?.id ?? ""}
          onChange={(event) => {
            const node = graphData.nodes.find((n) => n.id === event.target.value);
            if (node) handleNodeClick(node);
            else { setSelectedNode(null); setLearningPathTarget(null); }
          }}
          className="w-full sm:w-64 max-w-full rounded-lg border border-[#2a2a3a] bg-[#14141f] p-2 text-sm text-[#e8e8f0]">
          <option value="">选择概念并定位</option>
          {graphData.nodes.map((node) => <option key={node.id} value={node.id}>{optionLabels.get(node.id)}</option>)}
        </select>
      </div>
      <ConceptGraphLegend graph={graphData} hidden={hidden} onToggle={toggleRelation} visibleCount={displayData.links.length} />
      <ConceptTraceNotice selected={selectedNode}
        target={graphData.nodes.find((node) => node.id === learningPathTarget)}
        count={pathChain?.size ?? 0} onClear={() => setLearningPathTarget(null)} />

      {/* Sidebar */}
      {selectedNode && selectedNode.data && !selectedNode.isGhost && (
        <div
          className="fixed top-[56px] right-0 w-[400px] max-w-full h-[calc(100vh-56px)] bg-[#14141f] border-l border-[#2a2a3a] overflow-y-auto z-40 shadow-2xl"
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
            aria-label="关闭概念详情"
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

function ConceptTraceNotice({ selected, target, count, onClear }: {
  selected: GraphNode | null; target?: GraphNode; count: number; onClear: () => void;
}) {
  if (!target && !selected?.isGhost) return null;
  return <div className="absolute top-16 left-16 right-4 sm:max-w-md z-10 bg-[#14141f]/95 rounded-lg border border-[#ef4444]/50 px-3 py-2 text-sm flex flex-wrap items-center gap-2">
    {selected?.isGhost ? <p role="status" className="text-[#a0a0b8]">
      {selected.label}：目前只有引用记录，暂无定义及来源档案。
    </p> : <>
      <span className="text-[#ef4444]">前置追溯：</span>
      <span className="text-[#e8e8f0]">{target?.label}</span>
      <span className="text-[#8888a0]">（含当前概念，共 {count} 项）</span>
      <button onClick={onClear} className="text-[#a0a0b8] hover:text-[#e8e8f0]">清除</button>
    </>}
  </div>;
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
          <div className="text-xs text-[#8888a0] mb-2">前置概念记录</div>
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
          <div className="text-xs text-[#8888a0] mb-2">后续方向记录</div>
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

      {concept.related?.length > 0 && <div>
        <div className="text-xs text-[#8888a0] mb-2">相关概念记录</div>
        <div className="flex flex-wrap gap-1">
          {concept.related.map((slug) => <Link key={slug} href={`/concepts/${slug}`}
            className="px-2 py-0.5 text-xs rounded-full bg-[#2a2a3a] text-[#c4b5fd]">{slug}</Link>)}
        </div>
      </div>}
      <p className="text-xs text-[#8888a0]">{concept.review_note || "以上沿用本站概念记录，定义、关系与历史归属仍待逐项核实；前置追溯不代表唯一或严格的学习顺序。"}</p>

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
                  {displayName(ct.person)}
                </Link>
                <span className="text-[#8888a0] ml-2">（{CONCEPT_ROLE_LABELS[ct.role] || ct.role}）</span>
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
          查看详情与来源 →
        </Link>
      </div>
    </div>
  );
}
