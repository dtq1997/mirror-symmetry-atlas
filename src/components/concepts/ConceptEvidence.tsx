import type { Concept } from "@/lib/types";
import MathText from "@/components/shared/MathText";
import { publicSourceUrl } from "@/lib/source-url";

export default function ConceptEvidence({ concept }: { concept: Concept }) {
  return <>
    {concept.history_note && <section className="mb-8">
      <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">历史与文献</h2>
      <MathText className="text-sm text-[#aaaac0] leading-relaxed">{concept.history_note}</MathText>
    </section>}
    <section className="mb-8 rounded-xl border border-[#2a2a3a] p-5">
      <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">核对范围与来源</h2>
      <p className="text-sm text-[#aaaac0] leading-relaxed mb-3">
        {concept.review_note || "本条内容尚未完成逐项来源核对。已有论文链接不表示定义、年代、贡献与图中关系均已核实。"}
      </p>
      {(concept.sources?.length ?? 0) > 0 && <ul className="space-y-2 text-sm break-words">
        {concept.sources!.map((source, index) => <li key={index}>
          {publicSourceUrl(source.url)
            ? <a href={publicSourceUrl(source.url)} target="_blank" rel="noopener noreferrer" className="text-[#818cf8] hover:underline">{source.label} ↗</a>
            : <span className="text-[#aaaac0]">{source.label}（链接待补）</span>}
        </li>)}
      </ul>}
    </section>
  </>;
}
