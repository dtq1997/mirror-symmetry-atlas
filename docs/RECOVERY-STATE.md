# 全站整治当前状态

[Codex] 2026-10-08。Goal **active**，原目标见 `RECOVERY-PLAN.md`。这不是已完成的全库事实认证。

## 当前恢复入口（2026-10-08，第十批线上验收后）

[Codex] Goal仍active。以下是当前摘要；后面的早期“待发布/尚未恢复”是历史记录，不代表现在。

- 原网站已发布十批修复。最近公开内容 commit `1d002b0f288d4d37d1adb9be0c5b400d76e577e6`；Actions `37708026854` success，7个人物页及论文目录共8页HTTP核验，手机/桌面三组论文卡片实际核验完成。后续报告提交带skip ci，公开资产仍以上述commit为准。
- 当前96人物、61概念、115机构、3开放问题；人物原始论文2219行，目录1817组（包括书籍/章节及译版，不等于独立研究论文总数）。283HTML/22222站内链接/642公式实例，未检出坏目标或KaTeX解析错误；data lint 0errors/74warnings；28项网站回归及CI全部检查通过。这不是全库事实或数学认证。
- 新闻链与定时部署已恢复，72篇新闻在线；作者保留原始署名，不按姓氏猜身份。1237个完整arXiv当前元数据已取回，但并非全部归属已核实。
- 累计11条确认错挂、5条待核实归属已移出，1录像转网上痕迹，另8条来源确认的重复已合并。原始记录及来源分别保存在审核池或具名审计报告；身份排除受防回填检查保护，合并的有效DOI不能加入拒绝池。刘思齐41条、Mazzocco46条、Dubrovin64条。部分履历/论文修正不代表整个人物已核。
- 图谱空按钮、共享数据突变、布局持续散开、手机侧栏/搜索、公式跨行渲染已修；年份筛选是累计有日期记录，机构筛选是历史履历关联，不猜现职。小屏全图仍可能局部标签重叠，可搜索放大。
- 第八批统一出版线索口径；第九批修论文/新闻行内公式、重复与Hertling原刊标题；第十批修 Weyl 第一篇/续篇串接、1604.07123与1809.08806错题名，合并两组预印本/期刊重复。详见identifier-title-corrections.json、batch-ten-publication-counts.json、batch-ten-live-verification.json。Weyl续篇真实出版线索仍待补，不能说未发表。
- 下一步先看 `next-author-profile-leads.json`：Fang的Northwestern2010博士与笔记“Columbia博士”矛盾、NSFC12125101年份错写，CV原件已缓存。Liu2026年9月本人论文清单及arXiv确认2609.12955，尚未加入三位已建档作者。2504.15696v2摘要确实含有特定情形的equivariant mirror symmetric Gamma conjecture，不能当成虚构删除；应核scope并准确归因，尚未审证明。原PDF/提取文本及hash在.cache/msa/site-recovery与该报告。
- 继续复核52条题名差异和227条旧编号的早期快照（含已处理项/版本差异，不全是错）；郭帅2311.09804归属、2312.11174 Open MIND刊名、邬龙挺1103.4695归属、Boalch W4307615951幻灯片类型。旧 next-publication-source-leads.json 三组题名问题已由第十批处理，不重复修改。
- 全内容待办仍包括：人物公开叙述/履历/师生关系，Hertling整书/章节计数，61概念及概念图一侧related连线，115机构、会议/时间线/3开放问题一手来源，论文目录查找体验。必须继续覆盖这些类型，不能把论文元数据清理当全站完成。
- content-inventory.json是第一批未核实基线，旧数量/全pending不覆盖后续分项证据。当前覆盖以具名审计的具体字段为准。
- 不运行旧validate-publications.py --apply / detect-id-title-mismatch.py --write；OpenAlex v2仍有HTTP/缓存/评分风险，不能无人审查全库写入。
- 继续只在本仓库；先查git状态，再沿此Goal推进。不要回academic-formula-workbench，不启动无关数学campaign。本轮没有启动预览服务；浏览器尺寸已复原。

