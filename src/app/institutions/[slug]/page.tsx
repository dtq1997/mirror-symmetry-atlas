import { getAllInstitutions, getInstitutionsMap, getPeopleMap, getConceptsMap } from "@/lib/data";
import Link from "@/components/shared/AtlasLink";
import { notFound } from "next/navigation";
import { relevanceLabel } from "@/lib/inst";
import { recordedAffiliations } from "@/lib/institution-affiliations";
import { publicSourceUrl } from "@/lib/source-url";
import InstitutionPeople from "@/components/institution/InstitutionPeople";

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
  const records = recordedAffiliations(inst, [...peopleMap.values()]);
  const concepts = getConceptsMap();

  return (
    <div className="max-w-4xl mx-auto px-6 py-10 w-full min-w-0 break-words">
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
            {relevanceLabel(inst.relevance)}
          </span>
        </div>
      </div>

      <p className="text-sm text-[#a0a0b8] mb-6">机构资料正在逐项核对，已核对的字段见所附来源；旧名单和履历不能直接作为现任名单。</p>

      <InstitutionPeople records={records} />

      {/* Research groups */}
      {inst.research_groups && inst.research_groups.length > 0 && (
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">研究分组记录（待核实）</h2>
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
                        {concepts.get(t)?.name.zh || concepts.get(t)?.name.en || t}
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Events */}
      {inst.events && inst.events.length > 0 && (
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">重要事件</h2>
          <div className="space-y-2">
            {[...inst.events].sort((a, b) => (a.year ?? 0) - (b.year ?? 0)).map((e, i) => (
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
      {(inst.sources?.length ?? 0) > 0 && <section className="mb-8">
        <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">资料来源</h2>
        <ul className="space-y-2 text-sm">
          {inst.sources!.map((source, index) => <li key={index}>
            {publicSourceUrl(source.url) ? <a href={publicSourceUrl(source.url)} target="_blank" rel="noopener noreferrer" className="text-[#818cf8] hover:underline">{source.label} ↗</a> : <span>{source.label}（链接待补）</span>}
          </li>)}
        </ul>
      </section>}
      {publicSourceUrl(inst.url) && (
        <section className="mb-8">
          <a
            href={publicSourceUrl(inst.url)}
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
