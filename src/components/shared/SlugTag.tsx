"use client";

import { useState, useRef } from "react";
import Link from "next/link";

interface SlugTagProps {
  slug: string;
  type: "person" | "concept";
  // Inline hover data (passed from server component)
  hoverTitle?: string;
  hoverSubtitle?: string;
  hoverDetails?: string[];
}

export default function SlugTag({
  slug,
  type,
  hoverTitle,
  hoverSubtitle,
  hoverDetails,
}: SlugTagProps) {
  const [show, setShow] = useState(false);
  const timeoutRef = useRef<ReturnType<typeof setTimeout>>(undefined);

  const href = type === "person" ? `/people/${slug}` : `/concepts/${slug}`;
  const color =
    type === "person"
      ? "bg-[#f59e0b]/15 text-[#fbbf24] hover:bg-[#f59e0b]/25"
      : "bg-[#6366f1]/15 text-[#818cf8] hover:bg-[#6366f1]/25";

  const hasHover = hoverTitle != null;

  return (
    <span
      className="relative inline-block"
      onMouseEnter={() => {
        if (!hasHover) return;
        clearTimeout(timeoutRef.current);
        timeoutRef.current = setTimeout(() => setShow(true), 250);
      }}
      onMouseLeave={() => {
        clearTimeout(timeoutRef.current);
        setShow(false);
      }}
    >
      <Link
        href={href}
        className={`text-[10px] px-1.5 py-0.5 rounded ${color} transition-colors`}
      >
        {slug}
      </Link>

      {show && hasHover && (
        <div
          className="absolute z-50 bottom-full left-1/2 -translate-x-1/2 mb-2 w-56 bg-[#14141f] border border-[#2a2a3a] rounded-lg shadow-xl p-3"
          style={{ animation: "fadeIn 0.12s ease-out" }}
        >
          <style jsx>{`
            @keyframes fadeIn {
              from { opacity: 0; transform: translateY(4px); }
              to { opacity: 1; transform: translateY(0); }
            }
          `}</style>
          <div className="text-xs font-medium text-[#e8e8f0]">
            {hoverTitle}
          </div>
          {hoverSubtitle && (
            <div className="text-[10px] text-[#8888a0] mt-0.5">
              {hoverSubtitle}
            </div>
          )}
          {hoverDetails && hoverDetails.length > 0 && (
            <div className="mt-1.5 pt-1.5 border-t border-[#2a2a3a] space-y-0.5">
              {hoverDetails.map((d, i) => (
                <div key={i} className="text-[10px] text-[#8888a0]">{d}</div>
              ))}
            </div>
          )}
          <div className="absolute top-full left-1/2 -translate-x-1/2 -mt-[1px]">
            <div className="w-2 h-2 bg-[#14141f] border-r border-b border-[#2a2a3a] rotate-45" />
          </div>
        </div>
      )}
    </span>
  );
}
