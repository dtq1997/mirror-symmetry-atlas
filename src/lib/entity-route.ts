import routes from "./entity-routes.json";
import { displayName } from "./name";
import { institutionName } from "./inst";

const table: Record<string, string> = routes;

export function entityRoute(href: string) {
  const path = href.split(/[?#]/)[0].replace(/\/$/, "");
  const match = /^\/(people|concepts|institutions|problems)\/([^/]+)$/.exec(path);
  if (!match) return null;
  const [, kind, slug] = match;
  const exists = Object.hasOwn(table, path);
  const label = kind === "people" ? displayName(slug)
    : kind === "institutions" ? institutionName(slug) : (table[path] ?? slug);
  return { exists, slug, label };
}
