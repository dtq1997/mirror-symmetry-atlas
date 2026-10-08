import MathText from "@/components/shared/MathText";
import Link from "@/components/shared/AtlasLink";
import PublicationMetadata from "@/components/shared/PublicationMetadata";
import { displayName } from "@/lib/name";
import { publicationUrl } from "@/lib/paper-identity";
import type { CatalogPublication } from "@/lib/publications";

export default function PublicationCard({ paper }: { paper: CatalogPublication }) {
  const url = publicationUrl(paper);
  const idUrl = publicationUrl({ id: paper.id });
  return (
    <article data-catalog-record={paper.catalogKey} className="bg-[#14141f] rounded-lg p-4 border border-[#2a2a3a] min-w-0">
      <div className="flex items-start gap-3">
        <h3 className="min-w-0 flex-1 text-sm text-[#e8e8f0] leading-relaxed break-words">
          {url ? <a href={url} target="_blank" rel="noopener noreferrer" className="hover:text-[#a5b4fc] focus-visible:outline-2 focus-visible:outline-[#a5b4fc]">
            <MathText inline>{paper.title}</MathText>
          </a> : <MathText inline>{paper.title}</MathText>}
        </h3>
        <span className="text-xs font-mono text-[#a5b4fc] shrink-0 pt-1">{paper.year}</span>
      </div>
      <PublicationMetadata paper={paper} />
      <div className="flex flex-wrap items-center gap-1.5 mt-2">
        {paper.ownerSlugs.map((slug) => <Link key={slug} href={`/people/${slug}`}
          className="text-xs px-1.5 py-0.5 rounded bg-[#f59e0b]/15 text-[#fbbf24] hover:underline">
          {displayName(slug)}
        </Link>)}
        {paper.coauthors.filter((c) => !paper.ownerSlugs.includes(c)).map((c, i) => (
          !c.includes(" ") && c === c.toLowerCase()
            ? <Link key={i} href={`/people/${c}`} className="text-xs text-[#d97706] hover:underline">{displayName(c)}</Link>
            : <span key={i} className="text-xs text-[#8888a0]">{c}</span>
        ))}
      </div>
      <div className="text-xs font-mono text-[#8888a0] break-all mt-2">
        {idUrl ? <a href={idUrl} target="_blank" rel="noopener noreferrer" className="hover:text-[#e8e8f0]">{paper.id} ↗</a> : paper.id}
      </div>
    </article>
  );
}
