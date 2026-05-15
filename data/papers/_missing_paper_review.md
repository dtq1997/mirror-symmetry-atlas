# Missing-paper audit

生成方式: 用 arxiv author search 拉每位 owner 的论文,
与 yaml.publications 对比.

**Action**: 每个候选论文需人工判断:
  - 是这个人的 → 应该添加到 yaml
  - 是同名作者的 → 忽略 (但可能要加进 review_queue)
**Total missing-candidate count: 10**.


已知陷阱:
  - arxiv 拉取仍会含同名作者污染 (尤其 "Wang Zhiyuan" 等常见名)
  - 但**漏掉真正的论文比加进同名污染更严重** — 用户能看到多的不能看到漏的

扫描了 1 位学者.


## chen-zhuo (en=Zhuo Chen) — 10 candidates not in yaml

- [2025] Nonautonomous Dynamical Systems II: Variational Principles
  - arxiv: `2502.21149` (math.DS)
  - authors: Zhuo Chen, Jun Jie Miao

- [2025] Nonautonomous Dynamical Systems I: Topological Pressures and Entropies
  - arxiv: `2508.01363` (math.DS)
  - authors: Zhuo Chen, Jun Jie Miao

- [2025] Nonautonomous Dynamical Systems III: Symbolic and Expansive Systems
  - arxiv: `2509.11130` (math.DS)
  - authors: Zhuo Chen, Jun Jie Miao

- [2018] Two-dimensional supersymmetric gauge theories with exceptional gauge groups
  - arxiv: `1808.04070` (hep-th)
  - authors: Z. Chen, W. Gu, H. Parsian, E. Sharpe

- [2017] More Toda-like (0,2) mirrors
  - arxiv: `1705.08472` (hep-th)
  - authors: Z. Chen, J. Guo, E. Sharpe, R. Wu

- [2007] Omni-Lie algebroids
  - arxiv: `0710.1923` (math-ph)
  - authors: Z. Chen, Z. -J. Liu

- [2007] The Cohomology of Transitive Lie Algebroids
  - arxiv: `0712.4228` (math.DG)
  - authors: Z. Chen, Z. -J. Liu

- [2007] On (Co-)morphisms of Lie Pseudoalgebras and Groupoids
  - arxiv: `0710.2149` (math.RA)
  - authors: Z. Chen, Z. -J. Liu

- [2007] On the Existence of Global Bisections of Lie Groupoids
  - arxiv: `0710.3909` (math.DG)
  - authors: Z. Chen, Z. -J. Liu, D. -S. Zhong

- [2007] Lie Rinehart Bialgebras for Crossed Products
  - arxiv: `0710.3908` (math.AC)
  - authors: Z. Chen, Z. -J. Liu, D. -S. Zhong
