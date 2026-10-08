import { publicationMetadata, publicationMetadataNote } from "@/lib/publication-metadata";

export default function PublicationMetadata({ paper }: { paper: { id?: string; doi?: string; journal?: string } }) {
  const metadata = publicationMetadata(paper);
  const label = metadata.hasPublicationClue ? "有出版线索" : "待补出版线索";
  return (
    <div className="flex flex-wrap items-center gap-2 text-[10px] mt-1.5 break-words">
      <span title={publicationMetadataNote}
        className={metadata.hasPublicationClue ? "text-[#22c55e]" : "text-[#f59e0b]"}>
        {label}
      </span>
      {metadata.venue && <span className="text-[#8888a0]">
        {metadata.repositoryVenue ? "资料库" : "期刊/书籍记录"}：{metadata.venue}
      </span>}
      {metadata.doiUrl && <a href={metadata.doiUrl} target="_blank" rel="noopener noreferrer"
        title={metadata.doi} className="text-[#a5b4fc] hover:underline">
        {metadata.repositoryDoi ? "资料库 DOI" : "DOI"} ↗
      </a>}
    </div>
  );
}
