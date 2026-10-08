import Link from "@/components/shared/AtlasLink";
import { displayName } from "@/lib/name";
import { publicSourceUrl } from "@/lib/source-url";
import type { RecordedAffiliation } from "@/lib/institution-affiliations";

const careerLabels: Record<string, string> = { education: "求学", position: "任职", visit: "访问" };

export default function InstitutionPeople({ records }: { records: RecordedAffiliation[] }) {
  const checked = records.flatMap((r) => r.appointmentChecks);
  return (
    <>
      <section className="mb-8" id="appointment-checks">
        <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">任职来源核对</h2>
        <p className="text-sm text-[#a0a0b8] mb-3">
          {checked.length ? "以下仅列已核对的任职及核对日期，不是机构完整人员名单；后续变动仍需核实。" :
            "本机构尚未录入逐项核对的任职来源；下方历史记录不代表现任名单。"}
        </p>
        <div className="space-y-3">
          {checked.map((c, index) => (
            <div key={`${c.person}:${c.checked_on}:${index}`} className="bg-[#14141f] border border-[#2a2a3a] rounded-xl p-4">
              <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
                <Link href={`/people/${c.person}`} className="text-[#fbbf24] hover:underline">{displayName(c.person)}</Link>
                <span className="text-sm text-[#e8e8f0]">{c.role}</span>
              </div>
              <div className="flex flex-wrap gap-x-3 gap-y-1 text-xs mt-2 text-[#a0a0b8]">
                <span>核对日期：{c.checked_on}</span>
                {publicSourceUrl(c.source.url) && <a href={publicSourceUrl(c.source.url)} target="_blank" rel="noopener noreferrer" className="text-[#818cf8] hover:underline">{c.source.label} ↗</a>}
              </div>
            </div>
          ))}
        </div>
      </section>
      <section className="mb-8" id="recorded-affiliations">
        <h2 className="text-lg font-semibold text-[#e8e8f0] mb-3">本站关联记录（{records.length} 人）</h2>
        <p className="text-sm text-[#a0a0b8] mb-3">按已有档案列出求学、任职、访问和组别记录，尚未逐项核实。时段沿用原记载，“至今”也不自动视为当前仍在任。</p>
        {records.length === 0 && <p className="text-sm text-[#8888a0]">暂无关联记录。</p>}
        <div className="space-y-3">
          {records.map((r) => (
            <div key={r.person} className="bg-[#14141f] border border-[#2a2a3a] rounded-xl p-4">
              <Link href={`/people/${r.person}`} className="text-[#a78bfa] hover:underline">{displayName(r.person)}</Link>
              {r.career.length > 0 && <ul className="mt-2 space-y-1 text-sm text-[#a0a0b8]">
                {r.career.map((c, index) => <li key={index} className="break-words">
                  {careerLabels[c.type]} · {c.period || "时期待核实"}{c.role ? ` · ${c.role}` : ""}
                </li>)}
              </ul>}
              {r.groupClaims.length > 0 && <details className="mt-2 text-xs text-[#8888a0]">
                <summary className="cursor-pointer hover:text-[#c4b5fd]">组别旧记录（归属及时段待核实）</summary>
                <ul className="mt-2 space-y-1">
                  {r.groupClaims.map((g, index) => <li key={index}>
                    {g.group}：原记为“{g.recordedAs === "current" ? "现任" : "过往"}”，记载时点未核。
                  </li>)}
                </ul>
              </details>}
            </div>
          ))}
        </div>
      </section>
    </>
  );
}
