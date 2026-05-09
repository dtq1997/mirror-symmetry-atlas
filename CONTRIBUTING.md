# 加新人物 / 改信息防坑清单

> **每次更新 `data/people/*.yaml` 或 `data/institutions/*.yaml` 之前，先读完这份。**
> 历史上踩过的所有坑都在这里，prebuild lint 会拦住绝大多数，但人工核对仍是必须的。

---

## 加新人物 yaml 的强制流程

### 1. 准备阶段
- [ ] 确定 slug 命名：**姓-名拼音全拼**（如 `wang-zhiyuan`，不是 `wzy` 或 `wangzy`）
- [ ] 准备权威来源：**学校 faculty 页面 URL**（首选）/ Math Genealogy ID / arXiv author identifier
- [ ] 找出至少一个学术圈核心合作者（slug 已建档的）以便后续 strict 校验

### 2. 必填字段
```yaml
slug: ${slug}                  # 必须等于文件名
name:
  en: "${英文名}"               # 必填
  zh: "${中文名}"               # 中国学者必填，外籍可省
nationality: Chinese|...       # 必填
career_timeline:
  - period: "YYYY-YYYY"        # 时间段，可用 "[?]-2014" / "[待补充]"
    type: education|position|visit|award|event|teaching
    institution: ${slug}        # 必须是 data/institutions/<slug>.yaml 已存在的
    role: "..."
advisor: ${slug-or-omit}        # 必须是 slug（或省略）
identity_profile:               # 推荐填，为消歧多源验证
  coauthor_circle_core_slugs: [...]   # 论文级 strict-match 校验用
  email_domains: [..]                  # 后续 affiliation 校验用
```

### 3. 关键禁忌
| 禁忌 | 后果 | 防护 |
|---|---|---|
| `key_collaborators[].person: "Si Li (李思)"` 写 raw 名字 | 渲染层显示英文+中文混乱 | lint 阻断 |
| `career_timeline[].advisor: "Huijun Fan (樊慧君)"` 写 raw 名字 | advisor 渲染成英文 | lint 阻断 |
| `institution: "stanford"` 但 `data/institutions/stanford.yaml` 不存在 | 渲染回退成英文 slug | lint 阻断 |
| `period: null` 或缺失 | 时间线乱序 | lint 阻断（award 仅 warn） |
| 论文 title 含 `graphene` / `perovskite` / `Trojan Horse method` / `bone drill` 等非数学关键词 | 同名作者污染 | lint 阻断 |
| 期刊是 *Phys Rev C* / *EPJA* / *Nuclear Instruments* / *JACS* 等非数学刊 | 同名作者污染 | lint 阻断 |
| 论文 coauthor 是已建档作者却写 raw name | SSOT 违反 | lint 阻断（strict-match 唯一时） |

### 4. 加新机构 yaml
新人物 yaml 引用的所有 `institution:` 必须先在 `data/institutions/` 下有 yaml：

```bash
# 如果引用了未建档机构，自动建 stub:
python3 scripts/build-missing-institution-stubs.py
```

机构 yaml 最小字段：
```yaml
slug: ${slug}
name:
  zh: "${中文名}"  # 必填（中国机构）
  en: "${英文名}"
city: ${city}
country: ${country}
```

### 5. 添加论文
论文（在 `publications:` 列表）每条必须：
- `id`: 优先 arxiv id（`2401.12726`），其次 `doi:10.xxx/yyy`
- `title`: 论文标题
- `year`: 整数
- `coauthors`: 已建档的用 slug，未建档的用 raw 字符串（**不要写 `"Si Li (李思)"` 这种混合**）
- `journal` + `doi` 当已发表

**强烈建议先跑反向 audit 看是否漏了什么真论文**：
```bash
python3 scripts/audit-missing-papers.py --slug ${新人 slug}
# 看 data/papers/_missing_paper_review.md
```

---

## 改老人物 yaml 的强制流程

### 1. 改前
```bash
# 看一眼当前是否有 lint 错误（应为 0）
python3 scripts/lint-data.py
```

### 2. 改后
```bash
pnpm build              # prebuild 自动跑 lint，错误立即报
```

如果引入新引用（新机构 / 新合作者 slug），重新跑：
```bash
python3 scripts/build-missing-institution-stubs.py  # 缺机构则建 stub
python3 scripts/normalize-slug-references.py       # 把 raw name 自动改 slug
python3 scripts/lint-data.py                        # 再校验
```

---

## 加新人物后的最终检查清单

