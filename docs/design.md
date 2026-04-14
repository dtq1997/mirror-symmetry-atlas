# Mirror Symmetry Atlas

镜像对称领域的交互式知识平台。展示人物关系网络、概念知识图谱、学术会议、arXiv 监控、文献引用网络。

## 用户需求（原话）

1. 展示领域核心人物之间的联系，包括但不限于学术、私人生活等
2. 人物要越详细越好：什么时候在什么地方读书、怎么毕业的、老师是谁、认识什么人、在学术界活跃程度如何
3. 领域的学术内容（概念、定理、猜想的知识图谱）
4. 最新进展，监控 arXiv
5. 学术会议，聚焦国内为主
6. 时间线：领域发展的关键节点
7. 文献图谱：论文引用网络
8. 概念依赖图：学习路径可视化

**受众：** 小圈子同行分享，不需要用户系统
**策略：** 先搭框架再填数据，数据渐进填充

### UI 语言

**前端界面必须使用中文。** 包括导航栏、标题、按钮文字、标签、图例、提示文本等所有面向用户的文字。
- 人名优先显示中文名（`name.zh`），无中文名时显示英文
- 学术专有名词（如 Frobenius manifold、Stokes phenomenon）保留英文
- 代码注释和 YAML 数据文件中的 notes 字段中英皆可

---

## Tech Stack

| 层 | 选型 | 理由 |
|---|---|---|
| 框架 | **Next.js 15** (App Router) + TypeScript | SSG 友好，Vercel 零配置部署 |
| 样式 | **Tailwind CSS v4** + `next-themes` | 暗色主题，快速迭代 |
| 可视化 | **react-force-graph** (Three.js/WebGL) + Bloom | 发光效果 + 高性能，React 组件做信息面板 |
| 地图 | **react-simple-maps** 或 D3-geo | 机构地图视图 |
| 数学公式 | **KaTeX** | 轻量快速 |
| 搜索 | **Fuse.js** | 客户端模糊搜索 |
| YAML 解析 | **js-yaml** + **gray-matter** | Markdown frontmatter |
| 数据格式 | YAML + Markdown | 人和 AI 都能编辑 |
| 部署 | Vercel 或 `next export` 静态 | 分享方便 |

---

## 目录结构

```
mirror-symmetry-atlas/
├── CLAUDE.md                          # 本文件
├── GEMINI.md                          # Gemini 适配
├── AGENTS.md                          # 三家协同说明
├── package.json
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
│
├── data/                              # 所有内容数据（YAML），git tracked
│   ├── people/                        # 一人一文件 (slug.yaml)
│   │   ├── dubrovin.yaml
│   │   ├── xu-xiaomeng.yaml
│   │   ├── zhang-youjin.yaml
│   │   └── ...
│   ├── concepts/                      # 一概念一文件
│   │   ├── frobenius-manifold.yaml
│   │   ├── mirror-symmetry.yaml
│   │   └── ...
│   ├── papers/
│   │   ├── seminal.yaml               # 手工整理经典论文
│   │   └── arxiv-YYYY-MM-DD.yaml      # 自动抓取
│   ├── timeline/events.yaml           # 领域里程碑
│   ├── conferences/                   # 学术会议（聚焦国内）
│   │   ├── recurring.yaml             # 周期性会议系列
│   │   └── events-YYYY.yaml           # 按年
│   ├── connections/
│   │   ├── advisor-student.yaml
│   │   ├── coauthorship.yaml
│   │   └── institutional.yaml
│   ├── institutions/                  # ★ 机构作为一等实体
│   │   ├── sissa.yaml
│   │   ├── tsinghua.yaml
│   │   └── ...
│   ├── problems/                      # ★ Open problems / research programs
│   │   ├── hms-general-cy.yaml
│   │   ├── syz-metric.yaml
│   │   └── ...
│   ├── seminars/                      # ★ 常规 seminar / reading group
│   │   └── recurring.yaml
│   └── meta/
│       └── categories.yaml
│
├── content/                           # 长文本 Markdown (KaTeX)
│   ├── people/dubrovin.md             # 人物详细传记
│   └── concepts/frobenius-manifold.md # 概念详细说明
│
├── scripts/
│   ├── fetch-arxiv.ts                 # arXiv 每日抓取
│   ├── fetch-conferences.ts           # 会议信息抓取
│   ├── fetch-citations.ts             # Semantic Scholar 引用
│   └── validate-data.ts              # 数据校验（slug 引用完整性）
│
├── src/
│   ├── app/
│   │   ├── layout.tsx                 # 根布局：导航栏、主题切换、KaTeX CSS
│   │   ├── page.tsx                   # Dashboard 首页（统计数字 + 最近更新 + 快速入口）
│   │   ├── people/
│   │   │   ├── page.tsx               # ★ 人物关系网络（全屏力导向图）
│   │   │   └── [slug]/page.tsx        # 人物详情页（完整履历时间线 + 活跃度 + 合作者）
│   │   ├── concepts/
│   │   │   ├── page.tsx               # 概念知识图谱（有向依赖图）
│   │   │   └── [slug]/page.tsx        # 概念详情页（KaTeX 定义 + 前置/后续 + 关联人物论文）
│   │   ├── timeline/page.tsx          # 领域发展时间线（水平可滚动）
│   │   ├── papers/
│   │   │   ├── page.tsx               # arXiv feed + 论文浏览 + 筛选
│   │   │   └── [id]/page.tsx          # 论文详情
│   │   ├── conferences/page.tsx       # 学术会议（国内为主，日历 + 列表）
│   │   ├── institutions/
│   │   │   ├── page.tsx               # ★ 机构地图视图（世界地图 + 人物流动弧线）
│   │   │   └── [slug]/page.tsx        # 机构详情
│   │   ├── problems/page.tsx          # ★ Open problems 看板
│   │   └── literature/page.tsx        # 引用网络图
│   │
│   ├── components/
│   │   ├── graphs/
│   │   │   ├── ForceGraph.tsx         # ★★ 核心：可复用 D3 canvas 力导向图（详见下方规格）
│   │   │   ├── PeopleNetwork.tsx      # 人物图的配置层（节点着色、边类型、力参数）
│   │   │   ├── ConceptMap.tsx         # 概念图的配置层（有向箭头、层级布局）
│   │   │   ├── CitationNetwork.tsx    # 引用图的配置层（节点大小∝引用数）
│   │   │   ├── InstitutionMap.tsx     # ★ 世界地图 + 机构标点 + 人物流动弧线
│   │   │   ├── GraphControls.tsx      # 缩放/重置/筛选控件
│   │   │   ├── TimeSlider.tsx         # ★★ 时间滑块（拖到某年→显示该年快照）
│   │   │   └── GraphLegend.tsx        # 图例
│   │   ├── timeline/
│   │   │   ├── Timeline.tsx           # D3 水平时间线主组件
│   │   │   └── TimelineEvent.tsx      # 单个事件卡片
│   │   ├── person/
│   │   │   ├── PersonTimeline.tsx     # 个人履历垂直时间线
│   │   │   ├── PersonStats.tsx        # 活跃度雷达图/数字
│   │   │   └── PersonConnections.tsx  # 合作者列表
│   │   ├── conferences/
│   │   │   ├── ConferenceCard.tsx
│   │   │   └── ConferenceCalendar.tsx
│   │   └── shared/
│   │       ├── KaTeX.tsx              # KaTeX 渲染封装
│   │       ├── SearchBar.tsx          # 全局模糊搜索
│   │       └── DetailSidebar.tsx      # 右侧可折叠详情面板
│   │
│   ├── lib/
│   │   ├── types.ts                   # 所有 TypeScript 接口（详见下方 Schema）
│   │   ├── data.ts                    # YAML 加载 + slug 交叉引用解析
│   │   ├── graph.ts                   # YAML 数据 → D3 GraphNode[]/GraphLink[] 转换
│   │   ├── arxiv.ts                   # arXiv Atom API 客户端
│   │   └── search.ts                  # Fuse.js 封装
│   │
│   └── styles/globals.css             # Tailwind base + 自定义 CSS 变量
│
└── public/
    ├── photos/                        # 人物照片
    └── og-image.png
```

