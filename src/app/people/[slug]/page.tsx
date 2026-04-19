import { getAllPeople, getPerson, getAllConnections } from "@/lib/data";
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

  const coauthors = connections
    .filter((c) => c.type === "coauthor")
    .sort((a, b) => (b.weight ?? 0) - (a.weight ?? 0));

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
              return (
                <div
                  key={i}
                  className="flex items-center justify-between bg-[#14141f] rounded-lg p-3 border border-[#2a2a3a]"
                >
                  <Link
                    href={`/people/${otherSlug}`}
                    className="text-sm text-[#f59e0b] hover:text-[#fbbf24] transition-colors"
                  >
                    {otherSlug}
                  </Link>
                  <div className="flex items-center gap-3 text-xs text-[#8888a0]">
                    {c.weight && (
                      <a
                        href={`https://arxiv.org/search/?searchtype=author&query=${encodeURIComponent(otherSlug.replace(/-/g, " "))}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-[#6366f1] font-mono hover:text-[#818cf8] transition-colors"
                      >
                        {c.weight} 篇
                      </a>
                    )}
                    {c.period && <span>{c.period}</span>}
                  </div>
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
              const displayName = collab.person || (collab as { name?: string }).name || "";
              const searchName = (collab.person || (collab as { name?: string }).name || "").replace(/-/g, " ");
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
                  <div className="flex items-center gap-2 text-xs text-[#8888a0]">
                    {collab.papers_count && (
                      <a
                        href={`https://arxiv.org/search/?searchtype=author&query=${encodeURIComponent(searchName)}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-[#6366f1] hover:text-[#818cf8] transition-colors"
                      >
                        {collab.papers_count} 篇
                      </a>
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
              </div>
            );
            })}
          </div>
        </section>
      )}

      {/* Publications */}
      {(person as any).publications?.length > 0 && (
        <section className="mb-8" id="publications">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">
            论文（{(person as any).publications.length}）
          </h2>
          <div className="space-y-2">
            {(person as any).publications.map(
              (
                pub: {
                  id: string;
                  title: string;
                  year: number;
                  coauthors?: string[];
                  doi?: string;
                },
                i: number
              ) => (
                <div
                  key={pub.id || i}
                  className="bg-[#14141f] rounded-lg p-3 border border-[#2a2a3a] group"
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
                                    {c}
                                  </Link>
                                ) : (
                                  <span>{c}</span>
                                )}
                              </span>
                            );
                          })}
                        </div>
                      )}
                    </div>
                    <div className="flex items-center gap-2 shrink-0">
                      <span className="text-xs font-mono text-[#6366f1]">
                        {pub.year}
                      </span>
                      <a
                        href={`https://arxiv.org/abs/${pub.id}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-[10px] text-[#8888a0] hover:text-[#e8e8f0] font-mono"
                      >
                        {pub.id}
                      </a>
                    </div>
                  </div>
                </div>
              )
            )}
          </div>
        </section>
      )}

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