## 以下为分批历史与证据记录

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

[Codex] 2026-10-08 第三批进行中：论文身份的第一组实证纠错。

- 全部 1237 个完整 arXiv 编号已从当前 API 取回元数据（13 批，无失败），覆盖原有 1567 条人物论文记录；52 条规范化题名不一致，先进入复核，不能一概当错。固定报告及只读采集脚本：`arxiv-metadata-audit.json`、`collect-arxiv-metadata.py`。收集成功不等于身份或发表情况已核实。
- 已确认并修正 `2602.21532` / `2511.06984` 的 Si Li / Si-Qi Liu 混淆。两篇从 si-li 的论文列表移除，保留在真实作者档案；同步修复 liu-siqi、zhang-youjin、yang-di 的 coauthors，删掉 Zhang identity_profile 中由此污染的 Si Li 线索。论文 HTML 同时提供刘思齐的清华数学系署名和 liusq 邮箱；已补源。详见 `si-li-ownership-correction.json`。
- 修改后逐个还原这两篇的作者集合，与当前 arXiv 名单一致；名字匹配新增 Si Li / Si-Qi Liu 负例，新闻测试 12 项通过。数据检查 0 errors / 74 warnings；生产构建及 282 页链接审计通过。原始人物论文记录目前 2242 条；这两篇仍在目录中，因此全站论文去重数不因移除错挂而减少。
- 标识队列快照 `publication-audit-queue.json` 是修正前快照：1567 条有完整 arXiv，227 条旧七位号缺 archive，421 条 DOI、25 条 OpenAlex、4 条无可解析标识。不要把快照数量当后续实时数。
- 重大待办：`lib_truth.fetch_arxiv_authors` 对上述两个有效 ID 读回 None，存在旧 miss/cache 的永久屏蔽问题；先修失败缓存与旧 ID 前缀消歧，再重用旧自动审计器。`detect-id-title-mismatch.py` 还会缓存空结果、用不安全 v 切分并把缺检当略过；暂勿运行其 --write。
- 新红旗尚未判错：Mazzocco 的 1305.4067 是 neutrino/physics 大合作；liu-siqi 有 random geometric graphs、high-dimensional expanders、Goldbach 条目，需用本人主页/CV/论文单位排除同名；仅姓氏/全名相同不能放行。张友金某条 coauthors 竟有 `arXiv api core`，以及旧 DOI/编号错配，均待下一批来源修复。
- 合著数仍有字段漂移（例 Zhang→Liu 手填1 vs当前带 slug 的记录43；Liu→Dubrovin、Yang→Dubrovin 也不同）。下一步先统一有冲突保护的目录归并与双边记录计数；不要把单方 raw 计数重新宣传为真实唯一论文数。

[Codex] 新闻运行外部状态异常：代码部署 `37696562177` 成功；手动新闻 run `37696579573` 十余分钟无 jobs，GET 显示 queued，cancel API 返回409称尚未入队，CLI 又称已完成，尚未解释。显式 enable 已成功，已限一次重试 `37697928558`，禁止再无边界重复触发。没有成功取消任何远端任务；只停止了本轮自己的本地 watch 进程。自动抓取→提交→workflow_run 部署整链仍未验收，不宣称自动恢复。

为避免网站继续停留旧数据，本地正常执行同一已测试程序，4 页取回604条，写入 `data/news/2026-10-07.yaml` 的66条自动候选（UTC文件日，北京时间2026-10-08）。只含来源署名、题名、日期、版本和候选标签，没有自动人物绑定、没有机器编造中文摘要；正准备随四个人物纠错一并发布。最新页面成功抓取时间只能说明实际本地抓取成功，不能替代 GitHub 自动运行验收。

[Codex] 新闻链验收已有新结果：限次重试 `37697928558` 成功；GitHub runner 实际取回604条/4页，筛出66条，机器人提交 `a8ed377ec48553885236464945fe52e10ce46f8e`。它触发的 **workflow_run** 部署 `37697996080` 也成功。原始首次 run 的状态异常仍保留，不再因此阻塞正常工作。已把本地生成副本移到 `.cache/msa/site-recovery/news-local-generated.yaml`，fast-forward 合入机器人提交，保留较新的自动抓取时间，避免覆盖。接下来核对线上72条新闻及四个人物修正发布；定时配置为每日北京时间16:00，当前 workflow active。