---

## 视觉设计："Academic Blackboard"

### 配色

| 用途 | 色值 | 说明 |
|------|------|------|
| 背景 | `#0a0a0f` | 近黑，微蓝底 |
| 卡片/面板 | `#14141f` | |
| 边框 | `#2a2a3a` | |
| 主文字 | `#e8e8f0` | |
| 次文字 | `#8888a0` | |
| Accent | `#6366f1` | indigo-500 |

### 节点颜色

| 实体类型 | 颜色 | 色值 |
|----------|------|------|
| 人物 | 琥珀 | `#f59e0b` |
| 概念 | 靛蓝 | `#6366f1` |
| 论文 | 翡翠 | `#10b981` |
| 机构 | 紫色 | `#8b5cf6` |
| Ghost node（未记录） | 半透明白 | `rgba(255,255,255,0.2)` |

### 边样式

| 关系类型 | 样式 |
|----------|------|
| 师生 | 实线，琥珀色 |
| 合作 | 虚线，靛蓝色，宽度 ∝ 论文数量 |
| 前置依赖 | 有向箭头，红色 |
| 引用 | 有向箭头，翡翠色 |

### 字体

- 标题/正文：Inter 或 Geist（Next.js 默认）
- 数学：KaTeX（Computer Modern 衍生）
- 中文：PingFang SC（`-apple-system` fallback）

### 布局

- 顶部导航栏 56px：People / Concepts / Timeline / Papers / Conferences / Literature
- 图页面：全屏 canvas 图 + 右侧 400px 可折叠 DetailSidebar（点击节点滑入）
- 列表页面：左侧筛选面板 + 主内容区

---

## 设计原则

**实用性 > 视觉震撼。信息必须直观，不追求单纯的花哨。**

- 每个视觉元素（颜色、大小、线型）必须编码具体信息，不做纯装饰
- 节点标签始终可读（不能被发光遮盖）
- hover 就能看到关键信息（不需要点击才能看）
- 图的布局要稳定，不能每次刷新都乱跳
- 信息密度要高：一屏能看到尽可能多的有用信息

### 具体约束
- 发光效果适度：用于区分选中/未选中状态，不是为了好看
- 暗色主题的目的是减少视觉噪音、突出数据，不是为了酷
- 字体大小不能为了美观而牺牲可读性
- 交互反馈要即时：hover/click 的响应不超过 100ms

---

## ForceGraph 核心组件规格

经 GPT + Gemini 两轮评审后最终确定方案。

### 方案演变 [三模型对比]
1. ~~D3 canvas 裸写~~ → 发光效果差，性能差
2. ~~react-force-graph-3d (Three.js + Bloom)~~ → **Gemini 二审否决**：3D 空间标签遮挡严重、悬停判定困难、文字阅读吃力，对学术工具是灾难级 UX
3. **最终方案：`react-force-graph-2d`（WebGL canvas 渲染）** — 2D 平面，高对比度节点 + 清晰文本标签，力导向图作为探索模式；列表/表格视图作为精确筛选模式

### 技术方案
```
Canvas 层（react-force-graph-2d，WebGL 模式）：
  - 节点渲染：高对比度圆形/矩形，颜色编码类型
  - 边渲染：实线/虚线/箭头，按关系类型区分
  - 力模拟：内置 d3-force
  - 缩放/平移/拖拽：内置

React HTML 层（position: absolute 覆盖）：
  - Tooltip (hover 时浮动显示关键信息)
  - DetailSidebar (click 时滑入，400px 右侧面板)
  - GraphControls (缩放/重置/筛选/时间滑块)
  - GraphLegend (图例)
  - 同步 Table/List Panel（精确筛选 + 阅读，可与图联动）
```

### 依赖
```bash
pnpm add react-force-graph-2d
# d3-force 作为内置依赖自动安装
```

### 视觉目标
- **全局视图**：暗色背景，节点标签始终清晰可读，颜色编码类型，大小编码重要性
- **聚焦视图**：点击节点后 React 渲染干净的学术信息卡片，信息密度高
- **列表视图**：同步提供 Table/List 作为图的替代，支持精确筛选排序
- **移动端**：不做图，直接 fallback 为按字母/年份排序的列表视图 + 基础搜索
- **核心原则**：每个视觉元素都传递信息（颜色=类型，大小=重要性，线型=关系种类），没有纯装饰元素

