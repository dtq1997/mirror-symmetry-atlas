// Robust period parsing for career_timeline / events / etc.
// Period strings come in many shapes: "1966-1969", "2022-present", "1981",
// "2003.9-2006.3", "2008-08 — 2010-07", "[?]-1974", "~1980-1990",
// "[待验证]-2017", "present", etc.
//
// We extract a numeric (start, end) pair for sorting and grouping.
// Unknown side becomes ±Infinity-ish sentinel so it sorts to the end.

const FAR_FUTURE = 9999;
const FAR_PAST = -9999;

export interface ParsedPeriod {
  start: number; // start year for sorting; FAR_FUTURE if unknown
  end: number; // end year; FAR_FUTURE if "present" or unknown-future
  ongoing: boolean;
}

function findYears(s: string): number[] {
  const matches = s.match(/\b(1[6-9]\d{2}|20\d{2}|21\d{2})\b/g);
  return matches ? matches.map((m) => parseInt(m, 10)) : [];
}

export function parsePeriod(period: string | undefined | null): ParsedPeriod {
  if (!period) return { start: FAR_FUTURE, end: FAR_FUTURE, ongoing: false };
  const s = String(period).trim();
  const lower = s.toLowerCase();
  const ongoing = /present|至今|现在/.test(lower);

  const allYears = findYears(s);
  let start = FAR_FUTURE;
  let end = FAR_FUTURE;

  if (allYears.length >= 2) {
    start = allYears[0];
    end = allYears[allYears.length - 1];
  } else if (allYears.length === 1) {
    // Only one year. Decide whether it's start or end by which side it sits.
    const y = allYears[0];
    const idx = s.indexOf(String(y));
    const before = s.slice(0, idx);
    const after = s.slice(idx + 4);
    const hasUnknownLeft = /\[\??\]|\[待验证\]|\[待补充\]|^~?\s*$/.test(before.trim());
    const hasUnknownRight = /\[\??\]|\[待验证\]|present|至今/i.test(after);
    if (hasUnknownLeft && !hasUnknownRight) {
      // "[?]-1974" — year is the END
      start = y;
      end = y;
    } else if (ongoing || hasUnknownRight) {
      // "2024.1-present" — year is the START, end is open
      start = y;
      end = FAR_FUTURE;
    } else {
      // single year like "1981"
      start = y;
      end = y;
    }
  }

  // Override end for ongoing
  if (ongoing) end = FAR_FUTURE;

  return { start, end, ongoing };
}

/** Sort key in ascending chronological order (oldest first). */
export function periodSortKey(period: string | undefined | null): number {
  const { start } = parsePeriod(period);
  return start;
}

/** Stable chronological sort. Ties broken by end year, then by type if provided. */
export function sortByPeriod<T extends { period?: string }>(
  items: T[],
  opts?: { typeOrder?: (item: T) => number },
): T[] {
  return [...items].sort((a, b) => {
    const pa = parsePeriod(a.period);
    const pb = parsePeriod(b.period);
    if (pa.start !== pb.start) return pa.start - pb.start;
    if (pa.end !== pb.end) return pa.end - pb.end;
    if (opts?.typeOrder) return opts.typeOrder(a) - opts.typeOrder(b);
    return 0;
  });
}

export { FAR_FUTURE, FAR_PAST };
