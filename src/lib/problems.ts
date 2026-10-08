import type { OpenProblem } from "./types";
import { publicSourceUrl } from "./source-url";

const PENDING = { label: "状态待核", color: "#a1a1b5" };
const STATUS = {
  open: { label: "一般版本开放", color: "#f87171" },
  "partially-solved": { label: "部分解决", color: "#fbbf24" },
  solved: { label: "已解决", color: "#34d399" },
  abandoned: { label: "已停止追踪", color: "#a1a1b5" },
  "needs-review": PENDING,
};

/** A display gate for recorded reviews, never an automated mathematical verdict. */
export function problemStatus(problem: Pick<OpenProblem, "status" | "reviewed_on" | "review_note" | "status_note" | "sources">) {
  if (!problem.reviewed_on || !problem.review_note || !problem.status_note ||
      !problem.sources?.some(s => s.label && /^https?:\/\//.test(s.url) && publicSourceUrl(s.url))) return PENDING;
  return Object.hasOwn(STATUS, problem.status) ? STATUS[problem.status] : PENDING;
}
