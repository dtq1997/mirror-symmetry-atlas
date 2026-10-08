import { getAllPeople, getAllPapers } from "@/lib/data";
import Link from "@/components/shared/AtlasLink";
import { displayName } from "@/lib/name";
import { collectPublications } from "@/lib/publications";
import PublicationMetadata from "@/components/shared/PublicationMetadata";
import { publicationMetadataNote } from "@/lib/publication-metadata";
import { publicationUrl } from "@/lib/paper-identity";

export default function PapersPage() {
  const people = getAllPeople();
  const seminalPapers = getAllPapers();

  const allPubs = collectPublications(people);

  // Group by year
  const byYear = new Map<number, typeof allPubs>();
  for (const pub of allPubs) {
    const list = byYear.get(pub.year) || [];
    list.push(pub);
    byYear.set(pub.year, list);
  }
  const years = [...byYear.keys()].sort((a, b) => b - a);

  return (
    <div className="max-w-4xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-bold text-[#e8e8f0] mb-2">论文</h1>
      <p className="text-[#8888a0] mb-8">
        去重后保留 {allPubs.length} 条论文记录（{people.filter((p) => p.publications?.length).length} 位作者）
      </p>

      <p className="text-sm text-[#8888a0] mb-6">列表按现有 DOI、arXiv 编号及标题归并；标识冲突的记录暂时分开保留，待逐项核实。本表不代表作者全部成果。{publicationMetadataNote}</p>

      {years.map((year) => {
        const pubs = byYear.get(year)!;
        return (
          <section key={year} className="mb-8">
            <h2 className="text-lg font-semibold text-[#6366f1] mb-3 font-mono">
              {year}
              <span className="text-xs text-[#8888a0] font-sans ml-2">
                {pubs.length} 篇
              </span>
            </h2>
            <div className="space-y-2">
              {pubs.map((pub) => (
                <div
                  key={pub.catalogKey}
                  className="bg-[#14141f] rounded-lg p-3 border border-[#2a2a3a]"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div className="min-w-0">
                      <a
                        href={publicationUrl(pub)}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-sm text-[#e8e8f0] hover:text-[#6366f1] transition-colors leading-snug"
                      >
                        {pub.title}
                      </a>
                      <PublicationMetadata paper={pub} />
                      <div className="flex flex-wrap items-center gap-1 mt-1">
                        {pub.ownerSlugs.map((slug) => <Link
                          key={slug} href={`/people/${slug}`}
                          className="text-xs px-1.5 py-0.5 rounded bg-[#f59e0b]/15 text-[#fbbf24]"
                        >{displayName(slug)}</Link>)}
                        {pub.coauthors.filter((c) => !pub.ownerSlugs.includes(c)).map((c, i) => {
                          const isSlug = !c.includes(" ") && c === c.toLowerCase();
                          return isSlug ? (
                            <Link
                              key={i}
                              href={`/people/${c}`}
                              className="text-[10px] px-1.5 py-0.5 rounded bg-[#f59e0b]/10 text-[#d97706] hover:bg-[#f59e0b]/20"
                            >
                              {displayName(c)}
                            </Link>
                          ) : (
                            <span key={i} className="text-[10px] text-[#8888a0]">
                              {c}
                            </span>
                          );
                        })}
                      </div>
                    </div>
                    <a
                      href={publicationUrl(pub)}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-xs font-mono text-[#8888a0] hover:text-[#e8e8f0] max-w-[35%] break-all"
                    >
                      {pub.id}
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </section>
        );
      })}

      {/* Seminal papers */}
      {seminalPapers.length > 0 && (
        <section className="mt-12 pt-8 border-t border-[#2a2a3a]">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-4">
            经典文献
            <span className="text-xs text-[#8888a0] font-normal ml-2">
              手工精选
            </span>
          </h2>
          <div className="space-y-2">
            {seminalPapers
              .filter((p) => p.importance === "seminal" || p.importance === "major")
              .map((paper, i) => (
                <div
                  key={paper.arxiv_id || i}
                  className="bg-[#14141f] rounded-lg p-3 border border-[#2a2a3a]"
                  style={{
                    borderLeftColor:
                      paper.importance === "seminal" ? "#f59e0b" : "#6366f1",
                    borderLeftWidth: 3,
                  }}
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      {paper.arxiv_id ? (
                        <a
                          href={`https://arxiv.org/abs/${paper.arxiv_id}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-sm text-[#e8e8f0] hover:text-[#6366f1] transition-colors"
                        >
                          {paper.title}
                        </a>
                      ) : (
                        <span className="text-sm text-[#e8e8f0]">
                          {paper.title}
                        </span>
                      )}
                      <div className="text-xs text-[#8888a0] mt-1">
                        {paper.authors_raw?.join(", ")}
                        {paper.journal && ` · ${paper.journal}`}
                      </div>
                      {paper.notes && (
                        <div className="text-xs text-[#8888a0] mt-0.5 italic">
                          {paper.notes}
                        </div>
                      )}
                    </div>
                    <span className="text-xs font-mono text-[#6366f1] shrink-0">
                      {paper.year}
                    </span>
                  </div>
                </div>
              ))}
          </div>
        </section>
      )}
    </div>
  );
}
