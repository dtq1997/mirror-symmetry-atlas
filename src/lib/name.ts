/**
 * Single source of truth for person display names.
 *
 * Imports a JSON map produced by `scripts/build-people-names.py` from each
 * person YAML's name.zh / name.en. Works in both server and client components
 * (no fs / yaml dependency).
 *
 * RULE: every UI place that renders a person slug MUST go through
 * `displayName(slug)` — direct slug rendering is a SSOT violation.
 */
import names from "./people-names.json";

type NameEntry = {
  displayName: string;
  en: string;
  zh: string | null;
};

const TABLE = names as Record<string, NameEntry>;

/** Preferred display name: Chinese when available (and not a [待验证] placeholder),
 *  English otherwise. Returns the slug itself if not in the index. */
export function displayName(slug: string): string {
  return TABLE[slug]?.displayName ?? slug;
}

/** Both forms when distinct, e.g. "刘小博 (Xiaobo Liu)". */
export function fullName(slug: string): string {
  const entry = TABLE[slug];
  if (!entry) return slug;
  if (entry.zh && entry.en && entry.zh !== entry.en) {
    return `${entry.zh} (${entry.en})`;
  }
  return entry.displayName;
}

export function nameInfo(slug: string): NameEntry | undefined {
  return TABLE[slug];
}
