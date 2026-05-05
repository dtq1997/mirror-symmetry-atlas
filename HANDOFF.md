# Mirror Symmetry Atlas — 交接备忘

最后更新: 2026-05-06

## 当前状态

- 网站已部署到 https://dtq1997.github.io/mirror-symmetry-atlas/
- 92 人物 yaml + 44 ghost slugs (advisor/学生引用但未建档的)
- publications 已从 OpenAlex + Crossref + arxiv 三源融合, 经过证据驱动消歧器过滤
- 31 人有 score 10-19 的边界论文待人工核对 (`data/papers/_review_queue/`)

## SSOT 架构 (2026-05-06 已重构)

**单一权威映射表**: `src/lib/people-names.json`
- 由 `scripts/build-people-names.py` 生成 (prebuild hook 自动跑)
- 92 yaml + 44 ghost slugs
- 中文名优先 (除 `[待验证]` 标记), 否则英文

**单一权威 paper identity**: `scripts/paper_identity.py`
- `canonical_title` (NFKD 折叠 + LaTeX strip + 大小写折叠 + alnum)
- `canonical_doi` (排除 arxiv 自分配 `10.48550/arxiv.X`)
- `canonical_arxiv_id` (去版本号)
- 所有 dedup/match 必须走它

**单一 yaml → 前端流程**:
1. yaml `publications` 是真值 (一篇论文 = 一条 record)
2. `data.ts` 实时反推 coauthor 关系 (跨 published/preprint 桶 dedup)
3. UI 任何渲染 person slug 必须走 `displayName()` from `name.ts`

## 主要脚本 (按依赖顺序)

| 脚本 | 用途 |
|---|---|
| `scripts/paper_identity.py` | canonical_* 单一权威 |
| `scripts/build-identity-profiles.py` | 给每人 yaml 注入 identity_profile |
| `scripts/lib_disambiguate_v2.py` | 证据驱动消歧器 (ORCID/affiliation/coauthor/keyword/venue) |
| `scripts/enrich-from-openalex-v2.py` | 用消歧器从 OpenAlex 富化, 写 review_queue |
| `scripts/crossref-supplementary-enrich.py` | Crossref by-author 补抓 + by-title 补 journal |
| `scripts/fix-name-pollution.py` | 从 arxiv 真实 author 反查修错 slug 绑定 (v2: 错 slug 退回 raw name) |
| `scripts/canonicalize-publications.py` | union-find 跨 yaml 合并同篇论文, 计算 activity |
| `scripts/clean-title-jats.py` | 从 OpenAlex title 剥 JATS XML |
| `scripts/build-people-names.py` | 生成 src/lib/people-names.json (prebuild) |
| `scripts/apply-dossiers.py` | 把 dossier markdown 合并进 yaml personal_notes/links/sources |
| `scripts/detect-id-title-mismatch.py` | 抓 arxiv 真实 title 与 yaml 对比, 发现错 id |
| `scripts/health-check-people.py` | 综合体检 (advisor=null/students=[]/字符串污染等) |

## 已知未解决

### A. SSOT 类
- detect-id-title-mismatch 全量没跑过 (要 1+ 小时, ~1500 个 arxiv id)
- 有些 yaml 把错的 arxiv id 写在论文 title 旁边 (实例: zong-zhengyu 2211.09203 实为 EE 论文)
- 31 人 review_queue 边界论文没人工核对

### B. 待用户决定的问题 (`data/papers/_questions_for_user.md`)
1. zhang-wei 中文名 (4 候选, HUST 签到表确认)
2. wang-zhiyong 中文名
3. wang-luyao 中文名
4. zhang-qing vs zhang-qingsheng 是否合并
5. xu-xu 与刘小博合著实际是谁 (paper 真实是 Wanxu Yang)
6. li-ao 与 HUST 硕士生李澳是同一人吗

### C. 功能性 pending
- arxiv news 10 年回填 (`scripts/backfill-news-from-publications.py` 写好但没跑)
- 已发表论文 journal 名仍有缺 (Crossref 没全覆盖)
- 列表/sidebar 等少数地方可能还有英文残留 (institutions / concepts 页未审计)

## 关键 commits

- `6d61cf4` SSOT: people-names.json
- `ecc3f21` fix-name-pollution v2: 错 slug 退回 raw name
- `4dd821e` 应用 92 人 dossier
- `02b0866` paper_identity + union-find

## 端到端验证规则 (强制)

每次 commit + push 后必须:
```bash
gh run watch $(gh run list --limit 1 --json databaseId -q '.[0].databaseId') --exit-status
sleep 60  # CDN
curl -sL "https://dtq1997.github.io/mirror-symmetry-atlas/people/<slug>?cb=$(date +%s)" -o /tmp/p.html
grep -c "应消失的关键词" /tmp/p.html  # 验证修复真上线
```

## skill 更新位置

`~/.claude/skills/academic-data-fetch/skill.md` 已沉淀:
- 重名爆炸三层防御 (math 比例 / 5×arxiv 上限 / 严格 math 门槛)
- ORCID 命中即决定性
- core_coauthor + 任一其他证据 = accept (即使 score < 20)
- token-level 名字匹配 (不是子集)
- SSOT for paper identity (canonical_title 必须 NFKD 折叠等)
- 端到端验证强制项
