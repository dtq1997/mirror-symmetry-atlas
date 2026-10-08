import type { TimelineEvent } from "./types";

/** Sort by the known date components without inventing a month/day for display. */
export function sortTimelineEvents(events: TimelineEvent[]): TimelineEvent[] {
  return [...events].sort((a, b) => {
    const left = a.date.split("-").map(Number);
    const right = b.date.split("-").map(Number);
    for (let i = 0; i < 3; i++) {
      const difference = (left[i] ?? 0) - (right[i] ?? 0);
      if (difference) return difference;
    }
    return 0;
  });
}