### 备选方案
如果 react-force-graph-2d 满足不了自定义需求，降级到 **Sigma.js v3** + `@react-sigma/core`（WebGL 图专用，shader 自定义上限更高）。

### Ghost Nodes

引用了但尚未创建 YAML 文件的 slug：
- 渲染为半透明、虚线边框
- 标签显示 slug + "（未记录）"
- 不参与力模拟的 charge（避免推开真实节点）

### 自适应力参数

节点数量不同时自动调整：
- < 20 nodes: chargeStrength=-300, linkDistance=120
- 20-50 nodes: chargeStrength=-200, linkDistance=80
- 50+ nodes: chargeStrength=-100, linkDistance=60

---

## 完整 Data Schema

### Person (`data/people/*.yaml`)

人物数据是本项目最重要的部分。要尽可能详细。

```yaml
slug: dubrovin                      # 文件名即 slug，全局唯一
name:
  en: Boris Dubrovin
  zh: 杜布罗文
born: 1950
died: 2019                          # null if alive
nationality: Russian
gender: male
photo_url: null                     # 相对路径 /photos/dubrovin.jpg 或外部 URL

# ★ 完整学术履历时间线（核心需求：越详细越好）
career_timeline:
  - period: "1968-1974"
    type: education                 # education | position | visit | award | event
    institution: moscow-state       # → meta/institutions.yaml
    role: "本科 + 研究生"
    advisor: novikov-sergei         # person slug
    notes: "1974年获副博士学位"
  - period: "1974-1993"
    type: position
    institution: moscow-state
    role: "讲师 → 教授"
  - period: "1993-2019"
    type: position
    institution: sissa
    role: 正教授
    notes: "1993年移居意大利"
  - period: "1998"
    type: award
    title: "ICM invited speaker (Berlin)"
  - period: "2019"
    type: event
    notes: "因 ALS 去世"

# 研究方向
research_areas:                     # concept slugs
  - frobenius-manifolds
  - integrable-systems
  - topological-field-theory

# 关系：师承
advisor: novikov-sergei             # person slug
students:                           # person slugs
  - guzzetti
  - cotti
  - mazzocco
  - grava
  - bertola
  - brini
  - cafasso
  - carlet
  - lorenzoni

# 关系：关键合作者（何时认识、合作主题）
key_collaborators:
  - person: zhang-youjin
    since: 2001
    met_context: "可能通过 SISSA/ICTP 访问"
    topic: "Frobenius manifolds & integrable hierarchies"
    papers_count: 15
  - person: novikov-sergei
    since: 1968
    met_context: "导师"
    topic: "Integrable systems, algebraic geometry"
    papers_count: 20

# ★ 学术活跃度指标
activity:
  total_papers: 120
  h_index: 45
  mathscinet_citations: 5000
  google_scholar_citations: null
  active_period: "1974-2019"
  peak_period: "1994-2010"
  phd_students: 19
  academic_descendants: 52
  last_arxiv_paper: "2019-xx-xx"    # 最后一篇 arXiv 论文日期

# 外部链接 + 消歧 ID [GPT建议]
external_ids:                        # ★ 实体消歧用 canonical IDs
  orcid: null
  openalex: null                     # "A1234567890"
  mathgenealogy: "83136"
  zbmath: null
  inspire: null
links:
  homepage: null
  google_scholar: null
  mathscinet: null
  arxiv_author: null

# 轶事/非学术信息/私人生活
personal_notes: |
  极具人格魅力的导师。晚年与疾病（ALS）斗争期间仍坚持研究。
  SISSA 设立 Boris Dubrovin Medal 纪念。

# 标签（用于筛选）
tags:
  - sissa-school
  - moscow-school
  - fields-student                   # 导师是 Fields 得主
```

### Concept (`data/concepts/*.yaml`)

```yaml
slug: frobenius-manifold
name:
  en: Frobenius Manifold
  zh: Frobenius 流形
aliases:
  - Dubrovin-Frobenius manifold
category: algebraic-structure        # algebraic-structure | geometric-structure | equation | conjecture | technique
difficulty: advanced                 # introductory | intermediate | advanced | research-frontier
discipline: math                     # ★ math | physics | both [Gemini建议]
year_introduced: 1994
introduced_by: [dubrovin]            # person slugs

# KaTeX 渲染
definition: |
  A complex manifold $M$ equipped with a flat metric $\eta$,
  a commutative associative multiplication $\circ$ on $TM$ satisfying
  $\eta(X \circ Y, Z) = \eta(X, Y \circ Z)$, a unit vector field $e$,
  and an Euler vector field $E$.

# ★ 对偶关系（镜像对称核心）[Gemini建议]
dual_to: null                        # 镜像对偶概念的 slug（如 A-model ↔ B-model）
notation_variants: null              # 不同圈子的记号习惯（物理 vs 数学）

# 依赖关系（形成有向图）
prerequisites:                       # 学这个之前需要懂的
  - flat-connection
  - wdvv-equations
leads_to:                            # 学完这个可以继续学的
  - dubrovin-connection
  - quantum-cohomology
  - tt-star-geometry
related:                             # 相关但无依赖关系
  - mirror-symmetry
  - integrable-hierarchy

key_people: [dubrovin, manin]        # person slugs
key_papers: ["hep-th/9407018"]       # arxiv IDs
```

### Paper (`data/papers/seminal.yaml` + `data/papers/arxiv-*.yaml`)