[Codex] 2026-10-08 线上新闻核验完成：浏览器实际显示72条（66条自动元数据、6条人工核查旧记录），最近完整抓取北京时间06:43:14；自动条目标明未人工审读，article 内人物推断链接为0。390px视口无横向溢出，error日志为空，截图 `news-live-mobile.jpg`。四个人物纠错与机器人最新新闻合并后的最终生产构建成功：282页、21385条链接、0问题目标。准备发布本批人物修正。

[Codex] 2026-10-08 第三批作者纠错已上线：commit `533a5dfef53a37c365457dd726ff933988bd33a7`；部署 `37698552251` 成功。浏览器核对李思页面：40条收录，两篇错挂题名已不在论文区；来源核查脚注保留。没有把移除的错挂记录从全站真实作者目录删掉。

[Codex] 作者来源缓存修复：`lib_truth.py` 拒绝猜测旧七位编号；校验实际返回的 arXiv / DOI / OpenAlex 标识、完整作者字段、HTTP状态和类型。保留旧缓存，但不再信任无来源列表或永久miss；新缓存记录请求、时间与响应哈希，成功才原子写入，24小时失效。14项回归覆盖失败后恢复、错误编号、API错误、歧义旧号、旧缓存污染、过期与损坏缓存、缺检不能通过严格lint；12项新闻回归仍通过。真实API已取回两篇作者，并验证最终HTTP逻辑；见 `author-lookup-live.json`。此模块只提供来源署名，姓名匹配仍不证明个人身份。旧 validate-publications --apply / detect-id-title-mismatch --write 仍不得作为无人审查的真值修复器。

[Codex] 2026-10-08 第四批统计与图谱修复（本地验收完成，待本次部署）：

- `collectCoauthorship` 统一详情、侧栏、图谱的合著记录口径；只用双方相同完整标识归并，支持 DOI/arXiv bridge，不能用同题、同名或缺 archive 的七位编号造边。无对应论文的手填关系仍保存在 YAML / 详情待核实区，不拿手填值当篇数，也不画成已对照的合著线。
- 当前目录1837组、人物原始记录2242条、完整标识支持的双边关系122对。张友金—刘思齐40组；杜布罗文—张友金12组；杜布罗文—杨迪14组。仅为记录核算，不是这些人物实际全部作品或已完成人员身份核查。`coauthor-count-audit.json` 中253个手填字段与当前对照数不同（也含无法对照者），不能把253一概称为错误。
- 人物列表、详情和侧栏收录统计由记录即时去重计算，不再读漂移的 activity 手填总数；历史 h-index 等无核实时间的指标在详情明确待核实，侧栏只展示本站收录数。
- 删除由履历推测出生年的年龄着色及奖项混算影响力；人物图节点大小仅为收录覆盖，颜色表示建档/逝世记录；致谢大小明确是抽取次数，不是影响力。机构/履历事实的当前性仍未审完。
- 实际浏览器复现搜索后节点与连线脱离：force-graph 改写了传入端点，过滤复制节点却保留旧端点对象。现在 simulationGraph 给绘图库独立副本，保留坐标但重绑定端点；单元负例覆盖原始数据污染、旧端点对象与被过滤节点。桌面再次搜索张友金，线连到节点，点击打开侧栏，40篇计数与详情一致。
- 手机人物图搜索栏与致谢图控件换行约束，图例默认折叠、侧栏不超出视口。390px 人物图/致谢图无横向溢出；1280px 图谱搜索/侧栏实际通过。截图 `graph-sidebar-preview.jpg`。
- 17项网站回归、ESLint、TypeScript和最终构建通过；282页 / 21113条链接 / 0坏目标。数据lint仍0errors/74warnings。上批缓存修复已部署，run `37699035948` 成功。

