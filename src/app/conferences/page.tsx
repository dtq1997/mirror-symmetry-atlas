import { getAllConferenceEvents, getPeopleMap, getInstitutionsMap } from "@/lib/data";
import Link from "next/link";

export default function ConferencesPage() {
  const events = getAllConferenceEvents().slice().sort((a, b) =>
    b.date_start.localeCompare(a.date_start)
  );
  const peopleMap = getPeopleMap();
  const institutionsMap = getInstitutionsMap();

  const displayName = (slug: string): string => {
    const p = peopleMap.get(slug);
    if (!p) return slug;
    return p.name.zh || p.name.en;
  };

  const groupByInstitution = (slugs: string[]): Array<{ inst: string; members: string[] }> => {
    const groups = new Map<string, string[]>();
    for (const slug of slugs) {
      const p = peopleMap.get(slug);
      const latest = p?.career_timeline
        ?.slice()
        .reverse()
        .find((e) => (e.type === "position" || e.type === "education") && e.institution);
      const key = latest?.institution || "_unknown";
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key)!.push(slug);
    }
    return Array.from(groups.entries())
      .map(([inst, members]) => ({
        inst,
        members,
      }))
      .sort((a, b) => b.members.length - a.members.length);
  };

  const institutionLabel = (slug: string): string => {
    if (slug === "_unknown") return "其他";
    const inst = institutionsMap.get(slug);
    return inst?.name.zh || inst?.name.en || slug;
  };

  return (
    <div className="max-w-4xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-bold text-[#e8e8f0] mb-2">学术会议</h1>
      <p className="text-[#8888a0] mb-8">
        聚焦国内，{events.length} 个会议
      </p>

      {events.length === 0 ? (
        <p className="text-[#8888a0]">暂无会议数据</p>
      ) : (
        <div className="space-y-6">
          {events.map((evt) => (
            <div
              key={evt.slug}
              className="bg-[#14141f] rounded-xl border border-[#2a2a3a] overflow-hidden"
            >
              {/* Header */}
              <div className="p-5 border-b border-[#2a2a3a]">
                <h2 className="text-lg font-semibold text-[#e8e8f0]">
                  {evt.name.zh || evt.name.en}
                </h2>
                {evt.name.zh && (
                  <p className="text-sm text-[#8888a0]">{evt.name.en}</p>
                )}
                <div className="flex flex-wrap gap-4 mt-2 text-sm text-[#8888a0]">
                  <span className="text-[#6366f1] font-mono">
                    {evt.date_start}
                    {evt.date_end ? ` ~ ${evt.date_end}` : ""}
                  </span>
                  {evt.location && <span>{evt.location}</span>}
                  {evt.institution && (
                    <Link
                      href={`/institutions/${evt.institution}`}
                      className="text-[#a78bfa] hover:text-[#c4b5fd] transition-colors"
                    >
                      {institutionLabel(evt.institution)}
                    </Link>
                  )}
                </div>
              </div>

              {/* Speakers */}
              {evt.invited_speakers && evt.invited_speakers.length > 0 && (
                <div className="p-5 border-b border-[#2a2a3a]">
                  <h3 className="text-sm font-medium text-[#8888a0] mb-3">
                    邀请报告人（{evt.invited_speakers.length}）
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {evt.invited_speakers.map((s) => (
                      <Link
                        key={s}
                        href={`/people/${s}`}
                        className="px-2 py-1 text-xs rounded bg-[#f59e0b]/15 text-[#fbbf24] hover:bg-[#f59e0b]/25 transition-colors"
                      >
                        {displayName(s)}
                      </Link>
                    ))}
                  </div>
                </div>
              )}

              {/* Attendees — grouped by institution */}
              {evt.attendees && evt.attendees.length > 0 && (
                <div className="p-5 border-b border-[#2a2a3a]">
                  <h3 className="text-sm font-medium text-[#8888a0] mb-3">
                    全体参会人员（{evt.attendees.length}）
                  </h3>
                  <div className="space-y-3">
                    {groupByInstitution(evt.attendees).map(({ inst, members }) => (
                      <div key={inst} className="flex flex-wrap items-baseline gap-2">
                        <span className="text-xs text-[#6366f1] font-medium min-w-[5rem]">
                          {institutionLabel(inst)}（{members.length}）
                        </span>
                        <div className="flex flex-wrap gap-1.5">
                          {members.map((s) => (
                            <Link
                              key={s}
                              href={`/people/${s}`}
                              className="px-2 py-0.5 text-xs rounded bg-[#2a2a3a] text-[#a0a0b8] hover:bg-[#3a3a4a] hover:text-[#e8e8f0] transition-colors"
                            >
                              {displayName(s)}
                            </Link>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Topics */}
              {evt.topics && evt.topics.length > 0 && (
                <div className="p-5 border-b border-[#2a2a3a]">
                  <h3 className="text-sm font-medium text-[#8888a0] mb-3">
                    主题
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {evt.topics.map((t) => (
                      <Link
                        key={t}
                        href={`/concepts/${t}`}
                        className="px-2 py-1 text-xs rounded bg-[#6366f1]/15 text-[#818cf8] hover:bg-[#6366f1]/25 transition-colors"
                      >
                        {t}
                      </Link>
                    ))}
                  </div>
                </div>
              )}

              {/* Notes */}
              {evt.notes && (
                <div className="p-5">
                  <pre className="text-xs text-[#8888a0] whitespace-pre-wrap leading-relaxed">
                    {evt.notes}
                  </pre>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
