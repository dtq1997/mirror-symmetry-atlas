import { getAllInstitutions, getInstitutionsMap, getPeopleMap } from "@/lib/data";
import Link from "next/link";
import { notFound } from "next/navigation";

export function generateStaticParams() {
  return getAllInstitutions().map((i) => ({ slug: i.slug }));
}

export default async function InstitutionPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const inst = getInstitutionsMap().get(slug);
  if (!inst) notFound();

  const peopleMap = getPeopleMap();
  const personName = (s: string): string => {
    const p = peopleMap.get(s);
    return p ? p.name.zh || p.name.en : s;
  };

  // Gather all people whose career_timeline references this institution
  const affiliated = new Set<string>();
  const pastAffiliated = new Set<string>();
  for (const p of peopleMap.values()) {
    for (const e of p.career_timeline || []) {
      if (e.institution !== slug) continue;
      const period = e.period || "";
      const isPresent =
        period.toLowerCase().includes("present") || period.endsWith("-");
      if (isPresent || e.type === "position") {
        if (isPresent) affiliated.add(p.slug);
        else pastAffiliated.add(p.slug);
      } else {
        pastAffiliated.add(p.slug);
      }
    }
  }
  // Unify with research_groups members
  for (const g of inst.research_groups || []) {
    for (const m of g.current_members || []) affiliated.add(m);
    for (const m of g.past_members || []) {
      if (!affiliated.has(m)) pastAffiliated.add(m);
    }
  }
  // Remove overlap
  for (const s of affiliated) pastAffiliated.delete(s);

  const currentList = Array.from(affiliated).sort();
  const pastList = Array.from(pastAffiliated).sort();

  return (
    <div className="max-w-4xl mx-auto px-6 py-10 w-full">
      {/* Breadcrumb */}
      <div className="text-sm text-[#8888a0] mb-6">
        <Link href="/institutions" className="hover:text-[#e8e8f0] transition-colors">
          机构
        </Link>
        <span className="mx-2">/</span>
        <span className="text-[#e8e8f0]">{inst.name.zh || inst.name.en}</span>
      </div>

      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-[#e8e8f0] mb-1">
          {inst.name.zh || inst.name.en}
        </h1>
        {inst.name.zh && (
          <p className="text-lg text-[#8888a0]">{inst.name.en}</p>
        )}
        {inst.name.local && (
          <p className="text-sm text-[#8888a0] italic">{inst.name.local}</p>
        )}
        <div className="flex flex-wrap gap-4 mt-3 text-sm text-[#8888a0]">
          <span>
            {inst.city}, {inst.country}
          </span>
          {inst.founded && <span>成立 {inst.founded}</span>}
          <span
            className={`px-2 py-0.5 text-xs rounded-full ${
              inst.relevance === "high"
                ? "bg-[#8b5cf6]/25 text-[#a78bfa]"
                : inst.relevance === "medium"
                  ? "bg-[#6366f1]/15 text-[#818cf8]"
                  : "bg-[#2a2a3a] text-[#8888a0]"
            }`}
          >
            relevance: {inst.relevance}
          </span>
        </div>
      </div>

      {/* Research groups */}
      {inst.research_groups && inst.research_groups.length > 0 && (
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">研究方向</h2>
          <div className="space-y-4">
            {inst.research_groups.map((g, i) => (
              <div
                key={i}
                className="bg-[#14141f] rounded-xl p-5 border border-[#2a2a3a]"
              >
                <h3 className="text-sm font-medium text-[#e8e8f0] mb-2">
                  {g.name}
                </h3>
                {g.topics && g.topics.length > 0 && (
                  <div className="flex flex-wrap gap-2">
                    {g.topics.map((t) => (
                      <Link
                        key={t}
                        href={`/concepts/${t}`}
                        className="px-2 py-0.5 text-xs rounded bg-[#6366f1]/15 text-[#818cf8] hover:bg-[#6366f1]/25 transition-colors"
                      >
                        {t}
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Current members */}
      {currentList.length > 0 && (
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">
            现任成员（{currentList.length}）
          </h2>
          <div className="flex flex-wrap gap-2">
            {currentList.map((s) => (
              <Link
                key={s}
                href={`/people/${s}`}
                className="px-3 py-1 text-sm rounded-full bg-[#f59e0b]/15 text-[#fbbf24] hover:bg-[#f59e0b]/25 transition-colors"
              >
                {personName(s)}
              </Link>
            ))}
          </div>
        </section>
      )}

      {/* Past members */}
      {pastList.length > 0 && (
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">
            过往成员（{pastList.length}）
          </h2>
          <div className="flex flex-wrap gap-2">
            {pastList.map((s) => (
              <Link
                key={s}
                href={`/people/${s}`}
                className="px-3 py-1 text-sm rounded-full bg-[#2a2a3a] text-[#a0a0b8] hover:bg-[#3a3a4a] hover:text-[#e8e8f0] transition-colors"
              >
                {personName(s)}
              </Link>
            ))}
          </div>
        </section>
      )}

      {/* Events */}
      {inst.events && inst.events.length > 0 && (
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">重要事件</h2>
          <div className="space-y-2">
            {inst.events.map((e, i) => (
              <div
                key={i}
                className="bg-[#14141f] rounded-lg p-3 border border-[#2a2a3a] flex gap-4"
              >
                <span className="text-[#6366f1] font-mono text-sm shrink-0">
                  {e.year}
                </span>
                <span className="text-sm text-[#e8e8f0]">{e.description}</span>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Notes */}
      {inst.notes && (
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">备注</h2>
          <div className="bg-[#14141f] rounded-xl p-5 border border-[#2a2a3a] text-sm text-[#e8e8f0] leading-relaxed whitespace-pre-line">
            {inst.notes}
          </div>
        </section>
      )}

      {/* External link */}
      {inst.url && (
        <section className="mb-8">
          <a
            href={inst.url}
            target="_blank"
            rel="noopener noreferrer"
            className="px-4 py-2 text-sm bg-[#14141f] rounded-lg border border-[#2a2a3a] text-[#6366f1] hover:bg-[#2a2a3a] transition-colors inline-block"
          >
            官方主页 ↗
          </a>
        </section>
      )}
    </div>
  );
}