```yaml
# === seminal.yaml: 手工整理 ===
papers:
  - arxiv_id: "hep-th/9407018"
    doi: "10.1007/BFb0094793"         # ★ [GPT建议]
    title: "Geometry of 2D topological field theories"
    authors: [dubrovin]             # person slugs（在库中的用 slug，不在库中的用原始姓名）
    authors_raw: ["Boris Dubrovin"]  # 原始作者名（始终保留）
    year: 1996
    journal: "LNM 1620, Springer"
    type: published                  # ★ published | preprint | lecture_notes | unpublished_manuscript [Gemini建议]
    discipline: math                 # ★ math | physics | both [Gemini建议]
    categories: [hep-th, math-ph]
    concepts: [frobenius-manifold, wdvv-equations, dubrovin-connection]
    importance: seminal              # seminal | major | notable | regular
    citations_count: 1200
    cited_by: ["math/9801127"]       # arxiv IDs
    notes: "Frobenius 流形理论的奠基性文献，229 页"
    # ★ 数据溯源 [GPT建议]
    source: manual                   # manual | openalex | semantic-scholar | arxiv-fetch
    source_url: null
    last_verified: "2026-04-14"      # 最后人工校对日期

# === arxiv-YYYY-MM-DD.yaml: 自动生成 ===
fetch_date: "2026-04-14"
query_categories: [math-ph, math.AG, math.QA, hep-th, math.DG, math.SG]
papers:
  - arxiv_id: "2604.XXXXX"
    doi: null
    title: "..."
    authors_raw: ["First Last"]
    year: 2026
    abstract: "..."
    type: preprint
    categories: [math-ph]
    primary_category: math-ph
    relevance_score: 0.85            # 自动计算
    matched_people: []               # 匹配到的 person slugs
    matched_concepts: []             # 匹配到的 concept slugs
    reviewed: false                  # 人工标记是否已审阅
    source: arxiv-fetch
```

### Timeline Event (`data/timeline/events.yaml`)

```yaml
events:
  - slug: kontsevich-icm-1994
    date: "1994-08"
    precision: month                 # year | month | day
    title:
      en: "Kontsevich's ICM talk: Homological Mirror Symmetry"
      zh: "Kontsevich ICM 报告：同调镜像对称"
    description: |
      Proposes HMS at ICM Zurich:
      $D^b\mathrm{Coh}(X) \cong D^\pi\mathrm{Fuk}(\check{X})$
    people: [kontsevich]             # person slugs
    concepts: [homological-mirror-symmetry]
    papers: ["alg-geom/9411018"]
    era: modern                      # prehistory | classical | modern | contemporary
    importance: milestone            # milestone | major | notable
```

### Conference (`data/conferences/`)

数据模型覆盖全球，UI 默认聚焦国内 [GPT建议：不硬编码地域限制]。

```yaml
# === recurring.yaml: 周期性会议系列 ===
series:
  - slug: cim-workshop
    name:
      en: "CIM Workshop on Integrable Systems"
      zh: "清华丘成桐数学科学中心可积系统研讨会"
    organizers: [xu-xiaomeng, zhang-youjin]
    institution: tsinghua
    frequency: annual                # annual | biennial | irregular
    typical_month: 7
    location: 北京
    url: null
    relevance: high                  # high | medium | low
    region: china                    # ★ china | asia | europe | americas | global（用于筛选）
    topics: [integrable-systems, isomonodromy, frobenius-manifolds]
    notes: null

# === events-2026.yaml: 具体会议实例 ===
events:
  - slug: ustc-mirror-2026
    series: null                     # 关联 recurring slug，或 null
    name:
      en: "USTC Workshop on Mirror Symmetry and Related Topics"
      zh: "中科大镜像对称及相关课题研讨会"
    date_start: "2026-07-15"
    date_end: "2026-07-19"
    location: 合肥
    institution: ustc
    organizers: []                   # person slugs
    invited_speakers: []             # person slugs
    topics: [mirror-symmetry, homological-mirror-symmetry]
    url: null
    source: null                     # 数据来源标注
    notes: null
```

### Connection (`data/connections/*.yaml`)

```yaml
# === advisor-student.yaml ===
edges:
  - source: novikov-sergei
    target: dubrovin
    type: advisor-student
    year: 1976
    institution: moscow-state

# === coauthorship.yaml ===
edges:
  - source: zhang-youjin
    target: liu-siqi
    type: coauthor
    weight: 56                       # 论文数
    period: "2000-present"

# === institutional.yaml ===
edges:
  - source: dubrovin
    target: guzzetti
    type: institutional
    institution: sissa
    period: "1993-2019"
```

### Institution (`data/institutions/*.yaml`) — ★ 新增

机构作为一等实体，支持地图视图和人物流动可视化。

```yaml
slug: sissa
name:
  en: "International School for Advanced Studies (SISSA)"
  zh: "国际高等研究院"
  local: "Scuola Internazionale Superiore di Studi Avanzati"
type: research-institute             # university | research-institute | center
country: Italy
city: Trieste
location:                            # 地图标点
  lat: 45.6495
  lng: 13.7768
founded: 1978
url: "https://www.sissa.it/"

# 与本领域的关联
relevance: high                      # high | medium | low
research_groups:
  - name: "Mathematical Physics"
    topics: [integrable-systems, frobenius-manifolds, random-matrices]
    current_members: [guzzetti]      # person slugs（当前在职）
    past_members: [dubrovin, cotti, mazzocco, grava, bertola, brini]

# 重要事件
events:
  - year: 1993
    description: "Dubrovin 加入，建立 Frobenius 流形研究中心"
  - year: 2020
    description: "设立 Boris Dubrovin Medal"

notes: |
  Dubrovin 1993-2019 年间在此培养了整个 Frobenius 流形学派。
  Dubrovin Medal 每两年颁发一次。
```

### Open Problem / Research Program (`data/problems/*.yaml`) — ★ 新增

追踪领域内活跃的开放问题，有状态、有进展时间线。

```yaml
slug: hms-general-cy
name:
  en: "Homological Mirror Symmetry for general Calabi-Yau manifolds"
  zh: "一般 Calabi-Yau 流形的同调镜像对称"
status: open                         # open | partially-solved | solved | abandoned
importance: millennium               # millennium | major | significant | niche
year_proposed: 1994
proposed_by: [kontsevich]

description: |
  Kontsevich 1994 年 ICM 报告提出的猜想的完整版本。
  已在特殊情形证明（toric, abelian varieties, quartic surface），
  一般情形仍然开放。

# 依赖/相关
prerequisites: [homological-mirror-symmetry, derived-category, fukaya-category]
related_problems: [syz-metric, gamma-conjecture]
key_people: [kontsevich, seidel, sheridan, abouzaid]

# 进展时间线
progress:
  - date: "1994"
    description: "Kontsevich 提出猜想"
    papers: ["alg-geom/9411018"]
  - date: "2003"
    description: "Seidel 证明 quartic surface 情形"
    papers: []
  - date: "2009"
    description: "Sheridan 证明 Fermat hypersurface"
    papers: []
  - date: "2015"
    description: "Abouzaid-Sheridan framework for general type"
    papers: []

# 当前前沿
current_approaches:
  - "SYZ + family Floer cohomology"
  - "Categorical formal geometry"
  - "Non-commutative Hodge structures"

notes: null
```

