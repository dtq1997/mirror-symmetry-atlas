import { getAllProblems } from "@/lib/data";
import { notFound } from "next/navigation";
import Link from "@/components/shared/AtlasLink";
import MathText from "@/components/shared/MathText";
import { problemStatus } from "@/lib/problems";
import { publicationUrl } from "@/lib/paper-identity";
import { publicSourceUrl } from "@/lib/source-url";

export function generateStaticParams() {
  return getAllProblems().map(problem => ({ slug: problem.slug }));
}

export default async function ProblemPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const problem = getAllProblems().find(p => p.slug === slug);
  if (!problem) notFound();
  const status = problemStatus(problem);
  return <div className="max-w-4xl mx-auto px-6 py-10 w-full break-words">
    <Link href="/problems" className="text-sm text-[#818cf8] hover:underline">← 问题与进展</Link>
    <h1 className="text-2xl font-bold mt-6 mb-2">{problem.name.zh || problem.name.en}</h1>
    {problem.name.zh && <p className="text-sm text-[#aaaac0] mb-4">{problem.name.en}</p>}
    <div className="flex flex-wrap gap-4 text-sm mb-4">
      <span style={{ color: status.color }}>{status.label}</span>
      {problem.year_proposed && <span className="text-[#aaaac0]">提出年份：{problem.year_proposed}</span>}
      {problem.reviewed_on && <span className="text-[#aaaac0]">本页核对：{problem.reviewed_on}</span>}
    </div>
    <p className="text-sm text-[#aaaac0] leading-relaxed mb-8">{problem.status_note || "当前状态待核对。"}</p>
    {problem.description && <section className="mb-8">
      <h2 className="text-lg font-semibold mb-3">问题与适用范围</h2>
      <MathText className="bg-[#14141f] border border-[#2a2a3a] rounded-xl p-5 text-sm leading-relaxed">{problem.description}</MathText>
    </section>}
    <section className="mb-8">
      <h2 className="text-lg font-semibold mb-3">文献进展</h2>
      <ol className="space-y-4">
        {problem.progress.map((entry, index) => <li key={index} className="border-l-2 border-[#6366f1]/50 pl-4">
          <p className="text-sm text-[#818cf8] mb-2">{entry.date}</p>
          <MathText className="text-sm text-[#e8e8f0] leading-relaxed">{entry.description}</MathText>
          <div className="flex flex-wrap gap-3 mt-2 text-xs text-[#818cf8]">
            {entry.papers.map(id => {
              const url = publicationUrl({ id });
              return url ? <a key={id} href={url} target="_blank" rel="noopener noreferrer" className="hover:underline">{id} ↗</a>
                : <span key={id}>{id}（链接待核）</span>;
            })}
          </div>
        </li>)}
      </ol>
    </section>
    {(problem.current_approaches?.length ?? 0) > 0 && <section className="mb-8">
      <h2 className="text-lg font-semibold mb-3">相关方法及限制</h2>
      <ul className="list-disc pl-5 space-y-2 text-sm text-[#aaaac0]">
        {problem.current_approaches!.map((approach, index) => <li key={index}><MathText>{approach}</MathText></li>)}
      </ul>
    </section>}
    {problem.notes && <MathText className="text-sm text-[#aaaac0] mb-8 leading-relaxed">{problem.notes}</MathText>}
    <section className="mb-8 border border-[#2a2a3a] rounded-xl p-5">
      <h2 className="text-lg font-semibold mb-3">核对范围与来源</h2>
      <p className="text-sm text-[#aaaac0] leading-relaxed mb-4">{problem.review_note || "本条尚未完成逐项来源核对。"}</p>
      <ul className="space-y-3 text-sm text-[#818cf8]">
        {problem.sources?.map((source, index) => <li key={index}>
          {publicSourceUrl(source.url) ? <a href={publicSourceUrl(source.url)} target="_blank" rel="noopener noreferrer" className="hover:underline">{source.label} ↗</a>
            : <span>{source.label}（链接待补）</span>}
        </li>)}
      </ul>
    </section>
    <ReferenceGroup title="前置概念" kind="concepts" slugs={problem.prerequisites} />
    <ReferenceGroup title="相关问题" kind="problems" slugs={problem.related_problems} />
    <ReferenceGroup title="本站关联人物（不是完整作者名单）" kind="people" slugs={problem.key_people} />
  </div>;
}

function ReferenceGroup({ title, kind, slugs }: { title: string; kind: string; slugs: string[] }) {
  if (!slugs.length) return null;
  return <section className="mb-6">
    <h2 className="text-sm text-[#aaaac0] mb-3">{title}</h2>
    <div className="flex flex-wrap gap-3 text-sm text-[#818cf8]">
      {slugs.map(slug => <Link key={slug} href={`/${kind}/${slug}`} className="hover:underline">{slug}</Link>)}
    </div>
  </section>;
}
