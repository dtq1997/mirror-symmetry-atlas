import Link from "@/components/shared/AtlasLink";
import type { OpenProblem } from "@/lib/types";
import { problemStatus } from "@/lib/problems";

export default function ProblemCards({ problems }: { problems: OpenProblem[] }) {
  return <div className="space-y-3">
    {problems.map(problem => {
      const status = problemStatus(problem);
      return <Link key={problem.slug} href={`/problems/${problem.slug}`}
        className="block bg-[#14141f] rounded-lg p-4 border border-[#2a2a3a] hover:border-[#6366f1] transition-colors">
        <div className="flex items-start justify-between gap-3">
          <span className="text-sm font-medium text-[#e8e8f0]">{problem.name.zh || problem.name.en}</span>
          <span className="shrink-0 text-xs" style={{ color: status.color }}>{status.label}</span>
        </div>
        <p className="text-xs text-[#aaaac0] mt-2 leading-relaxed">{problem.status_note || "本条状态尚未完成来源核对。"}</p>
        <div className="text-xs text-[#818cf8] mt-3">查看条件、进展与来源 →</div>
      </Link>;
    })}
  </div>;
}