### Seminar / Reading Group (`data/seminars/recurring.yaml`) — ★ 新增

比 conference 粒度更细，追踪国内各组的常规活动。

```yaml
seminars:
  - slug: tsinghua-integrable
    name:
      en: "Tsinghua Integrable Systems Seminar"
      zh: "清华可积系统讨论班"
    institution: tsinghua
    organizers: [zhang-youjin, liu-siqi]
    frequency: weekly                # weekly | biweekly | monthly | irregular
    typical_day: "Thursday"
    typical_time: "14:00"
    location: "清华数学系 A304"
    url: null
    topics: [integrable-systems, frobenius-manifolds, wdvv-equations]
    active: true
    notes: null

  - slug: pku-stokes
    name:
      en: "PKU Stokes Phenomenon Reading Group"
      zh: "北大 Stokes 现象读书班"
    institution: pku
    organizers: [xu-xiaomeng]
    frequency: biweekly
    topics: [stokes-phenomenon, isomonodromy, quantum-groups]
    active: true
    notes: "了解一个组在做什么的最好窗口"
```

---

## 现有数据源（可直接迁移）

### 1. `~/ai/workspace/frobenius-manifolds/notes/academic-network.md`

**内容：** 20+ 人物的完整数据，包括：
- **学术谱系树**（L8-44）：Shafarevich → Manin, Novikov → Dubrovin → 9 students, Brieskorn → K.Saito/Hertling, Hitchin → Boalch, Alekseev → Xu → 唐乾
- **共著邻接矩阵**（L53-65）：9 人 × 9 人的论文数量矩阵。关键 pair：Zhang-Liu(56), Cotti-Guzzetti(14), Dubrovin-Zhang(15)
- **Xu 的合作者列表**（L76-88）：唐乾(4), Sheng(6), Lang(5), Alekseev(3), Lin(3), Ikeda(3), Neitzke(1), Toledano-Laredo(1), Wang(2)
- **现任职位表**（L89-103）：10 人的机构、职位、主页 URL
- **网络拓扑分析**（L113-139）：两个 cluster（SISSA/Dubrovin 学派 vs Xu/Alekseev 学派），唐乾是桥梁节点

### 2. `~/ai/workspace/frobenius-manifolds/CLAUDE.md` L82-138

**内容：** 五层知识层级结构，可直接映射为概念依赖图：
- 第一层：Frobenius 流形基础（3 篇核心文献）
- 第二层：WDVV 方程与可积系统（4 篇）
- 第三层：tt* geometry 与 Stokes 现象（3 篇）
- 第四层：Stokes 矩阵、Frobenius 流形与量子群（4 篇）
- 第 4.5 层：Gamma 猜想与 Dubrovin 猜想精化（6 篇）
- 第五层：具体计算与分类（3 篇）
- 补充层：Painlevé 方程（2 篇）

### 3. `~/ai/workspace/frobenius-manifolds/references/`

94 个参考文献文件，可作为 seminal.yaml 的种子数据。

---

## 外部数据源与 API

API Key 统一存储：`~/ai/data/keys/api-keys.json`
完整索引：`~/ai/data/keys/README.md`（40+ API 按领域分类）

### 核心学术 API（数据抓取脚本直接使用）

| API | 用途 | 限流 | 调用速查 |
|-----|------|------|---------|
| **arXiv** | 论文监控、摘要、PDF 链接 | 3 秒间隔 | `export.arxiv.org/api/query?search_query=au:{作者}&max_results=10` |
| **Semantic Scholar** | 引用网络、h-index、相关论文推荐 | 1 次/秒 | `api.semanticscholar.org/graph/v1/paper/search?query={q}&fields=title,year,citationCount,authors,abstract,externalIds` |
| **OpenAlex** | 2.5 亿论文，作者画像/机构/主题/引用趋势 | 需免费 Key | `api.openalex.org/works?filter=author.id:{id}&per_page=50` |
| **zbMATH** | 数学专属，专家评审、MSC 分类 | 无硬性限流 | `api.zbmath.org/v1/document/_search?search_string=au:{作者}&results_per_page=10` |
| **INSPIRE-HEP** | 数学物理文献核心库 | 无限流 | `inspirehep.net/api/literature?q=a%20{作者}&size=10` |
| **CrossRef** | DOI 元数据、引用格式 | 无限流 | `api.crossref.org/works/{doi}` |
| **Unpaywall** | 免费全文 PDF 链接 | 无限流 | `api.unpaywall.org/v2/{doi}?email={email}` |

### 已知作者 ID

| 人物 | OpenAlex ID | 说明 |
|------|------------|------|
| 徐晓濛 | A5019142880 | `api.openalex.org/authors/A5019142880` |
| 其他 | 待查 | 用论文标题搜索获取 |

### 参考级数据源

| 数据源 | 用途 | 接入方式 |
|--------|------|---------|
| **nLab** | 概念详情补充（范畴论/同伦论 wiki） | WebFetch `ncatlab.org/nlab/show/{page}` |
| **DLMF** | 特殊函数参考，Painlevé = Ch.32 | WebFetch `dlmf.nist.gov/32` |
| **Wikipedia** | 人物/机构/概念基础信息 | `en.wikipedia.org/w/api.php` |
| **Math Genealogy** | 学术谱系 | 页面抓取 `genealogy.math.ndsu.nodak.edu` |

### 脚本 ↔ API 映射

| 脚本 | 使用的 API | 输出 |
|------|-----------|------|
| `scripts/fetch-arxiv.ts` | arXiv Atom API | `data/papers/arxiv-YYYY-MM-DD.yaml` |
| `scripts/fetch-citations.ts` | Semantic Scholar + OpenAlex | 补充 `data/papers/seminal.yaml` 的引用数据 |
| `scripts/fetch-people.ts` | OpenAlex + zbMATH + Math Genealogy | 补充 `data/people/*.yaml` 的活跃度指标 |
| `scripts/fetch-conferences.ts` | 网页抓取（国内数学会议网站） | `data/conferences/events-YYYY.yaml` |
| `scripts/validate-data.ts` | 无（本地校验） | slug 引用完整性检查 |

