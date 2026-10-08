"use client";

import { useState, useMemo, useCallback } from "react";
import ForceGraph from "./ForceGraph";
import GraphControls from "./GraphControls";
import GraphLegend from "./GraphLegend";
import DetailSidebar from "../shared/DetailSidebar";
import type {
  GraphData,
  GraphLink,
  GraphNode,
  ConnectionType,
  Person,
} from "@/lib/types";
import { filterByYear, recordedInstitutions } from "@/lib/graph";

interface PeopleNetworkProps {
  graphData: GraphData;
  institutionNames?: Record<string, string>;
}

type GraphEndpoint = GraphLink["source"] | { id?: string };

function endpointId(endpoint: GraphEndpoint): string {
  return typeof endpoint === "string" ? endpoint : endpoint.id ?? "";
}

function personEnglishName(node: GraphNode): string | undefined {
  const data = node.data;
  return data && "name" in data ? data.name.en : undefined;
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
  const [currentYear] = useState(() => new Date().getFullYear());
  const [timeFilter, setTimeFilter] = useState<number | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [institutionFilter, setInstitutionFilter] = useState<string>("all");

  // Distinct institutions present in the graph
  const institutionOptions = useMemo(() => {
    const counts = new Map<string, number>();
    for (const n of graphData.nodes) {
      const p = n.data as Person | undefined;
      if (!p) continue;
      for (const inst of recordedInstitutions(p, timeFilter)) {
        counts.set(inst, (counts.get(inst) ?? 0) + 1);
      }
    }
    return Array.from(counts.entries())
      .sort((a, b) => b[1] - a[1])
      .map(([slug, n]) => ({ slug, n }));
  }, [graphData, timeFilter]);

  // Apply filters
  const filteredData = useMemo(() => {
    let data = graphData;

    // Edge type filter
    const filteredLinks = data.links.filter((l) => Object.hasOwn(edgeFilters, l.type) && edgeFilters[l.type as ConnectionType]);
    data = { ...data, links: filteredLinks };

    // Ghost filter
    if (!showGhosts) {
      const filteredNodes = data.nodes.filter((n) => !n.isGhost);
      const nodeIds = new Set(filteredNodes.map((n) => n.id));
      data = {
        nodes: filteredNodes,
        links: data.links.filter(
          (l) =>
            nodeIds.has(endpointId(l.source)) && nodeIds.has(endpointId(l.target))
        ),
      };
    }

    // Time filter
    if (timeFilter !== null) {
      data = filterByYear(data, timeFilter);
    }

    // Keep recorded affiliations through the same cutoff; never infer a current employer.
    if (institutionFilter !== "all") {
      const matched = new Set<string>();
      for (const n of data.nodes) {
        const p = n.data as Person | undefined;
        if (!p) continue;
        if (recordedInstitutions(p, timeFilter).includes(institutionFilter)) matched.add(n.id);
      }
      data = {
        nodes: data.nodes.filter((n) => matched.has(n.id)),
        links: data.links.filter((l) => matched.has(endpointId(l.source)) && matched.has(endpointId(l.target))),
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
        const s = endpointId(l.source);
        const t = endpointId(l.target);
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
          const s = endpointId(l.source);
          const t = endpointId(l.target);
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

  const focusNodeId = useMemo(() => {
    const q = searchQuery.trim().toLowerCase();
    if (!q) return null;
    const first = filteredData.nodes.find((n) => {
      const p = n.data as Person | undefined;
      return (
        n.id.toLowerCase().includes(q) ||
        n.label.toLowerCase().includes(q) ||
        (p?.name.en || "").toLowerCase().includes(q) ||
        (p?.name.zh || "").includes(searchQuery.trim())
      );
    });
    return first?.id ?? null;
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

      {filteredData.nodes.length === 0 && (
        <p className="absolute inset-x-4 top-1/2 text-center text-sm text-[#8888a0] pointer-events-none">
          此筛选下暂无可显示记录。可清除年份或选择全部履历机构。
        </p>
      )}

      {/* Search + institution filter — top center */}
      <div className="absolute top-4 left-16 right-4 sm:left-1/2 sm:right-auto sm:-translate-x-1/2 sm:w-max z-20 flex flex-wrap justify-center gap-2 max-w-[calc(100%_-_5rem)] items-center bg-[#14141f]/95 backdrop-blur-sm rounded-lg border border-[#2a2a3a] px-3 py-2 shadow-lg">
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
          className="bg-transparent text-[#e8e8f0] placeholder-[#8888a0] text-sm outline-none min-w-0 w-40 sm:w-52"
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
          title="按履历中记载的机构过滤"
          aria-label="履历机构"
        >
          <option value="all">全部履历机构</option>
          {institutionFilter !== "all" && !institutionOptions.some((option) => option.slug === institutionFilter) && (
            <option value={institutionFilter}>{institutionNames?.[institutionFilter] || institutionFilter}（该年份无记录）</option>
          )}
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
              {personEnglishName(hoveredNode)}
            </span>
          )}
        </div>
      )}

      {/* Time slider */}
      <div className="absolute bottom-4 right-4 z-10 bg-[#14141f]/90 backdrop-blur-sm rounded-lg border border-[#2a2a3a] p-3 w-72">
        <div className="flex items-center justify-between mb-1">
          <span className="text-xs text-[#8888a0]">截至年份</span>
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
          aria-label="截至年份"
          min={1950}
          max={currentYear}
          value={timeFilter ?? currentYear}
          onChange={(e) => {
            const val = parseInt(e.target.value);
            setTimeFilter(val);
          }}
          className="w-full h-1 bg-[#2a2a3a] rounded-lg appearance-none cursor-pointer accent-[#6366f1]"
        />
        <div className="flex justify-between text-[10px] text-[#8888a0] mt-1">
          <span>1950</span>
          <span>1980</span>
          <span>2000</span>
          <span>{currentYear}</span>
        </div>
        <p className="text-[10px] text-[#8888a0] mt-2" role="status" aria-label="图谱记录范围">
          {filteredData.nodes.length}个人物节点 · {filteredData.links.length}条关系记录。
          {timeFilter !== null ? "只含截至该年的有日期记录；缺年份不表示当时没有活动。" : "机构包含历史求学、任职与访问记录。"}
        </p>
      </div>

      {/* Detail sidebar */}
      <DetailSidebar node={filteredData.nodes.find((node) => node.id === selectedNode?.id) ?? null}
        contextNote={timeFilter !== null ? "完整人物档案：下列履历、论文及合著总数不受图谱年份筛选限制。" : undefined}
        onClose={() => setSelectedNode(null)}
        connections={graphData.links.flatMap((link) => link.data ? [link.data] : [])} />
    </div>
  );
}
