# 全站整治当前状态

[Codex] 2026-10-08。Goal **active**，原目标见 `RECOVERY-PLAN.md`。这不是已完成的全库事实认证。

## 第一批修复

- 所有实体链接按实际生成的路由判断；缺档对象保留文字并标“未建档”，不制造档案或猜名字绑定。
- 论文链接按 DOI / arXiv / OpenAlex 分开生成，模糊的旧七位 arXiv 号不编地址。
- 首页和论文列表共用归并逻辑。原始 2244 条人物论文记录归并为 1837 条；旧 raw-id 去重 1826 把 13 篇不同的 `[待补充]` 论文压成同一条，不能沿用。
- Python/TypeScript 的 arXiv 规范化修复 `solv-int` 和 `math.AG/` 等旧分类；DOI 前缀统一处理。不同强标识的同题论文不自动合并。
- 缺发表元数据的记录改称“发表待核实”，有 DOI/journal 的称“有发表信息”；不再把缺字段说成未发表。
- 会议按访问时北京时间筛选；首页不再把 2026-04 的会议说成即将举行。
- 手机导航可横向滑动；人物与概念默认列表，支持中英文查找；桌面保留图谱。
- 修复时间筛选遇到缺 period 崩溃、空论文区锚点、None/file: 等无效公共链接。

## 验证证据

- `pnpm test:site`：11 项回归通过，包含负例、跨语言一致性、旧 arXiv 分类、共享占位 ID、标题冲突与未知路径。
- `pnpm lint`、TypeScript 和生产构建通过；数据仍为 0 errors / 74 warnings，警告尚未逐项消除。
- `audit-site.py` 覆盖 282 个导出 HTML；基线 440 个断链目标、387 个错误论文 URL、1 种缺失锚点、1 个非法 scheme；修复后这些问题为 0。只覆盖导出链接，不代表内容真值或所有浏览器行为。
- 手机 390×844：人物默认列表、搜索“唐乾”仅一条，概念搜索“Frobenius”两条；首页无页面横向溢出。
- 桌面：图谱时间滑块 1950→2026、人物搜索已操作，浏览器 error 日志为空。未做全部图交互验收。
- `docs/audits/2026-10-08/`：基线/修后链接报告、手机截图、数据清单。

## 内容核查尚未完成

`content-inventory.json` 覆盖 289 个内容 YAML、3056 个审核单元、另列 30 个辅助/待审文件。所有单元目前均为本轮尚未核实；候选来源链接不等于已核实。

优先问题：

1. 新闻更新链：workflow 被 `disabled_inactivity` 停用；git diff 漏新文件；GITHUB_TOKEN push 不会触发普通 push 部署。修改前已向用户报告根因，本轮全面整治授权覆盖后续可逆修复。恢复抓取前先审计姓名绑定，防止同名错误持续入库。
2. `src/app/news/page.tsx` 的 `buildEntities` 按姓氏子串把新闻文字绑定人物，违反身份防错要求；`scripts/fetch-arxiv-news.py` 尚待逐段审计。尚未恢复 workflow，避免把有风险抓取当成功。
3. 合著关系 `getAllConnections()` 仍用单一优先 key，仍有手填 `key_collaborators` 回退；需复用有冲突防护的多标识逻辑，逐条核对来源，不能把同题推断当身份事实。
4. 机构归属多处取数组最后条目，未按实际时间判断；已故人物、历史职位、未知时期不能冒充当前单位。
5. 图颜色依赖估算年龄，大小混合奖项/论文“影响力”，图例没有准确解释不确定性。先改成有来源的收录指标或明确估计，不能当事实。
6. 概念重复/别名（例 `frobenius-manifold` / `frobenius-manifolds`）、中文显示、定义及关键引用待逐条核实；开放问题状态与历史归属需当前一手文献核对。
7. 全部人物论文 ID/标题/作者归属、DOI 发表信息、一手主页/CV/师生关系待核查；保留旧 review queue。旧 `detect-id-title-mismatch.py` 缓存空响应并略过失败，不可直接把它的 0 mismatch 当审核完成。
8. 致谢图手机体验、论文查找、全局搜索、机构/会议页面完整交互仍未验收。

## 下一轮入口

先读本文件和 `RECOVERY-PLAN.md`，检查 `git status` 与最新远端部署。沿既有 Goal 推进更新链和身份绑定审计，再分批核查内容。不要回到 academic-formula-workbench，不启动无关数学 campaign。

## 发布状态

第一批待提交部署。后续在本节追加实际 commit、Actions run 与线上验证结果。

## 更新链依据

- [GitHub：工作流触发规则](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)
- [GitHub：长期无活动的定时工作流](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows)

