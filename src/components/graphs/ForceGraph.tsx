"use client";

import { useRef, useCallback, useEffect, useState } from "react";
import dynamic from "next/dynamic";
import type { GraphData, GraphNode, GraphLink } from "@/lib/types";
import { getForceParams } from "@/lib/graph";

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

export default function ForceGraph({
  data,
  width,
  height,
  onNodeClick,
  onNodeHover,
  selectedNodeId,
  focusNodeId,
}: ForceGraphProps) {
  const fgRef = useRef<any>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [dimensions, setDimensions] = useState<{
    width: number;
    height: number;
  } | null>(null);
  const [mounted, setMounted] = useState(false);

  // Track mount for SSR safety
  useEffect(() => {
    setMounted(true);
  }, []);

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
    const fg = fgRef.current;
    if (!fg) return;

    const params = getForceParams(data.nodes.length);
    fg.d3Force("charge")?.strength(params.chargeStrength);
    fg.d3Force("link")?.distance(params.linkDistance);
    fg.d3Force("center")?.strength(0.05);
    // Collision force: prevents node overlap, adds breathing room
    import("d3-force").then(({ forceCollide }) => {
      fg.d3Force(
        "collide",
        forceCollide((n: any) => (n.radius ?? 5) + 6).strength(0.9)
      );
      fg.d3ReheatSimulation();
    });
  }, [data.nodes.length]);

  // Focus on external selection (e.g. search result)
  useEffect(() => {
    if (!focusNodeId) return;
    const fg = fgRef.current;
    if (!fg) return;
    const node = data.nodes.find((n) => n.id === focusNodeId) as any;
    if (!node || node.x == null || node.y == null) return;
    fg.centerAt(node.x, node.y, 600);
    fg.zoom(2.8, 600);
  }, [focusNodeId, data.nodes]);

  // Custom node rendering
  const paintNode = useCallback(
    (node: any, ctx: CanvasRenderingContext2D, globalScale: number) => {
      const gNode = node as GraphNode;
      const x = node.x ?? 0;
      const y = node.y ?? 0;
      const r = gNode.radius;
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

      if (globalScale > 0.4) {
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
    (link: any, ctx: CanvasRenderingContext2D, globalScale: number) => {
      const gLink = link as GraphLink & { source: any; target: any };
      const sx = gLink.source.x ?? 0;
      const sy = gLink.source.y ?? 0;
      const tx = gLink.target.x ?? 0;
      const ty = gLink.target.y ?? 0;

      if (gLink.opacity <= 0) return;

      // Weight-scaled line width (log scale so strong collabs stand out,
      // weak ones don't disappear). Coauthor weight=papers_count.
      const w = Math.max(1, gLink.weight);
      const widthScaled =
        gLink.type === "coauthor"
          ? Math.max(0.3, Math.min(0.4 + Math.log2(w) * 0.8, 4))
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
      ctx.lineTo(tx, ty);
      ctx.stroke();

      // Arrow for advisor-student
      if (gLink.type === "advisor-student") {
        const angle = Math.atan2(ty - sy, tx - sx);
        const arrowLen = 6 / globalScale;
        const mx = (sx + tx) / 2;
        const my = (sy + ty) / 2;

        ctx.setLineDash([]);
        ctx.beginPath();
        ctx.moveTo(mx, my);
        ctx.lineTo(
          mx - arrowLen * Math.cos(angle - Math.PI / 6),
          my - arrowLen * Math.sin(angle - Math.PI / 6)
        );
        ctx.moveTo(mx, my);
        ctx.lineTo(
          mx - arrowLen * Math.cos(angle + Math.PI / 6),
          my - arrowLen * Math.sin(angle + Math.PI / 6)
        );
        ctx.stroke();
      }

      // Weight label for coauthor
      if (gLink.label && gLink.type === "coauthor" && globalScale > 1.2) {
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
    (node: any) => {
      onNodeClick?.(node as GraphNode);
      fgRef.current?.centerAt(node.x, node.y, 500);
      fgRef.current?.zoom(2.5, 500);
    },
    [onNodeClick]
  );

  const ready = mounted && dimensions !== null;

  return (
    <div
      ref={containerRef}
      className="absolute inset-0"
      style={{ minHeight: 400 }}
    >
      {ready && (
        <ForceGraph2D
          ref={fgRef}
          graphData={data as any}
          width={dimensions.width}
          height={dimensions.height}
          backgroundColor="#0a0a0f"
          nodeCanvasObject={paintNode}
          nodePointerAreaPaint={(
            node: any,
            color: string,
            ctx: CanvasRenderingContext2D
          ) => {
            const r = (node as GraphNode).radius + 2;
            ctx.beginPath();
            ctx.arc(node.x ?? 0, node.y ?? 0, r, 0, 2 * Math.PI);
            ctx.fillStyle = color;
            ctx.fill();
          }}
          linkCanvasObject={paintLink}
          onNodeClick={handleNodeClick}
          onNodeHover={(node: any) =>
            onNodeHover?.(node as GraphNode | null)
          }
          enableNodeDrag={true}
          enableZoomInteraction={true}
          enablePanInteraction={true}
          cooldownTicks={100}
          minZoom={0.3}
          maxZoom={8}
        />
      )}
    </div>
  );
}
