import katex from "katex";

function escapeHtml(text: string): string {
  return text.replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  })[char]!);
}

function renderProse(text: string): string {
  return escapeHtml(text.replace(/\\\$/g, "$"))
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\n/g, "<br/>");
}

/** Parse source once: prose formatting must never rewrite KaTeX's HTML/MathML. */
export function renderMathText(text: string): string {
  const math = /(?<!\\)(\$\$|\$)(?!\$)([\s\S]*?)(?<!\\)\1(?!\$)/g;
  let output = "";
  let cursor = 0;
  for (const match of text.matchAll(math)) {
    output += renderProse(text.slice(cursor, match.index));
    const displayMode = match[1] === "$$";
    const tag = displayMode ? "div" : "span";
    const tex = match[2].trim();
    try {
      output += `<${tag} class="math-expression${displayMode ? " math-display" : ""}">${katex.renderToString(tex, {
        displayMode, throwOnError: false, trust: false,
      })}</${tag}>`;
    } catch {
      output += `<code>${escapeHtml(tex)}</code>`;
    }
    cursor = match.index! + match[0].length;
  }
  return output + renderProse(text.slice(cursor));
}
