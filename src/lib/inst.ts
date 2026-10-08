/**
 * Single source of truth for institution display names.
 * Mirror of name.ts but for institution slugs.
 */
import names from "./institution-names.json";

type InstEntry = { displayName: string; en: string; zh: string | null };
const TABLE = names as Record<string, InstEntry>;

/** Preferred display: Chinese when available, else English, else slug. */
export function institutionName(slug: string | undefined | null): string {
  if (!slug) return "";
  return TABLE[slug]?.displayName ?? slug;
}

export function institutionInfo(slug: string): InstEntry | undefined {
  return TABLE[slug];
}

export function relevanceLabel(value: string): string {
  return ({ high: "重点收录", medium: "相关收录", low: "补充收录" } as Record<string, string>)[value] ?? "待分类";
}
