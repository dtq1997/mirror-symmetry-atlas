import type { Connection } from "@/lib/types";
import Link from "@/components/shared/AtlasLink";
import { displayName } from "@/lib/name";
import { publicSourceUrl } from "@/lib/source-url";

export default function FundingEvidence({ slug, connections }: { slug: string; connections: Connection[] }) {
  const edges = connections.filter((e) => e.type === "grant" && e.review_status === "accepted"
    && e.funding_evidence?.length && (e.source === slug || e.target === slug));
  if (!edges.length) return null;
  return (
    <section className="mb-8" aria-label="同号基金资助">
      <h2 className="text-base font-semibold text-[#e8e8f0] mb-2">同号基金资助</h2>
      <p className="text-xs text-[#8888a0] mb-3 leading-relaxed">
        所列论文明确记载两人受到同一编号资助。仅覆盖已核条目，不表示完整资助记录，也不据此判断负责人、参与期限或直接合作。
      </p>
      <div className="space-y-3">
        {edges.map((edge) => {
          const other = edge.source === slug ? edge.target : edge.source;
          return (
            <div key={other} className="rounded-lg border border-[#2a2a3a] p-3 min-w-0">
              <Link href={`/people/${other}`} className="text-sm text-[#f472b6] hover:underline">{displayName(other)}</Link>
              {edge.funding_evidence!.map((funding) => (
                <div key={`${funding.agency}:${funding.number}`} className="text-xs mt-2">
                  <p className="text-[#e8e8f0] break-words">{funding.agency} {funding.number}</p>
                  <ul className="mt-1 space-y-1 text-[#a8a8b8]">
                    {funding.recipients.map((recipient) => {
                      const href = publicSourceUrl(recipient.source_url);
                      return <li key={`${recipient.person}:${recipient.paper}`}>
                        {displayName(recipient.person)}的依据：{href
                          ? <a className="text-[#818cf8] hover:underline" href={href} target="_blank" rel="noopener noreferrer">arXiv:{recipient.paper}</a>
                          : `arXiv:${recipient.paper}`}
                      </li>;
                    })}
                  </ul>
                </div>
              ))}
            </div>
          );
        })}
      </div>
    </section>
  );
}
