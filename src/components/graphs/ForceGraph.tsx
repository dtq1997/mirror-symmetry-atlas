"use client";

import { useRef, useCallback, useEffect, useState } from "react";
import type { RefCallback, ReactElement } from "react";
import dynamic from "next/dynamic";
import { forceCollide, forceX, forceY } from "d3-force";
import type { GraphData, GraphNode, GraphLink } from "@/lib/types";
import { getForceParams, simulationGraph } from "@/lib/graph";
import type { LinkObject, NodeObject } from "react-force-graph-2d";

const ForceGraph2D = dynamic(() => import("react-force-graph-2d"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-full flex items-center justify-center text-[#8888a0] text-sm">
      加载图谱...
    </div>
  ),
});

interface ForceGraphProps {
  data: GraphData;
  width?: number;
  height?: number;
  onNodeClick?: (node: GraphNode) => void;
  onNodeHover?: (node: GraphNode | null) => void;
  selectedNodeId?: string | null;
  focusNodeId?: string | null;
}

type ForceNode = NodeObject<GraphNode>;
type ForceLink = LinkObject<GraphNode, GraphLink>;
type ForceGraphCanvasData = {
  nodes: ForceNode[];
  links: ForceLink[];
};

interface ForceConfig {
  strength?: (value: number) => ForceConfig;
  distance?: (value: number) => ForceConfig;
}

interface ForceGraphHandle {
  d3Force(name: string): ForceConfig | undefined;
  d3Force(name: string, forceFn: unknown): unknown;
  d3ReheatSimulation(): unknown;
  centerAt(x?: number, y?: number, durationMs?: number): unknown;
  zoom(): number;
  zoom(scale: number, durationMs?: number): unknown;
  zoomToFit(durationMs?: number, padding?: number): unknown;
}

interface ForceGraphCanvasProps {
  ref?: RefCallback<ForceGraphHandle>;
  graphData: ForceGraphCanvasData;
  width: number;
  height: number;
  backgroundColor: string;
  nodeCanvasObject: (
    node: ForceNode,
    ctx: CanvasRenderingContext2D,
    globalScale: number
  ) => void;
  nodePointerAreaPaint: (
    node: ForceNode,
    color: string,
    ctx: CanvasRenderingContext2D,
    globalScale: number
  ) => void;
  linkCanvasObject: (
    link: ForceLink,
    ctx: CanvasRenderingContext2D,
    globalScale: number
  ) => void;
  onNodeClick: (node: ForceNode) => void;
  onNodeHover: (node: ForceNode | null) => void;
  onZoom: (transform: { k: number }) => void;
  onEngineStop: () => void;
  enableNodeDrag: boolean;
  enableZoomInteraction: boolean;
  enablePanInteraction: boolean;
  cooldownTicks: number;
  minZoom: number;
  maxZoom: number;
}

const ForceGraphCanvas = ForceGraph2D as unknown as (
  props: ForceGraphCanvasProps
) => ReactElement;

function endpointNode(endpoint: ForceLink["source"]): ForceNode | null {
  return typeof endpoint === "object" && endpoint !== null ? endpoint : null;
}

function paintArrow(ctx: CanvasRenderingContext2D, x: number, y: number, angle: number, scale: number) {
  const length = 6 / scale;
  ctx.setLineDash([]);
  ctx.beginPath();
  for (const side of [-1, 1]) {
    ctx.moveTo(x, y);
    ctx.lineTo(x - length * Math.cos(angle + side * Math.PI / 6),
      y - length * Math.sin(angle + side * Math.PI / 6));
  }
  ctx.stroke();
}

