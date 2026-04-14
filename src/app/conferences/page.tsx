import { getAllConferenceEvents } from "@/lib/data";
import Link from "next/link";

export default function ConferencesPage() {
  const events = getAllConferenceEvents();

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
                        {s}
                      </Link>
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
