"use client";

import { useMemo, useState } from "react";
import type { CatalogPublication } from "@/lib/publications";
import { fullName } from "@/lib/name";
import { catalogPageSize, catalogWindow, emptyCatalogFilters, filterCatalog, indexCatalog, type CatalogFilters } from "@/lib/catalog-search";
import CatalogControls from "./CatalogControls";
import PublicationCard from "./PublicationCard";

export default function PaperCatalog({ papers }: { papers: CatalogPublication[] }) {
  const [{ filters, limit }, setView] = useState({ filters: emptyCatalogFilters, limit: catalogPageSize });
  const index = useMemo(() => indexCatalog(papers), [papers]);
  const owners = useMemo(() => [...new Set(papers.flatMap((paper) => paper.ownerSlugs))]
    .sort((a, b) => fullName(a).localeCompare(fullName(b), "zh-CN")), [papers]);
  const years = useMemo(() => [...new Set(papers.map((paper) => paper.year))].sort((a, b) => b - a), [papers]);
  const matches = useMemo(() => filterCatalog(index, filters), [index, filters]);
  const { visible, total, nextCount } = catalogWindow(matches, limit);
  const changeFilters = (patch: Partial<CatalogFilters>) => setView((view) => ({ filters: { ...view.filters, ...patch }, limit: catalogPageSize }));
  const reset = () => setView({ filters: emptyCatalogFilters, limit: catalogPageSize });

  return (
    <section aria-label="论文目录">
      <CatalogControls filters={filters} owners={owners} years={years} onChange={changeFilters} onReset={reset} />
      <p role="status" aria-live="polite" aria-atomic="true" className="text-sm text-[#8888a0] mb-4">
        匹配 {total} 条 · 已显示 {visible.length} 条 · 全目录 {papers.length} 条
      </p>
      <noscript><p className="text-sm text-[#fbbf24] mb-4">启用 JavaScript 后可搜索和继续显示全部目录；各人物档案仍可查看其完整收录列表。</p></noscript>
      <div id="catalog-results" className="space-y-3">
        {visible.map((paper) => <PublicationCard key={paper.catalogKey} paper={paper} />)}
      </div>
      {total === 0 && <div className="rounded-lg border border-[#2a2a3a] p-6 text-sm text-[#8888a0]">
        没有匹配记录。可减少关键词或清除筛选；未收录不代表不存在。
      </div>}
      {nextCount > 0 && <button type="button" aria-controls="catalog-results"
        onClick={() => setView((view) => ({ ...view, limit: view.limit + catalogPageSize }))}
        className="w-full mt-5 min-h-12 rounded-lg border border-[#6366f1]/60 text-sm text-[#c7d2fe] hover:bg-[#6366f1]/15 focus-visible:outline-2 focus-visible:outline-[#a5b4fc]">
        继续显示 {nextCount} 条（剩余 {total - visible.length} 条）
      </button>}
    </section>
  );
}
