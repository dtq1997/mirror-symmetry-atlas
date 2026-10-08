import type { Institution } from "./types";

/** Resolve only reviewed, explicit aliases. Keep every old URL addressable. */
export function institutionLookup(records: Institution[]): Map<string, Institution> {
  const raw = new Map(records.map((record) => [record.slug, record]));
  if (raw.size !== records.length) throw new Error("Duplicate institution slug");
  for (const record of records) {
    if (!("alias_of" in record)) continue;
    const target = raw.get(record.alias_of!);
    if (!target || target.slug === record.slug || "alias_of" in target) {
      throw new Error(`Invalid institution alias: ${record.slug}`);
    }
    if (record.research_groups?.length || record.appointment_checks?.length || record.events?.length || record.notes) {
      throw new Error(`Institution alias would hide content: ${record.slug}`);
    }
  }
  const map = new Map(records.filter((record) => !record.alias_of)
    .map((record) => [record.slug, structuredClone(record)]));
  for (const record of records) {
    if (record.alias_of) map.set(record.slug, map.get(record.alias_of)!);
  }
  return map;
}

export function canonicalInstitutions(records: Institution[]): Institution[] {
  return [...new Set(institutionLookup(records).values())];
}