下一轮入口：先检查本批部署及工作区，继续既有 Goal。优先依据本人主页/CV/论文署名核查刘思齐的4篇理论计算机/数论候选及 Mazzocco neutrino 候选；复核52条题名差异、227条旧编号和其余 DOI/OpenAlex。机构当前/历史归属、概念定义与重复、时间线/开放问题、会议报告名单仍待逐项核查。未完成全内容审计，不得标 Goal complete。旧 validate-publications --apply 与 detect-id-title-mismatch --write 的自动身份/写入逻辑仍有风险，本次未运行。

[Codex] 2026-10-08 第四批已部署：commit `8cb9f9f21c126875bcbf8fd93f234d25e8acb3e3`，run `37699970356` 成功；线上人物图已显示新图例，旧年龄推断图例消失。

[Codex] 2026-10-08 第五批同名复核：刘思齐的 `2411.08839`、`2210.00158`、`2111.11316` 已确认属于另一位 Siqi Liu。原文分别署名IAS/UC Berkeley及 siqiliu@ias.edu / sliu18@berkeley.edu；IAS正式学者页记录2023年Berkeley博士并链接本人网页，网页列出三篇相同论文。清华正式教师页则为2007年清华博士、liusq@tsinghua.edu.cn。三篇从公开归属及known_arxiv_ids中移除，原记录/来源保存在 `data/papers/_review_queue/liu-siqi.yaml`，标 rejected-homonym。

`2408.13458` 原文为南昌大学数学系、siqiliu463@gmail.com；尚不足以确证另一人的完整身份，也没有绑定清华刘思齐的证据，故移入同一待核实池并标 needs-review，没有称为已证伪。全文署名来源与去向见 `liu-siqi-homonym-review.json`。同类ID/DOI全数据搜索只有此人物档案；身份线索同步去掉四条。

同一清华官方主页还查实四段任职起止月份，修正career_timeline及identity_profile，并补faculty_page与具名核查来源。现在刘思齐公开收录41条（34有发表信息/7发表待核实）；当前全站1833组、原始2238条。旧数量报告均为当时快照，不可用其旧数覆盖当前数据。其余论文、导师/学生关系与其他履历事实尚未全审。最后一次构建和出站前检查完成后发布本批。


[Codex] 2026-10-08 第五批线上验收完成：commit `7069d9dec9fb615ed7f9c43812d3356daadfc29d`，run `37700358947` 成功。浏览器读取刘思齐详情，41条（34有发表信息/7待核实）；四篇题名从论文区消失，四段清华官方任职日期均可见。截图 `liu-siqi-live.jpg`。

[Codex] 2026-10-08 第六批（本地验证中，未宣称上线）：

- 图谱原来的 + / − / 复位按钮未传处理函数，确认为空按钮。现三类图谱共用画布内的实际控制，显示缩放比例，加载前禁用，空图禁用复位，首次模拟稳定后适应全图；降低最小缩放使手机也能容纳全图。修复动态画布加载后力配置未执行的问题，防重叠力现在随实际画布挂载设置。
- 人物/致谢搜索栏在手机给左侧按钮留位；概念侧栏限制在屏幕内，补关闭按钮名称；学习路径计数明确包含当前概念。实际点击放大、缩小、复位有比例变化；张友金搜索后能点击打开侧栏；390px 人物/致谢图无横向溢出，致谢两类全关后0+0条、复位禁用、error日志为空。概念WDVV侧栏也已实际打开，宽度没有越界。最初小节点点击未命中是测试坐标偏差，裁剪定位后成功，不把它登记为确认的网站点击故障。
- 同时发现 MathText 的跨行单美元公式未解析；对显示公式生成的HTML继续做全局替换也会改坏MathML。改为单次切分文本/公式，KaTeX只处理公式、普通文本转义，禁用TeX可信HTML命令，长公式仅在自身容器横向滚动。WDVV的数学语义尚未审定；本批仅修渲染，不能据此称公式正确。
- Marta Mazzocco档案中的6条核物理论文已由帕多瓦大学机构记录的完整作者名 Marco Mazzocco 及相同DOI确认错挂；另4条仅有缩写或缺独立归属证据，隔离为needs-review，不宣称全部确认属于Marco。原始10条完整保留在 `data/papers/_review_queue/mazzocco.yaml`，逐条来源/处置见 `mazzocco-homonym-review.json`。检查全人物目录，没有这些ID/DOI的另一处重复归属。其余50条论文尚未逐条核实，现有活动/履历/引用指标也未借机宣称核准。
- 当前全站1823组、2228条人物原始论文行；Marta50条（42有发表信息/8待核实）。从原始2244行累计转出11条确认错挂+5条待核实归属。目录数减少不等于删掉真实作者的已建档作品；被移出的这些候选只有错误或未证实的本站owner。
- 新增明确审查保护：默认lint按人物和完整arXiv/DOI/OpenAlex标识阻止已排除或隔离条目回流；不同人物不连坐，同题/缺archive编号不构成排除依据。OpenAlex v2更新器在评分前遵守已有审查，空结果不删审查，保存用原子替换；不带--write现在不改审核池。8项回归覆盖负例、别名、保留记录、失败原子性和dry-run。旧更新器的其他HTTP/缓存/自动评分风险仍存在，未对全库执行--write。

