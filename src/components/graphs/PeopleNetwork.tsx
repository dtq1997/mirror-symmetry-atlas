"use client";

import { useState, useMemo, useCallback, useEffect } from "react";
import ForceGraph from "./ForceGraph";
import GraphControls from "./GraphControls";
import GraphLegend from "./GraphLegend";
import DetailSidebar from "../shared/DetailSidebar";
import type { GraphData, GraphNode, ConnectionType, Person } from "@/lib/types";
import { filterByYear } from "@/lib/graph";

interface PeopleNetworkProps {
  graphData: GraphData;
  institutionNames?: Record<string, string>;
}

// Get current institution of a person (from latest position entry)
function currentInstitutionOf(p: Person): string | null {
  const tl = p.career_timeline || [];
  // Prefer "present" position
  for (let i = tl.length - 1; i >= 0; i--) {
    const e = tl[i];
    if (e.type === "position" && e.institution) {
      const period = e.period || "";
      if (period.toLowerCase().includes("present")) return e.institution;
    }
  }
  // Else latest position or education
  for (let i = tl.length - 1; i >= 0; i--) {
    const e = tl[i];
    if ((e.type === "position" || e.type === "education") && e.institution) {
      return e.institution;
    }
  }
  return null;
}

export default function PeopleNetwork({ graphData, institutionNames }: PeopleNetworkProps) {
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [hoveredNode, setHoveredNode] = useState<GraphNode | null>(null);
  const [edgeFilters, setEdgeFilters] = useState<Record<ConnectionType, boolean>>({
    "advisor-student": true,
    "postdoc-mentor": true,
    "postdoc-group": true,
    coauthor: true,
    institutional: false,
    "co-student": true,
    grant: true,
    acknowledgement: false,
  });
  const [showGhosts, setShowGhosts] = useState(false);
  const [timeFilter, setTimeFilter] = useState<number | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [institutionFilter, setInstitutionFilter] = useState<string>("all");
  const [focusNodeId, setFocusNodeId] = useState<string | null>(null);

  // Distinct institutions present in the graph
  const institutionOptions = useMemo(() => {
    const counts = new Map<string, number>();
    for (const n of graphData.nodes) {
      const p = n.data as Person | undefined;
      if (!p) continue;
      const inst = currentInstitutionOf(p);
      if (inst) counts.set(inst, (counts.get(inst) ?? 0) + 1);
    }
    return Array.from(counts.entries())
      .sort((a, b) => b[1] - a[1])
      .map(([slug, n]) => ({ slug, n }));
  }, [graphData]);

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

    // Institution filter (dim non-matching)
    if (institutionFilter !== "all") {
      const matched = new Set<string>();
      for (const n of data.nodes) {
        const p = n.data as Person | undefined;
        if (!p) continue;
        if (currentInstitutionOf(p) === institutionFilter) matched.add(n.id);
      }
      data = {
        nodes: data.nodes.map((n) => ({
          ...n,
          opacity: matched.has(n.id) ? (n.opacity ?? 1) : 0.1,
        })),
        links: data.links.map((l) => {
          const s = typeof l.source === "string" ? l.source : (l.source as any).id;
          const t = typeof l.target === "string" ? l.target : (l.target as any).id;
          const visible = matched.has(s) && matched.has(t);
          return { ...l, opacity: visible ? l.opacity : 0.05 };
        }),
      };
    }

    // Search filter (dim non-matching, plus 1-hop neighbor glow)
    const q = searchQuery.trim().toLowerCase();
    if (q) {
      const matched = new Set<string>();
      for (const n of data.nodes) {
        const p = n.data as Person | undefined;
        const hit =
          n.id.toLowerCase().includes(q) ||
          n.label.toLowerCase().includes(q) ||
          (p?.name.en || "").toLowerCase().includes(q) ||
          (p?.name.zh || "").includes(searchQuery.trim());
        if (hit) matched.add(n.id);
      }
      const neighbors = new Set<string>(matched);
      for (const l of data.links) {
        const s = typeof l.source === "string" ? l.source : (l.source as any).id;
        const t = typeof l.target === "string" ? l.target : (l.target as any).id;
        if (matched.has(s)) neighbors.add(t);
        if (matched.has(t)) neighbors.add(s);
      }
      data = {
        nodes: data.nodes.map((n) => ({
          ...n,
          opacity: matched.has(n.id)
            ? 1
            : neighbors.has(n.id)
              ? 0.5
              : 0.08,
        })),
        links: data.links.map((l) => {
          const s = typeof l.source === "string" ? l.source : (l.source as any).id;
          const t = typeof l.target === "string" ? l.target : (l.target as any).id;
          const bothMatch = matched.has(s) && matched.has(t);
          const oneMatch = matched.has(s) || matched.has(t);
          return {
            ...l,
            opacity: bothMatch ? l.opacity : oneMatch ? l.opacity * 0.5 : 0.03,
          };
        }),
      };
    }

    return data;
  }, [graphData, edgeFilters, showGhosts, timeFilter, institutionFilter, searchQuery]);

  // Focus first match on search
  useEffect(() => {
    const q = searchQuery.trim().toLowerCase();
    if (!q) {
      setFocusNodeId(null);
      return;
    }
    const first = filteredData.nodes.find((n) => {
      const p = n.data as Person | undefined;
      return (
        n.id.toLowerCase().includes(q) ||
        n.label.toLowerCase().includes(q) ||
        (p?.name.en || "").toLowerCase().includes(q) ||
        (p?.name.zh || "").includes(searchQuery.trim())
      );
    });
    if (first) setFocusNodeId(first.id);
  }, [searchQuery, filteredData.nodes]);

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
        focusNodeId={focusNodeId}
      />

      {/* Search + institution filter — top center */}
      <div className="absolute top-4 left-1/2 -translate-x-1/2 z-20 flex gap-2 items-center bg-[#14141f]/95 backdrop-blur-sm rounded-lg border border-[#2a2a3a] px-3 py-2 shadow-lg">
        <svg
          className="w-4 h-4 text-[#8888a0]"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fillRule="evenodd"
            d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
            clipRule="evenodd"
          />
        </svg>
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="搜索人名或拼音..."
          className="bg-transparent text-[#e8e8f0] placeholder-[#8888a0] text-sm outline-none w-52"
        />
        {searchQuery && (
          <button
            onClick={() => setSearchQuery("")}
            className="text-[#8888a0] hover:text-[#e8e8f0] text-sm"
            title="清除搜索"
          >
            ×
          </button>
        )}
        <div className="w-px h-4 bg-[#2a2a3a]" />
        <select
          value={institutionFilter}
          onChange={(e) => setInstitutionFilter(e.target.value)}
          className="bg-[#0a0a0f] text-[#e8e8f0] text-xs px-2 py-1 rounded border border-[#2a2a3a] outline-none max-w-[10rem]"
          title="按机构过滤"
        >
          <option value="all">全部机构</option>
          {institutionOptions.map(({ slug, n }) => (
            <option key={slug} value={slug}>
              {institutionNames?.[slug] || slug} ({n})
            </option>
          ))}
        </select>
      </div>

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
            top: 60,
            transform: "translateX(-50%)",
          }}
        >
          <span className="text-[#e8e8f0] font-medium">{hoveredNode.label}</span>
          {hoveredNode.data && "name" in hoveredNode.data && (
            <span className="text-[#8888a0] ml-2">
              {(hoveredNode.data as any).name?.en}
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
