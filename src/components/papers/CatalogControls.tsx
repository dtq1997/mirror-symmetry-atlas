import type { CatalogFilters } from "@/lib/catalog-search";
import { fullName } from "@/lib/name";

const inputClass = "block w-full min-w-0 mt-1.5 rounded-lg border border-[#3a3a50] bg-[#0a0a0f] px-3 py-2.5 text-sm text-[#e8e8f0] focus-visible:outline-2 focus-visible:outline-[#a5b4fc]";

interface CatalogControlsProps {
  disabled: boolean;
  filters: CatalogFilters;
  owners: string[];
  years: number[];
  onChange: (patch: Partial<CatalogFilters>) => void;
  onReset: () => void;
}

export default function CatalogControls({ disabled, filters, owners, years, onChange, onReset }: CatalogControlsProps) {
  return (
    <div role="search" aria-label="论文目录">
      <fieldset disabled={disabled} aria-busy={disabled} aria-label="搜索与筛选" className="min-w-0 rounded-xl border border-[#2a2a3a] bg-[#14141f] p-4 mb-5">
        <label htmlFor="paper-search" className="block text-sm text-[#e8e8f0]">搜索论文
          <input id="paper-search" type="search" value={filters.query} onChange={(e) => onChange({ query: e.target.value })}
            placeholder="题名、中英文署名、期刊或完整 arXiv / DOI" aria-describedby="paper-search-help" className={inputClass} />
        </label>
        <p id="paper-search-help" className="text-xs text-[#8888a0] mt-2 leading-relaxed">在全部目录中查找，可输入多个词。署名含原始合作者姓名；搜索命中不确认同名者身份。</p>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-4">
          <label htmlFor="paper-owner" className="min-w-0 text-xs text-[#8888a0]">收录人物
            <select id="paper-owner" value={filters.owner} onChange={(e) => onChange({ owner: e.target.value })} className={inputClass}>
              <option value="">全部人物</option>
              {owners.map((slug) => <option key={slug} value={slug}>{fullName(slug)}</option>)}
            </select>
          </label>
          <label htmlFor="paper-year" className="min-w-0 text-xs text-[#8888a0]">记录年份
            <select id="paper-year" value={filters.year} onChange={(e) => onChange({ year: e.target.value })} className={inputClass}>
              <option value="">全部年份</option>
              {years.map((year) => <option key={year} value={year}>{year}</option>)}
            </select>
          </label>
          <label htmlFor="paper-publication" className="min-w-0 text-xs text-[#8888a0]">出版线索
            <select id="paper-publication" value={filters.publication} onChange={(e) => onChange({ publication: e.target.value as CatalogFilters["publication"] })} className={inputClass}>
              <option value="all">全部记录</option>
              <option value="with-clues">有出版线索</option>
              <option value="needs-clues">待补出版线索</option>
            </select>
          </label>
        </div>
        <button type="button" onClick={onReset} className="mt-3 min-h-11 px-3 rounded-lg text-sm text-[#a5b4fc] hover:bg-[#6366f1]/15 focus-visible:outline-2 focus-visible:outline-[#a5b4fc]">清除搜索与筛选</button>
      </fieldset>
    </div>
  );
}
