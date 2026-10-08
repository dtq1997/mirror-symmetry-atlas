import Link from "@/components/shared/AtlasLink";
import {
  getAllPeople,
  getAllConcepts,
  getAllConnections,
  getAllConferenceEvents,
  getAllTimelineEvents,
  getAllProblems,
} from "@/lib/data";
import { displayName, nameInfo } from "@/lib/name";
import { collectPublications } from "@/lib/publications";
import UpcomingConferences from "@/components/shared/UpcomingConferences";
import ProblemCards from "@/components/problems/ProblemCards";

export default function Dashboard() {
  const people = getAllPeople();
  const concepts = getAllConcepts();
  const connections = getAllConnections();
  const conferences = getAllConferenceEvents();
  const timeline = getAllTimelineEvents();
  const problems = getAllProblems();

  const totalPubs = collectPublications(people).length;
  const today = new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Shanghai", year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date());

  const stats = [
    { label: "人物", value: people.length, href: "/people", color: "#f59e0b" },
    { label: "概念", value: concepts.length, href: "/concepts", color: "#6366f1" },
    { label: "关系", value: connections.length, href: "/people", color: "#8b5cf6" },
    { label: "论文条目", value: totalPubs, href: "/papers", color: "#10b981" },
  ];

  const recentPeople = people
    .slice()
    .sort(
      (a, b) =>
        (b.publications?.length ?? 0) - (a.publications?.length ?? 0)
    )
    .slice(0, 8);

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
        <UpcomingConferences events={conferences} initialDate={today} />

        {/* Open problems */}
        {problems.length > 0 && (
          <div>
            <h2 className="text-xl font-semibold text-[#e8e8f0] mb-4">
              <Link href="/problems" className="hover:text-[#818cf8]">问题与进展 →</Link>
            </h2>
            <ProblemCards problems={problems} />
          </div>
        )}
      </div>

      {/* Active researchers */}
      <div>
        <h2 className="text-xl font-semibold text-[#e8e8f0] mb-4">
          收录论文较多的学者
        </h2>
        <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-3">
          {recentPeople.map((p) => (
            <Link
              key={p.slug}
              href={`/people/${p.slug}`}
              className="bg-[#14141f] rounded-lg p-4 border border-[#2a2a3a] hover:border-[#f59e0b]/50 transition-colors"
            >
              <div className="text-sm font-medium text-[#e8e8f0]">
                {displayName(p.slug)}
              </div>
              {nameInfo(p.slug)?.zh && (
                <div className="text-xs text-[#8888a0]">{nameInfo(p.slug)?.en}</div>
              )}
              {p.activity?.total_papers != null && (
                <div className="text-xs mt-1 flex flex-wrap gap-1">
                  {p.activity.published_count != null && (
                    <span className="text-[#22c55e]">
                      {p.activity.published_count} 有出版线索
                    </span>
                  )}
                  {p.activity.preprint_only_count != null && (
                    <span className="text-[#f59e0b]">
                      {p.activity.preprint_only_count} 待补出版线索
                    </span>
                  )}
                  {p.activity.published_count == null &&
                    p.activity.preprint_only_count == null && (
                      <span className="text-[#6366f1]">
                        {p.activity.total_papers} 篇论文
                      </span>
                    )}
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
