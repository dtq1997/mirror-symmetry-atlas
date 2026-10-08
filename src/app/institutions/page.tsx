import { getAllInstitutions, getAllPeople } from "@/lib/data";
import Link from "@/components/shared/AtlasLink";
import { institutionName, relevanceLabel } from "@/lib/inst";
import { recordedAffiliations } from "@/lib/institution-affiliations";

export default function InstitutionsPage() {
  const institutions = getAllInstitutions();
  const people = getAllPeople();

  const memberCount = new Map(institutions.map((inst) =>
    [inst.slug, recordedAffiliations(inst, people).length]));

  const relevanceRank: Record<string, number> = { high: 0, medium: 1, low: 2 };
  const sorted = institutions.slice().sort((a, b) => {
    const ra = relevanceRank[a.relevance] ?? 3;
    const rb = relevanceRank[b.relevance] ?? 3;
    if (ra !== rb) return ra - rb;
    return (memberCount.get(b.slug) ?? 0) - (memberCount.get(a.slug) ?? 0);
  });

  return (
    <div className="max-w-4xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-bold text-[#e8e8f0] mb-2">机构</h1>
      <p className="text-sm text-[#8888a0] mb-2">{institutions.length} 所机构，按本站收录重点排序</p>
      <p className="text-sm text-[#a0a0b8] mb-6">人数为本站求学、任职、访问及组别记录的关联人数，不是机构现任或全部人数。资料仍在逐项核对。</p>
      <div className="grid sm:grid-cols-2 gap-4">
        {sorted.map((inst) => {
          const n = memberCount.get(inst.slug) ?? 0;
          return (
            <Link
              key={inst.slug}
              href={`/institutions/${inst.slug}`}
              className="min-w-0 break-words bg-[#14141f] rounded-xl p-5 border border-[#2a2a3a] hover:border-[#8b5cf6]/50 transition-colors"
            >
              <h2 className="text-base font-semibold text-[#e8e8f0]">
                {institutionName(inst.slug)}
              </h2>
              <p className="text-sm text-[#8888a0]">{inst.name.en}</p>
              <div className="flex flex-wrap gap-2 items-center justify-between mt-2 text-xs text-[#8888a0]">
                <span>{inst.city}, {inst.country}</span>
                <div className="flex gap-2">
                  <span className="text-[#f59e0b]">本站关联 {n} 人</span>
                  <span
                    className={
                      inst.relevance === "high"
                        ? "text-[#a78bfa]"
                        : inst.relevance === "medium"
                          ? "text-[#818cf8]"
                          : "text-[#8888a0]"
                    }
                  >
                    {relevanceLabel(inst.relevance)}
                  </span>
                </div>
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
