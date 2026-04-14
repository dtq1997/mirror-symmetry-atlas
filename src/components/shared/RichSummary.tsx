"use client";

import { useState, useRef, Fragment } from "react";
import Link from "next/link";
import katex from "katex";

interface EntityInfo {
  slug: string;
  type: "person" | "concept";
  displayName: string;
  hoverTitle?: string;
  hoverSubtitle?: string;
  hoverDetails?: string[];
}

interface RichSummaryProps {
  text: string;
  entities: EntityInfo[];
  className?: string;
}

/**
 * Renders text with:
 * - Entity names auto-linked (with hover cards)
 * - Inline LaTeX ($...$) rendered via KaTeX
 * - Markdown bold (**...**) rendered
 */
export default function RichSummary({
  text,
  entities,
  className,
}: RichSummaryProps) {
  // Build a regex that matches all entity display names, longest first
  const sorted = [...entities].sort(
    (a, b) => b.displayName.length - a.displayName.length
  );

  // Process: first handle LaTeX, then entity linking
  const parts = processText(text, sorted);

  return <div className={className}>{parts}</div>;
}

function processText(text: string, entities: EntityInfo[]): React.ReactNode[] {
  // Step 1: Split by LaTeX ($...$$ and $...$)
  const segments = splitByLatex(text);

  // Step 2: For each non-LaTeX segment, link entities
  const result: React.ReactNode[] = [];
  let key = 0;

  for (const seg of segments) {
    if (seg.type === "display-math") {
      try {
        const html = katex.renderToString(seg.content, {
          displayMode: true,
          throwOnError: false,
        });
        result.push(
          <span
            key={key++}
            dangerouslySetInnerHTML={{ __html: html }}
          />
        );
      } catch {
        result.push(<code key={key++}>{seg.content}</code>);
      }
    } else if (seg.type === "inline-math") {
      try {
        const html = katex.renderToString(seg.content, {
          displayMode: false,
          throwOnError: false,
        });
        result.push(
          <span
            key={key++}
            dangerouslySetInnerHTML={{ __html: html }}
          />
        );
      } catch {
        result.push(<code key={key++}>{seg.content}</code>);
      }
    } else {
      // Plain text: link entities + handle bold + newlines
      const linked = linkEntities(seg.content, entities, key);
      key += linked.length + 1;
      result.push(...linked);
    }
  }

  return result;
}

function splitByLatex(
  text: string
): { type: "text" | "inline-math" | "display-math"; content: string }[] {
  const result: {
    type: "text" | "inline-math" | "display-math";
    content: string;
  }[] = [];
  let remaining = text;

  while (remaining.length > 0) {
    // Display math $$...$$
    const dd = remaining.indexOf("$$");
    const sd = remaining.indexOf("$");

    if (dd !== -1 && (dd <= sd || sd === -1)) {
      if (dd > 0) result.push({ type: "text", content: remaining.slice(0, dd) });
      const end = remaining.indexOf("$$", dd + 2);
      if (end !== -1) {
        result.push({
          type: "display-math",
          content: remaining.slice(dd + 2, end),
        });
        remaining = remaining.slice(end + 2);
      } else {
        result.push({ type: "text", content: remaining.slice(dd) });
        remaining = "";
      }
    } else if (sd !== -1) {
      if (sd > 0) result.push({ type: "text", content: remaining.slice(0, sd) });
      const end = remaining.indexOf("$", sd + 1);
      if (end !== -1) {
        result.push({
          type: "inline-math",
          content: remaining.slice(sd + 1, end),
        });
        remaining = remaining.slice(end + 1);
      } else {
        result.push({ type: "text", content: remaining.slice(sd) });
        remaining = "";
      }
    } else {
      result.push({ type: "text", content: remaining });
      remaining = "";
    }
  }

  return result;
}

function linkEntities(
  text: string,
  entities: EntityInfo[],
  startKey: number
): React.ReactNode[] {
  if (entities.length === 0) {
    return renderPlainText(text, startKey);
  }

  // Build pattern matching all entity names
  const escapedNames = entities.map((e) =>
    e.displayName.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")
  );
  const pattern = new RegExp(`(${escapedNames.join("|")})`, "g");

  const parts = text.split(pattern);
  const result: React.ReactNode[] = [];
  let key = startKey;

  for (const part of parts) {
    const entity = entities.find((e) => e.displayName === part);
    if (entity) {
      result.push(
        <EntitySpan key={key++} entity={entity} />
      );
    } else {
      result.push(...renderPlainText(part, key));
      key += 2;
    }
  }

  return result;
}

function renderPlainText(text: string, startKey: number): React.ReactNode[] {
  // Handle **bold** and newlines
  const result: React.ReactNode[] = [];
  let key = startKey;

  const boldParts = text.split(/\*\*(.*?)\*\*/g);
  for (let i = 0; i < boldParts.length; i++) {
    if (i % 2 === 1) {
      result.push(<strong key={key++}>{boldParts[i]}</strong>);
    } else {
      // Handle newlines
      const lines = boldParts[i].split("\n");
      for (let j = 0; j < lines.length; j++) {
        if (j > 0) result.push(<br key={key++} />);
        if (lines[j]) result.push(<Fragment key={key++}>{lines[j]}</Fragment>);
      }
    }
  }
  return result;
}

function EntitySpan({ entity }: { entity: EntityInfo }) {
  const [show, setShow] = useState(false);
  const timeoutRef = useRef<ReturnType<typeof setTimeout>>(undefined);

  const href =
    entity.type === "person"
      ? `/people/${entity.slug}`
      : `/concepts/${entity.slug}`;

  const color =
    entity.type === "person"
      ? "text-[#fbbf24] hover:text-[#fde68a]"
      : "text-[#818cf8] hover:text-[#a5b4fc]";

  return (
    <span
      className="relative inline"
      onMouseEnter={() => {
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
        className={`${color} underline decoration-dotted underline-offset-2 transition-colors`}
      >
        {entity.displayName}
      </Link>

      {show && entity.hoverTitle && (
        <span
          className="absolute z-50 bottom-full left-1/2 -translate-x-1/2 mb-2 w-56 bg-[#14141f] border border-[#2a2a3a] rounded-lg shadow-xl p-3 text-left"
          style={{ animation: "fadeIn 0.12s ease-out" }}
        >
          <span className="block text-xs font-medium text-[#e8e8f0]">
            {entity.hoverTitle}
          </span>
          {entity.hoverSubtitle && (
            <span className="block text-[10px] text-[#8888a0] mt-0.5">
              {entity.hoverSubtitle}
            </span>
          )}
          {entity.hoverDetails && entity.hoverDetails.length > 0 && (
            <span className="block mt-1.5 pt-1.5 border-t border-[#2a2a3a]">
              {entity.hoverDetails.map((d, i) => (
                <span key={i} className="block text-[10px] text-[#8888a0]">
                  {d}
                </span>
              ))}
            </span>
          )}
        </span>
      )}
    </span>
  );
}
