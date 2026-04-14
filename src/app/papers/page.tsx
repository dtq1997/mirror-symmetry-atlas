import { getAllPeople, getAllPapers } from "@/lib/data";
import Link from "next/link";

export default function PapersPage() {
  const people = getAllPeople();
  const seminalPapers = getAllPapers();

  // Collect all publications from people, deduplicate
  const allPubs: {
    id: string;
    title: string;
    year: number;
    coauthors: string[];
    ownerSlug: string;
    ownerName: string;
  }[] = [];
  const seenIds = new Set<string>();

  for (const p of people) {
    const pubs = (p as any).publications || [];
    const name = p.name.zh || p.name.en;
    for (const pub of pubs) {
      if (!seenIds.has(pub.id)) {
        seenIds.add(pub.id);
        allPubs.push({
          id: pub.id,
          title: pub.title,
          year: pub.year,
          coauthors: pub.coauthors || [],
          ownerSlug: p.slug,
          ownerName: name,
        });
      }
    }
  }

  allPubs.sort((a, b) => b.year - a.year || b.id.localeCompare(a.id));

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
        库中 {allPubs.length} 篇论文（{people.filter((p) => (p as any).publications?.length).length} 位作者）
      </p>

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
                  key={pub.id}
                  className="bg-[#14141f] rounded-lg p-3 border border-[#2a2a3a]"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div className="min-w-0">
                      <a
                        href={`https://arxiv.org/abs/${pub.id}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-sm text-[#e8e8f0] hover:text-[#6366f1] transition-colors leading-snug"
                      >
                        {pub.title}
                      </a>
                      <div className="flex flex-wrap items-center gap-1 mt-1">
                        <Link
                          href={`/people/${pub.ownerSlug}`}
                          className="text-[10px] px-1.5 py-0.5 rounded bg-[#f59e0b]/15 text-[#fbbf24] hover:bg-[#f59e0b]/25"
                        >
                          {pub.ownerName}
                        </Link>
                        {pub.coauthors.map((c, i) => {
                          const isSlug = !c.includes(" ") && c === c.toLowerCase();
                          return isSlug ? (
                            <Link
                              key={i}
                              href={`/people/${c}`}
                              className="text-[10px] px-1.5 py-0.5 rounded bg-[#f59e0b]/10 text-[#d97706] hover:bg-[#f59e0b]/20"
                            >
                              {c}
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
                      href={`https://arxiv.org/abs/${pub.id}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-[10px] font-mono text-[#8888a0] hover:text-[#e8e8f0] shrink-0"
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
