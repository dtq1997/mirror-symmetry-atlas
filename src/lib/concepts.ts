import type { Concept } from "./types";

export const CONCEPT_ROLE_LABELS: Record<string, string> = {
  founder: "创立", major: "主要贡献", promoter: "推广", applier: "应用",
};

/** [Codex] Resolve only declared, one-hop aliases; keep the input records intact. */
export function canonicalConcepts(records: Concept[]): Concept[] {
  const bySlug = new Map(records.map((c) => [c.slug, c]));
  if (bySlug.size !== records.length) throw new Error("Duplicate concept slug");
  const aliases = new Map<string, string>();
  for (const record of records) {
    if (!record.alias_of) continue;
    const target = bySlug.get(record.alias_of);
    if (!target || target.alias_of || target.slug === record.slug) {
      throw new Error(`Invalid concept alias: ${record.slug} -> ${record.alias_of}`);
    }
    aliases.set(record.slug, target.slug);
  }
  const resolve = (slug: string) => aliases.get(slug) ?? slug;
  return records.filter((c) => !c.alias_of).map((record) => {
    const concept = structuredClone(record);
    const aliasNames = records.filter((c) => c.alias_of === concept.slug)
      .flatMap((c) => [c.name.en, ...(c.aliases ?? [])]);
    concept.aliases = [...new Set([...(concept.aliases ?? []), ...aliasNames])];
    for (const field of ["prerequisites", "leads_to", "related"] as const) {
      concept[field] = [...new Set((concept[field] ?? []).map(resolve))]
        .filter((slug) => slug !== concept.slug);
    }
    if (concept.dual_to) concept.dual_to = resolve(concept.dual_to);
    return concept;
  });
}

/** Legacy URLs and references resolve to the same canonical content. */
export function conceptLookup(records: Concept[]): Map<string, Concept> {
  const canonical = canonicalConcepts(records);
  const map = new Map(canonical.map((c) => [c.slug, c]));
  for (const record of records) {
    if (record.alias_of) map.set(record.slug, map.get(record.alias_of)!);
  }
  return map;
}
