# Mirror Symmetry Atlas

镜像对称及相关领域的交互式知识平台。

## 核心规则

### 语言
**UI 和数据内容都用中文。** 导航、标题、按钮、图例、概念定义、personal_notes 全部中文。
- 人名优先显示 `name.zh`，无中文名时显示英文
- 概念 `definition` 字段用中文撰写，LaTeX 公式保留
- 学术专有名词（Frobenius manifold、Stokes phenomenon 等）保留英文
- YAML 字段名保持英文（slug、type 等结构性字段）

### 数据及时更新
**用户提到的任何人物、会议、机构、关系信息，必须立即写入对应 YAML 文件。**
- 新人物 → `data/people/{slug}.yaml`，信息不足时建 stub 标 `[待补充]`
- 新关系 → `data/connections/` 对应文件追加
- 新会议 → `data/conferences/events-{YYYY}.yaml`
- 已有人物的新信息 → 更新对应 YAML 字段
- 不等收尾，获知即写入

### 数据来源与可追溯
**关键事实必须附来源链接。** 人物 YAML 底部维护 `sources` 列表：
```yaml
sources:
  - label: "Math Genealogy"
    url: "https://www.mathgenealogy.org/id.php?id=51292"
  - label: "Faculty page (Wayback)"
    url: "https://web.archive.org/web/2024/..."
```
- `external_ids`（openalex, mathgenealogy, orcid）在前端自动生成链接，不需重复列入 sources
- 容易失效的页面（个人主页、faculty page）优先用 Wayback Machine 存档 URL
- 标 `[待验证]` 的事实应尽量附上来源以便后续核实
- 查 arXiv 限定 math 分类以避免重名；查 OpenAlex 注意 profile 碎片化/重名污染
- 当前机构以 arXiv 最新论文 affiliation 为准，不信 OpenAlex last_known_institution
- `personal_notes` 只写实质信息，不写数据源质量问题
- **论文列表**：每个人物应有 `publications` 字段，列出全部 arXiv 论文（id + title + year + coauthors slugs）。用 `scripts/fetch-arxiv-by-author.py` 拉取。常见名字用 `--filter-coauthors` 或限定 `--cats` 过滤
- **充实方法论详见 `docs/enrichment-methodology.md`**：每个人物必须过 checklist（当前机构、奖项、师承、论文列表、合作者、传记）

### 设计原则
- **实用性 > 视觉震撼**，每个视觉元素编码具体信息
- 暗色主题 "Academic Blackboard"，配色见 `src/app/globals.css`
- Ghost nodes：引用但未建档的 slug 渲染为半透明节点

## 技术栈
Next.js 16 (App Router) + TypeScript + Tailwind v4 + react-force-graph-2d + js-yaml + Fuse.js

## 目录结构
```
data/           # YAML 数据（people/, concepts/, papers/, connections/, institutions/, conferences/, ...）
docs/design.md  # 完整设计文档（schema、配色、phase 计划、评审记录）
src/app/        # 页面路由
src/components/ # React 组件（graphs/, person/, shared/）
src/lib/        # 数据加载(data.ts)、图转换(graph.ts)、搜索(search.ts)、类型(types.ts)
scripts/        # 数据抓取脚本
```

## 命令
```bash
pnpm dev          # 开发 http://localhost:3000
pnpm build        # 静态导出
```

## 实施进度
- [x] Phase 1: 脚手架 + 人物关系网络（力导向图、详情页、时间滑块）
- [ ] Phase 1b: 地图视图 + 机构人物流动弧线
- [x] Phase 2: 概念知识图谱（有向依赖图 + 学习路径 + KaTeX 中文定义）
- [ ] Phase 3: 时间线 + 会议 + Seminar + Open Problems
- [ ] Phase 4: arXiv 监控 + Dashboard 动态化
- [ ] Phase 5: 文献引用网络 + 对比视图

详细设计、完整 schema、配色规范、评审记录见 → `docs/design.md`
