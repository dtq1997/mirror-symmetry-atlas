import { getAllTimelineEvents } from "@/lib/data";
import Link from "next/link";

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
  const sorted = events.sort((a, b) => {
    const ya = parseInt(a.date.replace(/[^0-9]/g, "").slice(0, 4));
    const yb = parseInt(b.date.replace(/[^0-9]/g, "").slice(0, 4));
    return ya - yb;
  });

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
      <p className="text-[#8888a0] mb-8">
        镜像对称及相关领域的关键里程碑（{events.length} 个事件）
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
            <div className="absolute left-[59px] top-0 bottom-0 w-px bg-[#2a2a3a]" />

            <div className="space-y-4">
              {group.events.map((event) => (
                <div
                  key={event.slug}
                  className={`flex gap-4 ${IMPORTANCE_STYLES[event.importance] || ""}`}
                >
                  {/* Date */}
                  <div className="w-[52px] shrink-0 text-right">
                    <span className="text-sm font-mono text-[#6366f1]">
                      {event.date}
                    </span>
                  </div>

                  {/* Dot */}
                  <div className="relative">
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
                  <div className="bg-[#14141f] rounded-lg p-4 border border-[#2a2a3a] flex-1 min-w-0">
                    <h3 className="text-sm font-medium text-[#e8e8f0] mb-1">
                      {event.title.zh || event.title.en}
                    </h3>
                    {event.title.zh && (
                      <p className="text-xs text-[#8888a0] mb-2">
                        {event.title.en}
                      </p>
                    )}
                    {event.description && (
                      <p className="text-xs text-[#8888a0] leading-relaxed whitespace-pre-line">
                        {event.description}
                      </p>
                    )}
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
                      {event.papers?.map((p) => (
                        <a
                          key={p}
                          href={`https://arxiv.org/abs/${p}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-[10px] px-1.5 py-0.5 rounded bg-[#10b981]/15 text-[#34d399] hover:bg-[#10b981]/25 font-mono"
                        >
                          {p}
                        </a>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      ))}
    </div>
  );
}
