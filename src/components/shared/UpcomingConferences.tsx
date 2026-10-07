"use client";

import { useSyncExternalStore } from "react";
import Link from "./AtlasLink";
import type { ConferenceEvent } from "@/lib/types";

export function todayInShanghai() {
  return new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Shanghai", year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date());
}

function subscribe(callback: () => void) {
  const timer = setInterval(callback, 60_000);
  document.addEventListener("visibilitychange", callback);
  return () => { clearInterval(timer); document.removeEventListener("visibilitychange", callback); };
}

export default function UpcomingConferences({ events, initialDate }: { events: ConferenceEvent[]; initialDate: string }) {
  const today = useSyncExternalStore(subscribe, todayInShanghai, () => initialDate);
  const upcoming = events.filter((event) => (event.date_end || event.date_start) >= today)
    .sort((a, b) => a.date_start.localeCompare(b.date_start)).slice(0, 3);
  return <section>
    <h2 className="text-xl font-semibold mb-4 flex items-center justify-between">
      近期会议<Link href="/conferences" className="text-sm text-[#818cf8] font-normal">查看全部 →</Link>
    </h2>
    <p className="text-xs text-[#8888a0] mb-3">按北京时间 {today} 筛选已收录日程</p>
    {upcoming.length ? <div className="space-y-3">{upcoming.map((event) => <Link
      key={event.slug} href={`/conferences#${event.slug}`}
      className="block bg-[#14141f] rounded-lg p-4 border border-[#2a2a3a] hover:border-[#10b981]/50"
    >
      <div className="text-sm font-medium">{event.name.zh || event.name.en}</div>
      <div className="flex flex-wrap gap-3 mt-1 text-xs text-[#8888a0]">
        <span>{event.date_start}{event.date_end ? ` 至 ${event.date_end}` : ""}</span>
        <span>{event.date_start > today ? "尚未开始" : "日程进行中"}</span>
        {event.location && <span>{event.location}</span>}
      </div>
    </Link>)}</div> : <p className="text-sm text-[#8888a0] p-4 border border-[#2a2a3a] rounded-lg">
      暂未收录正在举行或即将举行的会议。
    </p>}
  </section>;
}