### 数据丰富化流程

人物数据可以从 API 半自动填充：
1. **OpenAlex** → `activity.total_papers`, `activity.cited_by_count`, `activity.h_index`, `activity.last_arxiv_paper`
2. **zbMATH** → MSC 分类码、专家评审、关键词
3. **Semantic Scholar** → 引用网络、合作者图谱
4. **Math Genealogy** → 师生关系、学术后代数
5. **INSPIRE-HEP** → 数学物理领域的额外文献覆盖
6. 最终由人工校对，标记 `[待验证]` → `[已核实]`

---

## 实施计划

### Phase 1：脚手架 + 人物关系网络 ← 当前阶段

**目标：** 启动 `pnpm dev` 后能看到可交互的人物关系力导向图。

#### 步骤 1.1：项目初始化
```bash
pnpm create next-app . --typescript --tailwind --app --src-dir --use-pnpm
pnpm add react-force-graph-2d js-yaml gray-matter fuse.js katex next-themes rehype-katex
pnpm add -D @types/js-yaml @types/katex
```
- next.config.ts: SSG 为主，Dashboard 页面用 ISR (revalidate: 3600)
- tailwind.config.ts: 自定义色值（Academic Blackboard 配色）
- globals.css: 暗色主题 CSS 变量

#### 步骤 1.2：目录结构
创建完整的 `data/`（含新增的 institutions/, problems/, seminars/）、`content/`、`scripts/`、组件目录。
创建 GEMINI.md、AGENTS.md。

#### 步骤 1.3：类型系统 (`src/lib/types.ts`)
定义所有 TypeScript 接口：Person, Concept, Paper, TimelineEvent, Conference, Connection, Institution, OpenProblem, Seminar, GraphNode, GraphLink, 等。

#### 步骤 1.4：数据加载层 (`src/lib/data.ts`)
- 读取 `data/` 下所有 YAML 文件
- 解析 slug 交叉引用（person.students[] 里的 slug → 实际 Person 对象）
- 缺失 slug 不报错，生成 ghost node（console.warn）
- 导出 `getAllPeople()`, `getPerson(slug)`, `getAllConnections()`, `getAllInstitutions()` 等函数

#### 步骤 1.5：图数据转换 (`src/lib/graph.ts`)
- `buildPeopleGraph()`: Person[] + Connection[] → { nodes: GraphNode[], links: GraphLink[] }
- `filterByYear(nodes, links, year)`: 时间滑块过滤函数（为 Phase 1b 预留）
- 节点属性：id, label, type, radius, color, data (原始 Person)
- 边属性：source, target, type, weight, color, dash, data (原始 Connection)

#### 步骤 1.6：种子数据
从 `academic-network.md` 迁移至少 10 个人物的 YAML 文件：
- dubrovin, novikov-sergei, manin-yuri
- xu-xiaomeng, tang-qian
- zhang-youjin, liu-siqi
- guzzetti, cotti, mazzocco
- boalch, sabbah, hertling
加上 advisor-student.yaml, coauthorship.yaml, 和 3-5 个 institution YAML。

#### 步骤 1.7：ForceGraph.tsx
按上方规格实现核心 canvas 力导向图组件。

#### 步骤 1.8：PeopleNetwork.tsx
配置 ForceGraph 的人物图参数：
- 节点颜色按 nationality/cluster 区分
- 边样式按 advisor-student/coauthor 区分
- 节点大小 ∝ academic_descendants 或 total_papers

#### 步骤 1.9：人物详情页 (`src/app/people/[slug]/page.tsx`)
- PersonTimeline：垂直时间线展示 career_timeline
- PersonStats：活跃度数字
- PersonConnections：合作者列表（链接到其他人物页）

#### 步骤 1.10：根布局 + Dashboard
- layout.tsx：导航栏（含所有页面入口）、暗色主题、KaTeX CSS
- page.tsx：统计数字 + 各模块快速入口卡片（Dashboard 的动态面板在 Phase 4 做）

### Phase 1b：时间滑块 + 地图视图

在 Phase 1 的人物图上叠加两个高冲击力特性：

1. **TimeSlider 组件**：底部滑块 1950–2026，拖动时动态过滤图中节点/边
2. **InstitutionMap 页面**：世界地图 + 机构标点 + 人物流动弧线
3. 种子 Institution 数据（SISSA, Tsinghua, PKU-BICMR, Moscow State, Bonn 等）

### Phase 2：概念知识图谱

1. 从五层知识层级结构迁移 15-20 个概念到 `data/concepts/`
2. **概念新增 contributions 字段**：founder / major / promoter / applier
3. `ConceptMap.tsx` — ForceGraph 配置层，有向箭头表示前置依赖
4. "学习路径"模式：点击概念 → 高亮其完整前置依赖链（递归上溯）
5. 概念详情页：KaTeX 渲染定义 + 前置/后续列表 + 关联人物（含贡献类型）和论文
6. 难度颜色编码：introductory=绿, intermediate=蓝, advanced=紫, research-frontier=红
7. TimeSlider 复用：拖动看概念何时出现

### Phase 3：时间线 + 学术会议 + Seminar + Open Problems

1. 种子 30-40 个里程碑事件到 `data/timeline/events.yaml`
2. `Timeline.tsx` — D3 水平可滚动时间线
   - 年代分区：prehistory / classical / modern / contemporary
   - 缩放级别：decade → year → month
   - 点击事件 → 弹出详情卡（关联人物、概念、论文）
3. `conferences/page.tsx` — 学术会议页面（聚焦国内）
   - 日历视图（年度）+ 列表视图
   - 按机构/话题筛选
   - 周期性会议系列折叠展示
   - **会议 ↔ 人物关联**：谁在哪个会议做了报告
4. `scripts/fetch-conferences.ts` — 从数学会议网站抓取信息
5. **Seminar 页面**：国内各组的常规讨论班列表（了解各组在做什么的窗口）
6. **Open Problems 看板**：状态标签 (open/partially-solved/solved) + 进展时间线

