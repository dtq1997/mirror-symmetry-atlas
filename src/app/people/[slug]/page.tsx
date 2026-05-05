import { getAllPeople, getPerson, getAllConnections, getAckMentions } from "@/lib/data";
import PersonTimeline from "@/components/person/PersonTimeline";
import PersonStats from "@/components/person/PersonStats";
import Link from "next/link";
import { notFound } from "next/navigation";

export function generateStaticParams() {
  return getAllPeople().map((p) => ({ slug: p.slug }));
}

export default async function PersonPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const person = getPerson(slug);
  if (!person) notFound();

  const connections = getAllConnections().filter(
    (c) => c.source === slug || c.target === slug
  );

  // Build slug -> display name map (zh preferred, fallback en, fallback slug)
  const peopleIndex = new Map<string, { displayName: string; en: string; zh?: string }>();
  for (const p of getAllPeople()) {
    const zh = p.name?.zh;
    const en = p.name?.en || p.slug;
    peopleIndex.set(p.slug, {
      displayName: zh && !zh.startsWith('[') ? zh : en,
      en,
      zh: zh && !zh.startsWith('[') ? zh : undefined,
    });
  }
  function nameOf(s: string): string {
    return peopleIndex.get(s)?.displayName ?? s;
  }

  const coauthors = connections
    .filter((c) => c.type === "coauthor")
    .sort((a, b) => (b.weight ?? 0) - (a.weight ?? 0));

  const ackMentions = getAckMentions();
  const acknowledges = (ackMentions.bySource.get(slug) ?? [])
    .slice()
    .sort((a, b) => b.papers.length - a.papers.length);
  const acknowledgedBy = (ackMentions.byTarget.get(slug) ?? [])
    .slice()
    .sort((a, b) => b.papers.length - a.papers.length);

  return (
    <div className="max-w-4xl mx-auto px-6 py-10 w-full">
      {/* Breadcrumb */}
      <div className="text-sm text-[#8888a0] mb-6">
        <Link href="/people" className="hover:text-[#e8e8f0] transition-colors">
          人物
        </Link>
        <span className="mx-2">/</span>
        <span className="text-[#e8e8f0]">{person.name.en}</span>
      </div>

      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-[#e8e8f0] mb-1">
          {person.name.en}
        </h1>
        {person.name.zh && (
          <p className="text-xl text-[#8888a0]">{person.name.zh}</p>
        )}
        <div className="flex items-center gap-3 mt-2 text-sm text-[#8888a0]">
          {person.nationality && <span>{person.nationality}</span>}
          {person.born && (
            <span>
              {person.born}
              {person.died ? ` – ${person.died}` : ""}
            </span>
          )}
        </div>

        {/* Tags */}
        {person.tags?.length > 0 && (
          <div className="flex flex-wrap gap-1 mt-3">
            {person.tags.map((tag) => (
              <span
                key={tag}
                className="px-2 py-0.5 text-xs rounded-full bg-[#2a2a3a] text-[#8888a0]"
              >
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Research areas */}
      {person.research_areas?.length > 0 && (
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">
            研究方向
          </h2>
          <div className="flex flex-wrap gap-2">
            {person.research_areas.map((area) => (
              <Link
                key={area}
                href={`/concepts/${area}`}
                className="px-3 py-1 text-sm rounded-full bg-[#6366f1]/15 text-[#818cf8] border border-[#6366f1]/30 hover:bg-[#6366f1]/25 transition-colors"
              >
                {area}
              </Link>
            ))}
          </div>
        </section>
      )}

      {/* Activity stats */}
      {person.activity && (
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">
            学术活跃度
          </h2>
          <PersonStats activity={person.activity} />
        </section>
      )}

      {/* Career Timeline */}
      {person.career_timeline?.length > 0 && (
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-4">
            学术履历
          </h2>
          <div className="bg-[#14141f] rounded-xl p-6 border border-[#2a2a3a]">
            <PersonTimeline timeline={person.career_timeline} />
          </div>
        </section>
      )}

      {/* Advisor & Students */}
      <section className="mb-8 grid md:grid-cols-2 gap-4">
        {person.advisor && (
          <div className="bg-[#14141f] rounded-xl p-5 border border-[#2a2a3a]">
            <h3 className="text-sm font-medium text-[#8888a0] mb-2">导师</h3>
            <Link
              href={`/people/${person.advisor}`}
              className="text-[#f59e0b] hover:text-[#fbbf24] transition-colors"
            >
              {person.advisor}
            </Link>
          </div>
        )}
        {person.students?.length > 0 && (
          <div className="bg-[#14141f] rounded-xl p-5 border border-[#2a2a3a]">
            <h3 className="text-sm font-medium text-[#8888a0] mb-2">
              学生（{person.students.length}）
            </h3>
            <div className="flex flex-wrap gap-2">
              {person.students.map((s) => (
                <Link
                  key={s}
                  href={`/people/${s}`}
                  className="text-sm text-[#f59e0b] hover:text-[#fbbf24] transition-colors"
                >
                  {s}
                </Link>
              ))}
            </div>
          </div>
        )}
      </section>

      {/* Co-authors */}
      {coauthors.length > 0 && (
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">
            合著者
          </h2>
          <div className="space-y-2">
            {coauthors.map((c, i) => {
              const otherSlug = c.source === slug ? c.target : c.source;
              const cp = c.coauthored_papers;
              const pubCount = cp?.published.length ?? 0;
              const preCount = cp?.preprint.length ?? 0;
              const totalKnown = pubCount + preCount;
              return (
                <div
                  key={i}
                  className="bg-[#14141f] rounded-lg p-3 border border-[#2a2a3a]"
                >
                  <div className="flex items-center justify-between gap-3">
                    <Link
                      href={`/people/${otherSlug}`}
                      className="text-sm text-[#f59e0b] hover:text-[#fbbf24] transition-colors"
                    >
                      {nameOf(otherSlug)}
                    </Link>
                    <div className="flex items-center gap-2 text-xs text-[#8888a0] flex-wrap justify-end">
                      {totalKnown > 0 ? (
                        <>
                          {pubCount > 0 && (
                            <span
                              className="px-1.5 py-0.5 rounded bg-[#22c55e]/10 text-[#22c55e] border border-[#22c55e]/20 font-mono"
                              title={cp!.published
                                .map((p) => `${p.year} ${p.title}`)
                                .join("\n")}
                            >
                              {pubCount} 已发表
                            </span>
                          )}
                          {preCount > 0 && (
                            <span
                              className="px-1.5 py-0.5 rounded bg-[#f59e0b]/10 text-[#f59e0b] border border-[#f59e0b]/20 font-mono"
                              title={cp!.preprint
                                .map((p) => `${p.year} ${p.title}`)
                                .join("\n")}
                            >
                              {preCount} 仅预印
                            </span>
                          )}
                        </>
                      ) : (
                        c.weight && (
                          <a
                            href={`https://arxiv.org/search/?searchtype=author&query=${encodeURIComponent(otherSlug.replace(/-/g, " "))}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-[#6366f1] font-mono hover:text-[#818cf8]"
                            title="未在双方 publications 列表中找到合著记录，回退到 key_collaborators 字段"
                          >
                            {c.weight} 篇 (键值)
                          </a>
                        )
                      )}
                      {c.period && <span>{c.period}</span>}
                    </div>
                  </div>
                  {totalKnown > 0 && (
                    <details className="mt-2">
                      <summary className="text-[10px] text-[#8888a0] cursor-pointer hover:text-[#e8e8f0]">
                        展开 {totalKnown} 篇合著论文
                      </summary>
                      <ul className="mt-2 space-y-1 text-[11px]">
                        {[...(cp?.published ?? []), ...(cp?.preprint ?? [])]
                          .sort((a, b) => (b.year ?? 0) - (a.year ?? 0))
                          .map((paper) => {
                            const isPub = "doi" in paper && (paper as { doi?: string; journal?: string }).doi;
                            const isPubByJournal = "journal" in paper && (paper as { journal?: string }).journal;
                            const published = isPub || isPubByJournal;
                            const href = (paper as { doi?: string }).doi
                              ? `https://doi.org/${(paper as { doi: string }).doi}`
                              : `https://arxiv.org/abs/${paper.id}`;
                            return (
                              <li key={paper.id} className="flex gap-2 items-baseline">
                                <span className={`shrink-0 w-2 h-2 rounded-full mt-1 ${published ? "bg-[#22c55e]" : "bg-[#f59e0b]"}`} />
                                <a
                                  href={href}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="text-[#a8a8b8] hover:text-[#e8e8f0]"
                                >
                                  [{paper.year}] {paper.title}
                                </a>
                              </li>
                            );
                          })}
                      </ul>
                    </details>
                  )}
                </div>
              );
            })}
          </div>
        </section>
      )}

      {/* Key collaborators (from person YAML) */}
      {person.key_collaborators?.length > 0 && (
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">
            主要合作者
          </h2>
          <div className="space-y-3">
            {person.key_collaborators.map((collab, idx) => {
              const hasSlug = !!collab.person;
              const collabSlug = collab.person || "";
              const displayName = collabSlug ? nameOf(collabSlug) : ((collab as { name?: string }).name || "");
              const searchName = (collabSlug || (collab as { name?: string }).name || "").replace(/-/g, " ");
              // Look up live coauthored_papers from publications-derived edge,
              // so the count + breakdown match the "合著者" panel exactly.
              const matchEdge = coauthors.find((c) => {
                const otherSlug = c.source === slug ? c.target : c.source;
                return otherSlug === collab.person;
              });
              const cp = matchEdge?.coauthored_papers;
              const pubCount = cp?.published.length ?? 0;
              const preCount = cp?.preprint.length ?? 0;
              const totalKnown = pubCount + preCount;
              return (
              <div
                key={collab.person || `${displayName}-${idx}`}
                className="bg-[#14141f] rounded-lg p-4 border border-[#2a2a3a]"
              >
                <div className="flex items-center justify-between mb-1">
                  {hasSlug ? (
                    <Link
                      href={`/people/${collab.person}`}
                      className="text-sm font-medium text-[#f59e0b] hover:text-[#fbbf24] transition-colors"
                    >
                      {displayName}
                    </Link>
                  ) : (
                    <span className="text-sm font-medium text-[#a8a8b8]">{displayName}</span>
                  )}
                  <div className="flex items-center gap-2 text-xs text-[#8888a0] flex-wrap justify-end">
                    {totalKnown > 0 ? (
                      <>
                        {pubCount > 0 && (
                          <span className="px-1.5 py-0.5 rounded bg-[#22c55e]/10 text-[#22c55e] border border-[#22c55e]/20 font-mono">
                            {pubCount} 已发表
                          </span>
                        )}
                        {preCount > 0 && (
                          <span className="px-1.5 py-0.5 rounded bg-[#f59e0b]/10 text-[#f59e0b] border border-[#f59e0b]/20 font-mono">
                            {preCount} 仅预印
                          </span>
                        )}
                      </>
                    ) : (
                      collab.papers_count && (
                        <a
                          href={`https://arxiv.org/search/?searchtype=author&query=${encodeURIComponent(searchName)}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-[#6366f1] hover:text-[#818cf8] font-mono"
                          title="未在双方 publications 列表中找到合著记录，显示的是 yaml 手填值"
                        >
                          {collab.papers_count} 篇 (键值)
                        </a>
                      )
                    )}
                    {collab.since && <span>{collab.since} 起</span>}
                  </div>
                </div>
                {collab.topic && (
                  <p className="text-xs text-[#8888a0]">{collab.topic}</p>
                )}
                {collab.met_context && (
                  <p className="text-xs text-[#8888a0] mt-1 italic">
                    {collab.met_context}
                  </p>
                )}
                {totalKnown > 0 && cp && (
                  <details className="mt-2">
                    <summary className="text-[10px] text-[#8888a0] cursor-pointer hover:text-[#e8e8f0]">
                      展开 {totalKnown} 篇合著论文
                    </summary>
                    <ul className="mt-2 space-y-1 text-[11px]">
                      {[...cp.published, ...cp.preprint]
                        .sort((a, b) => (b.year ?? 0) - (a.year ?? 0))
                        .map((paper) => {
                          const isPub = "doi" in paper && (paper as { doi?: string }).doi;
                          const isPubByJournal = "journal" in paper && (paper as { journal?: string }).journal;
                          const published = isPub || isPubByJournal;
                          const href = (paper as { doi?: string }).doi
                            ? `https://doi.org/${(paper as { doi: string }).doi}`
                            : `https://arxiv.org/abs/${paper.id}`;
                          return (
                            <li key={paper.id} className="flex gap-2 items-baseline">
                              <span className={`shrink-0 w-2 h-2 rounded-full mt-1 ${published ? "bg-[#22c55e]" : "bg-[#f59e0b]"}`} />
                              <a
                                href={href}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-[#a8a8b8] hover:text-[#e8e8f0]"
                              >
                                [{paper.year}] {paper.title}
                              </a>
                            </li>
                          );
                        })}
                    </ul>
                  </details>
                )}
              </div>
            );
            })}
          </div>
        </section>
      )}

      {/* Acknowledgement network */}
      {(acknowledges.length > 0 || acknowledgedBy.length > 0) && (
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">
            致谢网
            <span className="text-xs text-[#8888a0] font-normal ml-2">
              从 arXiv 论文致谢段抽取
            </span>
          </h2>
          <div className="grid md:grid-cols-2 gap-4">
            {acknowledgedBy.length > 0 && (
              <div className="bg-[#14141f] rounded-xl p-5 border border-[#2a2a3a]">
                <h3 className="text-sm font-medium text-[#8888a0] mb-3">
                  被致谢（{acknowledgedBy.length} 人）
                </h3>
                <div className="space-y-2">
                  {acknowledgedBy.map((m) => (
                    <div
                      key={m.source}
                      className="flex items-center justify-between gap-2"
                    >
                      <Link
                        href={`/people/${m.source}`}
                        className="text-sm text-[#f59e0b] hover:text-[#fbbf24] transition-colors truncate"
                      >
                        {m.source}
                      </Link>
                      <div className="flex items-center gap-1 shrink-0">
                        <span className="text-xs text-[#a8a29e] font-mono">
                          {m.papers.length}×
                        </span>
                        <div className="flex gap-1">
                          {m.papers.slice(0, 3).map((p) => (
                            <a
                              key={p}
                              href={`https://arxiv.org/abs/${p}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-[10px] text-[#8888a0] hover:text-[#e8e8f0] font-mono"
                              title={p}
                            >
                              ↗
                            </a>
                          ))}
                          {m.papers.length > 3 && (
                            <span className="text-[10px] text-[#8888a0]">
                              +{m.papers.length - 3}
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
            {acknowledges.length > 0 && (
              <div className="bg-[#14141f] rounded-xl p-5 border border-[#2a2a3a]">
                <h3 className="text-sm font-medium text-[#8888a0] mb-3">
                  致谢过（{acknowledges.length} 人）
                </h3>
                <div className="space-y-2">
                  {acknowledges.map((m) => (
                    <div
                      key={m.target}
                      className="flex items-center justify-between gap-2"
                    >
                      <Link
                        href={`/people/${m.target}`}
                        className="text-sm text-[#f59e0b] hover:text-[#fbbf24] transition-colors truncate"
                      >
                        {m.target}
                      </Link>
                      <div className="flex items-center gap-1 shrink-0">
                        <span className="text-xs text-[#a8a29e] font-mono">
                          {m.papers.length}×
                        </span>
                        <div className="flex gap-1">
                          {m.papers.slice(0, 3).map((p) => (
                            <a
                              key={p}
                              href={`https://arxiv.org/abs/${p}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-[10px] text-[#8888a0] hover:text-[#e8e8f0] font-mono"
                              title={p}
                            >
                              ↗
                            </a>
                          ))}
                          {m.papers.length > 3 && (
                            <span className="text-[10px] text-[#8888a0]">
                              +{m.papers.length - 3}
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </section>
      )}

      {/* Publications */}
      {(person as any).publications?.length > 0 && (() => {
        const pubs = (person as any).publications as Array<{
          id: string;
          title: string;
          year: number;
          coauthors?: string[];
          doi?: string;
          journal?: string;
          primary_category?: string;
        }>;
        const publishedCount = pubs.filter((p) => p.journal || p.doi).length;
        const preprintCount = pubs.length - publishedCount;
        return (
        <section className="mb-8" id="publications">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">
            论文（{pubs.length}
            {publishedCount > 0 || preprintCount > 0 ? (
              <span className="text-xs font-normal text-[#8888a0] ml-2">
                <span className="text-[#22c55e]">{publishedCount} 已发表</span>
                <span className="mx-1">/</span>
                <span className="text-[#f59e0b]">{preprintCount} 仅预印</span>
              </span>
            ) : null}
            ）
          </h2>
          <div className="space-y-2">
            {pubs.map(
              (
                pub,
                i
              ) => (
                <div
                  key={pub.id || i}
                  className="bg-[#14141f] rounded-lg p-3 border border-[#2a2a3a] group"
                >
                  {(() => {
                    const isDoiId = pub.id?.startsWith("doi:");
                    const isOaId = pub.id?.startsWith("openalex:");
                    const titleHref = pub.doi
                      ? `https://doi.org/${pub.doi}`
                      : isDoiId
                        ? `https://doi.org/${pub.id.slice(4)}`
                        : isOaId
                          ? `https://openalex.org/works/${pub.id.slice(9)}`
                          : `https://arxiv.org/abs/${pub.id}`;
                    const idHref = isDoiId
                      ? `https://doi.org/${pub.id.slice(4)}`
                      : isOaId
                        ? `https://openalex.org/works/${pub.id.slice(9)}`
                        : `https://arxiv.org/abs/${pub.id}`;
                    const idLabel = isDoiId
                      ? pub.id.slice(4)
                      : isOaId
                        ? pub.id.slice(9)
                        : pub.id;
                    return (
                  <div className="flex items-start justify-between gap-3">
                    <div className="min-w-0">
                      <a
                        href={titleHref}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-sm text-[#e8e8f0] hover:text-[#6366f1] transition-colors leading-snug"
                      >
                        {pub.title}
                      </a>
                      {pub.coauthors && pub.coauthors.length > 0 && (
                        <div className="text-xs text-[#8888a0] mt-1">
                          with{" "}
                          {pub.coauthors.map((c: string, j: number) => {
                            const isSlug =
                              !c.includes(" ") && c === c.toLowerCase();
                            return (
                              <span key={j}>
                                {j > 0 && ", "}
                                {isSlug ? (
                                  <Link
                                    href={`/people/${c}`}
                                    className="text-[#f59e0b] hover:text-[#fbbf24]"
                                  >
                                    {nameOf(c)}
                                  </Link>
                                ) : (
                                  <span>{c}</span>
                                )}
                              </span>
                            );
                          })}
                        </div>
                      )}
                      <div className="flex items-center gap-2 mt-1.5 text-[10px] font-mono flex-wrap">
                        {pub.journal || pub.doi ? (
                          pub.doi ? (
                            <a
                              href={`https://doi.org/${pub.doi}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="px-1.5 py-0.5 rounded bg-[#22c55e]/10 text-[#22c55e] border border-[#22c55e]/20 hover:bg-[#22c55e]/20"
                              title={`DOI: ${pub.doi}${pub.journal ? `\n${pub.journal}` : ""}`}
                            >
                              已发表{pub.journal ? `: ${pub.journal}` : ""}
                            </a>
                          ) : (
                            <span
                              className="px-1.5 py-0.5 rounded bg-[#22c55e]/10 text-[#22c55e] border border-[#22c55e]/20"
                              title={pub.journal}
                            >
                              已发表{pub.journal ? `: ${pub.journal}` : ""}
                            </span>
                          )
                        ) : (
                          <span
                            className="px-1.5 py-0.5 rounded bg-[#f59e0b]/10 text-[#f59e0b] border border-[#f59e0b]/20"
                            title="未在 arxiv journal_ref 或 Crossref 中找到正式发表记录"
                          >
                            仅预印
                          </span>
                        )}
                        {pub.primary_category && (
                          <span className="text-[#8888a0]" title="arXiv primary category">
                            {pub.primary_category}
                          </span>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center gap-2 shrink-0">
                      <span className="text-xs font-mono text-[#6366f1]">
                        {pub.year}
                      </span>
                      <a
                        href={idHref}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-[10px] text-[#8888a0] hover:text-[#e8e8f0] font-mono"
                      >
                        {idLabel}
                      </a>
                    </div>
                  </div>
                  );
                  })()}
                </div>
              )
            )}
          </div>
        </section>
        );
      })()}

      {/* Personal notes */}
      {person.personal_notes && (
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">备注</h2>
          <div className="bg-[#14141f] rounded-xl p-5 border border-[#2a2a3a] text-sm text-[#e8e8f0] leading-relaxed whitespace-pre-line">
            {person.personal_notes}
          </div>
        </section>
      )}

      {/* External links — manual + auto-generated from external_ids */}
      <section className="mb-8">
        <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">链接</h2>
        <div className="flex flex-wrap gap-3">
          {person.links?.homepage && (
            <ExtLink href={person.links.homepage} label="主页" />
          )}
          {person.links?.google_scholar && (
            <ExtLink href={person.links.google_scholar} label="Google Scholar" />
          )}
          {person.links?.mathscinet && (
            <ExtLink href={person.links.mathscinet} label="MathSciNet" />
          )}
          {person.external_ids?.openalex && (
            <ExtLink
              href={`https://openalex.org/authors/${person.external_ids.openalex}`}
              label="OpenAlex"
            />
          )}
          {person.external_ids?.mathgenealogy && (
            <ExtLink
              href={`https://www.mathgenealogy.org/id.php?id=${person.external_ids.mathgenealogy}`}
              label="Math Genealogy"
            />
          )}
          {person.external_ids?.orcid && (
            <ExtLink
              href={`https://orcid.org/${person.external_ids.orcid}`}
              label="ORCID"
            />
          )}
        </div>
      </section>
      {/* Sources */}
      {person.sources && person.sources.length > 0 && (
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">数据来源</h2>
          <div className="space-y-1">
            {person.sources.map((src, i) => (
              <div key={i} className="text-xs">
                <a
                  href={src.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-[#6366f1] hover:text-[#818cf8] transition-colors"
                >
                  {src.label} ↗
                </a>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}

function ExtLink({ href, label }: { href: string; label: string }) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className="px-4 py-2 text-sm bg-[#14141f] rounded-lg border border-[#2a2a3a] text-[#6366f1] hover:bg-[#2a2a3a] transition-colors"
    >
      {label} ↗
    </a>
  );
}