接续仍沿既有Goal，不能complete。待本批最终build、手机公式目检、Actions发布和线上验收后补commit/run。下一批优先：52条题名差异/227条旧编号/DOI与OpenAlex的真实归属；机构当前与历史区分；概念61项（含WDVV表述、Frobenius单复数重复、学习路径）的一手来源；时间滑块会把缺年份记录视为已活动且未按年份限制合著篇数，应修正语义；HUST报告名单与开放问题状态。Marta ICREA提供的CV入口是PDF（https://www.icrea.cat/cvs/33120/marta-mazzocco/），检索已发现任职日期可能与YAML有差异，正式修正前加载PDF/学术来源流程，当前未改这些日期。

[Codex] 第六批最终本地验收：19项网站回归、14项作者来源回归、8项审核持久化回归通过；ESLint、TypeScript、生产构建通过，282页/21036链接/0坏目标，data lint 0errors/74warnings。61个概念定义共127段KaTeX表达式未检出解析错误；这是渲染检查，不是数学判决。390px WDVV页面实际恢复两段公式、无源码外露、无页面横向溢出。详见 `render-and-interaction-review.json`；手机截图 `wdvv-render-preview-mobile.jpg`，概念侧栏修复前公式截图明确保留为 `concept-sidebar-before-math-fix.jpg`。准备提交发布。

[Codex] 防回填覆盖补齐：把之前已核实并发布的两条Si Li/Si-Qi Liu纠错（原始字段来自 `si-li-ownership-correction.json`）登记进 `data/papers/_review_queue/si-li.yaml`。与Liu4条、Mazzocco10条共同覆盖本轮转出的16条记录，未改公开人物内容。

[Codex] 2026-10-08 第六批已上线：commit `e73165a48cb58a70da42e9b25fe0ef463606b360`，Actions run `37702343881` 成功。线上Mazzocco50/42/8、10个转出题名均不在公开页；首页1823；WDVV实际渲染2段KaTeX、0解析错误、无横向溢出；图谱放大按钮14%→20%，浏览器error日志为空。curl同时核对三页。证据 `batch-six-live-verification.json`，截图 `wdvv-render-live.jpg`、`graph-controls-live.jpg`。Goal仍active，全内容事实核查远未完成。

