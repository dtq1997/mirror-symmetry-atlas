import { getAllInstitutions, getAllPeople } from "@/lib/data";
import Link from "next/link";

export default function InstitutionsPage() {
  const institutions = getAllInstitutions();
  const people = getAllPeople();

  // Count affiliated people per institution
  const memberCount = new Map<string, Set<string>>();
  for (const inst of institutions) {
    const s = new Set<string>();
    for (const g of inst.research_groups || []) {
      for (const m of g.current_members || []) s.add(m);
    }
    memberCount.set(inst.slug, s);
  }
  for (const p of people) {
    const latest = p.career_timeline
      ?.slice()
      .reverse()
      .find((e) => e.type === "position" && e.institution);
    if (!latest?.institution) continue;
    const set = memberCount.get(latest.institution);
    if (set) set.add(p.slug);
  }

  const relevanceRank: Record<string, number> = { high: 0, medium: 1, low: 2 };
  const sorted = institutions.slice().sort((a, b) => {
    const ra = relevanceRank[a.relevance] ?? 3;
    const rb = relevanceRank[b.relevance] ?? 3;
    if (ra !== rb) return ra - rb;
    return (memberCount.get(b.slug)?.size ?? 0) - (memberCount.get(a.slug)?.size ?? 0);
  });

  return (
    <div className="max-w-4xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-bold text-[#e8e8f0] mb-2">机构</h1>
      <p className="text-sm text-[#8888a0] mb-6">{institutions.length} 所机构，按相关度排序</p>
      <div className="grid sm:grid-cols-2 gap-4">
        {sorted.map((inst) => {
          const n = memberCount.get(inst.slug)?.size ?? 0;
          return (
            <Link
              key={inst.slug}
              href={`/institutions/${inst.slug}`}
              className="bg-[#14141f] rounded-xl p-5 border border-[#2a2a3a] hover:border-[#8b5cf6]/50 transition-colors"
            >
              <h2 className="text-base font-semibold text-[#e8e8f0]">
                {inst.name.zh || inst.name.en}
              </h2>
              <p className="text-sm text-[#8888a0]">{inst.name.en}</p>
              <div className="flex items-center justify-between mt-2 text-xs text-[#8888a0]">
                <span>{inst.city}, {inst.country}</span>
                <div className="flex gap-2">
                  {n > 0 && <span className="text-[#f59e0b]">{n} 人</span>}
                  <span
                    className={
                      inst.relevance === "high"
                        ? "text-[#a78bfa]"
                        : inst.relevance === "medium"
                          ? "text-[#818cf8]"
                          : "text-[#8888a0]"
                    }
                  >
                    {inst.relevance}
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