- [ ] `pnpm build` 通过（prebuild lint 0 errors）
- [ ] 在 dev server 看新人物详情页，**学术履历按时间顺序排列**
- [ ] 主要合作者列表显示中文名（不是 "Si Li (李思)"）
- [ ] 学术履历显示机构中文名（不是英文 slug）
- [ ] advisor 显示中文名
- [ ] 论文列表 **目视扫一遍标题**，发现疑似非数学论文（材料/医学/CS/工程）→ 立即手动删除并补到 `non_math_keywords.py`
- [ ] **跑反向 audit**：`python3 scripts/audit-missing-papers.py --slug ${slug}` 查 yaml 是否漏了真论文
- [ ] **OpenAlex 全量论文已拉取**：人物有 OpenAlex profile 的，跑 `python3 scripts/enrich-from-openalex.py --write ${slug}`；若被 5x 守门拦下，人工核验 profile（看 coauthor 集中度 + concept 主题），干净的话给 yaml 加 `identity_profile.openalex_audited: true` 后重跑
- [ ] **`activity.total_papers` 与 `len(publications)` 一致**：lint 会自动 warn，差 5 篇以上 = 数据漏失
- [ ] **DOI 必须来自 API 不许手敲**：每条带 `doi:` 的 publication 必须有 `sources: [openalex|crossref|...]` 标记。从主页或论文 PDF 抄来的 DOI，必须先用 `curl -s 'https://api.crossref.org/works/${doi}'` 验证 title 一致再写入
- [ ] **合作者名变体扫描**：检查 `key_collaborators` 是否有同人不同写（`Xinyue Li`/`X. Y. Li`，`Bó Wáng`/`Bo Wang`），用 `scripts/normalize-slug-references.py` 或手工合并

---

## 已知踩过的坑（历史教训，必看）

完整方法论与防御机制见 `~/.claude/skills/academic-data-fetch/skill.md`。简要列表：

1. **名字 substring 匹配灾难**：`'Ao Li' ⊂ 'Chien-Hao Liu'`，`'Zhang Qing' ⊂ 'Zhang Qingsheng'` —— 全局禁用 substring，必须 strict token-set
2. **OpenAlex 同名 profile 错合并**：strict-name 也会通过，靠**关键词+期刊围栏**拦
3. **7 位 legacy arxiv id 撞档案**：`9602001` 在 dg-ga / hep-th / math-ph 是不同论文 —— `lib_truth.py` 用 owner_hint
4. **学术履历不按时间排序**：渲染层 `sortByPeriod` 鲁棒解析 90+ 种 period 写法
5. **raw name → slug 自动绑定**：runtime `data.ts` 改用 paper-id 交集，不再靠英文名推断
6. **整篇论文错挂**（li-ao 收 1998 田刚论文）：`validate-publications.py` 用 owner_hint + names_compatible
7. **关键词列表写单 token**：`\brna\b` 误中 *Inte-rna-tional*——优先 bigram
8. **手填 DOI 编错指向他人论文**（zhao-qiulan 2026-05）：手敲 `10.1016/j.physd.2025.134711` 时尾号编错(应为 `134638`)，DOI 解析到 Yue Zhang 等人的湍流论文。**铁律：从此不再手填 DOI**。所有 DOI 必须来自 Crossref / OpenAlex / 论文自报，并在 yaml 加 `sources: [openalex]` 或 `[crossref]` 标记来源
9. **新增人物只录少量论文却写大 total_papers**（zhao-qiulan 同 commit）：activity 卡显示 80 篇但 publications 只列 11 条，用户察觉数据严重不全。lint 已新增 sanity check：`activity.total_papers` 与 `len(publications)` 偏差 ≥5 且 >25% 时 warn
10. **enrich-from-openalex 5x 守门把真高产学者拒之门外**（zhao-qiulan 同 commit）：她真有 80 篇 OpenAlex 论文但 yaml 只有 2 条 arxiv 种子，触发 5x 阈值守门；解决方案——人工核验 profile 干净后在 yaml 加 `identity_profile.openalex_audited: true` 旁路守门
11. **OpenAlex 作者名变体未合并**（zhao-qiulan 同 commit）：`Xinyue Li` 与 `X. Y. Li` 是同一人但被当成两个合作者；`Bó Wáng` (重音) vs `Bo Wang`。enrich 后必须扫一遍 `key_collaborators` 是否有同人不同写

---

## 如果还是踩坑了

请在 `~/.claude/skills/academic-data-fetch/skill.md` 末尾追加新案例。记录：
1. 触发条件（什么样的 yaml 字段 / 什么数据源）
2. 错误表现（页面上看到什么）
3. 修复办法（脚本 + 关键词更新 / 数据修正）
4. 防御加固（lint 是否能拦？需要新加什么规则？）

---

**这份指南本身也应该随着项目演进。每发现一个新坑就加一条。**
