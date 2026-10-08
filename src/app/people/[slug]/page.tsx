import MathText from "@/components/shared/MathText";
import { getAllPeople, getPerson, getAllConnections, getAckMentions } from "@/lib/data";
import { displayName as nameOf, nameInfo } from "@/lib/name";
import PersonTimeline from "@/components/person/PersonTimeline";
import PersonStats from "@/components/person/PersonStats";
import Link from "@/components/shared/AtlasLink";
import { notFound } from "next/navigation";
import { collectPublications } from "@/lib/publications";
import { publicationMetadata, publicationMetadataNote } from "@/lib/publication-metadata";
import PublicationMetadata from "@/components/shared/PublicationMetadata";
import { publicationUrl } from "@/lib/paper-identity";
import { publicSourceUrl } from "@/lib/source-url";
import type { LifeDateFact, OnlineTrace, Person, SourceRef } from "@/lib/types";

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
  const lifespan = formatLifespan(person);

  return (
    <div className="max-w-4xl mx-auto px-6 py-10 w-full">
      {/* Breadcrumb */}
      <div className="text-sm text-[#8888a0] mb-6">
        <Link href="/people" className="hover:text-[#e8e8f0] transition-colors">
          人物
        </Link>
        <span className="mx-2">/</span>
        <span className="text-[#e8e8f0]">{nameOf(slug)}</span>
      </div>

      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-[#e8e8f0] mb-1">
          {nameOf(slug)}
        </h1>
        {/* Show the OTHER name form below the title for context */}
        {nameInfo(slug)?.zh && (
          <p className="text-xl text-[#8888a0]">{person.name.en}</p>
        )}
        <div className="flex items-center gap-3 mt-2 text-sm text-[#8888a0]">
          {person.nationality && <span>{person.nationality}</span>}
          {lifespan && <span>{lifespan}</span>}
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

      <IdentityEvidence person={person} lifespan={lifespan} />

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
            收录论文与历史统计
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
              {nameOf(person.advisor)}
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
                  {nameOf(s)}
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
            合著记录
          </h2>
          <p className="text-xs text-[#8888a0] mb-3">仅按双方档案的相同论文标识计数，身份归属仍在逐篇复核；未对照到论文的关系单列待核实。</p>
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
                              {pubCount} 有出版线索
                            </span>
                          )}
                          {preCount > 0 && (
                            <span
                              className="px-1.5 py-0.5 rounded bg-[#f59e0b]/10 text-[#f59e0b] border border-[#f59e0b]/20 font-mono"
                              title={cp!.preprint
                                .map((p) => `${p.year} ${p.title}`)
                                .join("\n")}
                            >
                              {preCount} 待补出版线索
                            </span>
                          )}
                        </>
                      ) : (
                        <span className="text-[#8888a0]">关系待核实 · 暂无可对照论文</span>
                      )}
                      {c.period && <span>{c.period}</span>}
                    </div>
                  </div>
                  {totalKnown > 0 && (
                    <details className="mt-2">
                      <summary className="text-[10px] text-[#8888a0] cursor-pointer hover:text-[#e8e8f0]">
                        展开 {totalKnown} 篇共同收录论文
                      </summary>
                      <ul className="mt-2 space-y-1 text-[11px]">
                        {[...(cp?.published ?? []), ...(cp?.preprint ?? [])]
                          .sort((a, b) => (b.year ?? 0) - (a.year ?? 0))
                          .map((paper) => {
                            const published = publicationMetadata(paper).hasPublicationClue;
                            const href = publicationUrl(paper);
                            return (
                              <li key={paper.id} className="flex gap-2 items-baseline">
                                <span className={`shrink-0 w-2 h-2 rounded-full mt-1 ${published ? "bg-[#22c55e]" : "bg-[#f59e0b]"}`} />
                                <a
                                  href={href}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="text-[#a8a8b8] hover:text-[#e8e8f0]"
                                >
                                  [{paper.year}] <MathText inline>{paper.title}</MathText>
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
                            {pubCount} 有出版线索
                          </span>
                        )}
                        {preCount > 0 && (
                          <span className="px-1.5 py-0.5 rounded bg-[#f59e0b]/10 text-[#f59e0b] border border-[#f59e0b]/20 font-mono">
                            {preCount} 待补出版线索
                          </span>
                        )}
                      </>
                    ) : (
                      <span className="text-[#8888a0]">关系待核实 · 暂无可对照论文</span>
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
                      展开 {totalKnown} 篇共同收录论文
                    </summary>
                    <ul className="mt-2 space-y-1 text-[11px]">
                      {[...cp.published, ...cp.preprint]
                        .sort((a, b) => (b.year ?? 0) - (a.year ?? 0))
                        .map((paper) => {
                          const published = publicationMetadata(paper).hasPublicationClue;
                          const href = publicationUrl(paper);
                          return (
                            <li key={paper.id} className="flex gap-2 items-baseline">
                              <span className={`shrink-0 w-2 h-2 rounded-full mt-1 ${published ? "bg-[#22c55e]" : "bg-[#f59e0b]"}`} />
                              <a
                                href={href}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-[#a8a8b8] hover:text-[#e8e8f0]"
                              >
                                [{paper.year}] <MathText inline>{paper.title}</MathText>
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
                        {nameOf(m.source)}
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
                        {nameOf(m.target)}
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
      {(person.publications?.length ?? 0) > 0 && (() => {
        const pubs = collectPublications([person]);
        const publishedCount = pubs.filter((p) => publicationMetadata(p).hasPublicationClue).length;
        const preprintCount = pubs.length - publishedCount;
        return (
        <section className="mb-8" id="publications">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">
            论文（{pubs.length}）
            {publishedCount > 0 || preprintCount > 0 ? (
              <span className="text-xs font-normal text-[#8888a0] ml-2">
                <span className="text-[#22c55e]">{publishedCount} 有出版线索</span>
                <span className="mx-1">/</span>
                <span className="text-[#f59e0b]">{preprintCount} 待补出版线索</span>
              </span>
            ) : null}
          </h2>
          <p className="text-xs text-[#8888a0] mb-3">{publicationMetadataNote}</p>
          <div className="space-y-2">
            {pubs.map(
              (
                pub,
                i
              ) => (
                <div
                  key={`${pub.id || "unknown"}:${i}`}
                  className="bg-[#14141f] rounded-lg p-3 border border-[#2a2a3a] group"
                >
                  {(() => {
                    const isDoiId = pub.id?.startsWith("doi:");
                    const isOaId = pub.id?.startsWith("openalex:");
                    const titleHref = publicationUrl(pub);
                    const idHref = publicationUrl({ id: pub.id });
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
                        <MathText inline>{pub.title}</MathText>
                      </a>
                      {pub.coauthors && pub.coauthors.length > 0 && (
                        <div className="text-xs text-[#8888a0] mt-1">
                          合作者：{" "}
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
                        <PublicationMetadata paper={pub} />
                        {pub.primary_category && (
                          <span className="text-[#8888a0]" title="arXiv primary category">
                            {pub.primary_category}
                          </span>
                        )}
                      </div>
                    </div>
                    <div className="flex flex-wrap justify-end items-center gap-2 shrink-0 max-w-[35%] break-all">
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

      {!person.publications?.length && <section id="publications" className="mb-8 text-sm text-[#8888a0]">暂未收录论文记录；不代表该学者没有论文。</section>}

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
          {person.links?.faculty_page && (
            <ExtLink href={person.links.faculty_page} label="教师主页" />
          )}
          {person.links?.cv && <ExtLink href={person.links.cv} label="CV" />}
          {person.links?.google_scholar && (
            <ExtLink href={person.links.google_scholar} label="Google Scholar" />
          )}
          {person.links?.mathscinet && (
            <ExtLink href={person.links.mathscinet} label="MathSciNet" />
          )}
          {person.links?.arxiv_author && (
            <ExtLink href={person.links.arxiv_author} label="arXiv author" />
          )}
          {person.links?.zbmath && (
            <ExtLink href={person.links.zbmath} label="zbMATH" />
          )}
          {person.links?.researchgate && (
            <ExtLink href={person.links.researchgate} label="ResearchGate" />
          )}
          {person.links?.github && (
            <ExtLink href={person.links.github} label="GitHub" />
          )}
          {person.links?.youtube && (
            <ExtLink href={person.links.youtube} label="公开视频" />
          )}
          {person.links?.email && (
            <ExtLink href={`mailto:${person.links.email}`} label="Email" />
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
      {/* Online traces */}
      {person.online_traces && person.online_traces.length > 0 && (
        <section className="mb-8" id="online-traces">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">网上痕迹</h2>
          <div className="space-y-2">
            {person.online_traces.map((trace, i) => (
              <OnlineTraceItem key={`${trace.url}-${i}`} trace={trace} />
            ))}
          </div>
        </section>
      )}
      {/* Sources */}
      {person.sources && person.sources.length > 0 && (
        <section className="mb-8" id="sources">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">数据来源</h2>
          <div className="space-y-3">
            {person.sources.map((src, i) => {
              const href = publicSourceUrl(src.url);
              return (
                <div key={i} className="text-xs leading-relaxed break-words">
                  {href ? (
                    <a
                      href={href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-[#6366f1] hover:text-[#818cf8] transition-colors"
                    >
                      {src.label} ↗
                    </a>
                  ) : <span className="text-[#8888aa]">{src.label}</span>}
                  {src.notes && <p className="mt-1 text-[#8888aa]">{src.notes}</p>}
                  {src.last_verified && (
                    <p className="mt-1 text-[#8888aa]">本项核对：{src.last_verified}</p>
                  )}
                </div>
              );
            })}
          </div>
        </section>
      )}
    </div>
  );
}

function formatLifeDate(fact?: LifeDateFact, fallback?: number | string | null) {
  const raw = fact?.date ?? fallback;
  if (raw === null || raw === undefined || raw === "") return "";
  const place = fact?.place ? `（${fact.place}）` : "";
  return `${raw}${place}`;
}

function formatLifespan(person: Person) {
  const birth = formatLifeDate(person.birth, person.born);
  const death = formatLifeDate(person.death, person.died);
  if (birth && death) return `${birth} – ${death}`;
  return birth || death;
}

function uniqueStrings(values: Array<string | undefined>) {
  return Array.from(
    new Set(values.filter((value): value is string => !!value && value.trim() !== ""))
  );
}

function externalIdLinks(person: Person) {
  const ids = person.external_ids;
  if (!ids) return [];
  return [
    ids.openalex && {
      label: "OpenAlex",
      value: ids.openalex,
      href: `https://openalex.org/authors/${ids.openalex}`,
    },
    ids.mathgenealogy && {
      label: "Math Genealogy",
      value: ids.mathgenealogy,
      href: `https://www.mathgenealogy.org/id.php?id=${ids.mathgenealogy}`,
    },
    ids.orcid && {
      label: "ORCID",
      value: ids.orcid,
      href: `https://orcid.org/${ids.orcid}`,
    },
    ids.zbmath && {
      label: "zbMATH",
      value: ids.zbmath,
      href: `https://zbmath.org/authors/?q=${encodeURIComponent(ids.zbmath)}`,
    },
    ids.inspire && {
      label: "INSPIRE",
      value: ids.inspire,
      href: `https://inspirehep.net/authors/${ids.inspire}`,
    },
  ].filter((item): item is { label: string; value: string; href: string } => !!item);
}

function sourceLinks(sources?: SourceRef[]) {
  if (!sources?.length) return null;
  return (
    <div className="mt-1 flex flex-wrap gap-x-2 gap-y-1">
      {sources.map((src, i) => (
        <a
          key={`${src.url}-${i}`}
          href={publicSourceUrl(src.url)}
          target="_blank"
          rel="noopener noreferrer"
          className="text-[11px] text-[#6366f1] hover:text-[#818cf8]"
        >
          {src.label} ↗
        </a>
      ))}
    </div>
  );
}

function IdentityEvidence({
  person,
  lifespan,
}: {
  person: Person;
  lifespan: string;
}) {
  const emails = uniqueStrings([person.links?.email, ...(person.known_emails ?? [])]);
  const affiliations = uniqueStrings(person.known_affiliations ?? []);
  const ids = externalIdLinks(person);
  const hasLifeData = !!lifespan || !!person.birth?.notes || !!person.death?.notes;
  const hasEvidence =
    hasLifeData ||
    emails.length > 0 ||
    affiliations.length > 0 ||
    ids.length > 0 ||
    (person.online_traces?.length ?? 0) > 0;

  if (!hasEvidence) return null;

  return (
    <section className="mb-8">
      <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">身份线索</h2>
      <div className="bg-[#14141f] rounded-xl p-5 border border-[#2a2a3a] space-y-4 text-sm">
        {hasLifeData && (
          <div>
            <div className="text-xs text-[#8888a0] mb-1">生卒信息</div>
            {lifespan && <div className="text-[#e8e8f0]">{lifespan}</div>}
            {person.birth?.notes && (
              <div className="text-xs text-[#8888a0] mt-1">{person.birth.notes}</div>
            )}
            {person.death?.notes && (
              <div className="text-xs text-[#8888a0] mt-1">{person.death.notes}</div>
            )}
            {sourceLinks([...(person.birth?.sources ?? []), ...(person.death?.sources ?? [])])}
          </div>
        )}

        {emails.length > 0 && (
          <div>
            <div className="text-xs text-[#8888a0] mb-1">公开邮箱</div>
            <div className="flex flex-wrap gap-2">
              {emails.map((email) => (
                <a
                  key={email}
                  href={`mailto:${email}`}
                  className="text-[#6366f1] hover:text-[#818cf8] font-mono text-xs"
                >
                  {email}
                </a>
              ))}
            </div>
          </div>
        )}

        {affiliations.length > 0 && (
          <div>
            <div className="text-xs text-[#8888a0] mb-1">论文署名/已知单位</div>
            <div className="flex flex-wrap gap-2">
              {affiliations.map((affiliation) => (
                <span
                  key={affiliation}
                  className="px-2 py-1 rounded bg-[#2a2a3a] text-xs text-[#c8c8d8]"
                >
                  {affiliation}
                </span>
              ))}
            </div>
          </div>
        )}

        {ids.length > 0 && (
          <div>
            <div className="text-xs text-[#8888a0] mb-1">消歧 ID</div>
            <div className="flex flex-wrap gap-2">
              {ids.map((id) => (
                <a
                  key={`${id.label}-${id.value}`}
                  href={id.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-2 py-1 rounded bg-[#2a2a3a] text-xs text-[#6366f1] hover:text-[#818cf8] font-mono"
                >
                  {id.label}: {id.value} ↗
                </a>
              ))}
            </div>
          </div>
        )}

        {(person.online_traces?.length ?? 0) > 0 && (
          <div>
            <div className="text-xs text-[#8888a0] mb-1">公开网上痕迹</div>
            <a
              href="#online-traces"
              className="text-[#6366f1] hover:text-[#818cf8] text-sm"
            >
              {person.online_traces!.length} 条可复核记录
            </a>
          </div>
        )}
      </div>
    </section>
  );
}

function traceTypeLabel(type: OnlineTrace["type"]) {
  const labels: Record<OnlineTrace["type"], string> = {
    homepage: "主页",
    faculty: "教师主页",
    cv: "CV",
    google_scholar: "Google Scholar",
    orcid: "ORCID",
    mathgenealogy: "Math Genealogy",
    zbmath: "zbMATH",
    mathscinet: "MathSciNet",
    arxiv: "arXiv",
    openalex: "OpenAlex",
    video: "视频",
    interview: "访谈",
    lecture_notes: "讲义",
    slides: "Slides",
    news: "新闻",
    blog: "博客",
    github: "GitHub",
    wayback: "Wayback",
    other: "其他",
  };
  return labels[type];
}

function OnlineTraceItem({ trace }: { trace: OnlineTrace }) {
  const label = trace.label || traceTypeLabel(trace.type);
  return (
    <div className="bg-[#14141f] rounded-lg p-3 border border-[#2a2a3a] text-sm">
      <div className="flex flex-wrap items-center gap-2">
        <span className="text-xs px-2 py-0.5 rounded bg-[#2a2a3a] text-[#8888a0]">
          {traceTypeLabel(trace.type)}
        </span>
        <a
          href={publicSourceUrl(trace.url)}
          target="_blank"
          rel="noopener noreferrer"
          className="text-[#6366f1] hover:text-[#818cf8] transition-colors"
        >
          {label} ↗
        </a>
        {trace.archived_url && (
          <a
            href={publicSourceUrl(trace.archived_url)}
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs text-[#8888a0] hover:text-[#e8e8f0] transition-colors"
          >
            存档 ↗
          </a>
        )}
        {trace.last_verified && (
          <span className="text-xs text-[#8888a0]">
            核验 {trace.last_verified}
          </span>
        )}
      </div>
      {trace.notes && (
        <p className="text-xs text-[#8888a0] mt-2 leading-relaxed">{trace.notes}</p>
      )}
    </div>
  );
}

function ExtLink({ href, label }: { href: string; label: string }) {
  if (!publicSourceUrl(href)) return <span className="text-xs text-[#8888a0]">{label}（链接待核实）</span>;
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
