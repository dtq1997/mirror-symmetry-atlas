import { getAllTimelineEvents } from "@/lib/data";
import Link from "@/components/shared/AtlasLink";
import MathText from "@/components/shared/MathText";
import { sortTimelineEvents } from "@/lib/timeline";
import { publicSourceUrl } from "@/lib/source-url";
import { publicationUrl } from "@/lib/paper-identity";
import type { TimelineEvent } from "@/lib/types";

const ERA_LABELS: Record<string, { label: string; color: string }> = {
  prehistory: { label: "史前", color: "#8888a0" },
  classical: { label: "经典", color: "#3b82f6" },
  modern: { label: "现代", color: "#a855f7" },
  contemporary: { label: "当代", color: "#10b981" },
};

const IMPORTANCE_STYLES: Record<string, string> = {
  milestone: "border-l-4 border-l-[#f59e0b]",
  major: "border-l-4 border-l-[#6366f1]",
  notable: "border-l-4 border-l-[#2a2a3a]",
};

export default function TimelinePage() {
  const events = getAllTimelineEvents();
  const sorted = sortTimelineEvents(events);

  // Group by era
  const eras = ["prehistory", "classical", "modern", "contemporary"];
  const grouped = eras
    .map((era) => ({
      era,
      ...ERA_LABELS[era],
      events: sorted.filter((e) => e.era === era),
    }))
    .filter((g) => g.events.length > 0);

  return (
    <div className="max-w-4xl mx-auto px-6 py-10 w-full">
      <h1 className="text-2xl font-bold text-[#e8e8f0] mb-2">领域时间线</h1>
      <p className="text-[#8888a0] mb-3">
        镜像对称及相关领域的历史选录（{events.length} 个事件）
      </p>
      <p className="text-xs text-[#8888a0] leading-relaxed mb-8">
        每条注明日期依据与来源；讲座、预印本提交、期刊出版和获奖公告分别记载。
        仅知年份或月份的条目排在同年或同月的精确日期之前，不代表实际先后。
        重要程度是本站的编辑分类，选录不代表完整领域史。
      </p>

      {/* Legend */}
      <div className="flex gap-4 mb-8 text-xs">
        <span className="flex items-center gap-1">
          <span className="w-3 h-3 bg-[#f59e0b] rounded-sm" /> 里程碑
        </span>
        <span className="flex items-center gap-1">
          <span className="w-3 h-3 bg-[#6366f1] rounded-sm" /> 重要
        </span>
        <span className="flex items-center gap-1">
          <span className="w-3 h-3 bg-[#2a2a3a] rounded-sm" /> 值得注意
        </span>
      </div>

      {grouped.map((group) => (
        <section key={group.era} className="mb-10">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <span
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: group.color }}
            />
            <span style={{ color: group.color }}>{group.label}</span>
          </h2>

          <div className="relative">
            {/* Vertical line */}
            <div aria-hidden="true" className="absolute left-[6px] sm:left-[118px] top-0 bottom-0 w-px bg-[#2a2a3a]" />

            <div className="space-y-4">
              {group.events.map((event) => (
                <TimelineEventCard key={event.slug} event={event} />
              ))}
            </div>
          </div>
        </section>
      ))}
    </div>
  );
}

function TimelineEventCard({ event }: { event: TimelineEvent }) {
  return (
  <article
    id={event.slug}
    className="relative grid grid-cols-[12px_minmax(0,1fr)] sm:grid-cols-[96px_12px_minmax(0,1fr)] gap-x-4 scroll-mt-6"
  >
    {/* Date */}
    <div className="col-start-2 sm:col-start-1 row-start-1 sm:text-right pb-2 sm:pb-0">
      <time dateTime={event.date} className="text-sm font-mono text-[#818cf8] whitespace-nowrap">
        {event.date}
      </time>
    </div>

    {/* Dot */}
    <div aria-hidden="true" className="relative col-start-1 sm:col-start-2 row-start-1 row-span-2">
      <div
        className="w-3 h-3 rounded-full mt-1.5 relative z-10"
        style={{
          backgroundColor:
            event.importance === "milestone"
              ? "#f59e0b"
              : event.importance === "major"
                ? "#6366f1"
                : "#8888a0",
        }}
      />
    </div>

    {/* Content */}
    <div className={`col-start-2 sm:col-start-3 row-start-2 sm:row-start-1 bg-[#14141f] rounded-lg p-4 border border-[#2a2a3a] min-w-0 break-words ${IMPORTANCE_STYLES[event.importance] || ""}`}>
      <h3 className="text-sm font-medium text-[#e8e8f0] mb-1">
        {event.title.zh || event.title.en}
      </h3>
      {event.title.zh && (
        <p className="text-xs text-[#8888a0] mb-2">
          {event.title.en}
        </p>
      )}
      {event.description && (
        <MathText className="text-sm text-[#aaaac0] leading-relaxed">
          {event.description}
        </MathText>
      )}
      {event.date_note && <p className="text-xs text-[#8888a0] mt-3 leading-relaxed">日期依据：{event.date_note}</p>}
      {/* Related entities */}
      <div className="flex flex-wrap gap-1 mt-2">
        {event.people?.map((p) => (
          <Link
            key={p}
            href={`/people/${p}`}
            className="text-[10px] px-1.5 py-0.5 rounded bg-[#f59e0b]/15 text-[#fbbf24] hover:bg-[#f59e0b]/25"
          >
            {p}
          </Link>
        ))}
        {event.concepts?.map((c) => (
          <Link
            key={c}
            href={`/concepts/${c}`}
            className="text-[10px] px-1.5 py-0.5 rounded bg-[#6366f1]/15 text-[#818cf8] hover:bg-[#6366f1]/25"
          >
            {c}
          </Link>
        ))}
        {event.papers?.map((p) => publicationUrl({ id: p }) ? (
          <a
            key={p}
            href={publicationUrl({ id: p })}
            target="_blank"
            rel="noopener noreferrer"
            className="text-[10px] px-1.5 py-0.5 rounded bg-[#10b981]/15 text-[#34d399] hover:bg-[#10b981]/25 font-mono"
          >
            {p}
          </a>
        ) : <span key={p} className="text-xs text-[#8888a0]">{p}（链接待补）</span>)}
      </div>
      <details className="mt-4 border-t border-[#2a2a3a] pt-3 text-xs leading-relaxed">
        <summary className="cursor-pointer text-[#818cf8] hover:underline">
          来源与核对范围{event.reviewed_on ? ` · ${event.reviewed_on}` : " · 待核实"}
        </summary>
        <p className="text-[#8888a0] mt-2">{event.review_note || "尚未完成逐项来源核对。"}</p>
        {!!event.sources?.length && <ul className="mt-2 space-y-2">
          {event.sources.map((source, index) => <li key={index}>
            {publicSourceUrl(source.url)
              ? <a href={publicSourceUrl(source.url)} target="_blank" rel="noopener noreferrer" className="text-[#818cf8] hover:underline">{source.label} ↗</a>
              : <span className="text-[#8888a0]">{source.label}（链接待补）</span>}
            {source.notes && <p className="text-[#8888a0]">{source.notes}</p>}
          </li>)}
        </ul>}
      </details>
    </div>
  </article>
  );
}
