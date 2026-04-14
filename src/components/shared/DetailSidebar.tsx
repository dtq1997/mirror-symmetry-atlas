"use client";

import type { Person, GraphNode } from "@/lib/types";
import Link from "next/link";

interface DetailSidebarProps {
  node: GraphNode | null;
  onClose: () => void;
}

function PersonDetail({ person }: { person: Person }) {
  const currentPosition = person.career_timeline
    ?.filter((e) => e.type === "position")
    .pop();

  return (
    <div className="space-y-4">
      {/* Header */}
      <div>
        <h2 className="text-xl font-semibold text-[#e8e8f0]">
          {person.name.en}
        </h2>
        {person.name.zh && (
          <p className="text-[#8888a0] text-sm">{person.name.zh}</p>
        )}
        {person.born && (
          <p className="text-[#8888a0] text-xs mt-1">
            {person.born}
            {person.died ? ` – ${person.died}` : ""} · {person.nationality}
          </p>
        )}
      </div>

      {/* Current position */}
      {currentPosition && (
        <div className="bg-[#0a0a0f] rounded-lg p-3 border border-[#2a2a3a]">
          <div className="text-xs text-[#8888a0] mb-1">当前/最近职位</div>
          <div className="text-sm text-[#e8e8f0]">{currentPosition.role}</div>
          {currentPosition.institution && (
            <div className="text-xs text-[#8888a0]">{currentPosition.institution}</div>
          )}
          {currentPosition.period && (
            <div className="text-xs text-[#6366f1]">{currentPosition.period}</div>
          )}
        </div>
      )}

      {/* Research areas */}
      {person.research_areas?.length > 0 && (
        <div>
          <div className="text-xs text-[#8888a0] mb-2">研究方向</div>
          <div className="flex flex-wrap gap-1">
            {person.research_areas.map((area) => (
              <span
                key={area}
                className="px-2 py-0.5 text-xs rounded-full bg-[#6366f1]/20 text-[#818cf8] border border-[#6366f1]/30"
              >
                {area}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Activity stats */}
      {person.activity && (
        <div>
          <div className="text-xs text-[#8888a0] mb-2">学术活跃度</div>
          <div className="grid grid-cols-2 gap-2">
            {person.activity.total_papers != null && (
              <Stat label="论文" value={person.activity.total_papers} />
            )}
            {person.activity.h_index != null && (
              <Stat label="h-index" value={person.activity.h_index} />
            )}
            {person.activity.phd_students != null && (
              <Stat label="博士生" value={person.activity.phd_students} />
            )}
            {person.activity.academic_descendants != null && (
              <Stat label="学术后代" value={person.activity.academic_descendants} />
            )}
          </div>
        </div>
      )}

      {/* Key collaborators */}
      {person.key_collaborators?.length > 0 && (
        <div>
          <div className="text-xs text-[#8888a0] mb-2">主要合作者</div>
          <div className="space-y-1.5">
            {person.key_collaborators.slice(0, 5).map((collab) => (
              <div
                key={collab.person}
                className="text-xs bg-[#0a0a0f] rounded p-2 border border-[#2a2a3a]"
              >
                <span className="text-[#f59e0b]">{collab.person}</span>
                {collab.papers_count && (
                  <span className="text-[#8888a0]"> · {collab.papers_count} 篇</span>
                )}
                {collab.topic && (
                  <div className="text-[#8888a0] mt-0.5 truncate">{collab.topic}</div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Career timeline preview */}
      {person.career_timeline?.length > 0 && (
        <div>
          <div className="text-xs text-[#8888a0] mb-2">学术履历</div>
          <div className="space-y-1">
            {person.career_timeline.slice(0, 6).map((entry, i) => (
              <div key={i} className="flex gap-2 text-xs">
                <span className="text-[#6366f1] shrink-0 w-20 text-right">
                  {entry.period}
                </span>
                <span className="text-[#e8e8f0]">
                  {entry.title || entry.role || entry.notes}
                </span>
              </div>
            ))}
            {person.career_timeline.length > 6 && (
              <div className="text-xs text-[#8888a0] pl-22">
                还有 {person.career_timeline.length - 6} 条...
              </div>
            )}
          </div>
        </div>
      )}

      {/* Personal notes */}
      {person.personal_notes && (
        <div>
          <div className="text-xs text-[#8888a0] mb-1">备注</div>
          <p className="text-xs text-[#e8e8f0] leading-relaxed whitespace-pre-line">
            {person.personal_notes}
          </p>
        </div>
      )}

      {/* Links */}
      <div className="pt-2 border-t border-[#2a2a3a]">
        <Link
          href={`/people/${person.slug}`}
          className="text-sm text-[#6366f1] hover:text-[#818cf8] transition-colors"
        >
          查看完整资料 →
        </Link>
      </div>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: number }) {
  return (
    <div className="bg-[#0a0a0f] rounded p-2 border border-[#2a2a3a]">
      <div className="text-lg font-semibold text-[#e8e8f0]">{value}</div>
      <div className="text-xs text-[#8888a0]">{label}</div>
    </div>
  );
}

export default function DetailSidebar({ node, onClose }: DetailSidebarProps) {
  if (!node) return null;

  return (
    <div
      className="fixed top-[56px] right-0 w-[400px] h-[calc(100vh-56px)] bg-[#14141f] border-l border-[#2a2a3a] overflow-y-auto z-20 shadow-2xl animate-slide-in"
      style={{
        animation: "slideIn 0.2s ease-out",
      }}
    >
      <style jsx>{`
        @keyframes slideIn {
          from { transform: translateX(100%); }
          to { transform: translateX(0); }
        }
      `}</style>

      {/* Close button */}
      <button
        onClick={onClose}
        className="absolute top-3 right-3 w-8 h-8 flex items-center justify-center text-[#8888a0] hover:text-[#e8e8f0] hover:bg-[#2a2a3a] rounded transition-colors z-10"
      >
        ×
      </button>

      <div className="p-5">
        {node.type === "person" && node.data && (
          <PersonDetail person={node.data as Person} />
        )}
        {!node.data && (
          <div className="text-[#8888a0] text-sm">
            <h2 className="text-lg font-medium text-[#e8e8f0] mb-2">
              {node.label}
            </h2>
            <p>暂无数据。</p>
            {node.isGhost && (
              <p className="mt-2 text-xs">
                此节点被引用但尚未记录。
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
