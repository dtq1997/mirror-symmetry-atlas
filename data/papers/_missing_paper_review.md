# Missing-paper audit

生成方式: 用 arxiv author search 拉每位 owner 的论文,
与 yaml.publications 对比.

**Action**: 每个候选论文需人工判断:
  - 是这个人的 → 应该添加到 yaml
  - 是同名作者的 → 忽略 (但可能要加进 review_queue)
**Total missing-candidate count: 1**.


已知陷阱:
  - arxiv 拉取仍会含同名作者污染 (尤其 "Wang Zhiyuan" 等常见名)
  - 但**漏掉真正的论文比加进同名污染更严重** — 用户能看到多的不能看到漏的

扫描了 1 位学者.


## zhao-qiulan (en=Qiulan Zhao) — 1 candidates not in yaml

- [2016] On Box-Perfect Graphs
  - arxiv: `1608.04572` (math.CO)
  - authors: Guoli Ding, Wenan Zang, Qiulan Zhao
