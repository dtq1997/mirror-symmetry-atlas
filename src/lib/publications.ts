import type { Person, Publication } from "./types";
import { canonicalPaperId, groupPaperRecords } from "./paper-identity";

export interface CatalogPublication extends Publication {
  catalogKey: string;
  ownerSlugs: string[];
}

/** Catalog counts refer to recorded works, not a person's complete output. */
export function collectPublications(people: Person[]): CatalogPublication[] {
  const records = people.flatMap((person) => (person.publications ?? []).map((pub) => ({
    ...pub, ownerSlug: person.slug,
  })));
  return groupPaperRecords(records).map((group, index) => {
    const richest = [...group].sort((a, b) => Number(!!b.doi) - Number(!!a.doi) || Number(!!b.journal) - Number(!!a.journal))[0];
    return {
      ...richest,
      catalogKey: `${canonicalPaperId(richest) ?? "unknown"}:${index}`,
      ownerSlugs: [...new Set(group.map((pub) => pub.ownerSlug))],
      // Other records can contain ambiguous name bindings; preserve the chosen record.
      coauthors: richest.coauthors ?? [],
    };
  }).sort((a, b) => b.year - a.year || a.title.localeCompare(b.title));
}
