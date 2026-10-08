import type { CatalogPublication } from "./publications";
import { canonicalArxivId, canonicalTitle } from "./paper-identity";
import { publicationMetadata } from "./publication-metadata";
import { fullName } from "./name";

export interface CatalogFilters {
  query: string;
  owner: string;
  year: string;
  publication: "all" | "with-clues" | "needs-clues";
}

export const emptyCatalogFilters: CatalogFilters = { query: "", owner: "", year: "", publication: "all" };
export const catalogPageSize = 50;

/** Search text only: never used to bind people or merge paper identities. */
function searchText(value: string): string {
  return value.normalize("NFKD").replace(/\p{M}/gu, "").toLowerCase()
    .replace(/[^\p{L}\p{N}]+/gu, " ").trim();
}

function identifierKey(value: string): string | undefined {
  const arxiv = canonicalArxivId(value);
  if (arxiv) return `arxiv:${arxiv.toLowerCase()}`;
  const doi = publicationMetadata({ doi: value }).doi;
  return doi ? `doi:${doi}` : undefined;
}

export function indexCatalog(papers: CatalogPublication[]) {
  return papers.map((paper) => {
    const names = searchText([...paper.ownerSlugs.map(fullName), ...paper.coauthors.map(fullName)].join(" "));
    return {
      paper, names, nameWords: new Set(names.split(" ")),
      text: searchText([paper.title, canonicalTitle(paper.title), paper.journal ?? "", ...paper.identifiers].join(" ")),
      identifiers: new Set(paper.identifiers.map(identifierKey).filter(Boolean)),
      hasPublicationClue: publicationMetadata(paper).hasPublicationClue,
    };
  });
}

export function filterCatalog(index: ReturnType<typeof indexCatalog>, filters: CatalogFilters) {
  const query = filters.query.trim();
  const identifier = identifierKey(query);
  const tokens = searchText(query).split(" ").filter(Boolean);
  return index.filter(({ paper, text, names, nameWords, identifiers, hasPublicationClue }) => {
    if (filters.owner && !paper.ownerSlugs.includes(filters.owner)) return false;
    if (filters.year && String(paper.year) !== filters.year) return false;
    if (filters.publication === "with-clues" && !hasPublicationClue) return false;
    if (filters.publication === "needs-clues" && hasPublicationClue) return false;
    if (!query) return true;
    // Complete identifiers are exact matches; a DOI's components cannot match unrelated text.
    // Qian must not match Weiqiang in a name. Chinese names may be searched by part.
    return identifier ? identifiers.has(identifier) : tokens.length > 0 && tokens.every((token) =>
      text.includes(token) || nameWords.has(token) || /\p{Script=Han}/u.test(token) && names.includes(token));
  }).map(({ paper }) => paper);
}

export function catalogWindow(papers: CatalogPublication[], limit: number) {
  const visible = papers.slice(0, limit);
  return { visible, total: papers.length, nextCount: Math.min(catalogPageSize, papers.length - visible.length) };
}