### Phase 4：arXiv 监控 + Dashboard 动态化

1. `scripts/fetch-arxiv.ts` — 查询 arXiv Atom API
   - 类别：math-ph, math.AG, math.QA, hep-th, math.DG, math.SG
   - 输出：`data/papers/arxiv-YYYY-MM-DD.yaml`
2. 相关度评分：
   - 关键词匹配 concepts 库 → 0-1 分
   - 作者匹配 people 库 → 加 0.3 分
   - 综合 relevance_score
3. `ArxivFeed.tsx` — 可筛选论文列表
   - 按相关度排序
   - 按类别/日期/作者筛选
   - "已审阅"标记
4. 定时执行：GitHub Actions 每日 cron 或本地 launchd
5. **Dashboard 动态化**：最近 arXiv 论文 + 即将到来的会议/seminar + 活跃研究者 + 热门概念 + Open problem 进展

### Phase 5：文献引用网络 + 对比视图

1. 种子 30-50 篇经典论文到 `data/papers/seminal.yaml`（含手动标注的引用关系）
2. **Paper 新增 semantic_relations 字段**：generalizes / corrects / alternative-proof / surveys
3. `scripts/fetch-citations.ts` — Semantic Scholar API 补充引用数据
4. `CitationNetwork.tsx` — ForceGraph 配置层
   - 节点大小 ∝ citations_count
   - 有向边 = 引用方向，颜色/样式按 relation_type 区分
   - importance 着色：seminal=金, major=银, notable=铜
5. 论文详情页：引用/被引列表（含语义关系标签），关联概念和人物
6. **对比视图（Compare）**：选两人或两概念并排，高亮共同点/差异/潜在合作机会

---

## 丰富关系层（跨实体连接）

除了 `connections/*.yaml` 的人-人关系，以下跨实体关系通过各实体 YAML 中的 slug 引用实现：

| 关系 | 存储位置 | 说明 |
|------|---------|------|
| Person ↔ Concept | person.research_areas, concept.key_people | 双向 |
| Person → Concept (贡献类型) | concept.contributions[] | ★ 新增字段：`{person, role: founder\|major\|promoter\|applier}` |
| Person ↔ Paper | paper.authors, person 反向索引 | |
| Person ↔ Institution | person.career_timeline[].institution, institution.research_groups[].members | 双向 |
| Person ↔ Conference | conference.events[].invited_speakers, conference.events[].organizers | |
| Person ↔ Seminar | seminar.organizers | |
| Concept ↔ Paper | paper.concepts, concept.key_papers | 双向 |
| Concept ↔ Problem | problem.prerequisites, problem.related_problems | |
| Paper → Paper | paper.cited_by + 语义关系 | ★ 新增 `relation_type: cites\|generalizes\|corrects\|alternative-proof\|surveys` |
| Institution ↔ Institution | 人物流动弧线 | 通过 person.career_timeline 推导 |

### Concept 新增字段：contributions

```yaml
# 在 concept YAML 中新增
contributions:
  - person: dubrovin
    role: founder          # founder | major | promoter | applier
    description: "1994年引入 Frobenius 流形概念"
  - person: manin
    role: promoter
    description: "推广到量子上同调框架"
```

### Paper 新增字段：semantic_relations

```yaml
# 在 seminal.yaml 的 paper 条目中新增
semantic_relations:
  - target: "math/9801127"
    type: generalizes       # cites | generalizes | corrects | alternative-proof | surveys
    description: "推广到高维情形"
```

---

## 时间滑块（TimeSlider）— 动态快照 ★★

这是最有冲击力的特性。所有图视图（People, Concepts, Literature）都支持时间滑块。

### 行为
- 底部水平滑块，范围 1950–2026
- 拖到某个年份 Y 时，图仅显示在 Y 年时已存在的实体和关系：
  - **人物**：born ≤ Y 且 (died == null || died ≥ Y)，且 career_timeline 中有 Y 年内的条目
  - **关系**：advisor-student 仅当 year ≤ Y；coauthor 仅当 period 包含 Y
  - **概念**：year_introduced ≤ Y
  - **论文**：year ≤ Y
- 节点/边平滑淡入淡出（300ms）
- 可以按"播放"自动推进（每秒 1 年或 5 年）

### 数据要求
需要所有关系都带时间戳。现有 schema 已支持：
- person.career_timeline[].period
- connection.year / connection.period
- concept.year_introduced
- paper.year

### 实现要点
- ForceGraph 增加 `timeFilter: number | null` prop
- graph.ts 增加 `filterByYear(nodes, links, year)` 函数
- 模拟不重启，只修改节点/边的 opacity 和 charge 参与度

---

## 地图视图（InstitutionMap）★

### 行为
- 世界地图底图（TopoJSON 或 简化 GeoJSON，不需要完整地理细节）
- 机构作为标点，大小 ∝ 在本领域的人物数量
- 人物流动弧线：从 career_timeline 推导出 institution A → institution B 的迁移，画弧线
  - 弧线颜色按时代区分
  - 配合时间滑块可以看到人才流动的动态变化
- 点击机构 → 弹出该机构的人物列表、活跃 seminar、相关会议

### 技术
- D3 + TopoJSON 渲染（d3-geo），复用 canvas 模式
- 或用轻量级地图库如 `react-simple-maps`（SVG，节点少时性能够用）

---

## 对比视图（Compare）★

### 行为
- 选择两个同类实体（两个人 / 两个概念）并排展示
- 高亮共同点：共同合作者、共同引用、共同研究方向
- 高亮差异：各自独有的连接
- 用于发现潜在合作机会（如 academic-network.md 中分析的"网络空洞"）

### 实现
- URL: `/compare?a=dubrovin&b=xu-xiaomeng`
- 不需要独立页面，可作为 sidebar 的一个模式

---

## "谁在做什么"实时面板（Dashboard）★

Dashboard 首页不只是静态入口，而是领域动态快照：

- **最近 7 天 arXiv 论文**（按相关度排序前 10）
- **即将到来的会议/seminar**（未来 30 天）
- **活跃研究者**：最近 6 个月发论文最多的人
- **热门概念**：最近论文中被提到最多的 concept slugs
- **Open problem 进展**：状态最近有更新的问题