[Codex] 2026-10-08 第七批（待发布）：年份筛选改为截至所选年的累计有日期记录，不再推断无日期人物的活动或生存状态；已逝人物和已结束的历史关系仍保留，未来合著不进入线权重/数字或节点大小。无年份证据默认不显示，界面说明不代表当时没有活动；侧栏明确为未受年份限制的完整档案。机构过滤使用全部已记载求学/任职/访问，可与年份叠加，不再拿末条履历推断现职。年份上限由当前年给出，清除可恢复所有记录。
22项网站回归覆盖未知/未来日期、已结束的关系、去世后的历史记录、缺开始年份、合著计数/节点尺寸、历史访问机构与原始数据不可变。实库1950—2026共77个年份检查累计节点不减少、无悬空边、无未来合著；390px实际测试1950为空、2000为32节点/16边、牛津叠加为2节点、清除恢复96/235，error日志为空。见 `time-filter-audit.json`。快速筛选时立即适应全图后节点仍会移动，复位现会在布局稳定后再适应一次；用户拖拽/滚轮可取消自动视角。最终视觉检查仍在进行。
Mazzocco履历依据ICREA提供的本人CV第1页修正：Padova1988—1994、MSRI1998.11—1999.06、Oxford1999.07—2002.06、补Cambridge2002.07—2004.12、Manchester2005.01—2008.09、Loughborough2008.10—2018.01及2014.05升教授。Birmingham只确认2018.02开始，旧CV的open ended不当成现职，结束年月标待核实；ICREA当前主页与本人主页确认2024转UPC及当前ICREA研究教授。同步身份线索并新增剑桥机构页，原50条论文和activity保持不变。报告 `mazzocco-career-review.json` 限定逐字段核查范围，未把其他信息一并标已核。

[Codex] 第七批视觉修补：加入恢复力限制互不连通的节点持续散开；缩小后保留姓名与最低可见节点尺寸，触控命中区域至少8px半径。390px快速切到2000再复位，稳定后39%全图、姓名恢复显示；局部标签仍会重叠，可搜索放大查看。替换手机验收图。最终ESLint/TypeScript/build通过，283页、21054链接、0坏目标，data lint仍0errors/74warnings。

[Codex] 第七批提交 `56159899e749d5a7c90b7e4650006197f24d9aa2` 已推送main，run `37703966229` 发布中。下一批已定位出版状态分类问题：`journal: ArXiv.org` 等仓库名被 `doi || journal` 视为“有发表信息”；23条候选保存在 `repository-venue-candidates.json`，其中2条只是正常期刊备注提及arXiv，绝不能关键词一刀切。入口为 `src/lib/publications.ts` 与 `src/app/people/[slug]/page.tsx` 的重复分类；先统一分类与边界用语，原始metadata保留。随后继续Mazzocco的OA假合作者“Cherednik Algebras”、俄文作者重复/版本归并、旧编号与52条题名差异；概念、机构、会议和开放问题仍未全审。

[Codex] 第七批线上验收完成：Actions `37703966229` success；线上2000年筛选32节点/16边，桌面1280px无横向溢出，稳定复位92%，姓名显示正常。概念图和致谢开关同样检查，error日志为空。curl确认Mazzocco修正日期/未知结束年月/来源、剑桥新页面和新筛选控件。证据 `batch-seven-live-verification.json`，截图 `year-filter-live-desktop.jpg`。Goal仍active。


[Codex] 2026-10-08 第八批（本地验收完成，待发布）：统一人物列表、统计卡、侧栏、合著分组、详情及全站论文目录的出版线索分类。arXiv/SSRN/已识别机构库及对应资料库DOI本身不代表正式发表；未知非资料库DOI也只标线索，不授予已发表或同行评审结论。真实期刊备注提到arXiv仍保留；同ID优先选有真实刊物记录的一行。DOI标签规范前缀/大小写并拒绝无效值，保留资料库链接。16条剩余仓库刊名记录及13个人物统计变化在审计中保留；SSRN DOI-only 的倪大地条目也由共用分类器覆盖。

据出版社登记的Crossref信息补正郭帅/邬龙挺2001.05347的Forum of Mathematics, Pi 9 (2021), e3（两行）；Boalch1703.10376的Geometry and Physics: Volume II (2018), 433–454。据神户原文封面与署名页补正Mazzocco10.24546/81001100的Rokko Lectures in Mathematics 7 (2000), 91–100。只核这些出版字段，不扩为整个人物身份认证。原metadata逐条保留在 `publication-metadata-review.json`。

