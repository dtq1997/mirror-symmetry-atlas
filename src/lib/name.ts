import { getAllPeople } from "./data";

let _index: Map<string, { displayName: string; en: string; zh?: string }> | null = null;

function buildIndex() {
  const idx = new Map<string, { displayName: string; en: string; zh?: string }>();
  for (const p of getAllPeople()) {
    const zh = p.name?.zh;
    const en = p.name?.en || p.slug;
    // Use Chinese name when present and not a [待验证]-style placeholder
    const useZh = !!zh && !zh.startsWith("[") && !zh.startsWith("待");
    idx.set(p.slug, {
      displayName: useZh ? (zh as string) : en,
      en,
      zh: useZh ? (zh as string) : undefined,
    });
  }
  return idx;
}

/** Return the preferred display name for a person slug.
 *  Chinese name (when available and not a placeholder) is used; else English. */
export function displayName(slug: string): string {
  if (!_index) _index = buildIndex();
  return _index.get(slug)?.displayName ?? slug;
}

/** Return both forms when available, e.g. "刘小博 / Xiaobo Liu". */
export function fullName(slug: string): string {
  if (!_index) _index = buildIndex();
  const entry = _index.get(slug);
  if (!entry) return slug;
  if (entry.zh && entry.en && entry.zh !== entry.en) {
    return `${entry.zh} / ${entry.en}`;
  }
  return entry.displayName;
}

export function nameInfo(slug: string) {
  if (!_index) _index = buildIndex();
  return _index.get(slug);
}
