"use client";

import { useState, useMemo, useCallback } from "react";
import ForceGraph from "@/components/graphs/ForceGraph";
import DetailSidebar from "@/components/shared/DetailSidebar";
import type { GraphData, GraphNode, Person } from "@/lib/types";

interface Props {
  graphData: GraphData;
  peopleCount: number;
}

export default function AckNetworkClient({ graphData, peopleCount }: Props) {
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [hoveredNode, setHoveredNode] = useState<GraphNode | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [showCoauthor, setShowCoauthor] = useState(true);
  const [showAck, setShowAck] = useState(true);
  const [minAckWeight, setMinAckWeight] = useState(2);
  const [focusNodeId, setFocusNodeId] = useState<string | null>(null);

  const ackStats = useMemo(() => {
    const ackLinks = graphData.links.filter((l) => l.type === "acknowledgement");
    const coauthorLinks = graphData.links.filter((l) => l.type === "coauthor");
    return { ackCount: ackLinks.length, coauthorCount: coauthorLinks.length };
  }, [graphData]);

  const filteredData = useMemo(() => {
    let links = graphData.links.filter((l) => {
      if (l.type === "acknowledgement") {
        if (!showAck) return false;
        if ((l.weight ?? 1) < minAckWeight) return false;
      }
      if (l.type === "coauthor" && !showCoauthor) return false;
      return true;
    });

    // Drop isolated nodes
    const connected = new Set<string>();
    for (const l of links) {
      const s = typeof l.source === "string" ? l.source : (l.source as any).id;
      const t = typeof l.target === "string" ? l.target : (l.target as any).id;
      connected.add(s);
      connected.add(t);
    }
    let nodes = graphData.nodes.filter((n) => connected.has(n.id));

    // Search filter: dim non-matching
    const q = searchQuery.trim().toLowerCase();
    if (q) {
      const matched = new Set<string>();
      for (const n of nodes) {
        const p = n.data as Person | undefined;
        const hit =
          n.id.toLowerCase().includes(q) ||
          n.label.toLowerCase().includes(q) ||
          (p?.name.en || "").toLowerCase().includes(q) ||
          (p?.name.zh || "").includes(searchQuery.trim());
        if (hit) matched.add(n.id);
      }
      const neighbors = new Set<string>(matched);
      for (const l of links) {
        const s = typeof l.source === "string" ? l.source : (l.source as any).id;
        const t = typeof l.target === "string" ? l.target : (l.target as any).id;
        if (matched.has(s)) neighbors.add(t);
        if (matched.has(t)) neighbors.add(s);
      }
      nodes = nodes.map((n) => ({
        ...n,
        opacity: matched.has(n.id) ? 1 : neighbors.has(n.id) ? 0.5 : 0.08,
      }));
      links = links.map((l) => {
        const s = typeof l.source === "string" ? l.source : (l.source as any).id;
        const t = typeof l.target === "string" ? l.target : (l.target as any).id;
        const bothMatch = matched.has(s) && matched.has(t);
        const oneMatch = matched.has(s) || matched.has(t);
        return {
          ...l,
          opacity: bothMatch ? l.opacity : oneMatch ? l.opacity * 0.5 : 0.03,
        };
      });
    }

    return { nodes, links };
  }, [graphData, showCoauthor, showAck, minAckWeight, searchQuery]);

  const handleNodeClick = useCallback((node: GraphNode) => {
    setSelectedNode((prev) => (prev?.id === node.id ? null : node));
  }, []);

  const visibleAckCount = filteredData.links.filter(
    (l) => l.type === "acknowledgement"
  ).length;
  const visibleCoauthorCount = filteredData.links.filter(
    (l) => l.type === "coauthor"
  ).length;

  return (
    <div className="flex-1 flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between px-6 py-3 border-b border-[#2a2a3a] bg-[#14141f]/50">
        <div>
          <h1 className="text-lg font-semibold text-[#e8e8f0]">致谢网</h1>
          <p className="text-xs text-[#8888a0]">
            从 arXiv 论文致谢段抽取 · {peopleCount} 人 · {ackStats.ackCount} 条致谢边 ·{" "}
            {ackStats.coauthorCount} 条合著边 · 当前显示 {visibleAckCount}+{visibleCoauthorCount} 条
          </p>
        </div>
      </div>

      {/* Graph area */}
      <div
        className="relative flex-1"
        style={{ height: "calc(100vh - 56px - 52px)" }}
      >
        <ForceGraph
          data={filteredData}
          onNodeClick={handleNodeClick}
          onNodeHover={setHoveredNode}
          selectedNodeId={selectedNode?.id}
          focusNodeId={focusNodeId}
        />

        {/* Top controls */}
        <div className="absolute top-4 left-1/2 -translate-x-1/2 z-20 flex gap-3 items-center bg-[#14141f]/95 backdrop-blur-sm rounded-lg border border-[#2a2a3a] px-3 py-2 shadow-lg">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="搜索人名..."
            className="bg-transparent text-[#e8e8f0] placeholder-[#8888a0] text-sm outline-none w-40"
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery("")}
              className="text-[#8888a0] hover:text-[#e8e8f0] text-sm"
            >
              ×
            </button>
          )}
          <div className="w-px h-4 bg-[#2a2a3a]" />
          <label className="flex items-center gap-1 text-xs cursor-pointer">
            <input
              type="checkbox"
              checked={showAck}
              onChange={(e) => setShowAck(e.target.checked)}
              className="accent-[#a8a29e]"
            />
            <span className="w-3 h-0.5 inline-block" style={{ backgroundColor: "#a8a29e" }} />
            <span className="text-[#e8e8f0]">致谢</span>
          </label>
          <label className="flex items-center gap-1 text-xs cursor-pointer">
            <input
              type="checkbox"
              checked={showCoauthor}
              onChange={(e) => setShowCoauthor(e.target.checked)}
              className="accent-[#6366f1]"
            />
            <span className="w-3 h-0.5 inline-block" style={{ backgroundColor: "#6366f1" }} />
            <span className="text-[#e8e8f0]">合著</span>
          </label>
          <div className="w-px h-4 bg-[#2a2a3a]" />
          <div className="flex items-center gap-1 text-xs">
            <span className="text-[#8888a0]">致谢阈值 ≥</span>
            <input
              type="number"
              min={1}
              max={10}
              value={minAckWeight}
              onChange={(e) => setMinAckWeight(parseInt(e.target.value) || 1)}
              className="w-10 bg-[#0a0a0f] text-[#e8e8f0] text-xs px-1 py-0.5 rounded border border-[#2a2a3a]"
            />
          </div>
        </div>

        {/* Hover tooltip */}
        {hoveredNode && !selectedNode && (
          <div
            className="absolute z-30 pointer-events-none bg-[#14141f]/95 border border-[#2a2a3a] rounded-lg px-3 py-2 text-sm shadow-lg"
            style={{ left: "50%", top: 60, transform: "translateX(-50%)" }}
          >
            <span className="text-[#e8e8f0] font-medium">{hoveredNode.label}</span>
            {hoveredNode.data && "name" in hoveredNode.data && (
              <span className="text-[#8888a0] ml-2">
                {(hoveredNode.data as any).name?.en}
              </span>
            )}
          </div>
        )}

        <DetailSidebar
          node={selectedNode}
          onClose={() => setSelectedNode(null)}
        />
      </div>
    </div>
  );
}
