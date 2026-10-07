"use client";

import { useMemo } from "react";
import { renderMathText } from "@/lib/math-text";

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
