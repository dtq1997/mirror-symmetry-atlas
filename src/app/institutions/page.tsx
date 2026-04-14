import { getAllInstitutions } from "@/lib/data";
import Link from "next/link";

export default function InstitutionsPage() {
  const institutions = getAllInstitutions();

  return (
    <div className="max-w-4xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-bold text-[#e8e8f0] mb-4">机构</h1>
      <div className="grid sm:grid-cols-2 gap-4">
        {institutions.map((inst) => (
          <Link
            key={inst.slug}
            href={`/institutions/${inst.slug}`}
            className="bg-[#14141f] rounded-xl p-5 border border-[#2a2a3a] hover:border-[#8b5cf6]/50 transition-colors"
          >
            <h2 className="text-base font-semibold text-[#e8e8f0]">
              {inst.name.zh || inst.name.en}
            </h2>
            <p className="text-sm text-[#8888a0]">{inst.name.en}</p>
            <div className="flex gap-2 mt-2 text-xs text-[#8888a0]">
              <span>{inst.city}, {inst.country}</span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
