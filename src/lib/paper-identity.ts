// TS mirror of scripts/paper_identity.py — canonical paper identity.
// SSOT: every cross-yaml comparison MUST go through canonicalPaperId().
// The Python module is the original; this file must stay in sync.

function foldAccents(s: string): string {
  return s.normalize("NFKD").replace(/\p{M}/gu, "");
}

export function canonicalTitle(t: string | undefined | null): string {
  if (!t) return "";
  let s = foldAccents(t).toLowerCase();
  s = s.replace(/\\[a-z]+\{([^}]*)\}/g, "$1"); // \mathbb{P} → P
  s = s.replace(/\\[a-z]+/g, " "); // strip remaining commands
  s = s.replace(/\$([^$]*)\$/g, "$1"); // strip math delimiters
  s = s.replace(/<[^>]+>/g, " "); // drop xml/html
  s = s.replace(/[^a-z0-9 ]/g, " ");
  s = s.replace(/\s+/g, " ").trim();
  return s;
}

export function canonicalDoi(d: string | undefined | null): string | null {
  if (!d) return null;
  let s = String(d).toLowerCase().trim();
  s = s.replace(/^https?:\/\/(dx\.)?doi\.org\//, "");
  if (!s || s.startsWith("10.48550/arxiv.")) return null;
  return s;
}

export function canonicalArxivId(pid: string | undefined | null): string | null {
  if (!pid) return null;
  const s = String(pid).trim().split("v")[0];
  if (s.startsWith("doi:") || s.startsWith("openalex:") || s.startsWith("cr:")) return null;
  if (/^\d{4}\.\d{4,5}$|^\d{7}$|^[a-z-]+\/\d{7}$/.test(s)) return s;
  return null;
}

export interface PaperIdentityKeys {
  doi: string | null;
  arxiv: string | null;
  title: string;
}

export function paperIdentityKeys(pub: {
  id?: string;
  doi?: string;
  title?: string;
}): PaperIdentityKeys {
  return {
    doi: canonicalDoi(pub.doi),
    arxiv: canonicalArxivId(pub.id),
    title: canonicalTitle(pub.title),
  };
}

/** A single string key suitable for Map lookup. Same paper → same key.
 * Falls back from doi → arxiv → title so the strongest signal wins. */
export function canonicalPaperId(pub: {
  id?: string;
  doi?: string;
  title?: string;
}): string | null {
  const k = paperIdentityKeys(pub);
  if (k.doi) return `doi:${k.doi}`;
  if (k.arxiv) return `arxiv:${k.arxiv}`;
  if (k.title) return `title:${k.title}`;
  return null;
}
