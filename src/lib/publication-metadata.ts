// [Codex] Metadata clues are not verified publication or peer-review status.
// Repository names/DOIs identify deposited objects, which may be papers, data or video.
const repositoryVenues = new Set([
  "arxiv", "arxiv.org", "arxiv (cornell university)",
  "ssrn", "ssrn electronic journal",
  "institutional repositories database (irdb)",
  "circle (university of british columbia)",
  "repository for publications and research data (eth zurich)",
  "kyoto university research information repository (kyoto university)",
]);

export const publicationMetadataNote = "出版线索来自现有期刊、书籍记录或 DOI，已识别的资料库名称及其 DOI 不单独计入。线索尚未逐项核准，不代表已确认发表或经过同行评审；缺少线索也不代表未发表。";

type MetadataInput = { id?: string; doi?: string; journal?: string };

function meaningfulText(value: unknown): string | undefined {
  if (typeof value !== "string") return undefined;
  const text = value.trim();
  return !text || /^(?:none|null|nan|n\/a|unknown|[-—?]|\[.*\])$/i.test(text)
    ? undefined : text;
}

/** Keep arXiv-assigned DOIs for display; paper-identity intentionally excludes
 * them from publisher-DOI identity, so do not change that separate contract. */
function displayDoi(value: unknown): string | undefined {
  const doi = meaningfulText(value)?.replace(/^https?:\/\/(?:dx\.)?doi\.org\//i, "")
    .replace(/^doi:\s*/i, "").toLowerCase();
  return doi && /^10\.\d{4,9}\/[^\s<>"\u0000-\u001f]+$/.test(doi) ? doi : undefined;
}

export function publicationMetadata(paper: MetadataInput) {
  const venue = meaningfulText(paper.journal);
  // Exact labels only: a real journal citation can mention an arXiv version.
  const repositoryVenue = !!venue && repositoryVenues.has(venue.toLowerCase().replace(/\s+/g, " "));
  const doi = displayDoi(paper.doi) ?? displayDoi(paper.id?.startsWith("doi:") ? paper.id.slice(4) : undefined);
  const repositoryDoi = !!doi && /^(?:10\.48550\/arxiv\.|10\.2139\/ssrn\.|10\.14288\/|10\.24546\/|10\.3929\/)/.test(doi);
  const hasVenueClue = !!venue && !repositoryVenue;
  const hasDoiClue = !!doi && !repositoryDoi;
  return {
    venue, repositoryVenue, doi, repositoryDoi,
    doiUrl: doi ? `https://doi.org/${doi.split("/").map(encodeURIComponent).join("/")}` : undefined,
    hasPublicationClue: hasVenueClue || hasDoiClue,
    // Prefer a publication citation over a repository-only row for the same ID.
    score: 4 * Number(hasVenueClue) + 2 * Number(hasDoiClue) + Number(!!doi) + Number(!!venue),
  };
}