Mazzocco的10.14288/1.0377037由DataCite明确登记为MovingImage/Audiovisual，BIRS讲座页确认本人及2018-09-11日期；旧2019是资料库出版年。移至online_traces视频，原论文行完整进审核池，阻止自动回填但不否认Marta署名。当前Marta49条（40有出版线索/9待补）；全站2227原始行/1822目录组。累计11确认错挂+5待核实隔离+1媒体重分类，不能混称17篇同名错挂。

26项网站回归、ESLint、TypeScript和最终build通过，data lint 0errors/74warnings，283HTML/22221链接/0坏目标。390px实际检查arXiv标签、录像不在论文区及锚点跳转；修复粘性导航挡住锚点标题，正常点击后标题在72px（导航56px）处。1280px三条SSRN均显示资料库和待补出版线索，无横向溢出、error日志为空。截图 `publication-metadata-preview-mobile.jpg`。论文题名中的TeX目前仍直接显示源码，列为后续渲染修复；尚未做其数学语义审查。Goal仍active。


[Codex] 第八批已上线：commit `98b75fd452d18e87b5387d8a256d3f9ded1afddd`，Actions `37705478583` success。6个线上页面HTTP核对及Mazzocco的curl检查成功；浏览器390px宽度384无溢出，标题锚点72px、49/40/9、arXiv资料库标签、视频从论文移至网上痕迹均确认，error日志为空。证据 `batch-eight-live-verification.json`，截图 `publication-metadata-live-mobile.jpg`。临时预览已关闭，仅保留线上结果页。

下一轮先继续精确重复/作者错误：`mazzocco-duplicate-source-leads.json` 保存当前OpenAlex位置字段、来源哈希与SIGMA/arXiv一手复核。W2340152047原始来源直接指1409.4287及SIGMA2014/116，错把题名末尾Cherednik Algebras当作者；W2963917450原始来源指1404.0988。现有公开行尚未改动，先核原记录与来源，再合并归属并完整存档防回填。W2128014837只有Manchester PDF来源，需要读原文；Boalch W4307615951 API404不能推断幻灯片不存在。接着修论文题名TeX源码显示、俄文作者重复/版本、52题名差异/227旧编号，以及概念、机构、开放问题等全内容审计。Goal仍active，不要重新建Goal或返回academic-formula-workbench。


[Codex] 2026-10-08 第九批本地验收完成，待发布：

- 论文总目录、人物论文/展开合著列表、新闻标题现在使用安全的行内公式渲染；标题中双美元也不产生块级标签。默认正文显示公式不变，HTML/TeX链接仍不受信任。28项网站回归通过。
- Mazzocco的W2340152047、W2963917450和W2128014837由来源确认是已有记录的OCR/资料库重复；最后一条也在Dubrovin档案，合计移出4行，原行保留在审核池并按OA标识阻止回填。Cherednik Algebras是假合作者（题名末尾）。保留的Monodromy DOI记录补入完整math/9806056和期刊卷页，两位作者互用真实slug。Manchester封面记2000年、正文记1998预印本；2006是MIMS存档号，不能另算作品年份。
- MathNet原刊作者行修正rm9331的本人/重复合作者；俄文原版与英文译版仍保留不同DOI，不按相似题名强制合并。完整前后数据与来源见publication-duplicates-review.json。Mazzocco46条（40/6），Dubrovin64条（58/6），全库2223原始行/1819目录组；累计身份纠错数仍11确认+5隔离，另1录像和本批4重复，不能混算同名错挂。
- 全站公式扫描发现Hertling两个Springer章节标题的HTML转义和重复公式；据原刊citation_title及目录修正，补原书和页码，其他字段未动。详见paper-title-render-review.json。构建审计新增KaTeX解析失败拦截，错误公式负控exit1、正常/转义文字正控exit0。最终283HTML/22209链接/642公式实例/0问题；只验证显示，不验证数学。lint/typecheck/build通过，data lint仍0errors/74warnings。
- 浏览器390px检查Mazzocco46条、5处公式及新闻17处标题公式，1280px目录1819组/151处公式；均无页面横向溢出、无解析/console错误。
- 下一步已有一手确认线索：hep-th/9611200原页作者Boris Dubrovin、Youjin Zhang，期刊Compositio111(1998)167–219，两人当前旧9611200行却写arXiv api core；下批先完整读Zhang档案再修完整编号/作者，并找重复DOI。其余52题名差异、227缺archive旧号、郭帅/邬龙挺候选、概念/机构/会议/开放问题仍待审。Hertling同一本书和章节都计为记录，后续需要明确作品类型/计数口径，不能宣传为独立研究论文篇数。

