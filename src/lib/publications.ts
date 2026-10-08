import type { Connection, Person, Publication } from "./types";
import { canonicalPaperId, groupPaperRecords } from "./paper-identity";
import { publicationMetadata } from "./publication-metadata";

export interface CatalogPublication extends Publication {
  catalogKey: string;
  ownerSlugs: string[];
}

/** Catalog counts refer to recorded works, not a person's complete output. */
export function collectPublications(people: Person[], options: { matchTitles?: boolean } = {}): CatalogPublication[] {
  const records = people.flatMap((person) => (person.publications ?? []).map((pub) => ({
    ...pub, ownerSlug: person.slug,
  })));
  return groupPaperRecords(records, options).map((group, index) => {
    const richest = [...group].sort((a, b) => publicationMetadata(b).score - publicationMetadata(a).score)[0];
    return {
      ...richest,
      catalogKey: `${canonicalPaperId(richest) ?? "unknown"}:${index}`,
      ownerSlugs: [...new Set(group.map((pub) => pub.ownerSlug))],
      // Other records can contain ambiguous name bindings; preserve the chosen record.
      coauthors: richest.coauthors ?? [],
    };
  }).sort((a, b) => b.year - a.year || a.title.localeCompare(b.title));
}

/** Only shared complete identifiers support a recorded coauthor link. Title
 * equality or a matching raw author name cannot establish personal identity. */
export function collectCoauthorship(people: Person[]): Connection[] {
  const pairs = new Map<string, Connection>();
  for (const paper of collectPublications(people, { matchTitles: false })) {
    const slugs = [...paper.ownerSlugs].sort();
    for (let i = 0; i < slugs.length; i++) {
      for (let j = i + 1; j < slugs.length; j++) {
        const key = `${slugs[i]}|${slugs[j]}`;
        const edge = pairs.get(key) ?? {
          source: slugs[i], target: slugs[j], type: "coauthor", derived: true,
          coauthored_papers: { published: [], preprint: [] },
        };
        const bucket = publicationMetadata(paper).hasPublicationClue ? "published" : "preprint";
        edge.coauthored_papers![bucket].push(paper);
        pairs.set(key, edge);
      }
    }
  }
  return [...pairs.values()].map((edge) => {
    const papers = [...edge.coauthored_papers!.published, ...edge.coauthored_papers!.preprint];
    const years = papers.map((p) => p.year).filter(Number.isFinite).sort((a, b) => a - b);
    return { ...edge, weight: papers.length,
      period: years.length ? `${years[0]}-${years[years.length - 1]}` : undefined };
  });
}

export function recordedPublicationStats(person: Person) {
  const papers = collectPublications([person]);
  const published = papers.filter((p) => publicationMetadata(p).hasPublicationClue).length;
  return { total_papers: papers.length, published_count: published,
    preprint_only_count: papers.length - published };
}
