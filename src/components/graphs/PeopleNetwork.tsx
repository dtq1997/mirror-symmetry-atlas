"use client";

import { useState, useMemo, useCallback } from "react";
import ForceGraph from "./ForceGraph";
import GraphControls from "./GraphControls";
import GraphLegend from "./GraphLegend";
import DetailSidebar from "../shared/DetailSidebar";
import type { GraphData, GraphNode, ConnectionType } from "@/lib/types";
import { filterByYear } from "@/lib/graph";

interface PeopleNetworkProps {
  graphData: GraphData;
}

export default function PeopleNetwork({ graphData }: PeopleNetworkProps) {
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [hoveredNode, setHoveredNode] = useState<GraphNode | null>(null);
  const [edgeFilters, setEdgeFilters] = useState<Record<ConnectionType, boolean>>({
    "advisor-student": true,
    coauthor: true,
    institutional: true,
  });
  const [showGhosts, setShowGhosts] = useState(true);
  const [timeFilter, setTimeFilter] = useState<number | null>(null);

  // Apply filters
  const filteredData = useMemo(() => {
    let data = graphData;

    // Edge type filter
    const filteredLinks = data.links.filter((l) => edgeFilters[l.type]);
    data = { ...data, links: filteredLinks };

    // Ghost filter
    if (!showGhosts) {
      const filteredNodes = data.nodes.filter((n) => !n.isGhost);
      const nodeIds = new Set(filteredNodes.map((n) => n.id));
      data = {
        nodes: filteredNodes,
        links: data.links.filter(
          (l) =>
            nodeIds.has(l.source as string) && nodeIds.has(l.target as string)
        ),
      };
    }

    // Time filter
    if (timeFilter !== null) {
      data = filterByYear(data, timeFilter);
    }

    return data;
  }, [graphData, edgeFilters, showGhosts, timeFilter]);

  const handleNodeClick = useCallback((node: GraphNode) => {
    setSelectedNode((prev) => (prev?.id === node.id ? null : node));
  }, []);

  const handleEdgeFilterChange = useCallback(
    (type: ConnectionType, enabled: boolean) => {
      setEdgeFilters((prev) => ({ ...prev, [type]: enabled }));
    },
    []
  );

  return (
    <div className="relative w-full h-full">
      <ForceGraph
        data={filteredData}
        onNodeClick={handleNodeClick}
        onNodeHover={setHoveredNode}
        selectedNodeId={selectedNode?.id}
      />

      <GraphControls
        edgeFilters={edgeFilters}
        onEdgeFilterChange={handleEdgeFilterChange}
        showGhosts={showGhosts}
        onShowGhostsChange={setShowGhosts}
      />

      <GraphLegend />

      {/* Hover tooltip */}
      {hoveredNode && !selectedNode && (
        <div
          className="absolute z-30 pointer-events-none bg-[#14141f]/95 border border-[#2a2a3a] rounded-lg px-3 py-2 text-sm shadow-lg"
          style={{
            left: "50%",
            top: 12,
            transform: "translateX(-50%)",
          }}
        >
          <span className="text-[#e8e8f0] font-medium">{hoveredNode.label}</span>
          {hoveredNode.data && "name" in hoveredNode.data && (
            <span className="text-[#8888a0] ml-2">
              {(hoveredNode.data as any).name?.zh ||
                (hoveredNode.data as any).name?.en}
            </span>
          )}
        </div>
      )}

      {/* Time slider */}
      <div className="absolute bottom-4 right-4 z-10 bg-[#14141f]/90 backdrop-blur-sm rounded-lg border border-[#2a2a3a] p-3 w-72">
        <div className="flex items-center justify-between mb-1">
          <span className="text-xs text-[#8888a0]">时间筛选</span>
          {timeFilter !== null ? (
            <div className="flex items-center gap-2">
              <span className="text-sm font-mono text-[#6366f1]">{timeFilter}</span>
              <button
                onClick={() => setTimeFilter(null)}
                className="text-xs text-[#8888a0] hover:text-[#e8e8f0]"
              >
                清除
              </button>
            </div>
          ) : (
            <span className="text-xs text-[#8888a0]">全部</span>
          )}
        </div>
        <input
          type="range"
          min={1950}
          max={2026}
          value={timeFilter ?? 2026}
          onChange={(e) => {
            const val = parseInt(e.target.value);
            setTimeFilter(val === 2026 ? null : val);
          }}
          className="w-full h-1 bg-[#2a2a3a] rounded-lg appearance-none cursor-pointer accent-[#6366f1]"
        />
        <div className="flex justify-between text-[10px] text-[#8888a0] mt-1">
          <span>1950</span>
          <span>1980</span>
          <span>2000</span>
          <span>2026</span>
        </div>
      </div>

      {/* Detail sidebar */}
      <DetailSidebar node={selectedNode} onClose={() => setSelectedNode(null)} />
    </div>
  );
}