---

## 关键架构决策

1. **react-force-graph-2d + React 分工** [三模型对比]：力导向图用 `react-force-graph-2d`（WebGL canvas），React 管理控件/tooltip/面板/列表视图。所有图页面同步提供 Table/List 作为精确筛选替代。移动端直接 fallback 为列表。
2. **SSG + ISR 混合部署** [GPT+Gemini 建议]：人物/概念等慢变数据用纯 SSG；Dashboard 的 arXiv Feed 和会议日历用 ISR（1h revalidate）或客户端 fetch 预生成 JSON。
3. **KaTeX 服务端预渲染** [Gemini建议]：用 `rehype-katex` 在 build 时编译公式为 HTML+CSS，避免客户端渲染的布局跳动。
4. **Ghost nodes**：引用了但尚未创建 YAML 文件的 slug 渲染为半透明"未记录"节点，不报错。支持渐进填充数据。
5. **arXiv 是独立脚本**：cron 运行 → 写 YAML → git push → 触发重新部署。
6. **slug 是唯一标识**：所有实体用 slug 交叉引用，文件名即 slug。每个实体同时维护 `external_ids`（ORCID, OpenAlex, DOI 等）用于消歧 [GPT建议]。
7. **时间是一等维度**：所有关系都带时间戳，支持 TimeSlider 按年过滤。时间字段支持不确定性（`circa`、仅年份、未知结束）[GPT建议]。
8. **机构是一等实体**：不只是 meta 索引，有自己的页面、地理坐标、历史事件。
9. **关系有语义**：论文间有 generalizes/corrects/alternative-proof 等类型；人物对概念有 founder/major/promoter/applier 等角色；概念间有 `dual_to` 对偶关系 [Gemini建议]。
10. **数据溯源** [GPT建议]：每个实体/事实都携带 `source`、`last_verified`。页面展示 `last_updated` 时间戳，用户知道数据多新。
11. **会议全球建模，中国聚焦展示** [GPT建议]：数据模型覆盖全球，UI 默认筛选/高亮国内会议。
12. **每个详情页底部放 "Edit on GitHub" 按钮** [Gemini建议]：降低同行贡献门槛，这决定平台生命力。
13. **搜索渐进升级**：Phase 1 用 Fuse.js，数据量超 2000 实体后迁移到 Orama（前端预编译索引）[GPT+Gemini 建议]。

---

## 评审记录 [三模型对比]

### 2026-04-14 GPT+Gemini 联合评审

**采纳：**
- 3D→2D 降级 + 列表视图 (GPT+Gemini)
- Concept `dual_to` + `discipline` 字段 (Gemini) — 镜像对称核心是对偶
- Paper `type`(published/preprint/lecture_notes/unpublished) (Gemini) — 灰色文献很重要
- Paper `doi` + `discipline` 字段 (GPT+Gemini)
- KaTeX 服务端预渲染 `rehype-katex` (Gemini)
- 数据溯源 `source`/`last_verified` (GPT)
- 实体消歧 `external_ids` (GPT) — ORCID, OpenAlex, Math Genealogy ID
- 会议全球建模+中国筛选 (GPT)
- "Edit on GitHub" 按钮 (Gemini)
- 移动端降级为列表视图 (Gemini)
- SSG + ISR 混合 (GPT+Gemini)
- 搜索升级路径 Fuse.js → Orama (GPT+Gemini)

**不采纳：**
- 颜色按数学/物理学科分 (Gemini) — 当前按实体类型分更直观
- 完整 curation UI: review queue, conflict resolution (GPT) — 太重，用 GitHub Issues + PR
- Software/Tool 实体 (Gemini) — 优先级低，Phase 5+

---

## 多 AI 协作

三家（Claude/Gemini/Codex）共管项目。
- 写入文件时标注 `[Claude]`/`[Gemini]`/`[Codex]`
- GEMINI.md 和 AGENTS.md 与本文件同步维护
- 数据文件（YAML）任何一家都可以编辑

### 跨模型交叉验证

通过 MCP 工具 `mcp__multi-ai__ask` 可调用 GPT 和 Gemini：

| model 参数 | 说明 |
|-----------|------|
| `gpt-5.4` | GPT（当前走 foxcode 中转，备用 timicc） |
| `gemini-3.1-pro-preview` | Gemini（当前走 foxcode 中转） |
| `compare` | 同时问 GPT + Gemini，对比回答 |

**何时应该调用：**
- 技术选型有争议时（如 Phase 1 中 D3 vs react-force-graph 的决策就是 Gemini 建议的）
- 数据事实不确定时（人物生卒年、学术谱系等，标 `[待验证]` 的内容）
- 架构设计的关键决策点（让另一个模型做 code review 或提供替代方案）
- 后果严重的判断（如修改共享配置、删除数据文件前）

**注意事项：**
- 每次调用是独立的（无对话历史），需要在 prompt 中给足上下文
- 标注来源：`[Claude]` / `[Claude + GPT]` / `[Claude + Gemini]` / `[三模型对比]`
- 中转站偶尔不稳定（超时/限流），非关键路径可跳过

---

## 开发命令

```bash
pnpm dev          # 开发服务器 http://localhost:3000
pnpm build        # 静态导出到 out/
pnpm validate     # 数据校验：检查 slug 引用完整性、YAML 格式
```

## 验证清单

### Phase 1 完成标准
- [ ] `pnpm dev` 启动成功
- [ ] People 页面：力导向图正常渲染，节点可拖拽/点击/缩放
- [ ] 点击人物节点 → 右侧 sidebar 展示完整履历时间线
- [ ] 点击人物名字 → 跳转详情页
- [ ] Ghost nodes 正常显示（半透明）
- [ ] 暗色主题正常
- [ ] `pnpm build` 静态导出成功

### Phase 1b 完成标准
- [ ] 时间滑块：拖到 2000 年，只显示 2000 年时在世/活跃的人物
- [ ] 地图视图：机构在世界地图上正确标点
- [ ] 人物流动弧线正常渲染

### 全局完成标准
- [ ] 所有 slug 交叉引用无断链（`pnpm validate`）
- [ ] 每种图视图都支持 TimeSlider
- [ ] Dashboard 展示实时动态信息
