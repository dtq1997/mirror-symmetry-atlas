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