[Codex] 第九批已上线：commit `f57da999c1d6e9cdd9a72a3f4d3c1ab1da640ecf`，Actions `37706915633` success。Mazzocco/Dubrovin/Hertling/目录/新闻5页HTTP核对全部通过；手机390px实见46条、行内公式、恢复的math/9806056链接，无横向溢出/解析错误/console错误。截图paper-title-live-mobile.jpg；完整证据batch-nine-live-verification.json。Goal active，后续从当前恢复入口和next-publication-source-leads.json继续。


[Codex] 2026-10-08 第十批本地验收完成，待发布：

- 一手 arXiv、作者论文清单及出版社元数据确认三组题名/编号串接；7个人物档案共纠正11行，合并4行重复。完整前后记录在 identifier-title-corrections.json。没有把有效的合并 DOI 加入拒绝池，以免误封保留记录。
- Dubrovin/张友金：第一篇恢复 hep-th/9611200 和双方署名，10.1023/a:1000258122329 与 W1829033056 从续篇移回第一篇；续篇恢复 math/0502365 并补 Dafeng Zuo。续篇真实出版线索仍待补，未宣称未发表。
- Fang/Liu/Zong：1604.07123恢复 Remodeling 正确题名，补 JAMS DOI，Fang/Zong各合并一条DOI重复；1411.3557射影直线论文保持独立。Guo/Chang：1809.08806恢复 N-Mixed-Spin-P fields 题名；1809.11058补 Annals DOI/卷页，并各合并一条DOI重复，保留预印本题名/年份。在线年、卷期年与预印本年不同，不另算作品。
- 当前2219原始行/1817目录组；Dubrovin64(57有出版线索/7待补)、张友金64(53/11)、Fang23(18/5)、Liu59(47/12)、Zong23(15/8)、Guo25(14/11)、Chang26(17/9)。论文归并数变化不代表新增身份纠错；累计仍11确认错挂+5归属隔离+1媒体重分类，另8条重复已合并。
- 28项网站回归、生产构建通过；data lint 0errors/74warnings，283HTML/22222链接/642公式实例/0问题目标。报告 batch-ten-publication-counts.json 和 batch-ten-export-audit.json。源代码未改，本批不声称已完成其他人物或数学内容审核。
- 本轮附带得到两份作者原始材料：Liu_Publications_2609.pdf（2026年9月，含2609.12955等新条目）、Fang本人cv.pdf。Fang现有personal_notes仍有“哥伦比亚博士”与Northwestern博士互相矛盾，原CV明确Northwestern2010、Eric Zaslow；NSFC12125101年份原CV为2022—2026，现笔记2021—2026。下一批先据此完整核相关字段，再处理其余题名差异/归属候选；不能把新发现只当已修。

Goal active；当前尚待本批 GitHub Pages 发布与线上验收。


[Codex] 第十批已上线并完成验证：commit `1d002b0f288d4d37d1adb9be0c5b400d76e577e6`，Actions `37708026854` success。8页HTTP检查全部通过；张友金手机页两篇Weyl题名/作者/不同链接与不同出版状态正确，Fang手机页Remodeling仅一条，Guo桌面两篇NMSP题名/DOI/卷页分别正确；均无页面横向溢出、公式解析或console错误。截图weyl-identifiers-live-mobile.jpg，证据batch-ten-live-verification.json。Goal active，下一轮按当前恢复入口继续。补充：2504.15696v2摘要明确含相应Gamma结论，先前只是待核线索，不能自动当错误删除；应保留具体对象条件与文献归因。
