import { getAllConcepts } from "@/lib/data";
import Link from "next/link";
import { notFound } from "next/navigation";
import MathText from "@/components/shared/MathText";

const DIFFICULTY_COLORS: Record<string, string> = {
  introductory: "#22c55e",
  intermediate: "#3b82f6",
  advanced: "#a855f7",
  "research-frontier": "#ef4444",
};
const DIFFICULTY_LABELS: Record<string, string> = {
  introductory: "入门",
  intermediate: "中级",
  advanced: "进阶",
  "research-frontier": "前沿",
};

export function generateStaticParams() {
  return getAllConcepts().map((c) => ({ slug: c.slug }));
}

export default async function ConceptPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const concepts = getAllConcepts();
  const concept = concepts.find((c) => c.slug === slug);
  if (!concept) notFound();

  const diffColor = DIFFICULTY_COLORS[concept.difficulty] || "#6366f1";

  return (
    <div className="max-w-4xl mx-auto px-6 py-10 w-full">
      {/* Breadcrumb */}
      <div className="text-sm text-[#8888a0] mb-6">
        <Link
          href="/concepts"
          className="hover:text-[#e8e8f0] transition-colors"
        >
          概念
        </Link>
        <span className="mx-2">/</span>
        <span className="text-[#e8e8f0]">{concept.name.en}</span>
      </div>

      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-[#e8e8f0] mb-1">
          {concept.name.en}
        </h1>
        {concept.name.zh && (
          <p className="text-xl text-[#8888a0]">{concept.name.zh}</p>
        )}
        {concept.aliases && concept.aliases.length > 0 && (
          <p className="text-sm text-[#8888a0] mt-1">
            又名：{concept.aliases.join(", ")}
          </p>
        )}
        <div className="flex items-center gap-3 mt-3">
          <span
            className="px-2 py-0.5 text-xs rounded-full"
            style={{
              backgroundColor: `${diffColor}20`,
              color: diffColor,
            }}
          >
            {DIFFICULTY_LABELS[concept.difficulty]}
          </span>
          {concept.category && (
            <span className="text-xs text-[#8888a0]">{concept.category}</span>
          )}
          {concept.discipline && (
            <span className="text-xs text-[#8888a0]">{concept.discipline}</span>
          )}
          {concept.year_introduced && (
            <span className="text-xs text-[#6366f1]">
              {concept.year_introduced} 年引入
            </span>
          )}
        </div>
      </div>

      {/* Definition */}
      {concept.definition && (
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">定义</h2>
          <MathText className="bg-[#14141f] rounded-xl p-5 border border-[#2a2a3a] text-sm text-[#e8e8f0] leading-relaxed">
            {concept.definition}
          </MathText>
        </section>
      )}

      {/* Dependencies */}
      <div className="grid md:grid-cols-2 gap-4 mb-8">
        {concept.prerequisites?.length > 0 && (
          <div className="bg-[#14141f] rounded-xl p-5 border border-[#2a2a3a]">
            <h3 className="text-sm font-medium text-[#8888a0] mb-3">
              前置概念
            </h3>
            <div className="flex flex-wrap gap-2">
              {concept.prerequisites.map((p) => (
                <Link
                  key={p}
                  href={`/concepts/${p}`}
                  className="px-3 py-1 text-sm rounded-full bg-[#ef4444]/15 text-[#f87171] border border-[#ef4444]/30 hover:bg-[#ef4444]/25 transition-colors"
                >
                  {p}
                </Link>
              ))}
            </div>
          </div>
        )}

        {concept.leads_to?.length > 0 && (
          <div className="bg-[#14141f] rounded-xl p-5 border border-[#2a2a3a]">
            <h3 className="text-sm font-medium text-[#8888a0] mb-3">
              后续概念
            </h3>
            <div className="flex flex-wrap gap-2">
              {concept.leads_to.map((l) => (
                <Link
                  key={l}
                  href={`/concepts/${l}`}
                  className="px-3 py-1 text-sm rounded-full bg-[#6366f1]/15 text-[#818cf8] border border-[#6366f1]/30 hover:bg-[#6366f1]/25 transition-colors"
                >
                  {l}
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>

      {concept.related?.length > 0 && (
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">
            相关概念
          </h2>
          <div className="flex flex-wrap gap-2">
            {concept.related.map((r) => (
              <Link
                key={r}
                href={`/concepts/${r}`}
                className="px-3 py-1 text-sm rounded-full bg-[#2a2a3a] text-[#8888a0] hover:text-[#e8e8f0] transition-colors"
              >
                {r}
              </Link>
            ))}
          </div>
        </section>
      )}

      {/* Contributions */}
      {concept.contributions && concept.contributions.length > 0 && (
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">
            贡献者
          </h2>
          <div className="space-y-2">
            {concept.contributions.map((ct) => (
              <div
                key={ct.person}
                className="bg-[#14141f] rounded-lg p-4 border border-[#2a2a3a] flex items-start justify-between"
              >
                <div>
                  <Link
                    href={`/people/${ct.person}`}
                    className="text-sm font-medium text-[#f59e0b] hover:text-[#fbbf24]"
                  >
                    {ct.person}
                  </Link>
                  {ct.description && (
                    <p className="text-xs text-[#8888a0] mt-1">
                      {ct.description}
                    </p>
                  )}
                </div>
                <span className="text-xs text-[#8888a0] bg-[#2a2a3a] px-2 py-0.5 rounded shrink-0 ml-3">
                  {ct.role}
                </span>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Key people */}
      {concept.key_people?.length > 0 && (
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">
            关键人物
          </h2>
          <div className="flex flex-wrap gap-2">
            {concept.key_people.map((p) => (
              <Link
                key={p}
                href={`/people/${p}`}
                className="px-3 py-1 text-sm rounded-full bg-[#f59e0b]/15 text-[#fbbf24] border border-[#f59e0b]/30 hover:bg-[#f59e0b]/25 transition-colors"
              >
                {p}
              </Link>
            ))}
          </div>
        </section>
      )}

      {/* Key papers */}
      {concept.key_papers?.length > 0 && (
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">
            关键论文
          </h2>
          <div className="flex flex-wrap gap-2">
            {concept.key_papers.map((p) => (
              <a
                key={p}
                href={`https://arxiv.org/abs/${p}`}
                target="_blank"
                rel="noopener noreferrer"
                className="px-3 py-1 text-sm rounded-full bg-[#10b981]/15 text-[#34d399] border border-[#10b981]/30 hover:bg-[#10b981]/25 transition-colors font-mono"
              >
                {p}
              </a>
            ))}
          </div>
        </section>
      )}

      {/* Dual */}
      {concept.dual_to && (
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">
            对偶概念
          </h2>
          <Link
            href={`/concepts/${concept.dual_to}`}
            className="text-[#6366f1] hover:text-[#818cf8]"
          >
            {concept.dual_to}
          </Link>
        </section>
      )}
    </div>
  );
}
