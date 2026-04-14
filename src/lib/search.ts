import Fuse from "fuse.js";
import type { Person, Concept, Institution } from "./types";

export interface SearchResult {
  type: "person" | "concept" | "institution";
  slug: string;
  label: string;
  sublabel?: string;
}

export function buildSearchIndex(
  people: Person[],
  concepts: Concept[],
  institutions: Institution[]
): Fuse<SearchResult> {
  const items: SearchResult[] = [];

  for (const p of people) {
    items.push({
      type: "person",
      slug: p.slug,
      label: p.name.en,
      sublabel: p.name.zh || undefined,
    });
    if (p.name.zh) {
      items.push({
        type: "person",
        slug: p.slug,
        label: p.name.zh,
        sublabel: p.name.en,
      });
    }
  }

  for (const c of concepts) {
    items.push({
      type: "concept",
      slug: c.slug,
      label: c.name.en,
      sublabel: c.name.zh || undefined,
    });
  }

  for (const i of institutions) {
    items.push({
      type: "institution",
      slug: i.slug,
      label: i.name.en,
      sublabel: i.name.zh || undefined,
    });
  }

  return new Fuse(items, {
    keys: ["label", "sublabel", "slug"],
    threshold: 0.3,
    includeScore: true,
  });
}