export default function ForceGraph({
  data,
  width,
  height,
  onNodeClick,
  onNodeHover,
  selectedNodeId,
  focusNodeId,
}: ForceGraphProps) {
  const fgRef = useRef<ForceGraphHandle | null>(null);
  const [graphHandle, setGraphHandle] = useState<ForceGraphHandle | null>(null);
  const [zoomScale, setZoomScale] = useState(1);
  const viewAdjusted = useRef(false);
  const attachGraph = useCallback((graph: ForceGraphHandle | null) => {
    fgRef.current = graph;
    setGraphHandle(graph);
  }, []);
  const containerRef = useRef<HTMLDivElement>(null);
  const [dimensions, setDimensions] = useState<{
    width: number;
    height: number;
  } | null>(null);
  const [simulation, setSimulation] = useState(() => ({ source: data, graph: simulationGraph(data) }));
  if (simulation.source !== data) {
    setSimulation({ source: data, graph: simulationGraph(data, simulation.graph) });
  }
  const canvasData = simulation.graph;

  // Use ResizeObserver for reliable dimension tracking
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;

    function measure() {
      if (!el) return;
      const w = width ?? el.clientWidth;
      const h = height ?? el.clientHeight;
      if (w > 0 && h > 0) {
        setDimensions((prev) => {
          if (prev && prev.width === w && prev.height === h) return prev;
          return { width: w, height: h };
        });
      }
    }

    // Initial measure + fallback polling for client-side navigation
    measure();
    const fallback = setInterval(measure, 100);
    const timeout = setTimeout(() => clearInterval(fallback), 2000);

    const ro = new ResizeObserver(measure);
    ro.observe(el);

    return () => {
      ro.disconnect();
      clearInterval(fallback);
      clearTimeout(timeout);
    };
  }, [width, height]);

  // Configure forces
  useEffect(() => {
    const fg = graphHandle;
    if (!fg) return;

    const params = getForceParams(data.nodes.length);
    fg.d3Force("charge")?.strength?.(params.chargeStrength);
    fg.d3Force("link")?.distance?.(params.linkDistance);
    fg.d3Force("center")?.strength?.(0.05);
    // Disconnected components need a restoring force; center alone only moves
    // their centroid and cannot stop unbounded expansion after repeated filters.
    fg.d3Force("x", forceX<ForceNode>(0).strength(0.08));
    fg.d3Force("y", forceY<ForceNode>(0).strength(0.08));
    // Collision force: prevents node overlap, adds breathing room
    fg.d3Force(
      "collide",
      forceCollide<ForceNode>((n) => (n.radius ?? 5) + 6).strength(0.9)
    );
    fg.d3ReheatSimulation();
  }, [graphHandle, data.nodes.length]);

  // Focus on external selection (e.g. search result)
  useEffect(() => {
    if (!focusNodeId) return;
    const fg = fgRef.current;
    if (!fg) return;
    const node = canvasData.nodes.find((n) => n.id === focusNodeId);
    if (!node || node.x == null || node.y == null) return;
    fg.centerAt(node.x, node.y, 600);
    fg.zoom(2.8, 600);
    viewAdjusted.current = true;
  }, [focusNodeId, canvasData, graphHandle]);

  // Custom node rendering
  const paintNode = useCallback(
    (node: ForceNode, ctx: CanvasRenderingContext2D, globalScale: number) => {
      const gNode = node;
      const x = node.x ?? 0;
      const y = node.y ?? 0;
      const r = Math.max(gNode.radius, 2.5 / globalScale);
      const isSelected = gNode.id === selectedNodeId;
      const fontSize = Math.max(10 / globalScale, 2);
      const labelOffset = r + 2;

      ctx.globalAlpha = gNode.opacity;

      if (isSelected) {
        ctx.shadowColor = gNode.color;
        ctx.shadowBlur = 15;
      }

      ctx.beginPath();
      ctx.arc(x, y, r, 0, 2 * Math.PI);
      ctx.fillStyle = gNode.color;
      ctx.fill();

      if (gNode.isGhost) {
        ctx.strokeStyle = "rgba(255,255,255,0.3)";
        ctx.setLineDash([2, 2]);
        ctx.lineWidth = 1;
        ctx.stroke();
        ctx.setLineDash([]);
      }

      ctx.shadowColor = "transparent";
      ctx.shadowBlur = 0;

      if (isSelected || gNode.opacity >= 0.3) {
        ctx.font = `${isSelected ? "bold " : ""}${fontSize}px Inter, PingFang SC, sans-serif`;
        ctx.textAlign = "center";
        ctx.textBaseline = "top";
        ctx.fillStyle =
          gNode.opacity > 0.5 ? "#e8e8f0" : "rgba(232,232,240,0.3)";
        ctx.fillText(gNode.label, x, y + labelOffset);
      }

      ctx.globalAlpha = 1;
    },
    [selectedNodeId]
  );

  // Custom link rendering
  const paintLink = useCallback(
    (link: ForceLink, ctx: CanvasRenderingContext2D, globalScale: number) => {
      const gLink = link;
      const source = endpointNode(gLink.source);
      const target = endpointNode(gLink.target);
      const sx = source?.x ?? 0;
      const sy = source?.y ?? 0;
      const tx = target?.x ?? 0;
      const ty = target?.y ?? 0;

      if (gLink.opacity <= 0) return;

      // Weight-scaled line width (log scale so strong collabs stand out,
      // weak ones don't disappear). Coauthor weight counts shared recorded works.
      const w = Math.max(1, gLink.weight);
      const widthScaled =
        gLink.type === "coauthor"
          ? Math.max(0.3, Math.min(0.4 + Math.log2(w) * 0.8, 4))
          : gLink.type === "acknowledgement"
          ? Math.max(1, Math.min(w * 0.4, 3))
          : Math.max(0.5, Math.min(w * 0.3, 3));
      // Dim weak coauthor edges to reduce clutter; emphasize strong ones
      let alpha = gLink.opacity;
      if (gLink.type === "coauthor") {
        if (w >= 10) alpha = Math.min(1, alpha * 1.1);
        else if (w <= 2) alpha *= 0.45;
        else if (w <= 4) alpha *= 0.7;
      }
      ctx.globalAlpha = alpha;
      ctx.strokeStyle = gLink.color;
      ctx.lineWidth = widthScaled / globalScale;

      if (gLink.dash) {
        ctx.setLineDash(gLink.dash);
      } else {
        ctx.setLineDash([]);
      }

      ctx.beginPath();
      ctx.moveTo(sx, sy);
      const curve = gLink.curve ?? 0;
      const cx = (sx + tx) / 2 - (ty - sy) * curve;
      const cy = (sy + ty) / 2 + (tx - sx) * curve;
      if (curve) ctx.quadraticCurveTo(cx, cy, tx, ty);
      else ctx.lineTo(tx, ty);
      ctx.stroke();

      // A quadratic curve's midpoint tangent follows target minus source.
      if (["advisor-student", "prerequisite", "leads-to", "acknowledgement"].includes(gLink.type)) {
        paintArrow(ctx, (sx + 2 * cx + tx) / 4, (sy + 2 * cy + ty) / 4,
          Math.atan2(ty - sy, tx - sx), globalScale);
      }

      // Labels are recorded paper counts, including reviewed acknowledgements.
      if (gLink.label && ["coauthor", "acknowledgement"].includes(gLink.type) && globalScale > 1.2) {
        const mx = (sx + tx) / 2;
        const my = (sy + ty) / 2;
        const fontSize = Math.max(8 / globalScale, 2);
        ctx.font = `${fontSize}px Inter, sans-serif`;
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillStyle = "rgba(136,136,160,0.7)";
        ctx.setLineDash([]);
        ctx.fillText(gLink.label, mx, my - 3 / globalScale);
      }

      ctx.setLineDash([]);
      ctx.globalAlpha = 1;
    },
    []
  );

  const handleNodeClick = useCallback(
    (node: ForceNode) => {
      onNodeClick?.(node);
      viewAdjusted.current = true;
      fgRef.current?.centerAt(node.x, node.y, 500);
      fgRef.current?.zoom(2.5, 500);
    },
    [onNodeClick]
  );

  const ready = dimensions !== null;

  return (
    <div
      ref={containerRef}
      onPointerDownCapture={() => { viewAdjusted.current = true; }}
      onWheelCapture={() => { viewAdjusted.current = true; }}
      className="absolute inset-0"
      style={{ minHeight: 400 }}
    >
      {ready && (
        <ForceGraphCanvas
          ref={attachGraph}
          graphData={canvasData as unknown as ForceGraphCanvasData}
          width={dimensions.width}
          height={dimensions.height}
          backgroundColor="#0a0a0f"
          nodeCanvasObject={paintNode}
          nodePointerAreaPaint={(
            node: ForceNode,
            color: string,
            ctx: CanvasRenderingContext2D,
            globalScale: number
          ) => {
            const r = Math.max(node.radius + 2, 8 / globalScale);
            ctx.beginPath();
            ctx.arc(node.x ?? 0, node.y ?? 0, r, 0, 2 * Math.PI);
            ctx.fillStyle = color;
            ctx.fill();
          }}
          linkCanvasObject={paintLink}
          onNodeClick={handleNodeClick}
          onNodeHover={(node: ForceNode | null) => onNodeHover?.(node)}
          onZoom={({ k }) => setZoomScale(k)}
          onEngineStop={() => {
            if (!viewAdjusted.current && canvasData.nodes.length) {
              viewAdjusted.current = true;
              fgRef.current?.zoomToFit(400, 60);
            }
          }}
          enableNodeDrag={true}
          enableZoomInteraction={true}
          enablePanInteraction={true}
          cooldownTicks={100}
          minZoom={0.05}
          maxZoom={8}
        />
      )}
      <div className="absolute top-4 left-4 z-30 flex flex-col gap-1 bg-[#14141f]/95 rounded-lg border border-[#2a2a3a] p-1">
        <button
          aria-label="放大" title="放大" disabled={!graphHandle || zoomScale >= 8}
          onClick={() => { viewAdjusted.current = true; graphHandle?.zoom(Math.min(8, graphHandle.zoom() * 1.4), 250); }}
          className="w-8 h-8 rounded text-lg text-[#e8e8f0] hover:bg-[#2a2a3a] disabled:opacity-30"
        >+</button>
        <output aria-label="图谱缩放比例" className="text-[10px] text-center text-[#8888a0]">
          {Math.round(zoomScale * 100)}%
        </output>
        <button
          aria-label="缩小" title="缩小" disabled={!graphHandle || zoomScale <= 0.05}
          onClick={() => { viewAdjusted.current = true; graphHandle?.zoom(Math.max(0.05, graphHandle.zoom() / 1.4), 250); }}
          className="w-8 h-8 rounded text-lg text-[#e8e8f0] hover:bg-[#2a2a3a] disabled:opacity-30"
        >−</button>
        <button
          aria-label="重置视图" title="适应当前全图" disabled={!graphHandle || !canvasData.nodes.length}
          onClick={() => { viewAdjusted.current = false; graphHandle?.zoomToFit(400, 60); }}
          className="w-8 h-8 rounded text-[#e8e8f0] hover:bg-[#2a2a3a] disabled:opacity-30"
        >⟳</button>
      </div>
    </div>
  );
}
