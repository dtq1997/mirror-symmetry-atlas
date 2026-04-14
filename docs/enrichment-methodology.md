# 人物数据充实方法论

每次新增或更新人物时，按以下 checklist 逐项检查。不能只靠一个数据源。

## 核心 Checklist

### 1. 当前机构（最高优先级）
- **arXiv 最新论文的 affiliation** → 最可靠的当前位置
- 机构 faculty page 验证
- 不要用 OpenAlex last_known_institution（经常过期/错误）

### 2. 学术奖项（中国数学家必查）
搜索 `"{姓名}" 奖` 或 `"{name}" prize award`：
- 钟家庆数学奖（中国数学会，优秀博士论文）
- 陈省身数学奖
- NSFC：杰出青年基金、优秀青年基金
- 求是杰出青年学者奖
- 长江学者
- 国务院政府特殊津贴
- 教育部自然科学奖
- ICM invited speaker
- Dubrovin Medal
- Sloan Fellowship（海外）

### 3. 教育与师承
- Math Genealogy Project（ID 查询）
- 机构学位论文数据库
- 导师的 faculty page（通常列出学生）
- 如果以上都找不到，从合著模式推断但标 [待验证]

### 4. 论文数与引用
- arXiv（限 math 分类）→ 最准的数学论文计数
- OpenAlex → 补充引用数/h-index，但注意 profile 碎片化和重名污染
- 不要在 personal_notes 里写数据质量问题

### 5. 合作者
- arXiv 论文共著列表
- 不要只看 OpenAlex 的 co-author 数据

### 6. 个人传记
- 机构官方介绍
- 新闻报道（获奖、任命）
- 维基百科

## 质量规则

- `personal_notes` 只写对用户有价值的实质信息，不写数据源的技术问题
- 标 `[待验证]` 的信息尽量附 source URL
- 每次更新一个人时，顺便检查其合作者是否也需要更新（举一反三）

## 防错规则

- **奖项必须从原始表格逐行确认**：不能从搜索摘要里推断"某人获某奖"——同一页面上不同行的人名和奖名会被 agent 张冠李戴。必须 fetch 原始页面，确认人名和奖名在同一行/同一条目。
- **机构官方页面优先**：中国数学家的奖项去其所在机构的教师奖励/人才项目页面查，比 web search 摘要可靠得多。关键页面：
  - PKU 数学: `math.pku.edu.cn/bks/jxjl/jsjx0/index.htm`（教师奖项完整列表）
  - 清华数学: `math.tsinghua.edu.cn`
  - USTC 数学: `math.ustc.edu.cn`
- **不信 agent 对表格数据的解读**：agent 从 HTML 表格提取信息时错误率高，对关键事实（奖项、职称、年份）应手动验证或用结构化方式解析。
- **写入前复查**：关键事实（奖项、职称变更、师生关系）写入 YAML 前，至少有一个明确的 source URL 且已确认信息在该 URL 的正确位置。
- **内网 faculty 页面**：部分高校（如 HUST）的 faculty 系统 WebFetch 抓不到（TLS 问题），用 `curl -sL http://...` 能抓到。提取文本后 grep 关键词（博士、博士后、教育经历等）。
- **arXiv 精确搜索**：用 `au:"Name"` 双引号格式，限定 `cat:math-ph OR cat:math.AG` 等分类。不加引号会拆词搜索导致大量误匹配。OpenAlex 的 total_papers 对常见中文名严重不可靠，arXiv 计数更准。
