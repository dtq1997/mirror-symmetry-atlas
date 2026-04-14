"use client";

import { useMemo } from "react";
import katex from "katex";

interface MathTextProps {
  children: string;
  className?: string;
}

/**
 * Renders text with inline ($...$) and display ($$...$$) LaTeX math via KaTeX.
 * Markdown bold (**...**) is also handled.
 */
export default function MathText({ children, className }: MathTextProps) {
  const html = useMemo(() => renderMathText(children), [children]);
  return (
    <div
      className={className}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}

function renderMathText(text: string): string {
  // Split by display math first ($$...$$), then inline ($...$)
  let result = text;

  // Display math: $$...$$
  result = result.replace(/\$\$([\s\S]*?)\$\$/g, (_, tex) => {
    try {
      return katex.renderToString(tex.trim(), {
        displayMode: true,
        throwOnError: false,
        trust: true,
      });
    } catch {
      return `<code>${tex}</code>`;
    }
  });

  // Inline math: $...$  (but not $$)
  result = result.replace(/(?<!\$)\$(?!\$)(.*?)\$(?!\$)/g, (_, tex) => {
    try {
      return katex.renderToString(tex.trim(), {
        displayMode: false,
        throwOnError: false,
        trust: true,
      });
    } catch {
      return `<code>${tex}</code>`;
    }
  });

  // Markdown bold **...**
  result = result.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

  // Line breaks
  result = result.replace(/\n/g, "<br/>");

  return result;
}
