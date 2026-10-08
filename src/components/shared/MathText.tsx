"use client";

import { useMemo } from "react";
import { renderMathText } from "@/lib/math-text";

interface MathTextProps {
  children: string;
  className?: string;
  inline?: boolean;
}

/**
 * Renders text with inline ($...$) and display ($$...$$) LaTeX math via KaTeX.
 * Markdown bold (**...**) is also handled.
 */
export default function MathText({ children, className, inline = false }: MathTextProps) {
  const html = useMemo(() => renderMathText(children, { inline }), [children, inline]);
  const Tag = inline ? "span" : "div";
  return (
    <Tag
      className={className}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}
