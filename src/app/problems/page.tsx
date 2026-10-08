import { getAllProblems } from "@/lib/data";
import ProblemCards from "@/components/problems/ProblemCards";

export default function ProblemsPage() {
  const problems = getAllProblems();
  return <div className="max-w-4xl mx-auto px-6 py-10 w-full">
    <h1 className="text-2xl font-bold mb-3">问题与进展</h1>
    <p className="text-sm text-[#aaaac0] mb-6 leading-relaxed">收录 {problems.length} 个问题条目。每条分别列出适用条件、文献结果和核对范围；部分情形的结果不能代替一般情形。</p>
    <ProblemCards problems={problems} />
  </div>;
}
