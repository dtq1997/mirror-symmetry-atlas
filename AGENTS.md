<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version (Next.js 16, App Router) has breaking changes — APIs, conventions, and file structure may differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

---

# Mirror Symmetry Atlas — Codex 工作手册

镜像对称及相关领域的交互式知识平台。本文件是 Codex 在本仓库工作的入口。Claude Code 看的是 `CLAUDE.md`，两份必须保持核心规则同步——修改一份请同步另一份。

## 启动必读

动手前先 `cat`：
1. `CLAUDE.md`（项目规则全集，Codex/Claude 共享）
2. `docs/enrichment-methodology.md`（人物充实 checklist + 防错规则）
3. `docs/design.md`（schema、配色、阶段计划）

## 用户身份

唐乾（Qian Tang），清华博后。徐晓濛组（Stokes、isomonodromy、q-Painlevé）+ 张友金/刘思齐组（Frobenius 流形、WDVV、可积系统）。沟通用中文，技术术语保留英文，语气直接不客套。

## 核心规则（与 CLAUDE.md 对齐）

### 语言
- UI 与数据内容**全部中文**（导航、按钮、概念定义、personal_notes）
- 人名优先 `name.zh`，无中文名退英文
- 学术专有名词保留英文（Frobenius manifold、Stokes phenomenon）
- YAML 字段名保持英文

### 数据即时写入
用户提到的人物/会议/机构/关系，**当下就写进 YAML**，不等收尾：
- 新人物 → `data/people/{slug}.yaml`，资料不足建 stub 标 `[待补充]`
- 新关系 → `data/connections/`
- 新会议 → `data/conferences/events-{YYYY}.yaml`

### 来源可追溯
关键事实附 `sources` 链接。容易失效的页面（faculty page）用 Wayback。`external_ids`（openalex/mathgenealogy/orcid）前端自动生成链接，不重复列入 sources。

## 重名消歧（用户最高优先级诉求）

历史教训：很多人物的论文计数错得离谱，根因都是重名混入。**每次涉及论文计数或合作者推断必须按以下顺序硬过：**

### 1. arXiv 类目硬限定
- 调用 `scripts/fetch-arxiv-by-author.py "Firstname Lastname" --cats math-ph,math.AG,math.AT,nlin.SI,hep-th`
- arXiv search query 必须是 `au:"Full Name"`（带双引号）+ `AND (cat:math.* OR cat:math-ph OR cat:nlin.SI OR cat:hep-th)`
- 不带类目限制等于自杀，常见中文名会拉回数百篇 cs/q-bio 的同名论文

### 2. 多信号打分（lib_disambiguate.py 已实现）
对每篇候选论文累计：
- +5 primary_category 在 math.* / math-ph / nlin.SI / hep-th
- +10 每个匹配的已知合作者（cap 3）
- +3 每个匹配的研究领域关键词（题目里）
- +5 提交者（arXiv `From:` 字段）名字匹配
- +5 tex 源里抽到的 affiliation 与 `career_timeline` 中机构一致
- +5 tex 源里抽到的 email 域名与人物已记录 email 一致

阈值：≥15 强匹配 / 10–14 review / 5–9 弱 / <5 拒绝。

### 3. 邮箱与单位必须入档（schema 扩展）
现有 schema (`src/lib/types.ts` 的 `Person` 接口) **缺失**邮箱和历史 affiliation 字段，但 `lib_disambiguate.py` 已经在用。处理人物时按以下约定写入 YAML（schema 后续会正式扩字段）：

```yaml
known_emails:
  - "tangq@tsinghua.edu.cn"   # 当前
  - "tangqian@math.pku.edu.cn"  # 历史
known_affiliations:
  # 与 career_timeline 不同，这里记录 arXiv/论文署名实际出现过的字符串
  - "Yau Mathematical Sciences Center, Tsinghua University"
  - "School of Mathematical Sciences, Peking University"
```

来源：tex 源（`scripts/download-arxiv-sources.py` + grep `\author`/`\email`/`\affiliation`），机构 faculty page。每次为某人新增论文时顺便回填这两个字段。

### 4. 还查不准的处理
- 看论文 tex 源的 `\acknowledgments` 提到的基金、合作者
- 用论文里的导师/合作者反推（数学社群偏小，几篇就能锁定）
- 实在不确定 → 论文进 `[待验证]` 池，不要瞎归到某个 slug

## 主动审计（用户明确要求）

不要被动等用户报错。每次工作时顺手做：
- **打开任一人物 YAML 时**：检查 `publications` 里有没有明显跨领域的论文（cs/bio）→ 红旗
- **回填合作者时**：如果 `papers_count` 与 `publications` 列表实际计数不符，立即修正
- **发现一处错误时**：grep 同类问题（`grep -rn "可疑模式" data/people/`），不止改当前文件
- **发现 ghost slug**（被引用但未建档）：要么 stub 出来，要么从引用方移除

可以主动跑 `scripts/audit-publications.py` 做体检，把异常清单写入 `~/ai/memory/unresolved/` 让用户决断。

## 网站自动更新（已知失效，用户已提）

- `https://dtq1997.github.io/mirror-symmetry-atlas/` 长期没刷新
- 部署链：push to `main` → `.github/workflows/deploy.yml` 走 GitHub Pages
- 数据更新链：`.github/workflows/` 里有 `Daily arXiv News`（每天 UTC 08:00 跑 `fetch-arxiv-news.py`）
- 排查时先看 https://github.com/dtq1997/mirror-symmetry-atlas/actions 最近的 run 是否失败、deploy workflow 触发条件、`pnpm build` 输出是否落到 `out/`
- **不要自动修复 workflow**——先报告失败原因再请用户决定

## 命令

```bash
pnpm dev                                    # 本地预览 :3000
pnpm build                                  # 静态导出到 out/
python3 scripts/fetch-arxiv-by-author.py    # 抓某人的 arXiv 论文
python3 scripts/audit-publications.py       # 数据卫生体检
python3 scripts/enrich-publications.py      # 补全已有 publications 的字段
```

## 三家 AI 协同

本项目由 Claude / Codex / Gemini 共管。写入 `~/ai/memory/`、`~/ai/workspace/` 的共享区域时标注 `[Codex]`。读共享文件时预期内容可能被其他 AI 改过，不假设独占。

## 不确定性

- 不确定就说不确定，禁止猜了再装自信
- 事实写入 YAML 前必须有 source URL；不全的标 `[待验证]` 并附部分来源
- 关键判断（写入 100+ 人的批量改动、删除 ghost slug、改 schema）先与用户对齐再动手
