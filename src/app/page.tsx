import Link from "next/link";
import {
  getAllPeople,
  getAllConcepts,
  getAllConnections,
  getAllInstitutions,
  getAllConferenceEvents,
  getAllTimelineEvents,
  getAllProblems,
} from "@/lib/data";

export default function Dashboard() {
  const people = getAllPeople();
  const concepts = getAllConcepts();
  const connections = getAllConnections();
  const institutions = getAllInstitutions();
  const conferences = getAllConferenceEvents();
  const timeline = getAllTimelineEvents();
  const problems = getAllProblems();

  // Count total publications
  let totalPubs = 0;
  for (const p of people) {
    totalPubs += ((p as any).publications || []).length;
  }

  const stats = [
    { label: "人物", value: people.length, href: "/people", color: "#f59e0b" },
    { label: "概念", value: concepts.length, href: "/concepts", color: "#6366f1" },
    { label: "关系", value: connections.length, href: "/people", color: "#8b5cf6" },
    { label: "论文", value: totalPubs, href: "/papers", color: "#10b981" },
  ];

  const recentPeople = people
    .filter((p) => !p.died)
    .sort(
      (a, b) =>
        (b.activity?.total_papers ?? 0) - (a.activity?.total_papers ?? 0)
    )
    .slice(0, 8);

  // Upcoming conferences
  const upcomingConfs = conferences
    .filter((c) => c.date_start >= "2026-04-14")
    .sort((a, b) => a.date_start.localeCompare(b.date_start))
    .slice(0, 3);

  return (
    <div className="max-w-6xl mx-auto px-6 py-10 w-full">
      <div className="mb-10">
        <h1 className="text-3xl font-bold text-[#e8e8f0] mb-2">
          Mirror Symmetry Atlas
        </h1>
        <p className="text-[#8888a0] text-lg">
          镜像对称及相关领域的交互式知识平台
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
        {stats.map((stat) => (
          <Link
            key={stat.label}
            href={stat.href}
            className="bg-[#14141f] rounded-xl p-5 border border-[#2a2a3a] hover:border-[#6366f1]/50 transition-colors group"
          >
            <div
              className="text-3xl font-bold mb-1"
              style={{ color: stat.color }}
            >
              {stat.value}
            </div>
            <div className="text-sm text-[#8888a0] group-hover:text-[#e8e8f0] transition-colors">
              {stat.label}
            </div>
          </Link>
        ))}
      </div>

      {/* Quick links */}
      <div className="grid md:grid-cols-3 gap-4 mb-10">
        <QuickCard
          title="人物关系网络"
          description="学术关系力导向图，展示师承、合作、机构关联"
          href="/people"
          accent="#f59e0b"
        />
        <QuickCard
          title="概念知识图谱"
          description="概念依赖有向图，可视化学习路径"
          href="/concepts"
          accent="#6366f1"
        />
        <QuickCard
          title="领域时间线"
          description={`${timeline.length} 个里程碑事件`}
          href="/timeline"
          accent="#10b981"
        />
      </div>

      <div className="grid md:grid-cols-2 gap-8 mb-10">
        {/* Upcoming conferences */}
        {upcomingConfs.length > 0 && (
          <div>
            <h2 className="text-xl font-semibold text-[#e8e8f0] mb-4 flex items-center justify-between">
              即将到来的会议
              <Link
                href="/conferences"
                className="text-sm text-[#6366f1] hover:text-[#818cf8] font-normal"
              >
                查看全部 →
              </Link>
            </h2>
            <div className="space-y-3">
              {upcomingConfs.map((conf) => (
                <Link
                  key={conf.slug}
                  href="/conferences"
                  className="block bg-[#14141f] rounded-lg p-4 border border-[#2a2a3a] hover:border-[#10b981]/50 transition-colors"
                >
                  <div className="text-sm font-medium text-[#e8e8f0]">
                    {conf.name.zh || conf.name.en}
                  </div>
                  <div className="flex gap-3 mt-1 text-xs text-[#8888a0]">
                    <span className="text-[#6366f1] font-mono">
                      {conf.date_start}
                    </span>
                    {conf.location && <span>{conf.location}</span>}
                    {conf.invited_speakers && (
                      <span>{conf.invited_speakers.length} 位报告人</span>
                    )}
                  </div>
                </Link>
              ))}
            </div>
          </div>
        )}

        {/* Open problems */}
        {problems.length > 0 && (
          <div>
            <h2 className="text-xl font-semibold text-[#e8e8f0] mb-4">
              开放问题
            </h2>
            <div className="space-y-3">
              {problems.map((prob) => (
                <div
                  key={prob.slug}
                  className="bg-[#14141f] rounded-lg p-4 border border-[#2a2a3a]"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-[#e8e8f0]">
                      {prob.name.zh || prob.name.en}
                    </span>
                    <span
                      className={`text-[10px] px-2 py-0.5 rounded-full ${
                        prob.status === "open"
                          ? "bg-[#ef4444]/15 text-[#f87171]"
                          : prob.status === "partially-solved"
                            ? "bg-[#f59e0b]/15 text-[#fbbf24]"
                            : "bg-[#10b981]/15 text-[#34d399]"
                      }`}
                    >
                      {prob.status === "open"
                        ? "开放"
                        : prob.status === "partially-solved"
                          ? "部分解决"
                          : "已解决"}
                    </span>
                  </div>
                  <div className="text-xs text-[#8888a0] mt-1">
                    {prob.importance} · {prob.year_proposed} 年提出
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Active researchers */}
      <div>
        <h2 className="text-xl font-semibold text-[#e8e8f0] mb-4">
          活跃研究者
        </h2>
        <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-3">
          {recentPeople.map((p) => (
            <Link
              key={p.slug}
              href={`/people/${p.slug}`}
              className="bg-[#14141f] rounded-lg p-4 border border-[#2a2a3a] hover:border-[#f59e0b]/50 transition-colors"
            >
              <div className="text-sm font-medium text-[#e8e8f0]">
                {p.name.zh || p.name.en}
              </div>
              {p.name.zh && (
                <div className="text-xs text-[#8888a0]">{p.name.en}</div>
              )}
              {p.activity?.total_papers != null && (
                <div className="text-xs text-[#6366f1] mt-1">
                  {p.activity.total_papers} 篇论文
                </div>
              )}
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}

function QuickCard({
  title,
  description,
  href,
  accent,
}: {
  title: string;
  description: string;
  href: string;
  accent: string;
}) {
  return (
    <Link
      href={href}
      className="bg-[#14141f] rounded-xl p-6 border border-[#2a2a3a] hover:border-opacity-50 transition-all group"
    >
      <h3
        className="text-lg font-semibold mb-2 group-hover:opacity-90 transition-colors"
        style={{ color: accent }}
      >
        {title}
      </h3>
      <p className="text-sm text-[#8888a0]">{description}</p>
    </Link>
  );
}
