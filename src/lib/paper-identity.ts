// TS mirror of scripts/paper_identity.py — canonical paper identity.
// SSOT: cross-record comparisons use paperIdentityKeys/groupPaperRecords.
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
  s = s.replace(/^https?:\/\/(dx\.)?doi\.org\//, "").replace(/^doi:\s*/, "");
  if (!s || s.startsWith("10.48550/arxiv.")) return null;
  return s;
}

export function canonicalArxivId(pid: string | undefined | null): string | null {
  if (!pid) return null;
  const s = String(pid).trim().replace(/^https?:\/\/(?:export\.)?arxiv\.org\/abs\//i, "")
    .replace(/^arxiv:\s*/i, "").replace(/v\d+$/, "");
  if (s.startsWith("doi:") || s.startsWith("openalex:") || s.startsWith("cr:")) return null;
  if (/^\d{4}\.\d{4,5}$|^\d{7}$|^[a-z][a-z.-]*\/\d{7}$/i.test(s)) return s;
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
    doi: canonicalDoi(pub.doi || (pub.id?.startsWith("doi:") ? pub.id.slice(4) : undefined)),
    arxiv: canonicalArxivId(pub.id),
    title: canonicalTitle(pub.title),
  };
}

/** Display key only. Different records of one paper can have different keys;
 * use groupPaperRecords for deduplication across records. */
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

type IdentityRecord = { id?: string; doi?: string; title?: string };

/** Join shared identifiers transitively. Title-only joins cannot override
 * conflicting DOI/arXiv identifiers. Grouping does not verify authorship. */
export function groupPaperRecords<T extends IdentityRecord>(records: T[], options: { matchTitles?: boolean } = {}): T[][] {
  const parent = records.map((_, i) => i);
  const keys = records.map((record) => {
    const keys = paperIdentityKeys(record);
    // Archive-less legacy numbers can name different papers in different archives.
    return { ...keys, arxiv: keys.arxiv && !/^\d{7}$/.test(keys.arxiv) ? keys.arxiv : null };
  });
  const ids = keys.map((k) => ({ doi: new Set(k.doi ? [k.doi] : []), arxiv: new Set(k.arxiv ? [k.arxiv] : []) }));
  const root = (i: number): number => {
    while (parent[i] !== i) { parent[i] = parent[parent[i]]; i = parent[i]; }
    return i;
  };
  const join = (a: number, b: number) => {
    a = root(a); b = root(b);
    if (a === b) return;
    for (const kind of ["doi", "arxiv"] as const) {
      if (new Set([...ids[a][kind], ...ids[b][kind]]).size > 1) return;
    }
    parent[b] = a;
    for (const kind of ["doi", "arxiv"] as const) {
      for (const id of ids[b][kind]) ids[a][kind].add(id);
    }
  };
  const kinds: Array<keyof PaperIdentityKeys> = options.matchTitles === false ? ["doi", "arxiv"] : ["doi", "arxiv", "title"];
  for (const kind of kinds) {
    const seen = new Map<string, number[]>();
    keys.forEach((k, i) => {
      const key = k[kind];
      if (!key) return;
      for (const prior of seen.get(key) ?? []) join(prior, i);
      seen.set(key, [...(seen.get(key) ?? []), i]);
    });
  }
  const groups = new Map<number, T[]>();
  records.forEach((record, i) => {
    const r = root(i);
    groups.set(r, [...(groups.get(r) ?? []), record]);
  });
  return [...groups.values()];
}

/** Unknown and archive-less legacy IDs must not become fabricated arXiv URLs. */
export function publicationUrl(pub: IdentityRecord): string | undefined {
  const keys = paperIdentityKeys(pub);
  if (keys.doi && /^10\.\d{4,9}\/\S+$/i.test(keys.doi)) return `https://doi.org/${keys.doi}`;
  if (keys.arxiv && !/^\d{7}$/.test(keys.arxiv)) return `https://arxiv.org/abs/${keys.arxiv}`;
  if (/^openalex:W\d+$/i.test(pub.id ?? "")) return `https://openalex.org/${pub.id!.slice(9)}`;
  return undefined;
}