[Codex] 2026-10-08 发布进度：第一批 commit `c4fa7a32b75869728d90789ecb6a8c097d7a1087` 已 fast-forward push 到远端 main；Actions run `37694421829` 正在等待完成，暂不宣称上线。最后一次本地生产构建及 postbuild 全站链接检查通过（282 页，21379 条链接，0 问题目标）。

[Codex] 2026-10-08 补充检查：论文、会议、机构、时间线、新闻、致谢网六个桌面入口均能呈现标题，未见页面宽度溢出，检查期间 error 日志为空；致谢图确认载入一个画布，但标签拥挤问题仍待改善。GitHub 新一轮构建通过 lint/typecheck/build/upload，等待 deploy；Actions 报 Node 20 action runtime 弃用及 Ubuntu runner 即将迁移，列入后续依赖维护，不影响本次已通过的构建。

[Codex] 2026-10-08 第一批已上线：Actions run `37694421829` 成功（https://github.com/dtq1997/mirror-symmetry-atlas/actions/runs/37694421829）。curl 已核对线上首页、论文页、Dubrovin 详情页：新统计 1837、访问日期 2026-10-08、正确 DOI 链接、未建档对象不再可点；线上页面也在浏览器重新载入确认。证据见 `live-verification.json`。Goal 继续 active；全内容核实、新闻链与其余待办未完成。

[Codex] 下一轮不重复第一批修复：从新闻身份绑定/抓取失败处理/新文件检测/部署触发开始。读完现有抓取脚本可确认：全同名直接绑定第一个人物；抓取最多每类30条、不分页；网络和 XML 失败被静默略过；同日重跑可能覆写为空。需先做回归案例，再恢复定时任务。只有本次新建的本地预览进程会在本轮结束时关闭，其他进程不动。

[Codex] 2026-10-08 第二批：新闻真值与更新链（待本批发布验收）。

- 五篇旧新闻已逐条对照当前 arXiv 署名、题名、提交日期、主分类、版本与摘要；原新闻中 2601.19455 漏 Megan Howarth / Pavol Ševera，2602.15748 合作者错写为 Alexander Kröger，2602.14973 错写独著，均已纠正。人物 YAML 对应署名原本正确，本批没有重写人物库。
- 中文摘要按原始摘要重写，恢复近似复杂度容差、cluster 构造条件等限定；删除未经来源支持的 KV 历史归因。核查只覆盖元数据和摘要转述，不构成论文证明审计。
- HUST 官方通知补入新闻及会议 URL，只确认日期、主办单位、地点；17/18 报告人数差异与签到、报告细节另待会议手册审查，没有伪造已核标记。
- 移除新闻按姓氏/姓名子串生成的身份链接。自动抓取仅保存原始署名，姓名命中存 candidate_people，matched_people 留空；不回写人物论文。
- 新抓取按七类 OR + 固定日期窗口分页；HTTP/XML/页数变化/重复页/超限均失败退出，已有新闻不覆盖；同日重跑合并并保留人工摘要。记录成功时刻、查询、页哈希，空结果与失败分开。
- `scripts/test_arxiv_news.py` 11 项失败/分页/同名/重跑测试通过；原有网站 11 项回归、lint/typecheck/build 通过。完整导出检查仍为 282 页、21341 链接、0 问题目标。生产构建在最终文件改动后还会重跑。
- 实际一周 API 查询 604 条，4 页取全，筛出 66 条候选；最近一天为 0。已知 ID 与最新 math.AG 查询正控成功。详见 `news-source-review.json`，原始响应在 `.cache/msa/site-recovery/` 与 `.cache/msa/arxiv-news/`。这些候选尚未逐条人工审读。
- workflow 修复：先 stage 再检查新文件；任何失败不提交；成功（包括有效空结果）写运行记录；deploy 改由成功的 Daily arXiv News workflow_run 触发并检出 main。恢复定时任务前等本批构建、发布和真实手动运行。
- 手机新闻页面 390px 已目检，6 条旧记录作者与来源可见，无横向溢出；文章中自动推断的人物链接数为 0，error 日志为空。

[Codex] 2026-10-08 第二批 commit `7b2e33fe0ea27cf0953d8c661c0569dbaf9a0342` 的部署 run `37696283404` 成功。GitHub workflow 当前读回为 active（修改 workflow 后已恢复），无需重复启用。自动条目仅公开题名、原始署名和来源，摘要全文只留原始响应缓存供筛选/审阅；发布页面通过原始链接阅读摘要。最后一次本地 lint/typecheck/build/282 页链接检查通过。准备真实手动抓取验收，不能把已提交代码当作整链已验收。
