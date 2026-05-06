# Missing-paper audit

生成方式: 用 arxiv author search 拉每位 owner 的论文,
与 yaml.publications 对比.

**Action**: 每个候选论文需人工判断:
  - 是这个人的 → 应该添加到 yaml
  - 是同名作者的 → 忽略 (但可能要加进 review_queue)
**Total missing-candidate count: 1243**.


已知陷阱:
  - arxiv 拉取仍会含同名作者污染 (尤其 "Wang Zhiyuan" 等常见名)
  - 但**漏掉真正的论文比加进同名污染更严重** — 用户能看到多的不能看到漏的

扫描了 92 位学者.


## alekseev (en=Anton Alekseev) — 24 candidates not in yaml

- [2009] Dirac structures and Dixmier-Douady bundles
  - arxiv: `0907.1257` (math.DG)
  - authors: A. Alekseev, E. Meinrenken

- [2009] Kontsevich deformation quantization and flat connections
  - arxiv: `0906.0187` (math.QA)
  - authors: A. Alekseev, C. Torossian

- [2009] Drinfeld associators, braid groups and explicit solutions of the Kashiwara-Vergne equation
  - arxiv: `0903.4067` (math.QA)
  - authors: A. Alekseev, B. Enriquez, C. Torossian

- [2008] The Atiyah algebroid of the path fibration over a Lie group
  - arxiv: `0810.4402` (math.DG)
  - authors: A. Alekseev, E. Meinrenken

- [2007] Quantization of Wilson loops in Wess-Zumino-Witten models
  - arxiv: `hep-th/0702174` (hep-th)
  - authors: Anton Alekseev, Samuel Monnier

- [2006] Quantization of symplectic dynamical r-matrices and the quantum composition formula
  - arxiv: `math/0606498` (math.QA)
  - authors: Anton Alekseev, Damien Calaque

- [2005] Uniqueness in the Kashiwara-Vergne conjecture
  - arxiv: `math/0508077` (math.QA)
  - authors: Anton Alekseev, Emanuela Petracci

- [2005] Ginzburg-Weinstein via Gelfand-Zeitlin
  - arxiv: `math/0506112` (math.DG)
  - authors: A. Alekseev, E. Meinrenken

- [2005] On the Kashiwara-Vergne conjecture
  - arxiv: `math/0506499` (math.QA)
  - authors: A. Alekseev, E. Meinrenken

- [2004] Current Algebras and Differential Geometry
  - arxiv: `hep-th/0410183` (hep-th)
  - authors: Anton Alekseev, Thomas Strobl

- [2004] Equivariant cohomology and the Maurer-Cartan equation
  - arxiv: `math/0406350` (math.DG)
  - authors: A. Alekseev, E. Meinrenken

- [2003] Lie theory and the Chern-Weil homomorphism
  - arxiv: `math/0308135` (math.RT)
  - authors: A. Alekseev, E. Meinrenken

- [2000] Quasi-Poisson Manifolds
  - arxiv: `math/0006168` (math.DG)
  - authors: Anton Alekseev, Yvette Kosmann-Schwarzbach, Eckhard Meinrenken

- [2000] Linearization of Poisson actions and singular values of matrix products
  - arxiv: `math/0012112` (math.SG)
  - authors: Anton Alekseev, Eckhard Meinrenken, Chris Woodward

- [2000] Wilson lines on noncommutative tori
  - arxiv: `hep-th/0002101` (hep-th)
  - authors: Anton Alekseev, Andrei Bytsko

- [2000] A fixed point formula for loop group actions
  - arxiv: `math/0005046` (math.SG)
  - authors: Anton Alekseev, Eckhard Meinrenken, Chris Woodward

- [2000] Formulas of Verlinde type for non-simply connected groups
  - arxiv: `math/0005047` (math.SG)
  - authors: Anton Alekseev, Eckhard Meinrenken, Chris Woodward

- [2000] RR charges of D2-branes in the WZW model
  - arxiv: `hep-th/0007096` (hep-th)
  - authors: Anton Alekseev, Volker Schomerus

- [1999] Group-valued equivariant localization
  - arxiv: `math/9905130` (math.DG)
  - authors: Anton Alekseev, Eckhard Meinrenken, Chris Woodward

- [1999] Manin pairs and moment maps
  - arxiv: `math/9909176` (math.DG)
  - authors: Anton Alekseev, Yvette Kosmann-Schwarzbach

- [1999] Duistermaat-Heckman distributions for group valued moment maps
  - arxiv: `math/9903087` (math.DG)
  - authors: Anton Alekseev, Eckhard Meinrenken, Chris Woodward

- [1999] The non-commutative Weil algebra
  - arxiv: `math/9903052` (math.DG)
  - authors: Anton Alekseev, Eckhard Meinrenken

- [1997] Lie Group Valued Moment Maps
  - arxiv: `dg-ga/9707021` (math.DG)
  - authors: Anton Alekseev, Anton Malkin, Eckhard Meinrenken

- [1993] Quadratic brackets from symplectic forms
  - arxiv: `hep-th/9307026` (hep-th)
  - authors: Anton Alekseev, Ivan Todorov


## boalch (en=Philip Boalch) — 10 candidates not in yaml

- [2006] Regge and Okamoto symmetries
  - arxiv: `math/0603398` (math.RT)
  - authors: Philip Boalch

- [2005] Some explicit solutions to the Riemann-Hilbert problem
  - arxiv: `math/0501464` (math.DG)
  - authors: Philip Boalch

- [2005] Six results on Painleve VI
  - arxiv: `math/0503043` (math.AG)
  - authors: Philip Boalch

- [2005] Higher genus icosahedral Painleve curves
  - arxiv: `math/0506407` (math.AG)
  - authors: Philip Boalch

- [2004] The fifty-two icosahedral solutions to Painleve VI
  - arxiv: `math/0406281` (math.AG)
  - authors: Philip Boalch

- [2003] From Klein to Painleve via Fourier, Laplace and Jimbo
  - arxiv: `math/0308221` (math.AG)
  - authors: Philip Boalch

- [2002] Quasi-Hamiltonian Geometry of Meromorphic Connections
  - arxiv: `math/0203161` (math.DG)
  - authors: Philip Boalch

- [2001] G-bundles, isomonodromy and quantum Weyl groups
  - arxiv: `math/0108152` (math.DG)
  - authors: Philip Boalch

- [2001] Wild nonabelian Hodge theory on curves
  - arxiv: `math/0111098` (math.DG)
  - authors: Olivier Biquard, Philip Boalch

- [2000] Stokes Matrices and Poisson Lie Groups
  - arxiv: `math/0011062` (math.DG)
  - authors: Philip Boalch


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


## dai-bo (en=Bo Dai) — 3 candidates not in yaml

- [2006] On the space-time Monopole equation
  - arxiv: `math/0602607` (math.DG)
  - authors: Bo Dai, Chuu-Lian Terng, Karen Uhlenbeck

- [2004] Backlund transformations, Ward solitons, and unitons
  - arxiv: `math/0405363` (math.DG)
  - authors: Bo Dai, Chuu-Lian Terng

- [2004] Periodic and homoclinic solutions of the modified 2+1 Chiral model
  - arxiv: `math/0405365` (math.DG)
  - authors: Bo Dai, Chuu-Lian Terng


## dubrovin (en=Boris Dubrovin) — 25 candidates not in yaml

- [2016] Tau-structure for the Double Ramification Hierarchies
  - arxiv: `1602.05423` (math-ph)
  - authors: A. Buryak, B. Dubrovin, J. Guéré, P. Rossi

- [2013] On critical behaviour in systems of Hamiltonian partial differential equations
  - arxiv: `1311.7166` (math-ph)
  - authors: B. Dubrovin, T. Grava, C. Klein, A. Moro

- [2010] Numerical Study of breakup in generalized Korteweg-de Vries and Kawahara equations
  - arxiv: `1101.0268` (math-ph)
  - authors: B. Dubrovin, T. Grava, C. Klein

- [2010] Classical double, R-operators and negative flows of integrable hierarchies
  - arxiv: `1011.4894` (nlin.SI)
  - authors: B. Dubrovin, T. Skrypnyk

- [2007] On universality of critical behaviour in the focusing nonlinear Schrödinger equation, elli
  - arxiv: `0704.0501` (math.AP)
  - authors: B. Dubrovin, T. Grava, C. Klein

- [2006] On the Reductions and Classical Solutions of the Schlesinger equations
  - arxiv: `math/0610327` (math.DG)
  - authors: B. Dubrovin, M. Mazzocco

- [2005] On Hamiltonian perturbations of hyperbolic systems of conservation laws, II: universality 
  - arxiv: `math-ph/0510032` (math-ph)
  - authors: Boris Dubrovin

- [2005] Extended affine Weyl groups and Frobenius manifolds -- II
  - arxiv: `math/0502365` (math.DG)
  - authors: Boris Dubrovin, Youjin Zhang, Dafeng Zuo

- [2004] On Hamiltonian perturbations of hyperbolic systems of conservation laws
  - arxiv: `math/0410027` (math.DG)
  - authors: Boris Dubrovin, Si-Qi Liu, Youjin Zhang

- [2003] Virasoro Symmetries of the Extended Toda Hierarchy
  - arxiv: `math/0308152` (math.DG)
  - authors: Boris Dubrovin, Youjin Zhang

- [2003] On almost duality for Frobenius manifolds
  - arxiv: `math/0307374` (math.DG)
  - authors: Boris Dubrovin

- [2003] Canonical structure and symmetries of the Schlesinger equations
  - arxiv: `math/0311261` (math.DG)
  - authors: Boris Dubrovin, Marta Mazzocco

- [2003] The Extended Toda Hierarchy
  - arxiv: `nlin/0306060` (nlin.SI)
  - authors: Guido Carlet, Boris Dubrovin, Youjin Zhang

- [2001] Normal forms of hierarchies of integrable PDEs, Frobenius manifolds and Gromov - Witten in
  - arxiv: `math/0108160` (math.DG)
  - authors: Boris Dubrovin, Youjin Zhang

- [1998] Frobenius Manifolds And Virasoro Constraints
  - arxiv: `math/9808048` (math.AG)
  - authors: Boris Dubrovin, Youjin Zhang

- [1998] Geometry and analytic theory of Frobenius manifolds
  - arxiv: `math/9807034` (math.AG)
  - authors: Boris Dubrovin

- [1998] Painleve' transcendents and two-dimensional topological field theory
  - arxiv: `math/9803107` (math.AG)
  - authors: Boris Dubrovin

- [1998] Flat pencils of metrics and Frobenius manifolds
  - arxiv: `math/9803106` (math.DG)
  - authors: Boris Dubrovin

- [1998] Monodromy of certain Painleve' VI transcendents and reflection groups
  - arxiv: `math/9806056` (math.AG)
  - authors: B. Dubrovin, M. Mazzocco

- [1997] Bihamiltonian Hierarchies in 2D Topological Field Theory At One-Loop Approximation
  - arxiv: `hep-th/9712232` (hep-th)
  - authors: Boris Dubrovin, Youjin Zhang

- [1996] Extended affine Weyl groups and Frobenius manifolds
  - arxiv: `hep-th/9611200` (hep-th)
  - authors: Boris Dubrovin, Youjin Zhang

- [1994] Geometry of 2d topological field theories
  - arxiv: `hep-th/9407018` (hep-th)
  - authors: Boris Dubrovin

- [1993] Differential geometry of the space of orbits of a Coxeter group
  - arxiv: `hep-th/9303152` (hep-th)
  - authors: Boris Dubrovin

- [1992] Geometry and Integrability of Topological-Antitopological Fusion
  - arxiv: `hep-th/9206037` (hep-th)
  - authors: Boris Dubrovin

- [1992] Integrable Systems and Classification of 2-dimensional Topological Field Theories
  - arxiv: `hep-th/9209040` (hep-th)
  - authors: B. Dubrovin


## faddeev (en=Ludvig Faddeev) — 10 candidates not in yaml

- [2008] An alternative interpretation of the Weinberg-Salam model
  - arxiv: `0811.3311` (hep-th)
  - authors: L. Faddeev

- [2006] Spin-Charge Separation, Conformal Covariance and the SU(2) Yang-Mills Theory
  - arxiv: `hep-th/0608111` (hep-th)
  - authors: Ludvig D. Faddeev, Antti J. Niemi

- [2002] Knotted solitons
  - arxiv: `math-ph/0212079` (math-ph)
  - authors: Ludvig D. Faddeev

- [2001] Aspects of Electric and Magnetic Variables in SU(2) Yang-Mills Theory
  - arxiv: `hep-th/0101078` (hep-th)
  - authors: Ludvig Faddeev, Antti J. Niemi

- [2001] Hidden symmetry and knot solitons in a charged two-condensate Bose system
  - arxiv: `cond-mat/0106152` (cond-mat.supr-con)
  - authors: Egor Babaev, Ludvig D. Faddeev, Antti J. Niemi

- [2000] Shafranov's virial theorem and magnetic plasma confinement
  - arxiv: `physics/0009061` (physics.plasm-ph)
  - authors: Ludvig Faddeev, Lisa Freyhult, Antti J. Niemi, Peter Rajan

- [2000] Magnetic Geometry and the Confinement of Electrically Conducting Plasmas
  - arxiv: `physics/0003083` (physics.plasm-ph)
  - authors: Ludvig Faddeev, Antti J. Niemi

- [1999] Modular Double of Quantum Group
  - arxiv: `math/9912078` (math.QA)
  - authors: Ludvig Faddeev

- [1999] Decomposing the Yang-Mills Field
  - arxiv: `hep-th/9907180` (hep-th)
  - authors: Ludvig Faddeev, Antti J. Niemi

- [1998] Partially Dual variables in SU(2) Yang-Mills Theory
  - arxiv: `hep-th/9807069` (hep-th)
  - authors: Ludvig Faddeev, Antti J. Niemi


## fan-huijun (en=Huijun Fan) — 5 candidates not in yaml

- [2005] Martin points on open manifolds of non-positive curvature
  - arxiv: `math/0505575` (math.DG)
  - authors: Jianguo Cao, Huijun Fan, Francois Ledrappier

- [2004] Geometry and analysis of spin equations
  - arxiv: `math/0409434` (math.DG)
  - authors: Huijun Fan, Tyler J. Jarvis, Yongbin Ruan

- [2003] Conley Index Theory and Novikov-Morse Theory
  - arxiv: `math/0312018` (math.GT)
  - authors: Huijun Fan, Juergen Jost

- [2001] Harmonic Hopf Constructions Between Spheres II
  - arxiv: `math/0106234` (math.DG)
  - authors: Weiyue Ding, Huijun Fan, Jiayu Li

- [2000] Novikov-Morse theory for dynamical systems
  - arxiv: `math/0010295` (math.DS)
  - authors: Huijun Fan, Juergen Jost


## guzzetti (en=Davide Guzzetti) — 3 candidates not in yaml

- [2003] The Singularity of Kontsevich's Solution for $QH^{*}(CP^2)$
  - arxiv: `math-ph/0301011` (math-ph)
  - authors: Davide Guzzetti

- [2001] The Elliptic Representation of the General Painlevé 6 Equation
  - arxiv: `math/0108073` (math.CV)
  - authors: Davide Guzzetti

- [1999] Stokes Matrices and Monodromy of the Quantum Cohomology of Projective Spaces
  - arxiv: `math/9904099` (math.AG)
  - authors: D. Guzzetti


## hertling (en=Claus Hertling) — 10 candidates not in yaml

- [2008] An update on semisimple quantum cohomology and F-manifolds
  - arxiv: `0803.2769` (math.AG)
  - authors: C. Hertling, Yu. Manin, C. Teleman

- [2006] Nilpotent orbits of a generalization of Hodge structures
  - arxiv: `math/0603564` (math.AG)
  - authors: Claus Hertling, Christian Sevenheck

- [2004] Bernoulli moments of spectral numbers and Hodge numbers
  - arxiv: `math/0405501` (math.AG)
  - authors: Thomas Brélivet, Claus Hertling

- [2002] Unfoldings of meromorphic connections and a construction of Frobenius manifolds
  - arxiv: `math/0207089` (math.AG)
  - authors: Claus Hertling, Yuri Manin

- [2002] tt* geometry, Frobenius manifolds, their connections, and the construction for singulariti
  - arxiv: `math/0203054` (math.AG)
  - authors: Claus Hertling

- [2001] Semistable bundles on curves and reducible representations of the fundamental group
  - arxiv: `math/0101194` (math.AG)
  - authors: Hélène Esnault, Claus Hertling

- [2000] Variance of the spectral numbers
  - arxiv: `math/0007187` (math.CV)
  - authors: Claus Hertling

- [1999] Multiplication on the tangent bundle
  - arxiv: `math/9910116` (math.AG)
  - authors: Claus Hertling

- [1998] Weak Frobenius manifolds
  - arxiv: `math/9810132` (math.QA)
  - authors: Claus Hertling, Yuri Manin

- [1995] Moduli spaces of semiquasihomogeneous singularities with fixed principal part
  - arxiv: `alg-geom/9503013` (math.AG)
  - authors: G. -M. Greuel, C. Hertling, G. Pfister


## hong-wei (en=Wei Hong) — 18 candidates not in yaml

- [2026] Asymptotics of Multi-Scale McKean--Vlasov Diffusions with Super-Linear Kernels: a Lifted S
  - arxiv: `2604.22510` (math.PR)
  - authors: Wei Hong, Shanshan Hu, Wei Liu, Shiyuan Yang

- [2025] Large Deviations for Slow-Fast Mean-Field Diffusions
  - arxiv: `2501.11874` (math.PR)
  - authors: Wei Hong, Wei Liu, Shiyuan Yang

- [2025] Mean Field Stochastic Partial Differential Equations with Nonlinear Kernels
  - arxiv: `2508.12547` (math.PR)
  - authors: Wei Hong, Shihu Li, Wei Liu

- [2025] Generalized Yosida Approximation and Multi-Valued Stochastic Evolution Inclusions
  - arxiv: `2502.11640` (math.PR)
  - authors: Wujing Fan, Wei Hong, Wei Liu

- [2025] Stochastic Forced 3D Navier-Stokes Equations in $\mathbb{H}^{1/2}$-Space
  - arxiv: `2511.15223` (math.PR)
  - authors: Wei Hong, Shihu Li, Wei Liu

- [2024] Regularization by Nonlinear Noise for PDEs: Well-posedness and Finite Time Extinction
  - arxiv: `2407.06840` (math.PR)
  - authors: Wei Hong, Shihu Li, Wei Liu

- [2024] Large Deviation Principle for Multi-Scale Fully Local Monotone Stochastic Dynamical System
  - arxiv: `2402.18108` (math.PR)
  - authors: Wei Hong, Wei Liu, Luhan Yang

- [2023] Multi-Scale McKean-Vlasov SDEs: Moderate Deviation Principle in Different Regimes
  - arxiv: `2306.11569` (math.PR)
  - authors: Wei Hong, Ge Li, Shihu Li

- [2023] McKean-Vlasov Stochastic Partial Differential Equations: Existence, Uniqueness and Propaga
  - arxiv: `2306.15508` (math.PR)
  - authors: Wei Hong, Shihu Li, Wei Liu

- [2022] McKean-Vlasov SDE and SPDE with Locally Monotone Coefficients
  - arxiv: `2205.04043` (math.PR)
  - authors: Wei Hong, Shanshan Hu, Wei Liu

- [2022] Diffusion Approximation for Multi-Scale McKean-Vlasov SDEs Through Different Methods
  - arxiv: `2206.01928` (math.PR)
  - authors: Wei Hong, Shihu Li, Xiaobin Sun

- [2021] Distribution Dependent Stochastic Porous Media Equations
  - arxiv: `2103.10135` (math.PR)
  - authors: Jingyue Gao, Wei Hong, Wei Liu

- [2021] Central Limit Type Theorem and Large Deviation Principle for Multi-Scale McKean-Vlasov SDE
  - arxiv: `2112.08203` (math.PR)
  - authors: Wei Hong, Shihu Li, Wei Liu, Xiaobin Sun

- [2021] Large Deviation Principle for McKean-Vlasov Quasilinear Stochastic Evolution Equations
  - arxiv: `2103.11398` (math.PR)
  - authors: Wei Hong, Shihu Li, Wei Liu

- [2021] Freidlin-Wentzell Type Large Deviation Principle for Multi-Scale Locally Monotone SPDEs
  - arxiv: `2102.10855` (math.PR)
  - authors: Wei Hong, Shihu Li, Wei Liu

- [2021] Strong Convergence Rates in Averaging Principle for Slow-Fast McKean-Vlasov SPDEs
  - arxiv: `2107.14401` (math.PR)
  - authors: Wei Hong, Shihu Li, Wei Liu

- [2019] Shearing-induced contact pattern formation in hydrogels sliding in polymer solution
  - arxiv: `1901.06149` (cond-mat.soft)
  - authors: Shintaro Yashima, Satoshi Hirayama, Takayuki Kurokawa, Thomas Salez, Haruna Takefuji

- [2016] Poisson Cohomology of holomorphic toric Poisson manifolds. I
  - arxiv: `1611.08485` (math-ph)
  - authors: Wei Hong


## hu-chuangqiang (en=Chuangqiang Hu) — 1 candidates not in yaml

- [2015] Multi-point Codes from Generalized Hermitian Curves
  - arxiv: `1504.04171` (cs.IT)
  - authors: Chuangqiang Hu, Chang-An Zhao


## hu-jianxun (en=Jianxun Hu) — 5 candidates not in yaml

- [2006] Birational cobordism invariance of uniruled symplectic manifolds
  - arxiv: `math/0611592` (math.SG)
  - authors: Jianxun Hu, Tian-Jun Li, Yongbin Ruan

- [2005] The Donaldson-Thomas invariants under blowups and flops
  - arxiv: `math/0505542` (math.AG)
  - authors: Jianxun Hu, Wei-Ping Li

- [2003] Mukai Flop and Ruan Cohomology
  - arxiv: `math/0302022` (math.AG)
  - authors: Jianxun Hu, Wanchuan Zhang

- [1998] Gromov-Witten Invariants of Blow-ups Along Points and Curces
  - arxiv: `math/9810081` (math.AG)
  - authors: Jianxun Hu

- [1996] Topological quantum field theory and crossing number
  - arxiv: `hep-th/9612184` (hep-th)
  - authors: Zhujun Zheng, Ke Wu, Shikun Wang, Jianxun Hu


## k-saito (en=Kyoji Saito) — 4 candidates not in yaml

- [2012] The skew-growth function on the monoid of square matrices
  - arxiv: `1208.3727` (math.GR)
  - authors: Kyoji Saito

- [2006] Eta-product $η(7τ)^7/η(τ)$
  - arxiv: `math/0602367` (math.NT)
  - authors: Kyoji Saito

- [2005] Principal $Γ$-cone for a tree
  - arxiv: `math/0510623` (math.CO)
  - authors: Kyoji Saito

- [2005] Matrix Factorizations and Representations of Quivers II: type ADE case
  - arxiv: `math/0511155` (math.AG)
  - authors: Hiroshige Kajiura, Kyoji Saito, Atsushi Takahashi


## kontsevich (en=Maxim Kontsevich) — 24 candidates not in yaml

- [2007] Notes on motives in finite characteristic
  - arxiv: `math/0702206` (math.AG)
  - authors: Maxim Kontsevich

- [2006] On Malliavin measures, SLE and CFT
  - arxiv: `math-ph/0609056` (math-ph)
  - authors: Maxim Kontsevich, Yuri Suhov

- [2006] Notes on A-infinity algebras, A-infinity categories and non-commutative geometry. I
  - arxiv: `math/0606241` (math.RA)
  - authors: Maxim Kontsevich, Yan Soibelman

- [2006] Integrality of instanton numbers and p-adic B-model
  - arxiv: `hep-th/0603106` (hep-th)
  - authors: Maxim Kontsevich, Albert Schwarz, Vadim Vologodsky

- [2005] Automorphisms of the Weyl algebra
  - arxiv: `math/0512169` (math.RA)
  - authors: Alexei Belov-Kanel, Maxim Kontsevich

- [2005] The Jacobian Conjecture is stably equivalent to the Dixmier Conjecture
  - arxiv: `math/0512171` (math.RA)
  - authors: Alexei Belov-Kanel, Maxim Kontsevich

- [2005] Quantization on Curves
  - arxiv: `math-ph/0507021` (math-ph)
  - authors: Christian Fronsdal, Maxim Kontsevich

- [2005] Symmetries of WDVV equations
  - arxiv: `hep-th/0508221` (hep-th)
  - authors: Yujun Chen, Maxim Kontsevich, Albert Schwarz

- [2004] Affine structures and non-archimedean analytic spaces
  - arxiv: `math/0406564` (math.AG)
  - authors: Maxim Kontsevich, Yan Soibelman

- [2001] Deformation quantization of algebraic varieties
  - arxiv: `math/0106006` (math.AG)
  - authors: M. Kontsevich

- [2000] Deformations of algebras over operads and Deligne's conjecture
  - arxiv: `math/0001151` (math.QA)
  - authors: Maxim Kontsevich, Yan Soibelman

- [2000] Homological mirror symmetry and torus fibrations
  - arxiv: `math/0011041` (math.SG)
  - authors: Maxim Kontsevich, Yan Soibelman

- [2000] On Poly(ana)logs I
  - arxiv: `math/0008089` (math.KT)
  - authors: Philippe Elbaz-Vincent, Herbert Gangl, Maxim Kontsevich

- [1999] Operads and Motives in Deformation Quantization
  - arxiv: `math/9904055` (math.QA)
  - authors: Maxim Kontsevich

- [1998] Noncommutative smooth spaces
  - arxiv: `math/9812158` (math.AG)
  - authors: Maxim Kontsevich, Alexander Rosenberg

- [1997] Deformation quantization of Poisson manifolds, I
  - arxiv: `q-alg/9709040` (math.QA)
  - authors: Maxim Kontsevich

- [1997] Product formulas for modular forms on O(2,n) (after R.Borcherds)
  - arxiv: `alg-geom/9709006` (math.AG)
  - authors: Maxim Kontsevich

- [1997] Rozansky-Witten invariants via formal geometry
  - arxiv: `dg-ga/9704009` (math.DG)
  - authors: M. Kontsevich

- [1997] Frobenius Manifolds and Formality of Lie Algebras of Polyvector Fields
  - arxiv: `alg-geom/9710032` (math.AG)
  - authors: Sergey Barannikov, Maxim Kontsevich

- [1997] Lyapunov exponents and Hodge theory
  - arxiv: `hep-th/9701164` (hep-th)
  - authors: M. Kontsevich, A. Zorich

- [1997] Relations between the correlators of the topological sigma-model coupled to gravity
  - arxiv: `alg-geom/9708024` (math.AG)
  - authors: Maxim Kontsevich, Yuri I. Manin

- [1994] Geometry of determinants of elliptic operators
  - arxiv: `hep-th/9406140` (hep-th)
  - authors: Maxim Kontsevich, Simeon Vishik

- [1994] Homological Algebra of Mirror Symmetry
  - arxiv: `alg-geom/9411018` (math.AG)
  - authors: Maxim Kontsevich

- [1994] Determinants of elliptic pseudo-differential operators
  - arxiv: `hep-th/9404046` (hep-th)
  - authors: Maxim Kontsevich, Simeon Vishik


## leung-naichung (en=Naichung Conan Leung) — 65 candidates not in yaml

- [2026] Lagrangian Intersections, Symplectic Reduction and Kirwan Surjectivity
  - arxiv: `2602.11718` (math.AG)
  - authors: Naichung Conan Leung, Ying Xie, Yu Tung Yau

- [2026] Grassmannian perspectives of classical Lie groups and Cartan involutions
  - arxiv: `2602.00602` (math.DG)
  - authors: Yunxia Chen, Naichung Conan Leung

- [2025] Quantization commutes with reduction for coisotropic A-branes
  - arxiv: `2506.06859` (math.SG)
  - authors: Naichung Conan Leung, Ying Xie, Yutung Yau

- [2025] Intersections of twisted cotangent bundles and symplectic duality
  - arxiv: `2510.19259` (math.RT)
  - authors: Naichung Conan Leung, Yunsong Wei

- [2023] Hidden Sp(1)-Symmetry and Brane Quantization on HyperKähler manifolds
  - arxiv: `2303.14992` (math.SG)
  - authors: NaiChung Conan Leung, YuTung Yau

- [2023] Limit of geometric quantizations on Kähler manifolds with T-symmetry
  - arxiv: `2307.07759` (math.SG)
  - authors: Naichung Conan Leung, Dan Wang

- [2023] Geometric quantizations of mixed polarizations on Kähler manifolds with T-symmetry
  - arxiv: `2301.01011` (math.SG)
  - authors: Naichung Conan Leung, Dan Wang

- [2023] On Derived Categories of Generalized Grassmannian Flips
  - arxiv: `2309.11136` (math.AG)
  - authors: Naichung Conan Leung, Ying Xie

- [2022] Geodesic rays in the space of Kähler metrics with $T$-symmetry
  - arxiv: `2211.05324` (math.SG)
  - authors: Naichung Conan Leung, Dan Wang

- [2022] Elliptic Hypertoric Varieties
  - arxiv: `2204.12233` (math.AG)
  - authors: Naichung Conan Leung, Xiao Zheng

- [2022] ADE Bundles over Surfaces
  - arxiv: `2210.08771` (math.AG)
  - authors: Yunxia Chen, Naichung Conan Leung

- [2022] Quantum $K$-theory of $G/P$ and $K$-homology of affine Grassmannian
  - arxiv: `2201.12951` (math.AG)
  - authors: Chi Hong Chow, Naichung Conan Leung

- [2021] Berezin-Toeplitz Quantization in Real Polarizations with Toric Singularities
  - arxiv: `2105.02587` (math.SG)
  - authors: NaiChung Conan Leung, YuTung Yau

- [2021] Deformation quantization via Toeplitz operators on geometric quantization in real polariza
  - arxiv: `2104.05301` (math.SG)
  - authors: Naichung Conan Leung, Yutung Yau

- [2021] Peterson conjecture via Lagrangian correspondences and wonderful compactifications
  - arxiv: `2102.03103` (math.SG)
  - authors: Hanwool Bae, Naichung Conan Leung

- [2021] Applications of the theory of Floer to symmetric spaces
  - arxiv: `2103.00382` (math.SG)
  - authors: Hanwool Bae, Chi Hong Chow, Naichung Conan Leung

- [2020] Sharp Hardy inequalities via Riemannian submanifolds
  - arxiv: `2009.09478` (math.DG)
  - authors: Yunxia Chen, Naichung Conan Leung, Wei Zhao

- [2019] Refined scattering diagrams and theta functions from asymptotic analysis of Maurer-Cartan 
  - arxiv: `1902.05765` (math.AG)
  - authors: Naichung Conan Leung, Ziming Nikolas Ma, Matthew B. Young

- [2019] DK Conjecture for Some $K$-inequivalences from Grassmannians
  - arxiv: `1911.07715` (math.AG)
  - authors: Naichung Conan Leung, Ying Xie

- [2018] Equivariant deformation quantization and coadjoint orbit method
  - arxiv: `1809.09082` (math.RT)
  - authors: Naichung Conan Leung, Shilin Yu

- [2018] Embeddings from noncompact symmetric spaces to their compact duals
  - arxiv: `1811.02778` (math.AG)
  - authors: Yunxia Chen, Yongdong Huang, Naichung Conan Leung

- [2018] Categorical duality between joins and intersections
  - arxiv: `1811.05135` (math.AG)
  - authors: Qingyuan Jiang, Naichung Conan Leung

- [2018] $ADE$ bundles over $ADE$ singular surfaces and flag varieties of $ADE$ type
  - arxiv: `1811.02777` (math.AG)
  - authors: Yunxia Chen, Naichung Conan Leung

- [2018] Blowing up linear categories, refinements, and homological projective duality with base lo
  - arxiv: `1811.05132` (math.AG)
  - authors: Qingyuan Jiang, Naichung Conan Leung

- [2018] Derived category of projectivizations and flops
  - arxiv: `1811.12525` (math.AG)
  - authors: Qingyuan Jiang, Naichung Conan Leung

- [2018] Energy bound for Kapustin-Witten solutions on $S^3\times\mathbb{R}^+$
  - arxiv: `1801.04412` (math.DG)
  - authors: Naichung Conan Leung, Ryosuke Takahashi

- [2017] Categorical Plücker Formula and Homological Projective Duality
  - arxiv: `1704.01050` (math.AG)
  - authors: Qingyuan Jiang, Naichung Conan Leung, Ying Xie

- [2015] Orientability for gauge theories on Calabi-Yau manifolds
  - arxiv: `1502.01141` (math.AG)
  - authors: Yalong Cao, Naichung Conan Leung

- [2015] Relative Donaldson-Thomas theory for Calabi-Yau 4-folds
  - arxiv: `1502.04417` (math.AG)
  - authors: Yalong Cao, Naichung Conan Leung

- [2015] Mukai flops and Plücker type formulas for hyper-Kähler manifolds
  - arxiv: `1510.05889` (math.AG)
  - authors: Yalong Cao, Naichung Conan Leung

- [2014] Fukaya's conjecture on Witten's twisted $A_\infty$-structures
  - arxiv: `1401.5867` (math.DG)
  - authors: Kaileung Chan, Naichung Conan Leung, Ziming Nikolas Ma

- [2014] Donaldson-Thomas theory for Calabi-Yau 4-folds
  - arxiv: `1407.7659` (math.AG)
  - authors: Yalong Cao, Naichung Conan Leung

- [2014] Cox rings of rational surfaces and flag varieties of ADE-types
  - arxiv: `1409.2325` (math.AG)
  - authors: Naichung Conan Leung, Jiajin Zhang

- [2013] Instantons in G2 manifolds from J-holomorphic curves in coassociative submanifolds
  - arxiv: `1303.6728` (math.DG)
  - authors: Naichung Conan Leung, Xiaowei Wang, Ke Zhu

- [2013] Lattice point counting via Einstein metrics
  - arxiv: `1305.4830` (math.DG)
  - authors: Ziming Nikolas Ma, Naichung Conan Leung

- [2013] Affine ADE bundles over complex surfaces with p_g=0
  - arxiv: `1303.5578` (math.AG)
  - authors: Yunxia Chen, Naichung Conan Leung

- [2012] ADE bundles over surfaces with ADE singularities
  - arxiv: `1209.4979` (math.AG)
  - authors: Yunxia Chen, Naichung Conan Leung

- [2011] Thin instantons in G_2-manifolds and Seiberg-Witten invariants
  - arxiv: `1107.1947` (math.DG)
  - authors: Naichung Conan Leung, Xiaowei Wang, Ke Zhu

- [2009] Moduli of bundles over rational surfaces and elliptic curves I: simply laced cases
  - arxiv: `0906.3900` (math.AG)
  - authors: Naichung Conan Leung, Jiajin Zhang

- [2009] Moduli of bundles over rational surfaces and elliptic curves II: non-simply laced cases
  - arxiv: `0908.1645` (math.AG)
  - authors: Naichung Conan Leung, Jiajin Zhang

- [2008] Calabi-Yau components in general type hypersurfaces
  - arxiv: `0807.1784` (math.AG)
  - authors: Naichung Conan Leung, Tom Y. H. Wan

- [2008] Open Orbits and Augmentations of Dynkin Diagrams
  - arxiv: `0812.1078` (math.RT)
  - authors: Sin Tsun Edward Fan, Naichung Conan Leung

- [2007] Hodge Theory for G2-manifolds: Intermediate Jacobians and Abel-Jacobi maps
  - arxiv: `0709.2987` (math.DG)
  - authors: Spiro Karigiannis, Naichung Conan Leung

- [2004] Intersection theory of coassociative submanifolds in G_(2)-manifolds and Seiberg-Witten in
  - arxiv: `math/0401419` (math.DG)
  - authors: Naichung Conan Leung, Xiaowei Wang

- [2004] Yau-Zaslow formula on K3 surfaces for non-primitive classes
  - arxiv: `math/0404537` (math.SG)
  - authors: Junho Lee, Naichung Conan Leung

- [2004] Counting Elliptic Curves in K3 Surfaces
  - arxiv: `math/0405041` (math.SG)
  - authors: Junho Lee, Naichung Conan Leung

- [2004] Instantons and branes in manifolds with vector cross product
  - arxiv: `math/0402044` (math.DG)
  - authors: Jae-Hyouk Lee, Naichung Conan Leung

- [2003] Riemannian geometry over different normed division algebra
  - arxiv: `math/0303153` (math.DG)
  - authors: Naichung Conan Leung

- [2003] Almost toric symplectic four-manifolds
  - arxiv: `math/0312165` (math.SG)
  - authors: Naichung Conan Leung, Margaret Symington

- [2002] Topological Quantum Field Theory for Calabi-Yau threefolds and G_2 manifolds
  - arxiv: `math/0208124` (math.DG)
  - authors: Naichung Conan Leung

- [2002] Geometric Aspects of Mirror Symmetry (with SYZ for Rigid CY manifolds)
  - arxiv: `math/0204168` (math.DG)
  - authors: Naichung Conan Leung

- [2002] Geometric structures on G2 and Spin(7)-manifolds
  - arxiv: `math/0202045` (math.DG)
  - authors: Jae-Hyouk Lee, Naichung Conan Leung

- [2001] The signature of a toric variety
  - arxiv: `math/0111064` (math.AG)
  - authors: Naichung Conan Leung, Victor Reiner

- [2001] Lagrangian submanifolds in Hyperkahler manifolds, Legendre transformation
  - arxiv: `math/0110330` (math.SG)
  - authors: Naichung Conan Leung

- [2001] A general Plucker formula
  - arxiv: `math/0111179` (math.AG)
  - authors: Naichung Conan Leung

- [2001] Harmonic maps and the topology of conformally compact Einstein manifolds
  - arxiv: `math/0112023` (math.DG)
  - authors: Naichung Conan Leung, Tom Yau-heng Wan

- [2000] From Special Lagrangian to Hermitian-Yang-Mills via Fourier-Mukai Transform
  - arxiv: `math/0005118` (math.DG)
  - authors: Naichung Conan Leung, Shing-Tung Yau, Eric Zaslow

- [2000] Mirror symmetry without corrections
  - arxiv: `math/0009235` (math.DG)
  - authors: Naichung Conan Leung

- [2000] ADE-bundles over rational surfaces, configuration of lines and rulings
  - arxiv: `math/0009192` (math.AG)
  - authors: Naichung Conan Leung

- [2000] G-bundles on Abelian surfaces, hyperkahler manifolds, and stringy Hodge numbers
  - arxiv: `math/0004159` (math.AG)
  - authors: Jim Bryan, Ron Donagi, Naichung Conan Leung

- [1999] Multiple covers and the integrality conjecture for rational curves in Calabi-Yau threefold
  - arxiv: `math/9911056` (math.AG)
  - authors: Jim Bryan, Sheldon Katz, Naichung Conan Leung

- [1998] Generating functions for the number of curves on Abelian surfaces
  - arxiv: `math/9802125` (math.AG)
  - authors: Jim Bryan, Naichung Conan Leung

- [1997] Uniformization of four manifolds
  - arxiv: `dg-ga/9705001` (math.DG)
  - authors: Naichung Conan Leung

- [1997] Analytic Torsion for Quaternionic manifolds and related topics
  - arxiv: `dg-ga/9710022` (math.DG)
  - authors: Naichung Conan Leung, Sangkug Yi

- [1997] The enumerative geometry of K3 surfaces and modular forms
  - arxiv: `alg-geom/9711031` (math.AG)
  - authors: Jim Bryan, Naichung Conan Leung


## li-ao (en=Ao Li) — 2 candidates not in yaml

- [2022] The Circular Matern Covariance Function and its Link to Markov Random Fields on the Circle
  - arxiv: `2201.12856` (math.ST)
  - authors: Chunfeng Huang, Ao Li

- [2019] On White Noise Space and Levy's Brownian Motion on the Circle
  - arxiv: `1911.03374` (math.PR)
  - authors: Chunfeng Huang, Ao Li


## li-qin (en=Qin Li) — 28 candidates not in yaml

- [2025] Least-Squares Problem Over Probability Measure Space
  - arxiv: `2501.09097` (math.OC)
  - authors: Qin Li, Li Wang, Yunan Yang

- [2025] Control of a Uniformly Magnetized Plasma with External Electric Fields
  - arxiv: `2509.07988` (physics.plasm-ph)
  - authors: Peiyi Chen, Rogerio Jorge, Qin Li, Yukun Yue

- [2025] Stability of the reconstruction of the heat reflection coefficient in the phonon transport
  - arxiv: `2512.24394` (math.AP)
  - authors: Peiyi Chen, Irene M. Gamba, Qin Li, Anjali Nair

- [2025] Evaporative Refrigeration Effect in Evaporation and Condensation between Two Parallel Plat
  - arxiv: `2504.09864` (cond-mat.stat-mech)
  - authors: Peiyi Chen, Qin Li, Gang Chen

- [2025] Inverse Problems Over Probability Measure Space
  - arxiv: `2504.18999` (math.OC)
  - authors: Qin Li, Maria Oprea, Li Wang, Yunan Yang

- [2024] Stochastic Inverse Problem: stability, regularization and Wasserstein gradient flow
  - arxiv: `2410.00229` (stat.ML)
  - authors: Qin Li, Maria Oprea, Li Wang, Yunan Yang

- [2024] Bayesian sampling using interacting particles
  - arxiv: `2401.13100` (math.NA)
  - authors: Shi Chen, Zhiyan Ding, Qin Li

- [2024] Reconstruction of the Doping Profile in Vlasov-Poisson
  - arxiv: `2401.04834` (math.AP)
  - authors: Ru-Yu Lai, Qin Li, Weiran Sun

- [2024] Control of Instability in a Vlasov-Poisson System Through an External Electric Field
  - arxiv: `2407.15008` (physics.plasm-ph)
  - authors: Lukas Einkemmer, Qin Li, Clément Mouhot, Yukun Yue

- [2023] Beyond expectations: Residual Dynamic Mode Decomposition and Variance for Stochastic Dynam
  - arxiv: `2308.10697` (math.DS)
  - authors: Matthew J. Colbrook, Qin Li, Ryan V. Raut, Alex Townsend

- [2023] Reconstructing the kinetic chemotaxis kernel using macroscopic data: well-posedness and il
  - arxiv: `2309.05004` (math.NA)
  - authors: Kathrin Hellmuth, Christian Klingenberg, Qin Li, Min Tang

- [2022] Inference of interaction kernels in mean-field models of opinion dynamics
  - arxiv: `2212.14489` (cs.SI)
  - authors: Weiqi Chu, Qin Li, Mason A. Porter

- [2022] Scintillation Minimization versus Intensity Maximization in Optimal Beams
  - arxiv: `2211.09265` (physics.optics)
  - authors: Qin Li, Anjali Nair, Samuel N Stechmann

- [2022] Kinetic chemotaxis tumbling kernel determined from macroscopic quantities
  - arxiv: `2206.01629` (math.AP)
  - authors: Kathrin Hellmuth, Christian Klingenberg, Qin Li, Min Tang

- [2021] Multiscale convergence of the inverse problem for chemotaxis in the Bayesian setting
  - arxiv: `2110.13787` (math.AP)
  - authors: Kathrin Hellmuth, Christian Klingenberg, Qin Li, Min Tang

- [2021] Local Well-posedness of Vlasov-Poisson-Boltzmann Equation with Generalized Diffuse Boundar
  - arxiv: `2103.14665` (math.AP)
  - authors: Hongxu Chen, Chanwoo Kim, Qin Li

- [2021] Unique Reconstruction of the Heat-Reflection Indices at Solid Interfaces
  - arxiv: `2108.03310` (math.AP)
  - authors: Qin Li, Weiran Sun

- [2020] Variance reduction for Random Coordinate Descent-Langevin Monte Carlo
  - arxiv: `2006.06068` (stat.ML)
  - authors: Zhiyan Ding, Qin Li

- [2020] Manifold Learning and Nonlinear Homogenization
  - arxiv: `2011.00568` (math.NA)
  - authors: Shi Chen, Qin Li, Jianfeng Lu, Stephen J. Wright

- [2020] On diffusive scaling in acousto-optic imaging
  - arxiv: `2001.07858` (math.AP)
  - authors: Francis J. Chung, Ru-Yu Lai, Qin Li

- [2020] Reconstruction of the emission coefficient in the nonlinear radiative transfer equation
  - arxiv: `2006.14674` (math.AP)
  - authors: Christian Klingenberg, Ru-Yu Lai, Qin Li

- [2019] Structured random sketching for PDE inverse problems
  - arxiv: `1909.11290` (math.NA)
  - authors: Ke Chen, Qin Li, Kit Newton, Steve Wright

- [2019] Ensemble Kalman Inversion: mean-field limit and convergence analysis
  - arxiv: `1908.05575` (math.NA)
  - authors: Zhiyan Ding, Qin Li

- [2019] Parameter Reconstruction for general transport equation
  - arxiv: `1904.10049` (math.AP)
  - authors: Ru-Yu Lai, Qin Li

- [2019] Applications of Kinetic Tools to Inverse Transport Problems
  - arxiv: `1908.00094` (math.AP)
  - authors: Qin Li, Weiran Sun

- [2018] Inverse problems for the stationary transport equation in the diffusion scaling
  - arxiv: `1808.02071` (math.AP)
  - authors: Ru-Yu Lai, Qin Li, Gunther Uhlmann

- [2016] Validity and regularization of classical half-space equations
  - arxiv: `1606.01311` (math.AP)
  - authors: Qin Li, Jianfeng Lu, Weiran Sun

- [2014] A convergent method for linear half-space kinetic equations
  - arxiv: `1408.6630` (math.AP)
  - authors: Qin Li, Jianfeng Lu, Weiran Sun


## li-xiaobin (en=Xiaobin Li) — 1 candidates not in yaml

- [2026] Understanding and Improving UMAP with Geometric and Topological Priors: The JORC-UMAP Algo
  - arxiv: `2601.16552` (cs.LG)
  - authors: Xiaobin Li, Run Zhang


## liu-melissa (en=Chiu-Chu Melissa Liu) — 15 candidates not in yaml

- [2006] Yang-Mills Connections on Nonorientable Surfaces
  - arxiv: `math/0605587` (math.SG)
  - authors: Nan-Kuo Ho, Chiu-Chu Melissa Liu

- [2005] Formulae of one-partition and two-partition Hodge integrals
  - arxiv: `math/0502430` (math.AG)
  - authors: Chiu-Chu Melissa Liu

- [2005] The local Gromov-Witten invariants of configurations of rational curves
  - arxiv: `math/0506488` (math.AG)
  - authors: Dagan Karp, Chiu-Chu Melissa Liu, Marcos Marino

- [2004] A Mathematical Theory of the Topological Vertex
  - arxiv: `math/0408426` (math.AG)
  - authors: Jun Li, Chiu-Chu Melissa Liu, Kefeng Liu, Jian Zhou

- [2004] Positivity of quasi-local mass II
  - arxiv: `math/0412292` (math.DG)
  - authors: Chiu-Chu Melissa Liu, Shing-Tung Yau

- [2004] Connected Components of the Space of Surface Group Representations II
  - arxiv: `math/0406069` (math.SG)
  - authors: Nan-Kuo Ho, Chiu-Chu Melissa Liu

- [2003] A Proof of a Conjecture of Marino-Vafa on Hodge Integrals
  - arxiv: `math/0306434` (math.AG)
  - authors: Chiu-Chu Melissa Liu, Kefeng Liu, Jian Zhou

- [2003] A Formula of Two-Partition Hodge Integrals
  - arxiv: `math/0310272` (math.AG)
  - authors: Chiu-Chu Melissa Liu, Kefeng Liu, Jian Zhou

- [2003] On a Proof of a Conjecture of Marino-Vafa on Hodge Integrals
  - arxiv: `math/0306257` (math.AG)
  - authors: Chiu-Chu Melissa Liu, Kefeng Liu, Jian Zhou

- [2003] Connected Components of The Space of Surface Group Representations
  - arxiv: `math/0303255` (math.SG)
  - authors: Nan-Kuo Ho, Chiu-Chu Melissa Liu

- [2003] Positivity of Quasilocal Mass
  - arxiv: `gr-qc/0303019` (gr-qc)
  - authors: Chiu-Chu Melissa Liu, Shing-Tung Yau

- [2003] Mariño-Vafa Formula and Hodge Integral Identities
  - arxiv: `math/0308015` (math.AG)
  - authors: Chiu-Chu Melissa Liu, Kefeng Liu, Jian Zhou

- [2002] On the Connectedness of Moduli Spaces of Flat Connections over Compact Surfaces
  - arxiv: `math/0211388` (math.SG)
  - authors: Nan-Kuo Ho, Chiu-Chu Melissa Liu

- [2002] Moduli of J-Holomorphic Curves with Lagrangian Boundary Conditions and Open Gromov-Witten 
  - arxiv: `math/0210257` (math.SG)
  - authors: Chiu-Chu Melissa Liu

- [2001] Enumerative geometry of stable maps with Lagrangian boundary conditions and multiple cover
  - arxiv: `math/0103074` (math.AG)
  - authors: Sheldon Katz, Chiu-Chu Melissa Liu


## liu-siqi (en=Siqi Liu) — 4 candidates not in yaml

- [2023] New Codes on High Dimensional Expanders
  - arxiv: `2308.15563` (cs.IT)
  - authors: Irit Dinur, Siqi Liu, Rachel Yun Zhang

- [2021] Hypercontractivity on High Dimensional Expanders: Approximate Efron-Stein Decompositions f
  - arxiv: `2111.09375` (cs.CC)
  - authors: Tom Gur, Noam Lifshitz, Siqi Liu

- [2021] On statistical inference when fixed points of belief propagation are unstable
  - arxiv: `2101.10882` (cs.DS)
  - authors: Siqi Liu, Sidhanth Mohanty, Prasad Raghavendra

- [2019] High-Dimensional Expanders from Expanders
  - arxiv: `1907.10771` (cs.DM)
  - authors: Siqi Liu, Sidhanth Mohanty, Elizabeth Yang


## liu-xiaobo (en=Xiaobo Liu) — 12 candidates not in yaml

- [2006] Quantum hyperbolic invariants for diffeomorphisms of small surfaces
  - arxiv: `math/0603467` (math.GT)
  - authors: Xiaobo Liu

- [2005] A Genus-3 Topological Recursion Relation
  - arxiv: `math/0502457` (math.DG)
  - authors: Takashi Kimura, Xiaobo Liu

- [2004] The quantum Teichmuller space as a noncommutative algebraic object
  - arxiv: `math/0408361` (math.GT)
  - authors: Xiaobo Liu

- [2004] Representations of the quantum Teichmuller space, and invariants of surface diffeomorphism
  - arxiv: `math/0407086` (math.GT)
  - authors: Francis Bonahon, Xiaobo Liu

- [2003] Idempotents on the big phase space
  - arxiv: `math/0310409` (math.DG)
  - authors: Xiaobo Liu

- [2003] Genus-2 Gromov-Witten invariants for manifolds with semisimple quantum cohomology
  - arxiv: `math/0310410` (math.DG)
  - authors: Xiaobo Liu

- [2003] Relations Among Universal Equations For Gromov-Witten Invariants
  - arxiv: `math/0301161` (math.DG)
  - authors: Xiaobo Liu

- [2001] Quantum product on the big phase space and the Virasoro conjecture
  - arxiv: `math/0104030` (math.AG)
  - authors: Xiaobo Liu

- [2000] Isoparametric submanifolds and a Chevalley-type restriction theorem
  - arxiv: `math/0004028` (math.DG)
  - authors: Ernst Heintze, Xiaobo Liu, Carlos Olmos

- [1999] Elliptic Gromov-Witten Invariants And Virasoro Conjecture
  - arxiv: `math/9907113` (math.AG)
  - authors: Xiaobo Liu

- [1999] Homogeneity of infinite dimensional isoparametric submanifolds
  - arxiv: `math/9901150` (math.DG)
  - authors: Ernst Heintze, Xiaobo Liu

- [1998] Virasoro Constraints For Quantum Cohomology
  - arxiv: `math/9806028` (math.AG)
  - authors: Xiaobo Liu, Gang Tian


## liu-zhangju (en=Zhang-Ju Liu) — 3 candidates not in yaml

- [2002] The Local Structure of Lie Bialgebroids
  - arxiv: `math/0210104` (math.DG)
  - authors: Zhang-Ju Liu, Ping Xu

- [1999] Dirac structures and dynamical r-matrices
  - arxiv: `math/9903119` (math.DG)
  - authors: Zhang-Ju Liu, Ping Xu

- [1995] Manin Triples for Lie Bialgebroids
  - arxiv: `dg-ga/9508013` (math.DG)
  - authors: Zhang-Ju Liu, Alan Weinstein, Ping Xu


## lu-wen (en=Wen Lu) — 7 candidates not in yaml

- [2024] Stability equivalence for stochastic differential equations, stochastic differential delay
  - arxiv: `2405.07519` (math.PR)
  - authors: Wen Lu

- [2015] Mean-field backward stochastic differential equations on Markov chains
  - arxiv: `1501.00955` (math.PR)
  - authors: Wen Lu, Yong Ren

- [2013] Mean-field backward stochastic differential equations with subdifferrential operator and i
  - arxiv: `1310.5845` (math.PR)
  - authors: Wen Lu, Yong Ren, Lanying Hu

- [2013] Multivalued backward doubly stochastic differential equations with time delayed coefficien
  - arxiv: `1308.2748` (math.PR)
  - authors: Wen Lu, Yong Ren, Lanying Hu

- [2011] Backward stochastic Volterra integral equations associated with a Levy process and applica
  - arxiv: `1106.6129` (math.PR)
  - authors: Wen Lu

- [2009] $L^p$-solutions of Reflected Backward Doubly Stochastic Differential Equations
  - arxiv: `0912.5060` (math.PR)
  - authors: Wen Lu

- [2009] Reflected BSDE with stochastic Lipschitz coefficient
  - arxiv: `0912.2162` (math.PR)
  - authors: Wen Lu


## manin-yuri (en=Yuri Manin) — 27 candidates not in yaml

- [2022] Cohn-Elkies functions from Gabor frames
  - arxiv: `2212.06778` (math.FA)
  - authors: Yuri Manin, Matilde Marcolli

- [2019] Monoidal structures on the categories of quadratic data
  - arxiv: `1902.03778` (math.CT)
  - authors: Yuri I. Manin, Bruno Vallette

- [2018] Higher structures, quantum groups, and genus zero modular operad
  - arxiv: `1802.04072` (math.CT)
  - authors: Yuri Manin

- [2018] Time and periodicity from Ptolemy to Schroedinger: paradigm shifts vs continuity
  - arxiv: `1812.00364` (math.HO)
  - authors: Yuri I. Manin

- [2015] Symbolic Dynamics, Modular Curves, and Bianchi IX Cosmologies
  - arxiv: `1504.04005` (gr-qc)
  - authors: Yuri Manin, Matilde Marcolli

- [2015] Neural codes and homotopy types: mathematical models of place field recognition
  - arxiv: `1501.00897` (math.HO)
  - authors: Yuri I. Manin

- [2014] Forgotten Motives: the Varieties of Scientific Experience
  - arxiv: `1402.2155` (math.HO)
  - authors: Yuri I. Manin

- [2013] Complexity vs Energy: Theory of Computation and Theoretical Physics
  - arxiv: `1302.6695` (cs.CC)
  - authors: Yuri I. Manin

- [2013] Kolmogorov complexity as a hidden factor of scientific discourse: from Newton's law to dat
  - arxiv: `1301.0081` (math.HO)
  - authors: Yuri I. Manin

- [2012] Foundations as Superstructure. (Reflections of a practicing mathematician)
  - arxiv: `1205.6044` (math.HO)
  - authors: Yuri I. Manin

- [2009] Error-correcting codes and phase transitions
  - arxiv: `0910.5135` (cs.IT)
  - authors: Yuri I. Manin, Matilde Marcolli

- [2007] Modular shadows and the Levy-Mellin infinity-adic transform
  - arxiv: `math/0703718` (math.NT)
  - authors: Yuri Manin, Matilde Marcolli

- [2006] Stability Conditions, Wall-crossing and weighted Gromov-Witten Invariants
  - arxiv: `math/0607580` (math.AG)
  - authors: Arend Bayer, Yuri I. Manin

- [2005] The notion of dimension in geometry and algebra
  - arxiv: `math/0502016` (math.AG)
  - authors: Yuri I. Manin

- [2004] F-manifolds with flat structure and Dubrovin's duality
  - arxiv: `math/0402451` (math.DG)
  - authors: Yuri I. Manin

- [2002] Unfoldings of meromorphic connections and a construction of Frobenius manifolds
  - arxiv: `math/0207089` (math.AG)
  - authors: Claus Hertling, Yuri Manin

- [2002] Holography principle and arithmetic of algebraic curves
  - arxiv: `hep-th/0201036` (hep-th)
  - authors: Yuri I. Manin, Matilde Marcolli

- [2002] Georg Cantor and his heritage
  - arxiv: `math/0209244` (math.AG)
  - authors: Yuri I. Manin

- [2002] Von Zahlen und Figuren
  - arxiv: `math/0201005` (math.AG)
  - authors: Yuri I. Manin

- [2002] Real Multiplication and noncommutative geometry
  - arxiv: `math/0202109` (math.AG)
  - authors: Yuri I. Manin

- [2001] Continued fractions, modular symbols, and non-commutative geometry
  - arxiv: `math/0102006` (math.NT)
  - authors: Yuri I. Manin, Matilde Marcolli

- [2001] (Semi)simple exercises in quantum cohomology
  - arxiv: `math/0103164` (math.AG)
  - authors: Arend Bayer, Yuri Manin

- [2000] Theta functions, quantum tori and Heisenberg groups
  - arxiv: `math/0011197` (math.AG)
  - authors: Yuri I. Manin

- [2000] Moduli, Motives, Mirrors (Plenary talk at the 3rd ECM, Barcelona, July 10-14, 2000)
  - arxiv: `math/0005144` (math.AG)
  - authors: Yuri I. Manin

- [1999] Classical computing, quantum computing, and Shor's factoring algorithm
  - arxiv: `quant-ph/9903008` (quant-ph)
  - authors: Yuri I. Manin

- [1998] Weak Frobenius manifolds
  - arxiv: `math/9810132` (math.QA)
  - authors: Claus Hertling, Yuri Manin

- [1997] Relations between the correlators of the topological sigma-model coupled to gravity
  - arxiv: `alg-geom/9708024` (math.AG)
  - authors: Maxim Kontsevich, Yuri I. Manin


## mazzocco (en=Marta Mazzocco) — 12 candidates not in yaml

- [2007] A remark on the Hankel determinant formula for solutions of the Toda equation
  - arxiv: `nlin/0701029` (nlin.SI)
  - authors: Kenji Kajiwara, Marta Mazzocco, Yasuhiro Ohta

- [2006] The Hamiltonian Structure of the Second Painleve Hierarchy
  - arxiv: `nlin/0610066` (nlin.SI)
  - authors: Marta Mazzocco, Man Yue Mo

- [2006] On the Reductions and Classical Solutions of the Schlesinger equations
  - arxiv: `math/0610327` (math.DG)
  - authors: B. Dubrovin, M. Mazzocco

- [2005] Generating Function Associated with the Hankel Determinant Formula for the Solutions of th
  - arxiv: `nlin/0512041` (nlin.SI)
  - authors: Nalini Joshi, Kenji Kajiwara, Marta Mazzocco

- [2004] Generating Function Associated with the Determinant Formula for the Solutions of the Painl
  - arxiv: `nlin/0406035` (nlin.SI)
  - authors: Nalini Joshi, Kenji Kajiwara, Marta Mazzocco

- [2003] Canonical structure and symmetries of the Schlesinger equations
  - arxiv: `math/0311261` (math.DG)
  - authors: Boris Dubrovin, Marta Mazzocco

- [2003] Irregular isomonodromic deformations for Garnier systems and Okamoto's canonical transform
  - arxiv: `nlin/0306020` (nlin.SI)
  - authors: M. Mazzocco

- [2002] Existence and Uniqueness of Tri-tronquée Solutions of the second Painlevé hierarchy
  - arxiv: `math/0212117` (math.CA)
  - authors: N. Joshi, M. Mazzocco

- [2001] The geometry of the classical solutions of the Garnier systems
  - arxiv: `math/0106208` (math.CA)
  - authors: Marta Mazzocco

- [2000] Rational Solutions of the Painleve' VI Equation
  - arxiv: `nlin/0007036` (nlin.SI)
  - authors: M. Mazzocco

- [1999] Picard and Chazy solutions to the Painleve' VI equation
  - arxiv: `math/9901054` (math.AG)
  - authors: M. Mazzocco

- [1998] Monodromy of certain Painleve' VI transcendents and reflection groups
  - arxiv: `math/9806056` (math.AG)
  - authors: B. Dubrovin, M. Mazzocco


## novikov-sergei (en=Sergei Novikov) — 4 candidates not in yaml

- [2010] 2D Schrodinger Operator, (2+1) Systems and New Reductions. The 2D Burgers Hierarchy and In
  - arxiv: `1005.0612` (math-ph)
  - authors: P. Grinevich, A. Mironov, S. Novikov

- [2010] On the Ground Level of Purely Magnetic Algebro-Geometric 2D Pauli Operator (spin 1/2)
  - arxiv: `1004.1157` (math-ph)
  - authors: P. Grinevich, A. Mironov, S. Novikov

- [2010] New Reductions and Nonlinear Systems for 2D Schrodinger Operators
  - arxiv: `1001.4300` (nlin.SI)
  - authors: P. Grinevich, A. Mironov, S. Novikov

- [2009] Singular Finite-Gap Operators and Indefinite Metric
  - arxiv: `0903.3976` (math-ph)
  - authors: P. Grinevich, S. Novikov


## qiao-yu (en=Yu Qiao) — 7 candidates not in yaml

- [2024] Intrinsic nonequilibrium distribution of large ions in charged small nanopores
  - arxiv: `2407.04599` (cond-mat.soft)
  - authors: Yu Qiao, Meng Wang

- [2023] Second law of thermodynamics: Spontaneous cold-to-hot heat transfer in a nonchaotic medium
  - arxiv: `2312.09161` (cond-mat.stat-mech)
  - authors: Yu Qiao, Zhaoru Shang

- [2023] Searching for quantum non-thermodynamic phenomena
  - arxiv: `2310.05849` (cond-mat.stat-mech)
  - authors: Yu Qiao

- [2022] On the second law of thermodynamics: An ideal-gas flow spontaneously induced by a locally 
  - arxiv: `2206.12736` (cond-mat.stat-mech)
  - authors: Yu Qiao, Zhaoru Shang

- [2021] Molecular-Sized Outward-Swinging Gate: Experiment and Theoretical Analysis of a Locally No
  - arxiv: `2106.06648` (cond-mat.soft)
  - authors: Yu Qiao, Zhaoru Shang, Rui Kou

- [2021] Producing Useful Work in a Cycle by Absorbing Heat from a Single Thermal Reservoir: An Inv
  - arxiv: `2104.01491` (cond-mat.stat-mech)
  - authors: Yu Qiao, Zhaoru Shang

- [2012] Uniform shift estimates for transmission problems and optimal rates of convergence for the
  - arxiv: `1212.6287` (math.NA)
  - authors: Hengguang Li, Victor Nistor, Yu Qiao


## ruan-yongbin (en=Yongbin Ruan) — 19 candidates not in yaml

- [2006] Birational cobordism invariance of uniruled symplectic manifolds
  - arxiv: `math/0611592` (math.SG)
  - authors: Jianxun Hu, Tian-Jun Li, Yongbin Ruan

- [2006] A Stringy Product on Twisted Orbifold K-theory
  - arxiv: `math/0605534` (math.AT)
  - authors: Alejandro Adem, Yongbin Ruan, Bin Zhang

- [2005] Gerbes and twisted orbifold quantum cohomology
  - arxiv: `math/0504369` (math.AG)
  - authors: Jianzhong Pan, Yongbin Ruan, Xiaoqin Yin

- [2004] Geometry and analysis of spin equations
  - arxiv: `math/0409434` (math.DG)
  - authors: Huijun Fan, Tyler J. Jarvis, Yongbin Ruan

- [2002] Stringy orbifolds
  - arxiv: `math/0201123` (math.AG)
  - authors: Yongbin Ruan

- [2001] Orbifold Gromov-Witten Theory
  - arxiv: `math/0103156` (math.AG)
  - authors: Weimin Chen, Yongbin Ruan

- [2001] Cohomology ring of crepant resolutions of orbifolds
  - arxiv: `math/0108195` (math.AG)
  - authors: Yongbin Ruan

- [2001] Twisted Orbifold K-Theory
  - arxiv: `math/0107168` (math.AT)
  - authors: Alejandro Adem, Yongbin Ruan

- [2000] Stringy Geometry and Topology of Orbifolds
  - arxiv: `math/0011149` (math.AG)
  - authors: Yongbin Ruan

- [2000] A New Cohomology Theory for Orbifold
  - arxiv: `math/0004129` (math.AG)
  - authors: Weimin Chen, Yongbin Ruan

- [2000] Orbifold Quantum Cohomology
  - arxiv: `math/0005198` (math.AG)
  - authors: Weimin Chen, Yongbin Ruan

- [2000] Discrete torsion and twisted orbifold cohomology
  - arxiv: `math/0005299` (math.AG)
  - authors: Yongbin Ruan

- [1998] Symplectic surgery and Gromov-Witten invariants of Calabi-Yau 3-folds I
  - arxiv: `math/9803036` (math.AG)
  - authors: An-Min Li, Yongbin Ruan

- [1998] Surgery, quantum cohomology and birational geometry
  - arxiv: `math/9810039` (math.AG)
  - authors: Yongbin Ruan

- [1996] Higher genus symplectic invariants and sigma model coupled with gravity
  - arxiv: `alg-geom/9601005` (math.AG)
  - authors: Yongbin Ruan, Gang Tian

- [1996] Virtual neighborhoods and pseudo-holomorphic curves
  - arxiv: `alg-geom/9611021` (math.AG)
  - authors: Yongbin Ruan

- [1996] Composition law and Nodal genus-2 curves in P^2
  - arxiv: `alg-geom/9606014` (math.AG)
  - authors: Sheldon Katz, Zhenbo Qin, Yongbin Ruan

- [1996] Quantum cohomology of projective bundles over P^n
  - arxiv: `math/9607223` (math.AG)
  - authors: Zhenbo Qin, Yongbin Ruan

- [1995] Quantum cohomology of projective bundles over $\Pee^n$
  - arxiv: `alg-geom/9510010` (math.AG)
  - authors: Zhenbo Qin, Yongbin Ruan


## ryszard-nest (en=Ryszard Nest) — 17 candidates not in yaml

- [2009] Equivariant Poincaré duality for quantum group actions
  - arxiv: `0902.3987` (math.KT)
  - authors: Ryszard Nest, Christian Voigt

- [2008] C*-Algebras over Topological Spaces: Filtrated K-Theory
  - arxiv: `0810.0096` (math.OA)
  - authors: Ralf Meyer, Ryszard Nest

- [2008] Twisted cyclic theory, equivariant KK theory and KMS States
  - arxiv: `0808.3029` (math.OA)
  - authors: Alan L. Carey, Sergey Neshveyev, Ryszard Nest, Adam Rennie

- [2008] Fibrations with noncommutative fibers
  - arxiv: `0810.0118` (math.KT)
  - authors: Siegfried Echterhoff, Ryszard Nest, Herve Oyono-Oyono

- [2007] KK-theory and Spectral Flow in von Neumann Algebras
  - arxiv: `math/0701326` (math.OA)
  - authors: Jens Kaad, Ryszard Nest, Adam Rennie

- [2007] Deformations of gerbes on smooth manifolds
  - arxiv: `math/0701380` (math.QA)
  - authors: P. Bressler, A. Gorokhovsky, R. Nest, B. Tsygan

- [2006] Deformations of Azumaya algebras
  - arxiv: `math/0609575` (math.QA)
  - authors: P. Bressler, A. Gorokhovsky, R. Nest, B. Tsygan

- [2005] A Continuous Field of C*-algebras and the Tangent Groupoid for Manifolds with Boundary
  - arxiv: `math/0507317` (math.FA)
  - authors: Johannes Aastrup, Ryszard Nest, Elmar Schrohe

- [2005] Deformation quantization of gerbes
  - arxiv: `math/0512136` (math.QA)
  - authors: P. Bressler, A. Gorokhovsky, R. Nest, B. Tsygan

- [2004] Remarks on modules over deformation quantization algebras
  - arxiv: `math-ph/0411066` (math-ph)
  - authors: Ryszard Nest, Boris Tsygan

- [2001] The Existence and Stability of Noncommutative Scalar Solitons
  - arxiv: `hep-th/0107121` (hep-th)
  - authors: Bergfinnur Durhuus, Thordur Jonsson, Ryszard Nest

- [2001] The Connes-Kasparov conjecture for almost connected groups
  - arxiv: `math/0110130` (math.OA)
  - authors: Jerome Chabert, Siegfried Echterhoff, Ryszard Nest

- [2000] Local formula for the index of a Fourier Integral Operator
  - arxiv: `math/0004022` (math.DG)
  - authors: Eric Leichtnam, Ryszard Nest, Boris Tsygan

- [2000] Riemann-Roch via deformation quantization, II
  - arxiv: `math/0002115` (math.KT)
  - authors: Paul Bressler, Ryszard Nest, Boris Tsygan

- [1999] Index of $Γ$-equivariant Toeplitz operators
  - arxiv: `math/9911042` (math.OA)
  - authors: Ryszard Nest, Florin Radulescu

- [1999] Deformations of symplectic Lie algebroids, deformations of holomorphic symplectic structur
  - arxiv: `math/9906020` (math.QA)
  - authors: Ryszard Nest, Boris Tsygan

- [1998] Fukaya Type Categories for Associative Algebras
  - arxiv: `math/9803140` (math.QA)
  - authors: Ryszard Nest, Boris Tsygan


## sabbah (en=Claude Sabbah) — 14 candidates not in yaml

- [2006] Asymptotic expansion of holonomic distributions of one complex variable
  - arxiv: `math/0611474` (math.CA)
  - authors: Claude Sabbah

- [2006] The Abelian/Nonabelian Correspondence and Frobenius Manifolds
  - arxiv: `math/0610265` (math.AG)
  - authors: Ionut Ciocan-Fontanine, Bumsig Kim, Claude Sabbah

- [2006] Quantum cohomology of the Grassmannian and alternate Thom-Sebastiani
  - arxiv: `math/0611475` (math.AG)
  - authors: Bumsig Kim, Claude Sabbah

- [2005] Fourier-Laplace transform of a variation of polarized complex Hodge structure
  - arxiv: `math/0508551` (math.AG)
  - authors: Claude Sabbah

- [2005] Polarizable twistor D-modules
  - arxiv: `math/0503038` (math.AG)
  - authors: Claude Sabbah

- [2004] Fourier-Laplace transform of irreducible regular differential systems on the Riemann spher
  - arxiv: `math/0408294` (math.AG)
  - authors: Claude Sabbah

- [2002] Gauss-Manin systems, Brieskorn lattices and Frobenius structures (I)
  - arxiv: `math/0211352` (math.AG)
  - authors: Antoine Douai, Claude Sabbah

- [2002] Gauss-Manin systems, Brieskorn lattices and Frobenius structures (II)
  - arxiv: `math/0211353` (math.AG)
  - authors: Antoine Douai, Claude Sabbah

- [1999] Harmonic metrics and connections with irregular singularities
  - arxiv: `math/9905039` (math.AG)
  - authors: Claude Sabbah

- [1999] Vanishing cycles and Hermitian duality
  - arxiv: `math/9910156` (math.AG)
  - authors: Claude Sabbah

- [1998] Hypergeometric periods for a tame polynomial
  - arxiv: `math/9805077` (math.AG)
  - authors: Claude Sabbah

- [1998] Semicontinuity of the spectrum at infinity
  - arxiv: `math/9805086` (math.AG)
  - authors: Andras Nemethi, Claude Sabbah

- [1998] On a twisted de Rham complex
  - arxiv: `math/9805087` (math.AG)
  - authors: Claude Sabbah

- [1995] Moduli of pre-$\cal D$-modules, perverse sheaves and the Riemann-Hilbert morphism -I
  - arxiv: `alg-geom/9503021` (math.AG)
  - authors: Nitin Nitsure, Claude Sabbah


## si-li (en=Si Li) — 3 candidates not in yaml

- [2012] Reconstruction of Network Evolutionary History from Extant Network Topology and Duplicatio
  - arxiv: `1203.2430` (q-bio.PE)
  - authors: Si Li, Kwok Pui Choi, Taoyang Wu, Louxin Zhang

- [2005] Supersymmetric Quantum Mechanics and Lefschetz fixed-point formula
  - arxiv: `hep-th/0511101` (hep-th)
  - authors: Si Li

- [2005] Hamiltonian Formalism of the de-Sitter Invariant Special Relativity
  - arxiv: `hep-th/0512319` (hep-th)
  - authors: Mu-Lin Yan, Neng-Chao Xiao, Wei Huang, Si Li


## sun-shanzhong (en=Shanzhong Sun) — 1 candidates not in yaml

- [2026] Two Regularized Determinants of Laplacian through Resurgence theory
  - arxiv: `2605.03960` (math-ph)
  - authors: Wen Shen, Shanzhong Sun


## tian-gang (en=Gang Tian) — 118 candidates not in yaml

- [2025] Stability thresholds for big classes
  - arxiv: `2501.18150` (math.DG)
  - authors: Chenzi Jin, Yanir A. Rubinstein, Gang Tian

- [2025] Compactification of metric moduli space of $K3$ surfaces
  - arxiv: `2512.13315` (math.DG)
  - authors: Zexuan Ouyang, Gang Tian

- [2025] Hermitian-Einstein Metrics on Parabolic Bundles over compact complex surfaces
  - arxiv: `2506.15458` (math.DG)
  - authors: Xilun Li, Gang Tian

- [2025] A geometric characterization of potential Navier-Stokes singularities
  - arxiv: `2501.08976` (math.AP)
  - authors: Zhen Lei, Xiao Ren, Gang Tian

- [2025] The biharmonic hypersurface flow and the Willmore flow in higher dimensions
  - arxiv: `2505.19727` (math.DG)
  - authors: Yu Fu, Min-Chun Hong, Gang Tian

- [2025] Laplace comparison on Kähler Ricci flow and convergence
  - arxiv: `2509.14820` (math.DG)
  - authors: Gang Tian, Qi S. Zhang, Zhenlei Zhang, Meng Zhu, Xiaohua Zhu

- [2024] Asymptotics of discrete Okounkov bodies and thresholds
  - arxiv: `2410.20694` (math.AG)
  - authors: Chenzi Jin, Yanir A. Rubinstein, Gang Tian

- [2024] Gauged linear sigma model in geometric phase. II. the virtual cycle
  - arxiv: `2407.14545` (math-ph)
  - authors: Gang Tian, Guangbo Xu

- [2024] Global solutions to the Euler-Coriolis system
  - arxiv: `2405.18390` (math.AP)
  - authors: Xiao Ren, Gang Tian

- [2023] Finite time singularities of the Kähler-Ricci flow
  - arxiv: `2310.07945` (math.DG)
  - authors: Wangjian Jian, Jian Song, Gang Tian

- [2023] A new proof of Perelman's scalar curvature and diameter estimates for the Kähler-Ricci flo
  - arxiv: `2310.07943` (math.DG)
  - authors: Wangjian Jian, Jian Song, Gang Tian

- [2023] Geometric regularity of blow-up limits of the Kähler-Ricci flow
  - arxiv: `2310.08610` (math.DG)
  - authors: Max Hallgren, Wangjian Jian, Jian Song, Gang Tian

- [2022] A Note On Kähler-Ricci Flow on Fano Threefolds
  - arxiv: `2210.15263` (math.DG)
  - authors: Minghao Miao, Gang Tian

- [2022] Horosymmetric limits of Kähler-Ricci flow on Fano $G$-manifolds
  - arxiv: `2209.05029` (math.DG)
  - authors: Gang Tian, Xiaohua Zhu

- [2022] Kähler stability of symplectic forms
  - arxiv: `2202.04564` (math.DG)
  - authors: Jeffrey Streets, Gang Tian

- [2022] Principal minors of Gaussian orthogonal ensemble
  - arxiv: `2205.05732` (math.PR)
  - authors: Renjie Feng, Gang Tian, Dongyi Wei, Dong Yao

- [2021] Counting pointlike instantons virtually without gluing
  - arxiv: `2110.15379` (math.SG)
  - authors: Gang Tian, Guangbo Xu

- [2021] Kähler-Ricci flow for deformed complex structures
  - arxiv: `2107.12680` (math.DG)
  - authors: Gang Tian, Liang Zhang, Xiaohua Zhu

- [2020] Basis divisors and balanced metrics
  - arxiv: `2008.08829` (math.DG)
  - authors: Yanir A. Rubinstein, Gang Tian, Kewei Zhang

- [2020] Singular Kähler-Einstein metrics on $\mathbb Q$-Fano compactifications of Lie groups
  - arxiv: `2001.11320` (math.DG)
  - authors: Yan Li, Gang Tian, Xiaohua Zhu

- [2020] Almost Hermitian Ricci flow
  - arxiv: `2001.06670` (math.DG)
  - authors: Casey Lynn Kelleher, Gang Tian

- [2019] Collapsing behavior of Ricci-flat Kahler metrics and long time solutions of the Kahler-Ric
  - arxiv: `1904.08345` (math.DG)
  - authors: Jian Song, Gang Tian, Zhenlei Zhang

- [2019] A wall-crossing formula and the invariance of GLSM correlation functions
  - arxiv: `1905.05032` (math.SG)
  - authors: Gang Tian, Guangbo Xu

- [2019] The uniform version of Yau-Tian-Donaldson conjecture for singular Fano varieties
  - arxiv: `1903.01215` (math.DG)
  - authors: Chi Li, Gang Tian, Feng Wang

- [2019] The Berry-Esseen Theorem for Circular $β$-ensemble
  - arxiv: `1905.09448` (math.PR)
  - authors: Renjie Feng, Gang Tian, Dongyi Wei

- [2019] On the existence of conic Kahler-Einstein metrics
  - arxiv: `1903.12547` (math.DG)
  - authors: Gang Tian, Feng Wang

- [2019] Small gaps of GOE
  - arxiv: `1901.01567` (math.PR)
  - authors: Renjie Feng, Gang Tian, Dongyi Wei

- [2018] On uniform K-stability of pairs
  - arxiv: `1812.05746` (math.DG)
  - authors: Gang Tian

- [2018] Spectrum of SYK model
  - arxiv: `1801.10073` (math-ph)
  - authors: Renjie Feng, Gang Tian, Dongyi Wei

- [2018] Gauged Linear Sigma Model in Geometric Phases. I
  - arxiv: `1809.00424` (math-ph)
  - authors: Gang Tian, Guangbo Xu

- [2018] Spectrum of SYK model II: Central limit theorem
  - arxiv: `1806.05714` (math-ph)
  - authors: Renjie Feng, Gang Tian, Dongyi Wei

- [2018] Spectrum of SYK model III: Large deviations and concentration of measures
  - arxiv: `1806.04701` (math-ph)
  - authors: Renjie Feng, Gang Tian, Dongyi Wei

- [2018] Cheeger-Colding-Tian theory for conic Kahler-Einstein metrics
  - arxiv: `1807.07209` (math.DG)
  - authors: Gang Tian, Feng Wang

- [2018] Singular limits of Kähler-Ricci flow on Fano $G$-manifolds
  - arxiv: `1807.09167` (math.DG)
  - authors: Yan Li, Gang Tian, Xiaohua Zhu

- [2018] Relative volume comparison of Ricci Flow and its applications
  - arxiv: `1802.09506` (math.DG)
  - authors: Gang Tian, Zhenlei Zhang

- [2017] Uniqueness of the Mean Field Equation and Rigidity of Hawking Mass
  - arxiv: `1706.06766` (math.AP)
  - authors: Yuguang Shi, Jiacheng Sun, Gang Tian, Dongyi Wei

- [2017] The symplectic approach of gauged linear $σ$-model
  - arxiv: `1702.01428` (math.SG)
  - authors: Gang Tian, Guangbo Xu

- [2017] On the Yau-Tian-Donaldson conjecture for singular Fano varieties
  - arxiv: `1711.09530` (math.DG)
  - authors: Chi Li, Gang Tian, Feng Wang

- [2016] Virtual cycles of gauged Witten equation
  - arxiv: `1602.07638` (math.SG)
  - authors: Gang Tian, Guangbo Xu

- [2016] Asypmtotics of enumerative invariants in $\CC P^2$
  - arxiv: `1609.06425` (math.AP)
  - authors: Gang Tian, Dongyi Wei

- [2015] Orbifold regularity of weak Kahler-Einstein metrics
  - arxiv: `1505.01925` (math.DG)
  - authors: Chi Li, Gang Tian

- [2015] Compactness results for triholomorphic maps
  - arxiv: `1507.06558` (math.AP)
  - authors: Costante Bellettini, Gang Tian

- [2015] Convergence of Kähler-Ricci flow on lower dimensional algebraic manifolds of general type
  - arxiv: `1505.01038` (math.DG)
  - authors: Gang Tian, Zhenlei Zhang

- [2015] Properness of log $F$-functionals
  - arxiv: `1504.03197` (math.DG)
  - authors: Gang Tian, Xiaohua Zhu

- [2015] Correction to Section 19.2 of Ricci Flow and the Poincare Conjecture
  - arxiv: `1512.00699` (math.DG)
  - authors: John Morgan, Gang Tian

- [2015] Bounding diameter of singular Kähler metric
  - arxiv: `1503.03159` (math.DG)
  - authors: Gabriele La Nave, Gang Tian, Zhenlei Zhang

- [2014] K-stability implies CM-stability
  - arxiv: `1409.7836` (math.DG)
  - authors: Gang Tian

- [2014] A continuity method to construct canonical metrics
  - arxiv: `1410.3157` (math.DG)
  - authors: Gabriele La Nave, Gang Tian

- [2014] A compactness result for Fano manifolds and Kähler Ricci flows
  - arxiv: `1404.3783` (math.DG)
  - authors: Gang Tian, Qi S. Zhang

- [2014] Correlation functions of gauged linear $σ$-model
  - arxiv: `1406.4253` (math.SG)
  - authors: Gang Tian, Guangbo Xu

- [2014] Analysis of gauged Witten equation
  - arxiv: `1405.6352` (math.SG)
  - authors: Gang Tian, Guangbo Xu

- [2013] Stability of pairs
  - arxiv: `1310.5544` (math.DG)
  - authors: Gang Tian

- [2013] The Yang-Mills α-flow in vector bundles over four manifolds and its applications
  - arxiv: `1303.0628` (math.DG)
  - authors: Min-Chun Hong, Gang Tian, Hao Yin

- [2013] On the distance control problem in Ricci flows
  - arxiv: `1303.1895` (math.DG)
  - authors: Gang Tian, Qi S. Zhang

- [2013] Regularity of Kähler-Ricci flow
  - arxiv: `1304.2651` (math.DG)
  - authors: Gang Tian, Zhenlei Zhang

- [2013] Regularity of Kähler-Ricci flows on Fano manifolds
  - arxiv: `1310.5897` (math.DG)
  - authors: Gang Tian, Zhenlei Zhang

- [2012] K-stability and Kähler-Einstein metrics
  - arxiv: `1211.4669` (math.DG)
  - authors: Gang Tian

- [2012] On the structure of almost Einstein manifolds
  - arxiv: `1202.2912` (math.DG)
  - authors: Gang Tian, Bing Wang

- [2012] Isoperimetric inequality under Kähler Ricci flow
  - arxiv: `1203.1400` (math.DG)
  - authors: Gang Tian, Qi S. Zhang

- [2012] On smoothness of timelike maximal cylinders in three dimensional vacuum spacetimes
  - arxiv: `1201.5183` (math.DG)
  - authors: Luc Nguyen, Gang Tian

- [2011] Generalized Kahler Geometry and the Pluriclosed Flow
  - arxiv: `1109.0503` (math.DG)
  - authors: Jeffrey Streets, Gang Tian

- [2011] Supremum of Perelman's entropy and Kähler-Ricci flow on a Fano manifold
  - arxiv: `1107.4018` (math.DG)
  - authors: Gang Tian, Shijin Zhang, Zhenlei Zhang, Xiaohua Zhu

- [2011] Convergence of Kähler-Ricci flow on Fano manifolds, II
  - arxiv: `1102.4798` (math.DG)
  - authors: Gang Tian, Xiaohua Zhu

- [2011] Bounding scalar curvature for global solutions of the Kahler-Ricci flow
  - arxiv: `1111.5681` (math.DG)
  - authors: Jian Song, Gang Tian

- [2010] Symplectic curvature flow
  - arxiv: `1012.2104` (math.DG)
  - authors: Jeffrey Streets, Gang Tian

- [2010] Degeneration of Kähler-Ricci solitons
  - arxiv: `1006.1577` (math.DG)
  - authors: Gang Tian, Zhenlei Zhang

- [2010] Regularity results for pluriclosed flow
  - arxiv: `1008.2794` (math.DG)
  - authors: Jeff Streets, Gang Tian

- [2009] Orientability and real Seiberg-Witten invariants
  - arxiv: `0905.0280` (math.DG)
  - authors: Gang Tian, Shuguang Wang

- [2009] The Kahler-Ricci flow through singularities
  - arxiv: `0909.4898` (math.DG)
  - authors: Jian Song, Gang Tian

- [2009] Soliton-type metrics and Kähler-Ricci flow on symplectic quotients
  - arxiv: `0903.2413` (math.DG)
  - authors: Gabriele La Nave, Gang Tian

- [2009] Geometric Structures of Collapsing Riemannian Manifolds II: N*-bundles and Almost Ricci Fl
  - arxiv: `0906.4646` (math.DG)
  - authors: Aaron Naber, Gang Tian

- [2009] A parabolic flow of pluriclosed metrics
  - arxiv: `0903.4418` (math.DG)
  - authors: Jeffrey Streets, Gang Tian

- [2008] Completion of the Proof of the Geometrization Conjecture
  - arxiv: `0809.4040` (math.DG)
  - authors: John Morgan, Gang Tian

- [2008] Canonical measures and Kahler-Ricci flow
  - arxiv: `0802.2570` (math.DG)
  - authors: Jian Song, Gang Tian

- [2008] A note on Kähler-Ricci soliton
  - arxiv: `0806.2848` (math.DG)
  - authors: Xiuxiong Chen, Song Sun, Gang Tian

- [2008] Hermitian Curvature Flow
  - arxiv: `0804.4109` (math.DG)
  - authors: Jeffrey Streets, Gang Tian

- [2008] Geometric Structures of Collapsing Riemannian Manifolds I
  - arxiv: `0804.2275` (math.DG)
  - authors: Aaron Naber, Gang Tian

- [2008] Perelman's W-functional and stability of Kähler-Ricci flow
  - arxiv: `0801.3504` (math.DG)
  - authors: Gang Tian, Xiaohua Zhu

- [2007] Translating solutions to Lagrangian mean curvature flow
  - arxiv: `0711.4341` (math.DG)
  - authors: André Neves, Gang Tian

- [2007] Existence and Uniqueness of constant mean curvature foliation of asymptotically hyperbolic
  - arxiv: `0711.4331` (math.DG)
  - authors: Andre Neves, Gang Tian

- [2007] A uniform L^{\infty} estimate for complex Monge-Ampere equations
  - arxiv: `0710.1144` (math.DG)
  - authors: Slawomir Kolodziej, Gang Tian

- [2006] Ricci Flow and the Poincare Conjecture
  - arxiv: `math/0607607` (math.DG)
  - authors: John W. Morgan, Gang Tian

- [2006] Constructing virtual Euler cycles and classes
  - arxiv: `math/0605290` (math.SG)
  - authors: Guangcun Lu, Gang Tian

- [2006] CM Stability And The Generalized Futaki Invariant II
  - arxiv: `math/0606505` (math.DG)
  - authors: Sean Timothy Paul, Gang Tian

- [2006] Existence and Uniqueness of constant mean curvature foliation of asymptotically hyperbolic
  - arxiv: `math/0610767` (math.DG)
  - authors: André Neves, Gang Tian

- [2006] The Kähler-Ricci flow on surfaces of positive Kodaira dimension
  - arxiv: `math/0602150` (math.DG)
  - authors: Jian Song, Gang Tian

- [2006] Volume growth, curvature decay, and critical metrics
  - arxiv: `math/0612491` (math.DG)
  - authors: Jeff Viaclovsky, Gang Tian

- [2006] Virtual Manifolds and Localization
  - arxiv: `math/0610369` (math.GT)
  - authors: Bohui Chen, Gang Tian

- [2006] CM Stability and the Generalized Futaki Invariant I
  - arxiv: `math/0605278` (math.AG)
  - authors: Sean T. Paul, Gang Tian

- [2005] On the uniqueness of the foliation of spheres of constant mean curvature in asymptotically
  - arxiv: `math/0506005` (math.DG)
  - authors: Jie Qing, Gang Tian

- [2005] The log term of Szego Kernel
  - arxiv: `math/0505587` (math.DG)
  - authors: Zhiqin Lu, Gang Tian

- [2005] A note on uniformization of Riemann surfaces by Ricci flow
  - arxiv: `math/0505163` (math.DG)
  - authors: Xiuxiong Chen, Peng Lu, Gang Tian

- [2004] Algebraic and Analytic K-Stability
  - arxiv: `math/0405530` (math.DG)
  - authors: Sean T. Paul, Gang Tian

- [2004] A compactification of the moduli space of twisted holomorphic maps
  - arxiv: `math/0404407` (math.SG)
  - authors: Ignasi Mundet i Riera, Gang Tian

- [2004] Analysis of Geometric Stability
  - arxiv: `math/0404223` (math.DG)
  - authors: Sean Timothy Paul, Gang Tian

- [2004] Rigidity of Asymptotically Hyperboblic Manifolds
  - arxiv: `math/0402358` (math.DG)
  - authors: Yuguang Shi, Gang Tian

- [2004] Geometry of Kaehler metrics and holomorphic foliation by discs
  - arxiv: `math/0409433` (math.DG)
  - authors: Xiuxiong Chen, Gang Tian

- [2003] The Singular Set of 1-1 Integral Currents
  - arxiv: `math/0310052` (math.AP)
  - authors: Tristan Riviere, Gang Tian

- [2003] Bach-flat asymptotically locally Euclidean metrics
  - arxiv: `math/0310302` (math.DG)
  - authors: Gang Tian, Jeff Viaclovsky

- [2003] Moduli spaces of critical Riemannian metrics in dimension four
  - arxiv: `math/0312318` (math.DG)
  - authors: Jeff Viaclovsky, Gang Tian

- [2003] On the holomorphicity of genus two Lefschetz fibrations
  - arxiv: `math/0305343` (math.SG)
  - authors: Bernd Siebert, Gang Tian

- [2002] Infinite geodesic rays in the space of Kahler potentials
  - arxiv: `math/0210389` (math.DG)
  - authors: Claudio Arezzo, Gang Tian

- [2002] A singularity removal theorem for Yang-Mills fields in higher dimensions
  - arxiv: `math/0209352` (math.DG)
  - authors: Terence Tao, Gang Tian

- [2002] Compactification of the moduli spaces of vortices and coupled vortices
  - arxiv: `math/0203078` (math.DG)
  - authors: Gang Tian, Baozhong Yang

- [2002] Geometry and nonlinear analysis
  - arxiv: `math/0212404` (math.DG)
  - authors: Gang Tian

- [2000] Instantons and the monopole-like equations in eight dimensions
  - arxiv: `hep-th/0004167` (hep-th)
  - authors: Yi-hong Gao, Gang Tian

- [2000] Ricci flow on Kaehler-Einstein surfaces
  - arxiv: `math/0010008` (math.DG)
  - authors: Xiuxiong Chen, Gang Tian

- [2000] Ricci flow on Kaehler manifolds
  - arxiv: `math/0010007` (math.DG)
  - authors: Xiuxiong Chen, Gang Tian

- [2000] Gauge theory and calibrated geometry, I
  - arxiv: `math/0010015` (math.DG)
  - authors: Gang Tian

- [1998] Virasoro Constraints For Quantum Cohomology
  - arxiv: `math/9806028` (math.AG)
  - authors: Xiaobo Liu, Gang Tian

- [1998] Comparison of the algebraic and the symplectic Gromov-Witten invariants
  - arxiv: `alg-geom/9712035` (math.AG)
  - authors: Jun Li, Gang Tian

- [1997] Weinstein Conjecture and GW Invariants
  - arxiv: `dg-ga/9712020` (math.DG)
  - authors: Gang Liu, Gang Tian

- [1996] Higher genus symplectic invariants and sigma model coupled with gravity
  - arxiv: `alg-geom/9601005` (math.AG)
  - authors: Yongbin Ruan, Gang Tian

- [1996] Virtual moduli cycles and Gromov-Witten invariants of general symplectic manifolds
  - arxiv: `alg-geom/9608032` (math.AG)
  - authors: Jun Li, Gang Tian

- [1996] Virtual moduli cycles and Gromov-Witten invariants of algebraic varieties
  - arxiv: `alg-geom/9602007` (math.AG)
  - authors: Jun Li, Gang Tian

- [1996] On the semi-simplicity of the quantum cohomology algebras of complete intersections
  - arxiv: `alg-geom/9611035` (math.AG)
  - authors: Gang Tian, Geng Xu

- [1995] The quantum cohomology of homogeneous varieties
  - arxiv: `alg-geom/9504009` (math.AG)
  - authors: Jun Li, Gang Tian

- [1994] On Quantum Cohomology Rings of Fano Manifolds and a Formula of Vafa and Intriligator
  - arxiv: `alg-geom/9403010` (math.AG)
  - authors: Bernd Siebert, Gang Tian


## wang-xin (en=Xin Wang) — 120 candidates not in yaml

- [2026] Solution of the Ising model with Brascamp-Kunz boundary conditions by the transfer matrix 
  - arxiv: `2604.16992` (cond-mat.stat-mech)
  - authors: De-Zhang Li, Xin Wang

- [2026] More on 5d Wilson Loops in Higher-Rank Theories and Blowup Equations
  - arxiv: `2602.09807` (hep-th)
  - authors: Minhao Liu, Xin Wang, Rui-Dong Zhu

- [2026] A Unified Glassy Rheology for Granular Matter
  - arxiv: `2604.14109` (cond-mat.soft)
  - authors: Zhikun Zeng, Jiazhao Xu, Hanyu Li, Shiang Zhang, Houfei Yuan

- [2026] Indirect Reciprocity with Environmental Feedback
  - arxiv: `2602.02553` (physics.soc-ph)
  - authors: Yishen Jiang, Xin Wang, Ming Wei, Wenqiang Zhu, Longzhao Liu

- [2026] On $E_{7+1/2}$ gauge theory
  - arxiv: `2602.02082` (hep-th)
  - authors: Xin Wang, Yi-Nan Wang

- [2025] Refined BPS numbers on compact Calabi-Yau threefolds from Wilson loops
  - arxiv: `2503.16270` (hep-th)
  - authors: Min-xin Huang, Sheldon Katz, Albrecht Klemm, Xin Wang

- [2025] Thermal Uhlmann-Chern Number: Bridging Pure and Mixed States
  - arxiv: `2506.18022` (quant-ph)
  - authors: Xin Wang, Xu-Yang Hou, Yan He, Hao Guo

- [2025] Free-fermion approach to the partition function zeros : Special boundary conditions and pr
  - arxiv: `2507.21943` (cond-mat.stat-mech)
  - authors: De-Zhang Li, Xin Wang

- [2025] New results of Bollobás-type theorem for affine subspaces and projective subspaces
  - arxiv: `2501.09215` (math.CO)
  - authors: Shuhui Yu, Xin Wang

- [2025] Geometric optimization for quantum communication
  - arxiv: `2509.15106` (quant-ph)
  - authors: Chengkai Zhu, Hongyu Mao, Kun Fang, Xin Wang

- [2025] Higher Form and Higher Group Symmetries via Mirror Symmetry
  - arxiv: `2503.09967` (hep-th)
  - authors: Jiahua Tian, Xin Wang

- [2025] Heat dissipation in marginally stable linear time-delayed Langevin systems
  - arxiv: `2506.23939` (cond-mat.stat-mech)
  - authors: Xin Wang

- [2025] Characteristic oscillations in frequency-resolved heat dissipation of linear time-delayed 
  - arxiv: `2501.01151` (cond-mat.stat-mech)
  - authors: Xin Wang, Ruicheng Bao, Naruo Ohga

- [2025] Resurgent structure of 2d Yang-Mills theory on a torus
  - arxiv: `2507.19943` (hep-th)
  - authors: Jiashen Chen, Jie Gu, Xin Wang

- [2025] A homoclinic route to chaos in omnivore communities
  - arxiv: `2508.18038` (nlin.CD)
  - authors: Yiyuan Niu, Ju Kang, Wei Tao, Xin Wang

- [2025] Nakayama automorphisms of graded double Ore extensions of Koszul Artin-Schelter regular al
  - arxiv: `2507.15252` (math.RA)
  - authors: Yan Cao, Yuan Shen, Xin Wang

- [2025] New Bounds and Constructions for Variable Packet-Error Coding
  - arxiv: `2506.15233` (cs.IT)
  - authors: Xiangliang Kong, Xin Wang, Ron M. Roth, Itzhak Tamo

- [2025] Cosmological Consequences of Domain Walls Biased by Quantum Gravity
  - arxiv: `2501.16414` (hep-ph)
  - authors: Yann Gouttenoire, Stephen F. King, Rishav Roshan, Xin Wang, Graham White

- [2025] Probing Quantum Curves and Transitions in 5d SQFTs via Defects and Blowup Equations
  - arxiv: `2503.15591` (hep-th)
  - authors: Hee-Cheol Kim, Minsung Kim, Sung-Soo Kim, Kimyeong Lee, Xin Wang

- [2025] Topological defects govern plasticity and shear band formation in two-dimensional amorphou
  - arxiv: `2507.03771` (cond-mat.soft)
  - authors: Xin Wang, Jin Shang, Yujie Wang, Jie Zhang, Matteo Baggioli

- [2025] Testing the cosmological principle on gigaparsec scales
  - arxiv: `2505.19055` (astro-ph.CO)
  - authors: Xin Wang, Zhiqi Huang

- [2025] Magnetization-resolved density of states and quasi-first order transition in the two-dimen
  - arxiv: `2505.04298` (cond-mat.dis-nn)
  - authors: Yi Liu, Ding Wang, Xin Wang, Dao-Xin Yao, Lei-Han Tang

- [2025] Nonlinear Public Goods Game in Dynamical Environments
  - arxiv: `2510.10259` (nlin.AO)
  - authors: Yishen Jiang, Xin Wang, Wenqiang Zhu, Ming Wei, Longzhao Liu

- [2024] Free-fermion models and the two-dimensional Ising models under the zero field and imaginar
  - arxiv: `2406.00232` (cond-mat.stat-mech)
  - authors: De-Zhang Li, Xin Wang, Xiao-Bao Yang

- [2024] Residual Entropy of Ice: A Study Based on Transfer Matrices
  - arxiv: `2404.13897` (cond-mat.stat-mech)
  - authors: De-Zhang Li, Yu-Jie Cen, Xin Wang, Xiao-Bao Yang

- [2024] Modular Invariant Hilltop Inflation
  - arxiv: `2405.08924` (hep-ph)
  - authors: Stephen F. King, Xin Wang

- [2024] Low-temperature series expansion of square lattice Ising model: A study based on Fisher ze
  - arxiv: `2412.07328` (cond-mat.stat-mech)
  - authors: De-Zhang Li, Xin Wang, Xiao-Bao Yang

- [2024] Modular domain walls and gravitational waves
  - arxiv: `2411.04900` (hep-ph)
  - authors: Stephen F. King, Xin Wang, Ye-Ling Zhou

- [2024] Stability of diverse dodecagonal quasicrystals in T-shaped liquid crystalline molecules
  - arxiv: `2410.06048` (cond-mat.soft)
  - authors: Xin Wang, An-Chang Shi, Pingwen Zhang, Kai Jiang

- [2024] Mathematical Foundation of the U$^N(1)$ Quantum Geometric Tensor
  - arxiv: `2410.11664` (math-ph)
  - authors: Xin Wang, Xu-Yang Hou, Jia-Chen Tang, Hao Guo

- [2024] Skew Knörrer's periodicity Theorem
  - arxiv: `2406.03024` (math.RA)
  - authors: Yang Liu, Yuan Shen, Xin Wang

- [2023] D-type Minimal Conformal Matter: Quantum Curves, Elliptic Garnier Systems, and the 5d Desc
  - arxiv: `2304.04383` (hep-th)
  - authors: Jin Chen, Yongchao Lü, Xin Wang

- [2023] Virtual Quantum Markov Chains
  - arxiv: `2312.02031` (quant-ph)
  - authors: Yu-Ao Chen, Chengkai Zhu, Keming He, Mingrui Jing, Xin Wang

- [2023] Reversible Entanglement Beyond Quantum Operations
  - arxiv: `2312.04456` (quant-ph)
  - authors: Xin Wang, Yu-Ao Chen, Lei Zhang, Chenghong Zhu

- [2023] Wilson loops, holomorphic anomaly equations and blowup equations
  - arxiv: `2305.09171` (hep-th)
  - authors: Xin Wang

- [2023] Computable and Faithful Lower Bound on Entanglement Cost
  - arxiv: `2311.10649` (quant-ph)
  - authors: Xin Wang, Mingrui Jing, Chengkai Zhu

- [2023] Estimate distillable entanglement and quantum capacity by squeezing useless entanglement
  - arxiv: `2303.07228` (quant-ph)
  - authors: Chengkai Zhu, Chenghong Zhu, Xin Wang

- [2023] Quantum Gravity Effects on Dark Matter and Gravitational Waves
  - arxiv: `2308.03724` (hep-ph)
  - authors: Stephen F. King, Rishav Roshan, Xin Wang, Graham White, Masahito Yamazaki

- [2023] Efficient information recovery from Pauli noise via classical shadow
  - arxiv: `2305.04148` (quant-ph)
  - authors: Yifei Chen, Zhan Yu, Chenghong Zhu, Xin Wang

- [2023] Power of quantum measurement in simulating unphysical operations
  - arxiv: `2309.09963` (quant-ph)
  - authors: Xuanqiang Zhao, Lei Zhang, Benchi Zhao, Xin Wang

- [2023] Overflow metabolism originates from growth optimization and cell heterogeneity
  - arxiv: `2303.14159` (physics.bio-ph)
  - authors: Xin Wang

- [2023] Schur indices for $\mathcal{N}=4$ super-Yang-Mills with more general gauge groups
  - arxiv: `2311.08714` (hep-th)
  - authors: Bao-ning Du, Min-xin Huang, Xin Wang

- [2023] Self-organized biodiversity in biotic resource systems
  - arxiv: `2311.13830` (q-bio.PE)
  - authors: Ju Kang, Shijie Zhang, Yiyuan Niu, Xin Wang

- [2023] Data Generation-based Operator Learning for Solving Partial Differential Equations on Unbo
  - arxiv: `2309.02446` (math.NA)
  - authors: Jihong Wang, Xin Wang, Jing Li, Bin Liu

- [2023] Quantum Gravity Effects on Fermionic Dark Matter and Gravitational Waves
  - arxiv: `2311.12487` (hep-ph)
  - authors: Stephen F. King, Rishav Roshan, Xin Wang, Graham White, Masahito Yamazaki

- [2023] Theory of polygonal phases self-assembled from T-shaped liquid crystalline molecules
  - arxiv: `2309.13262` (cond-mat.soft)
  - authors: Zhijuan He, Xin Wang, Pingwen Zhang, An-Chang Shi, Kai Jiang

- [2022] Topological strings and Wilson loops
  - arxiv: `2205.02366` (hep-th)
  - authors: Min-xin Huang, Kimyeong Lee, Xin Wang

- [2022] Quantum Phase Processing and its Applications in Estimating Phase and Entropies
  - arxiv: `2209.14278` (quant-ph)
  - authors: Youle Wang, Lei Zhang, Zhan Yu, Xin Wang

- [2022] Optimal quantum dataset for learning a unitary transformation
  - arxiv: `2203.00546` (quant-ph)
  - authors: Zhan Yu, Xuanqiang Zhao, Benchi Zhao, Xin Wang

- [2022] Twisted Elliptic Genera
  - arxiv: `2212.07341` (hep-th)
  - authors: Kimyeong Lee, Kaiwen Sun, Xin Wang

- [2022] Power and limitations of single-qubit native quantum neural networks
  - arxiv: `2205.07848` (quant-ph)
  - authors: Zhan Yu, Hongshun Yao, Mujin Li, Xin Wang

- [2022] Information recoverability of noisy quantum states
  - arxiv: `2203.04862` (quant-ph)
  - authors: Xuanqiang Zhao, Benchi Zhao, Zihan Xia, Xin Wang

- [2022] Uhlmann phase of coherent states and the Uhlmann-Berry correspondence
  - arxiv: `2208.07001` (quant-ph)
  - authors: Xin Wang, Xu-Yang Hou, Zheng Zhou, Hao Guo, Chih-Chun Chien

- [2021] Towards the ultimate limits of quantum channel discrimination and quantum communication
  - arxiv: `2110.14842` (quant-ph)
  - authors: Kun Fang, Gilad Gour, Xin Wang

- [2021] Elliptic Quantum Curves of 6d SO(N) theories
  - arxiv: `2110.13487` (hep-th)
  - authors: Jin Chen, Babak Haghighat, Hee-Cheol Kim, Kimyeong Lee, Marcus Sperling

- [2021] A Hybrid Quantum-Classical Hamiltonian Learning Algorithm
  - arxiv: `2103.01061` (quant-ph)
  - authors: Youle Wang, Guangxi Li, Xin Wang

- [2021] Symmetric distinguishability as a quantum resource
  - arxiv: `2102.12512` (quant-ph)
  - authors: Robert Salzmann, Nilanjana Datta, Gilad Gour, Xin Wang, Mark M. Wilde

- [2021] Practical distributed quantum information processing with LOCCNet
  - arxiv: `2101.12190` (quant-ph)
  - authors: Xuanqiang Zhao, Benchi Zhao, Zihe Wang, Zhixin Song, Xin Wang

- [2021] Mitigating Quantum Errors via Truncated Neumann Series
  - arxiv: `2111.00691` (quant-ph)
  - authors: Kun Wang, Yu-Ao Chen, Xin Wang

- [2021] Intraspecific predator interference promotes biodiversity in ecosystems
  - arxiv: `2112.05098` (q-bio.PE)
  - authors: Ju Kang, Shijie Zhang, Yiyuan Niu, Fan Zhong, Xin Wang

- [2021] Lower bound for the T count via unitary stabilizer nullity
  - arxiv: `2103.09999` (quant-ph)
  - authors: Jiaqing Jiang, Xin Wang

- [2021] E-string Quantum Curve
  - arxiv: `2103.16996` (hep-th)
  - authors: Jin Chen, Babak Haghighat, Hee-Cheol Kim, Marcus Sperling, Xin Wang

- [2021] Hybrid subconvexity bounds for twists of $\rm GL(3)$ $L$-functions
  - arxiv: `2112.15378` (math.NT)
  - authors: Xin Wang, Tengyou Zhu

- [2021] Twisted 6d $(2,0)$ SCFTs on a Circle
  - arxiv: `2103.06044` (hep-th)
  - authors: Zhihao Duan, Kimyeong Lee, June Nahmgoong, Xin Wang

- [2021] Improved Lower Bounds for Secure Codes and Related Structures
  - arxiv: `2108.07987` (cs.IT)
  - authors: Bingchen Qian, Xin Wang, Gennian Ge

- [2021] Improved Lower Bounds for Strongly Separable Matrices and Related Combinatorial Structures
  - arxiv: `2110.07381` (math.CO)
  - authors: Bingchen Qian, Xin Wang, Gennian Ge

- [2021] A preliminary study about gravitational wave radiation and cosmic heat death
  - arxiv: `2102.12054` (astro-ph.CO)
  - authors: Jianming Zhang, Qiyue Qian, Yiqing Guo, Xin Wang, Xiao-Dong Li

- [2020] Elliptic Blowup Equations for 6d SCFTs. IV: Matters
  - arxiv: `2006.03030` (hep-th)
  - authors: Jie Gu, Babak Haghighat, Albrecht Klemm, Kaiwen Sun, Xin Wang

- [2020] Cost of quantum entanglement simplified
  - arxiv: `2007.14270` (quant-ph)
  - authors: Xin Wang, Mark M. Wilde

- [2020] Physical Implementability of Linear Maps and Its Application in Error Mitigation
  - arxiv: `2012.10959` (quant-ph)
  - authors: Jiaqing Jiang, Kun Wang, Xin Wang

- [2020] Quantum Periods and Spectra in Dimer Models and Calabi-Yau Geometries
  - arxiv: `2006.13482` (hep-th)
  - authors: Min-xin Huang, Yuji Sugimoto, Xin Wang

- [2020] The three-level coupled Maxwell-Bloch equations: rogue waves, semirational rogue waves and
  - arxiv: `2002.04174` (nlin.SI)
  - authors: Xin Wang, Lei Wang, Chong Liu

- [2020] Variational Quantum Algorithms for Trace Distance and Fidelity Estimation
  - arxiv: `2012.05768` (quant-ph)
  - authors: Ranyiliu Chen, Zhixin Song, Xuanqiang Zhao, Xin Wang

- [2020] Variational quantum Gibbs state preparation with a truncated Taylor series
  - arxiv: `2005.08797` (quant-ph)
  - authors: Youle Wang, Guangxi Li, Xin Wang

- [2020] Observation of non-Hermitian topology with non-unitary dynamics of solid-state spins
  - arxiv: `2012.09191` (quant-ph)
  - authors: Wengang Zhang, Xiaolong Ouyang, Xianzhi Huang, Xin Wang, Huili Zhang

- [2020] On Lattice Packings and Coverings of Asymmetric Limited-Magnitude Balls
  - arxiv: `2005.14519` (cs.IT)
  - authors: Hengjia Wei, Xin Wang, Moshe Schwartz

- [2020] Matching preclusion and strong matching preclusion of the bubble-sort star graphs
  - arxiv: `2001.00424` (math.CO)
  - authors: Xin Wang, Chaoqun Ma, Jia Guo

- [2020] An auto-parameter denoising method for nuclear magnetic resonance spectroscopy based on lo
  - arxiv: `2001.11815` (physics.med-ph)
  - authors: Tianyu Qiu, Wenjing Liao, Di Guo, Dongbao Liu, Xin Wang

- [2019] $α$-Logarithmic negativity
  - arxiv: `1904.10437` (quant-ph)
  - authors: Xin Wang, Mark M. Wilde

- [2019] Elliptic Blowup Equations for 6d SCFTs. III: E-strings, M-strings and Chains
  - arxiv: `1911.11724` (hep-th)
  - authors: Jie Gu, Babak Haghighat, Albrecht Klemm, Kaiwen Sun, Xin Wang

- [2019] Elliptic Blowup Equations for 6d SCFTs. II: Exceptional Cases
  - arxiv: `1905.00864` (hep-th)
  - authors: Jie Gu, Albrecht Klemm, Kaiwen Sun, Xin Wang

- [2019] Finite generation and holomorphic anomaly equation for equivariant Gromov-Witten invariant
  - arxiv: `1908.03691` (math.AG)
  - authors: Xin Wang

- [2019] Resource theory of asymmetric distinguishability for quantum channels
  - arxiv: `1907.06306` (quant-ph)
  - authors: Xin Wang, Mark M. Wilde

- [2019] Resource theory of asymmetric distinguishability
  - arxiv: `1905.11629` (quant-ph)
  - authors: Xin Wang, Mark M. Wilde

- [2019] Quasi-modularity and holomorphic anomaly equation for the twisted Gromov-Witten theory: $\
  - arxiv: `1906.11643` (math.AG)
  - authors: Xin Wang

- [2019] Quantifying the magic of quantum channels
  - arxiv: `1903.04483` (quant-ph)
  - authors: Xin Wang, Mark M. Wilde, Yuan Su

- [2019] Pursuing the fundamental limits for quantum communication
  - arxiv: `1912.00931` (quant-ph)
  - authors: Xin Wang

- [2019] One-shot entanglement distillation beyond local operations and classical communication
  - arxiv: `1906.01648` (quant-ph)
  - authors: Bartosz Regula, Kun Fang, Xin Wang, Mile Gu

- [2019] Quantifying the unextendibility of entanglement
  - arxiv: `1911.07433` (quant-ph)
  - authors: Kun Wang, Xin Wang, Mark M. Wilde

- [2019] New bounds and constructions for constant weighted $X$-codes
  - arxiv: `1903.06434` (cs.IT)
  - authors: Xiangliang Kong, Xin Wang, Gennian Ge

- [2019] Initial conditions of the universe: Decaying tensor modes
  - arxiv: `1910.01416` (astro-ph.CO)
  - authors: Darsh Kodwani, P. Daniel Meerburg, Ue-Li Pen, Xin Wang

- [2019] Initial conditions of the universe: A sign of the sine mode
  - arxiv: `1903.05042` (astro-ph.CO)
  - authors: Darsh Kodwani, P. Daniel Meerburg, Ue-Li Pen, Xin Wang

- [2018] Gaussian quantum resource theories
  - arxiv: `1801.05450` (quant-ph)
  - authors: Ludovico Lami, Bartosz Regula, Xin Wang, Rosanna Nichols, Andreas Winter

- [2018] Blowup Equations for 6d SCFTs. I
  - arxiv: `1811.02577` (hep-th)
  - authors: Jie Gu, Babak Haghighat, Kaiwen Sun, Xin Wang

- [2018] Efficiently computable bounds for magic state distillation
  - arxiv: `1812.10145` (quant-ph)
  - authors: Xin Wang, Mark M. Wilde, Yuan Su

- [2018] Geometric ergodicity of Polya-Gamma Gibbs sampler for Bayesian logistic regression with a 
  - arxiv: `1802.06248` (math.ST)
  - authors: Xin Wang, Vivekananda Roy

- [2018] Quantum Information Scrambling Through a High-Complexity Operator Mapping
  - arxiv: `1806.00472` (quant-ph)
  - authors: Xiaopeng Li, Guanyu Zhu, Muxin Han, Xin Wang

- [2018] Large and moderate deviations for a $\mathbb{R}^d$-valued branching random walk with a ran
  - arxiv: `1811.01503` (math.PR)
  - authors: Chunmao Huang, Xin Wang, Xiaoqiang Wang

- [2018] Constructions of Augmented Orthogonal Arrays
  - arxiv: `1804.05137` (math.CO)
  - authors: Xin Wang, Lijun Ji, Yun Li, Miao Liang

- [2017] On converse bounds for classical communication over quantum channels
  - arxiv: `1709.05258` (quant-ph)
  - authors: Xin Wang, Kun Fang, Marco Tomamichel

- [2017] Blowup Equations for Refined Topological Strings
  - arxiv: `1711.09884` (hep-th)
  - authors: Min-xin Huang, Kaiwen Sun, Xin Wang

- [2017] A strengthened inequality of Alon-Babai-Suzuki's conjecture on set systems with restricted
  - arxiv: `1701.00585` (math.CO)
  - authors: Xin Wang, Hengjia Wei, Gennian Ge

- [2017] Periodic and rational solutions of the reduced Maxwell-Bloch equations
  - arxiv: `1705.09881` (nlin.SI)
  - authors: Jiao Wei, Xin Wang, Xianguo Geng

- [2017] Analysis of the Polya-Gamma block Gibbs sampler for Bayesian logistic linear mixed models
  - arxiv: `1708.00100` (math.ST)
  - authors: Xin Wang, Vivekananda Roy

- [2017] Convergence analysis of the block Gibbs sampler for Bayesian probit linear mixed models wi
  - arxiv: `1706.01846` (math.ST)
  - authors: Xin Wang, Vivekananda Roy

- [2017] Some intriguing upper bounds for separating hash families
  - arxiv: `1707.01758` (math.CO)
  - authors: Gennian Ge, Chong Shangguan, Xin Wang

- [2016] Exact Quantization Conditions, Toric Calabi-Yau and Nonperturbative Topological String
  - arxiv: `1606.07330` (hep-th)
  - authors: Kaiwen Sun, Xin Wang, Min-xin Huang

- [2016] Invertible binary matrix with maximum number of $2$-by-$2$ invertible submatrices
  - arxiv: `1601.02109` (cs.IT)
  - authors: Yiwei Zhang, Tao Zhang, Xin Wang, Gennian Ge

- [2016] Optical rogue waves and W-shaped solitons in the multiple self-induced transparency system
  - arxiv: `1606.09323` (nlin.PS)
  - authors: Xin Wang, Chong Liu

- [2015] New Exact Quantization Condition for Toric Calabi-Yau Geometries
  - arxiv: `1505.05360` (hep-th)
  - authors: Xin Wang, Guojun Zhang, Min-xin Huang

- [2015] Modulation instability and controllable rogue waves with multiple compression points for p
  - arxiv: `1512.07938` (nlin.SI)
  - authors: Xin Wang, Yong Chen

- [2014] A Note on Instanton Effects in ABJM Theory
  - arxiv: `1409.4967` (hep-th)
  - authors: Xian-fu Wang, Xin Wang, Min-xin Huang

- [2014] New Bounds For Frameproof Codes
  - arxiv: `1411.5782` (cs.IT)
  - authors: Chong Shangguan, Xin Wang, Gennian Ge, Ying Miao

- [2014] Generalized Darboux transformation and higher-order rogue wave solutions of the coupled Hi
  - arxiv: `1409.5013` (nlin.SI)
  - authors: Xin Wang, Yong Chen

- [2013] Rogue wave solutions in AB system
  - arxiv: `1312.6479` (math-ph)
  - authors: Xin Wang, Yuqi Li, Yong Chen

- [2013] Sublinear expectation linear regression
  - arxiv: `1304.3559` (math.ST)
  - authors: Lu Lin, Yufeng Shi, Xin Wang, Shuzhen Yang

- [2013] Generalized Darboux transformation and localized waves in coupled Hirota equations
  - arxiv: `1312.3436` (math-ph)
  - authors: Xin Wang, Yuqi Li, Yong Chen

- [2010] Topology of large scale structure as test of modified gravity
  - arxiv: `1010.3035` (astro-ph.CO)
  - authors: Xin Wang, Xuelei Chen, Changbom Park

- [2010] Cosmological models with Lagrange Multiplier Field
  - arxiv: `1003.6056` (astro-ph.CO)
  - authors: Changjun Gao, Yan Gong, Xin Wang, Xuelei Chen

- [2002] Athermodynamic Alignment in the Two-Dimensional Enstrophy Cascade
  - arxiv: `nlin/0201043` (nlin.CD)
  - authors: Xin Wang, Shiyi Chen, Robert E. Ecke, Gregory L. Eyink


## wang-zhiyong (en=Zhiyong Wang) — 6 candidates not in yaml

- [2024] Several functional capacities and Carleson type embeddings of fractional Sobolev sapces on
  - arxiv: `2409.18720` (math.AP)
  - authors: Zhiyong Wang, Pengtao Li, Yu Liu

- [2024] Geometric topics related to Besov type spaces on the Grushin setting
  - arxiv: `2401.03409` (math.AP)
  - authors: Nan Zhao, Zhiyong Wang, Pengtao Li, Yu Liu

- [2020] Regularity of fractional heat semigroup associated with Schrödinger operators
  - arxiv: `2012.07234` (math.CA)
  - authors: P. Li, Z. Wang, T. Qian, C. Zhang

- [2015] Life Span of Solutions for a Semilinear Heat Equation with Initial Data Non-Rarefied at $\
  - arxiv: `1501.02856` (math.AP)
  - authors: Zhiyong Wang, Jingxue Yin

- [2007] A geometric growth model interpolating between regular and small-world networks
  - arxiv: `cond-mat/0701231` (cond-mat.stat-mech)
  - authors: Zhongzhi Zhang, Shuigeng Zhou, Zhiyong Wang, Zhen Shen

- [2000] A new massive vector field theory
  - arxiv: `hep-th/0001043` (hep-th)
  - authors: Zhiyong Wang, Ailin Zhang


## wang-zhiyuan (en=Zhiyuan Wang) — 9 candidates not in yaml

- [2025] Secret communication games and a hierarchy of quasiparticle statistics in 3 + 1D topologic
  - arxiv: `2510.11818` (quant-ph)
  - authors: Zhiyuan Wang

- [2024] Hopf algebras and solvable unitary circuits
  - arxiv: `2409.17215` (quant-ph)
  - authors: Zhiyuan Wang

- [2024] Parastatistics and a secret communication challenge
  - arxiv: `2412.13360` (quant-ph)
  - authors: Zhiyuan Wang

- [2023] Particle exchange statistics beyond fermions and bosons
  - arxiv: `2308.05203` (quant-ph)
  - authors: Zhiyuan Wang, Kaden R. A. Hazzard

- [2023] Hierarchical generalization of dual unitarity
  - arxiv: `2307.03138` (quant-ph)
  - authors: Xie-Hang Yu, Zhiyuan Wang, Pavel Kos

- [2022] Locality of gapped ground states in systems with power-law decaying interactions
  - arxiv: `2208.13057` (quant-ph)
  - authors: Zhiyuan Wang, Kaden R. A. Hazzard

- [2022] Topological correlations in three dimensional classical Ising models: an exact solution wi
  - arxiv: `2202.11303` (cond-mat.stat-mech)
  - authors: Zhiyuan Wang, Kaden R. A. Hazzard

- [2020] Bounding the finite-size error of quantum many-body dynamics simulations
  - arxiv: `2009.12032` (quant-ph)
  - authors: Zhiyuan Wang, Michael Foss-Feig, Kaden R. A. Hazzard

- [2019] Tightening the Lieb-Robinson Bound in Locally-Interacting Systems
  - arxiv: `1908.03997` (quant-ph)
  - authors: Zhiyuan Wang, Kaden R. A. Hazzard


## xu-xu (en=Xu Xu) — 41 candidates not in yaml

- [2026] Probing Late-Stage Hadronic Interactions at High Baryon Density via $K^{*0}$ Production in
  - arxiv: `2601.14884` (nucl-ex)
  - authors:  STAR Collaboration, B. E. Aboona, J. Adam, G. Agakishiev, I. Aggarwal

- [2025] Challenging Spontaneous Quantum Collapse with XENONnT
  - arxiv: `2506.05507` (hep-ex)
  - authors: E. Aprile, J. Aalbers, K. Abe, S. Ahmed Maouloud, L. Althueser

- [2025] Generalized circle patterns on surfaces with cusps
  - arxiv: `2504.09172` (math.GT)
  - authors: Zhiwen Xiong, Xu Xu

- [2024] Stringent Tests of Lorentz Invariance Violation from LHAASO Observations of GRB 221009A
  - arxiv: `2402.06009` (astro-ph.HE)
  - authors:  The LHAASO Collaboration, Zhen Cao, F. Aharonian,  Axikegu, Y. X. Bai

- [2024] A discrete uniformization theorem for decorated piecewise hyperbolic metrics on surfaces
  - arxiv: `2401.05056` (math.DG)
  - authors: Xu Xu, Chao Zheng

- [2023] Deformation of discrete conformal structures on surfaces
  - arxiv: `2312.02484` (math.DG)
  - authors: Xu Xu

- [2023] A discrete uniformization theorem for decorated piecewise Euclidean metrics on surfaces, I
  - arxiv: `2309.06685` (math.DG)
  - authors: Xu Xu, Chao Zheng

- [2023] A discrete uniformization theorem for decorated piecewise Euclidean metrics on surfaces
  - arxiv: `2309.05215` (math.DG)
  - authors: Xu Xu, Chao Zheng

- [2023] Combinatorial curvature flows with surgery for inversive distance circle packings on surfa
  - arxiv: `2308.02271` (math.DG)
  - authors: Xu Xu, Chao Zheng

- [2023] Rigidity of generalized Thurston's sphere packings on 3-dimensional manifolds with boundar
  - arxiv: `2309.02457` (math.GT)
  - authors: Xu Xu, Chao Zheng

- [2023] On the classification of discrete conformal structures on surfaces
  - arxiv: `2307.13223` (math.DG)
  - authors: Xu Xu, Chao Zheng

- [2023] Rigidity and deformation of generalized sphere packings on 3-dimensional manifolds with bo
  - arxiv: `2309.01205` (math.DG)
  - authors: Xu Xu, Chao Zheng

- [2022] Beam Energy Dependence of Triton Production and Yield Ratio ($\mathrm{N}_t \times \mathrm{
  - arxiv: `2209.08058` (nucl-ex)
  - authors:  STAR Collaboration, M. I. Abdulhamid, B. E. Aboona, J. Adam, J. R. Adams

- [2022] A new proof for global rigidity of vertex scaling on polyhedral surfaces
  - arxiv: `2204.08172` (math.GT)
  - authors: Xu Xu, Chao Zheng

- [2022] Combinatorial Yamabe flow on hyperbolic bordered surfaces
  - arxiv: `2204.08191` (math.DG)
  - authors: Shengyu Li, Xu Xu, Ze Zhou

- [2022] Rigidity of infinite inversive distance circle packings in the plane
  - arxiv: `2211.07464` (math.GT)
  - authors: Yanwen Luo, Xu Xu, Siqi Zhang

- [2022] Combinatorial curvature flows for generalized circle packings on surfaces with boundary
  - arxiv: `2208.03643` (math.DG)
  - authors: Xu Xu, Chao Zheng

- [2022] The convergence of inversive distance circle packings to the Riemann mapping
  - arxiv: `2204.08145` (math.DG)
  - authors: Yuxiang Chen, Yanwen Luo, Xu Xu

- [2021] Evidence for Nonlinear Gluon Effects in QCD and their $A$ Dependence at STAR
  - arxiv: `2111.10396` (nucl-ex)
  - authors:  STAR Collaboration, M. S. Abdallah, B. E. Aboona, J. Adam, L. Adamczyk

- [2021] Rigidity of discrete conformal structures on surfaces
  - arxiv: `2103.05272` (math.DG)
  - authors: Xu Xu

- [2021] Prescribing discrete Gaussian curvature on polyhedral surfaces
  - arxiv: `2110.12326` (math.DG)
  - authors: Xu Xu, Chao Zheng

- [2021] Parameterized discrete uniformization theorems and curvature flows for polyhedral surfaces
  - arxiv: `2103.16077` (math.GT)
  - authors: Xu Xu, Chao Zheng

- [2021] A new class of discrete conformal structures on surfaces with boundary
  - arxiv: `2110.08474` (math.GT)
  - authors: Xu Xu

- [2021] Fractional combinatorial Calabi flow on surfaces
  - arxiv: `2107.14102` (math.GT)
  - authors: Tianqi Wu, Xu Xu

- [2021] Parameterized combinatorial curvatures and parameterized combinatorial curvature flows for
  - arxiv: `2105.14714` (math.GT)
  - authors: Xu Xu, Chao Zheng

- [2021] Combinatorial Calabi flows on surfaces with boundary
  - arxiv: `2110.01142` (math.DG)
  - authors: Yanwen Luo, Xu Xu

- [2020] Combinatorial Ricci flow on cusped 3-manifolds
  - arxiv: `2009.05477` (math.GT)
  - authors: Xu Xu

- [2020] Combinatorial Ricci flow on compact 3-manifolds with boundary
  - arxiv: `2009.02496` (math.GT)
  - authors: Xu Xu

- [2019] A new proof of Bowers-Stephenson conjecture
  - arxiv: `1904.11127` (math.GT)
  - authors: Xu Xu

- [2019] Thurston's sphere packings on 3-dimensional manifolds, I
  - arxiv: `1904.11122` (math.GT)
  - authors: Xiaokai He, Xu Xu

- [2018] Combinatorial Calabi flow with surgery on surfaces
  - arxiv: `1806.02166` (math.GT)
  - authors: Xiang Zhu, Xu Xu

- [2018] Parameterized discrete uniformization theorems and curvature flows for polyhedral surfaces
  - arxiv: `1806.04516` (math.GT)
  - authors: Xu Xu

- [2017] On a combinatorial curvature for surfaces with inversive distance circle packing metrics
  - arxiv: `1701.01795` (math.GT)
  - authors: Huabin Ge, Xu Xu

- [2017] Rigidity of inversive distance circle packings revisited
  - arxiv: `1705.02714` (math.GT)
  - authors: Xu Xu

- [2016] On the global rigidity of sphere packings on 3-dimensional manifolds
  - arxiv: `1611.08835` (math.GT)
  - authors: Xu Xu

- [2015] Metastability of finite state Markov chains: a recursive procedure to identify slow variab
  - arxiv: `1512.06597` (math.PR)
  - authors: C. Landim, T. Xu

- [2015] A combinatorial Yamabe problem on two and three dimensional manifolds
  - arxiv: `1504.05814` (math.DG)
  - authors: Huabin Ge, Xu Xu

- [2015] $α$-curvatures and $α$-flows on low dimensional triangulated manifolds
  - arxiv: `1505.05077` (math.DG)
  - authors: Huabin Ge, Xu Xu

- [2015] A Discrete Ricci Flow on Surfaces in Hyperbolic Background Geometry
  - arxiv: `1505.05076` (math.DG)
  - authors: Huabin Ge, Xu Xu

- [2013] Positive energy theorem for (4+1)-dimensional asymptotically anti-de Sitter spacetimes
  - arxiv: `1302.4517` (math.DG)
  - authors: Yaohua Wang, Xu Xu

- [2012] Hyperbolic positive energy theorem with electromagnetic fields
  - arxiv: `1210.2017` (math.DG)
  - authors: Yaohua Wang, Xu Xu


## yang-di (en=Di Yang) — 4 candidates not in yaml

- [2020] On the solution of the coupled steady-state dual-porosity-Navier-Stokes fluid flow model w
  - arxiv: `2012.10819` (math.AP)
  - authors: Di Yang, Yinnian He, Luling Cao

- [2010] On a Novel Class of Integrable ODEs Related to the Painlevé Equations
  - arxiv: `1009.5125` (nlin.SI)
  - authors: A. S. Fokas, D. Yang

- [2010] A Novel Approach to Elastodynamics: I. The Two-Dimensional Case
  - arxiv: `1010.2941` (math.AP)
  - authors: A. S. Fokas, D. Yang

- [2010] A Novel Approach to Elastodynamics: II. The Three-Dimensional Case
  - arxiv: `1010.2947` (math.AP)
  - authors: A. S. Fokas, D. Yang


## yang-yi (en=Yi Yang) — 85 candidates not in yaml

- [2026] Neutral-Fermion constructions of factorial $gp$-and $gq$-Functions
  - arxiv: `2603.20865` (math.CO)
  - authors: Koushik Brahma, Takeshi Ikeda, Shinsuke Iwao, Yi Yang

- [2025] The Virasoro symmetries of the bigraded modified Toda hierarchy
  - arxiv: `2503.11303` (nlin.SI)
  - authors: Yi Yang

- [2025] A graphical framework for proving holographic entanglement entropy inequalities in multipa
  - arxiv: `2512.18726` (quant-ph)
  - authors: Chia-Jui Chou, Hans B. Lao, Yi Yang

- [2025] Revisited for existence proof of optimal solution in Bernoulli free boundary problem using
  - arxiv: `2511.02702` (math.AP)
  - authors: Shiouhe Wang, Fang Shen, Yi Yang, Xueshang Feng

- [2024] The stringy scaling loop expansion and stringy scaling violation
  - arxiv: `2405.03938` (hep-th)
  - authors: Sheng-Hong Lai, Jen-Chi Lee, Yi Yang

- [2024] The Modified Toda Hierarchy
  - arxiv: `2408.09450` (nlin.SI)
  - authors: Wenjuan Rui, Wenchuang Guan, Yi Yang, Jipeng Cheng

- [2024] Stringy scaling of multi-tensor hard string scattering amplitudes and the K-identities
  - arxiv: `2412.19640` (hep-th)
  - authors: Sheng-Hong Lai, Jen-Chi Lee, Yi Yang

- [2024] Stringy Scaling
  - arxiv: `2408.12612` (hep-th)
  - authors: Sheng-Hong Lai, Jen-Chi Lee, Yi Yang

- [2023] Stringy scaling of n-point Regge string scattering amplitudes
  - arxiv: `2303.17909` (hep-th)
  - authors: Sheng-Hong Lai, Jen-Chi Lee, Yi Yang

- [2023] To Define the Core Entropy for All Polynomials Having a Connected Julia Set
  - arxiv: `2301.12610` (math.DS)
  - authors: Jun Luo, Bo Tan, Yi Yang, Xiao-Ting Yao

- [2023] Page Curve of AdS-Vaidya Model for Evaporating Black Holes
  - arxiv: `2306.16744` (hep-th)
  - authors: Chia-Jui Chou, Hans B. Lao, Yi Yang

- [2022] Stringy scaling of n-point hard string scattering amplitudes
  - arxiv: `2207.09236` (hep-th)
  - authors: Sheng-Hong Lai, Jen-Chi Lee, Yi Yang

- [2022] The $SL(K+3,\mathbb{C})$ symmetry of string scatterings from D-branes
  - arxiv: `2204.13308` (hep-th)
  - authors: Sheng-Hong Lai, Jen-Chi Lee, Yi Yang

- [2022] Krylov complexity and orthogonal polynomials
  - arxiv: `2205.12815` (hep-th)
  - authors: Wolfgang Mück, Yi Yang

- [2021] CKP hierarchy and free Bosons
  - arxiv: `2105.07344` (nlin.SI)
  - authors: Yi Yang, Lumin Geng, Jipeng Cheng

- [2021] Bilinear equations in Darboux transformations by Boson-Fermion correspondence
  - arxiv: `2101.02520` (nlin.SI)
  - authors: Yi Yang, Jipeng Cheng

- [2021] Residues of bosonic string scattering amplitudes and the Lauricella functions
  - arxiv: `2109.08601` (hep-th)
  - authors: Sheng-Hong Lai, Jen-Chi Lee, Yi Yang

- [2021] Page Curve of Effective Hawking Radiation
  - arxiv: `2111.14551` (hep-th)
  - authors: Chia-Jui Chou, Hans B. Lao, Yi Yang

- [2021] Constraints on cosmic strings using data from the third Advanced LIGO-Virgo observing run
  - arxiv: `2101.12248` (gr-qc)
  - authors:  The LIGO Scientific Collaboration,  the Virgo Collaboration,  the KAGRA Collaboration, R. Abbott, T. D. Abbott

- [2021] Comment on "High Energy Symmetry of String Theory"
  - arxiv: `2103.14472` (hep-th)
  - authors: Sheng-Hong Lai, Jen-Chi Lee, Yi Yang

- [2021] The exact SL(K+3,C) symmetry of string theory
  - arxiv: `2108.06326` (hep-th)
  - authors: Sheng-Hong Lai, Jen-Chi Lee, Yi Yang

- [2020] Recent developments of the Lauricella string scattering amplitudes and their exact SL(K+3,
  - arxiv: `2012.14726` (hep-th)
  - authors: Sheng-Hong Lai, Jen-Chi Lee, Yi Yang

- [2020] Analytic Study of Magnetic Catalysis in Holographic QCD
  - arxiv: `2004.01965` (hep-th)
  - authors: Song He, Yi Yang, Pei-Hung Yuan

- [2020] Entanglement Entropy Inequalities in BCFT by Holography
  - arxiv: `2011.02790` (hep-th)
  - authors: Chia-Jui Chou, Bo-Han Lin, Bin Wang, Yi Yang

- [2020] New bosonic hard string scattering amplitudes and extended Gross conjecture in superstring
  - arxiv: `2011.00260` (hep-th)
  - authors: Sheng-Hong Lai, Jen-Chi Lee, Yi Yang

- [2020] Analytic Study on Chiral Phase Transition in Holographic QCD
  - arxiv: `2009.05694` (hep-th)
  - authors: Meng-Wei Li, Yi Yang, Pei-Hung Yuan

- [2020] QCD Phase Diagram by Holography
  - arxiv: `2011.11941` (hep-th)
  - authors: Yi Yang, Pei-Hung Yuan

- [2019] Overview on High energy String Scattering Amplitudes and Symmetries of String Theory
  - arxiv: `1907.12810` (hep-th)
  - authors: Jen-Chi Lee, Yi Yang

- [2019] Spin polarization independence of hard polarized fermion string scattering amplitudes
  - arxiv: `1905.04858` (hep-th)
  - authors: Sheng-Hong Lai, Jen-Chi Lee, Yi Yang

- [2018] Imprints of Early Universe on Gravitational Waves from First-Order Phase Transition in QCD
  - arxiv: `1812.09676` (hep-th)
  - authors: Meng-Wei Li, Yi Yang, Pei-Hung Yuan

- [2018] Holographic Entanglement Entropy in Boundary Quantum Field Theory
  - arxiv: `1805.06117` (hep-th)
  - authors: En-Jui Chang, Chia-Jui Chou, Yi Yang

- [2018] Peano Model for Planar Compacta and a Lemma by Beardon
  - arxiv: `1803.09199` (math.DS)
  - authors: Jun Luo, Yi Yang, Xiao-Ting Yao

- [2018] Holographic Superconductors: An Analytic Method Revisit
  - arxiv: `1812.04288` (hep-th)
  - authors: En-Jui Chang, Chia-Jui Chou, Yi Yang

- [2018] The SL(K+3,C) Symmetry of the Bosonic String Scattering Amplitudes
  - arxiv: `1806.05033` (hep-th)
  - authors: Sheng-Hong Lai, Jen-Chi Lee, Yi Yang

- [2017] Approaching Confinement Structure for Light Quarks in a Holographic Soft Wall QCD Model
  - arxiv: `1703.09184` (hep-th)
  - authors: Meng-Wei Li, Yi Yang, Pei-Hung Yuan

- [2017] Universal Behaviors of Speed of Sound from Holography
  - arxiv: `1705.07587` (hep-th)
  - authors: Yi Yang, Pei-Hung Yuan

- [2017] A Core Decomposition of Compact Sets in the Plane
  - arxiv: `1712.06300` (math.DS)
  - authors: Benoit Loridant, Jun Luo, Yi Yang

- [2017] Solving Lauricella String Scattering Amplitudes through Recurrence Relations
  - arxiv: `1707.01281` (hep-th)
  - authors: Sheng-Hong Lai, Jen-Chi Lee, Taejin Lee, Yi Yang

- [2017] String Scattering Amplitudes and Deformed Cubic String Field Theory
  - arxiv: `1706.08025` (hep-th)
  - authors: Sheng-Hong Lai, Jen-Chi Lee, Yi Yang, Taejin Lee

- [2016] Fluid/Gravity Correspondence with Scalar Field and Electromagnetic Field
  - arxiv: `1601.01946` (hep-th)
  - authors: Chia-Jui Chou, Xiaoning Wu, Yi Yang, Pei-Hung Yuan

- [2016] The String BCJ Relations Revisited and Extended Recurrence relations of Nonrelativistic St
  - arxiv: `1601.03813` (hep-th)
  - authors: Sheng-Hong Lai, Jen-Chi Lee, Yi Yang

- [2016] Inverse Magnetic Catalysis in the Soft-Wall Model of AdS/QCD
  - arxiv: `1610.04618` (hep-th)
  - authors: Danning Li, Mei Huang, Yi Yang, Pei-Hung Yuan

- [2016] The Exact SL(K+3,C) Symmetry of String Scattering Amplitudes
  - arxiv: `1603.00396` (hep-th)
  - authors: Sheng-Hong Lai, Jen-Chi Lee, Yi Yang

- [2016] The Lauricella Functions and Exact String Scattering Amplitudes
  - arxiv: `1609.06014` (hep-th)
  - authors: Sheng-Hong Lai, Jen-Chi Lee, Yi Yang

- [2015] Confinement-Deconfinment Phase Transition for Heavy Quarks
  - arxiv: `1506.05930` (hep-th)
  - authors: Yi Yang, Pei-Hung Yuan

- [2015] An Isodiametric Problem with Additional Constraints in Euclidean space R^3
  - arxiv: `1503.03364` (math.DS)
  - authors: Yi Yang

- [2015] Rotating Black Holes and Coriolis Effect
  - arxiv: `1511.08691` (hep-th)
  - authors: Xiaoning Wu, Yi Yang, Pei-Hung Yuan, Chia-Jui Cho

- [2015] Extremal RN/CFT in Both Hands Revisited
  - arxiv: `1512.02934` (hep-th)
  - authors: En-Jui Kuo, Yi Yang

- [2015] Review on High energy String Scattering Amplitudes and Symmetries of String Theory
  - arxiv: `1510.03297` (hep-th)
  - authors: Jen-Chi Lee, Yi Yang

- [2014] A Refined Holographic QCD Model and QCD Phase Structure
  - arxiv: `1406.1865` (hep-th)
  - authors: Yi Yang, Pei-Hung Yuan

- [2014] The Appell Function $F_1$ and Regge String Scattering Amplitudes
  - arxiv: `1406.1285` (hep-th)
  - authors: Jen-Chi Lee, Yi Yang

- [2013] Phase Structure in a Dynamical Soft-Wall Holographic QCD Model
  - arxiv: `1301.0385` (hep-th)
  - authors: Song He, Shang-Yu Wu, Yi Yang, Pei-Hung Yuan

- [2013] BCFW Deformation and Regge Limit
  - arxiv: `1305.7442` (hep-th)
  - authors: Chih-Hao Fu, Jen-Chi Lee, Chung-I Tan, Yi Yang

- [2013] Recurrence Relations of Higher Spin BPST Vertex Operators for Open String
  - arxiv: `1304.6948` (hep-th)
  - authors: Chih-Hao Fu, Jen-Chi Lee, Chung-I Tan, Yi Yang

- [2012] A note on on-shell recursion relation of string amplitudes
  - arxiv: `1210.1776` (hep-th)
  - authors: Yung-Yeh Chang, Bo Feng, Chih-Hao Fu, Jen-Chi Lee, Yihong Wang

- [2011] String Scattering Amplitudes in High Energy Limits
  - arxiv: `1112.6077` (hep-th)
  - authors: Yi Yang, Jenchi Lee

- [2011] Phase Structure of Kerr-AdS Black Hole
  - arxiv: `1104.0502` (hep-th)
  - authors: Yu-Dai Tsai, X. N. Wu, Yi Yang

- [2011] Higher Spin String States Scattered from D-particle in the Regge Regime and Factorized Rat
  - arxiv: `1101.1228` (hep-th)
  - authors: Jen-Chi Lee, Yoshihiro Mitsuka, Yi Yang

- [2010] High-Energy String Scattering Amplitudes and Signless Stirling Number Identity
  - arxiv: `1012.5225` (hep-th)
  - authors: Jen-Chi Lee, Catherine H. Yan, Yi Yang

- [2010] Regge Closed String Scattering and its Implication on Fixed angle Closed String Scattering
  - arxiv: `1001.4843` (hep-th)
  - authors: Jen-Chi Lee, Yi Yang

- [2010] Exponential fall-off Behavior of Regge Scatterings in Compactified Open String Theory
  - arxiv: `1012.3158` (hep-th)
  - authors: Song He, Jen-Chi Lee, Yi Yang

- [2010] Massive Superstring Scatterings in the Regge Regime
  - arxiv: `1001.5392` (hep-th)
  - authors: Song He, Jen-Chi Lee, Keijiro Takahashi, Yi Yang

- [2009] Stirling number Identities and High energy String Scatterings
  - arxiv: `0909.3894` (hep-th)
  - authors: Jen-Chi Lee, Yi Yang, Sheng-Lan Ko

- [2008] High-energy String Scatterings of Compactified Open String
  - arxiv: `0805.3168` (hep-th)
  - authors: Jen-Chi Lee, Tomohisa Takimi, Yi Yang

- [2008] Kummer function and High energy String Scatterings
  - arxiv: `0811.4502` (hep-th)
  - authors: Sheng-Lan Ko, Jen-Chi Lee, Yi Yang

- [2008] Patterns of High energy Massive String Scatterings in the Regge regime
  - arxiv: `0812.4190` (hep-th)
  - authors: Sheng-Lan Ko, Jen-Chi Lee, Yi Yang

- [2007] High-energy Massive String Scatterings from Orientifold Planes
  - arxiv: `0712.4245` (hep-th)
  - authors: Jen-Chi Lee, Yi Yang

- [2007] Confront Holographic QCD with Regge Trajectories of vectors and axial-vectors
  - arxiv: `0710.0988` (hep-ph)
  - authors: Song He, Mei Huang, Qi-Shu Yan, Yi Yang

- [2007] Linear Relations and their Breakdown in High Energy Massive String Scatterings in Compact 
  - arxiv: `0705.1872` (hep-th)
  - authors: Jen-Chi Lee, Yi Yang

- [2007] Power-law Behavior of High Energy String Scatterings in Compact Spaces
  - arxiv: `0709.4657` (hep-th)
  - authors: Jen-Chi Lee, Yi Yang

- [2006] Linear Relations of High Energy Absorption/Emission Amplitudes of D-brane
  - arxiv: `hep-th/0612059` (hep-th)
  - authors: Jen-Chi Lee, Yi Yang

- [2006] Power-law Behavior of Strings Scattered from Domain-wall at High Energies and Breakdown of
  - arxiv: `hep-th/0610219` (hep-th)
  - authors: Chuan Tsung Chan, Jen-Chi Lee, Yi Yang

- [2006] Scatterings of Massive String States from D-brane and Their Linear Relations at High Energ
  - arxiv: `hep-th/0610062` (hep-th)
  - authors: Chuan-Tsung Chan, Jen-Chi Lee, Yi Yang

- [2006] Notes on High Energy Limit of Bosonic Closed String Scattering Amplitudes
  - arxiv: `hep-th/0604122` (hep-th)
  - authors: Chuan-Tsung Chan, Jen-Chi Lee, Yi Yang

- [2005] High-energy zero-norm states and symmetries of string theory
  - arxiv: `hep-th/0505035` (hep-th)
  - authors: Chuan-Tsung Chan, Pei-Ming Ho, Jen-Chi Lee, Shunsuke Teraguchi, Yi Yang

- [2005] High Energy Scattering Amplitudes of Superstring Theory
  - arxiv: `hep-th/0510247` (hep-th)
  - authors: Chuan-Tsung Chan, Jen-Chi Lee, Yi Yang

- [2005] Generalizations of Lunin-Maldacena transformation on the $AdS sub 5 x S sup 5$ background
  - arxiv: `hep-th/0509058` (hep-th)
  - authors: R. C. Rashkov, K. S. Viswanathan, Yi Yang

- [2005] Solving all 4-point correlation functions for bosonic open string theory in the high energ
  - arxiv: `hep-th/0504138` (hep-th)
  - authors: Chuan-Tsung Chan, Pei-Ming Ho, Jen-Chi Lee, Shunsuke Teraguchi, Yi Yang

- [2005] Comments on the high energy limit of bosonic open string theory
  - arxiv: `hep-th/0509009` (hep-th)
  - authors: Chuan-Tsung Chan, Pei-Ming Ho, Jen-Chi Lee, Shunsuke Teraguchi, Yi Yang

- [2005] Anatomy of Zero-norm States in String Theory
  - arxiv: `hep-th/0501020` (hep-th)
  - authors: Chuan-Tsung Chan, Jen-Chi Lee, Yi Yang

- [2004] Semiclassical Analysis of String/Gauge Duality on Non-commutative Space
  - arxiv: `hep-th/0404122` (hep-th)
  - authors: R. C. Rashkov, K. S. Viswanathan, Yi Yang

- [2001] Non-orientable Boundary Superstring Field theory with Tachyon field
  - arxiv: `hep-th/0107098` (hep-th)
  - authors: K. S. Viswanathan, Yi Yang

- [2001] Tachyon Condensation and Background Independent Superstring Field Theory
  - arxiv: `hep-th/0104099` (hep-th)
  - authors: K. S. Viswanathan, Y. Yang

- [2001] Boundary String Field Theory at One-loop
  - arxiv: `hep-th/0109032` (hep-th)
  - authors: Taejin Lee, K. S. Viswanathan, Yi Yang

- [2001] Background Independent Open String Field Theory with Constant B field On the Annulus
  - arxiv: `hep-th/0101207` (hep-th)
  - authors: R. Rashkov, K. S. Viswanathan, Y. Yang


## yau-shingtung (en=Shing-Tung Yau) — 192 candidates not in yaml

- [2026] Polylab: A MATLAB Toolbox for Multivariate Polynomial Modeling
  - arxiv: `2604.06575` (cs.MS)
  - authors: Yi-Shuai Niu, Shing-Tung Yau

- [2026] Microlocal index theorems and analytic torsion invariants in the geometric theory of parti
  - arxiv: `2603.11198` (math.AG)
  - authors: Jacob Kryczka, Vladimir Rubtsov, Artan Sheshmani, Shing-Tung Yau

- [2026] Algebra of Path Integrals on Digraphs
  - arxiv: `2603.01531` (math.AT)
  - authors: Shing-Tung Yau, Mengmeng Zhang, Yunpeng Zi

- [2026] Affine Normal Directions via Log-Determinant Geometry: Scalable Computation under Sparse P
  - arxiv: `2604.01163` (math.OC)
  - authors: Yi-Shuai Niu, Artan Sheshmani, Shing-Tung Yau

- [2026] A Proof of the Eigenvalue Ratio Bound for Embedded Surfaces
  - arxiv: `2603.21035` (math.DG)
  - authors: Ricardo Gloria-Picazzo, Yingying Wu, Shing-Tung Yau

- [2025] Semi-Global Existence and Trapped Surface Formation for the Einstein-Vlasov System
  - arxiv: `2510.12429` (math.AP)
  - authors: Nikolaos Athanasiou, Puskar Mondal, Shing-Tung Yau

- [2025] Tropical super Gromov-Witten invariants
  - arxiv: `2510.17400` (math.AG)
  - authors: Artan Sheshmani, Shing-Tung Yau, Benjamin Zhou

- [2025] Dynamical Formation of Black Holes due to Boundary Effect in Vacuum Gravity
  - arxiv: `2511.09508` (gr-qc)
  - authors: Puskar Mondal, Shing-Tung Yau

- [2025] The Critical LYZ Equation in Kähler Geometry
  - arxiv: `2511.21492` (math.DG)
  - authors: Jixiang Fu, Shing-Tung Yau, Dekai Zhang

- [2024] Futaki Invariants and Reflexive Polygons
  - arxiv: `2410.18476` (hep-th)
  - authors: Jiakang Bao, Eugene Choi, Yang-Hui He, Rak-Kyeong Seong, Shing-Tung Yau

- [2024] A proposal of quasi-local mass for 2-surfaces of timelike mean curvature
  - arxiv: `2407.00593` (gr-qc)
  - authors: Bowen Zhao, Shing-Tung Yau, Lars Andersson

- [2024] A new conformal quasi-local energy in general relativity
  - arxiv: `2406.02621` (gr-qc)
  - authors: Puskar Mondal, Shing-Tung Yau

- [2024] Derived Moduli Spaces of Nonlinear PDEs II: Variational Tricomplex and BV Formalism
  - arxiv: `2406.16825` (math.AG)
  - authors: Jacob Kryczka, Artan Sheshmani, Shing-Tung Yau

- [2024] Strong field behavior of Wang-Yau Quasi-local energy
  - arxiv: `2406.10751` (gr-qc)
  - authors: Bowen Zhao, Lars Andersson, Shing-Tung Yau

- [2024] Some Remarks on Wang-Yau Quasi-Local Mass
  - arxiv: `2402.19310` (gr-qc)
  - authors: Bowen Zhao, Lars Andersson, Shing-Tung Yau

- [2024] The Cellular Homology of Digraphs
  - arxiv: `2402.05682` (math.CO)
  - authors: Xinxing Tang, Shing-Tung Yau

- [2024] C-R-T Fractionalization in the First Quantized Hamiltonian Theory
  - arxiv: `2412.11958` (cond-mat.str-el)
  - authors: Yang-Yang Li, Zheyan Wan, Juven Wang, Shing-Tung Yau, Yi-Zhuang You

- [2023] Torus Actions on Moduli Spaces of Super Stable Maps of Genus Zero
  - arxiv: `2306.09730` (math.DG)
  - authors: Enno Keßler, Artan Sheshmani, Shing-Tung Yau

- [2023] Duality in Gauge Theory, Gravity and String Theory
  - arxiv: `2311.07934` (hep-th)
  - authors: Uri Kol, Shing-Tung Yau

- [2023] Transformation of mass-angular momentum aspect under BMS transformations
  - arxiv: `2305.04617` (gr-qc)
  - authors: Po-Ning Chen, Mu-Tao Wang, Ye-Kai Wang, Shing-Tung Yau

- [2023] Super Gromov-Witten Invariants via torus localization
  - arxiv: `2311.09074` (math.AG)
  - authors: Enno Keßler, Artan Sheshmani, Shing-Tung Yau

- [2023] Formation of trapped surfaces in the Einstein-Yang-Mills system
  - arxiv: `2302.06915` (math.AP)
  - authors: Nikolaos Athanasiou, Puskar Mondal, Shing-Tung Yau

- [2023] Derived Moduli Spaces of Nonlinear PDEs I: Singular Propagations
  - arxiv: `2312.05226` (math.AG)
  - authors: Jacob Kryczka, Artan Sheshmani, Shing-Tung Yau

- [2023] Generalized Monge-Ampère functionals and related variational problems
  - arxiv: `2306.01636` (math.AP)
  - authors: Freid Tong, Shing-Tung Yau

- [2023] C-R-T Fractionalization, Fermions, and Mod 8 Periodicity
  - arxiv: `2312.17126` (hep-th)
  - authors: Zheyan Wan, Juven Wang, Shing-Tung Yau, Yi-Zhuang You

- [2023] A Quasi-Local Mass
  - arxiv: `2309.02770` (math.DG)
  - authors: Aghil Alaee, Marcus Khuri, Shing-Tung Yau

- [2022] 3-manifolds and Vafa-Witten theory
  - arxiv: `2207.05775` (math.GT)
  - authors: Sergei Gukov, Artan Sheshmani, Shing-Tung Yau

- [2022] Soft noncommutative flag schemes
  - arxiv: `2204.12773` (math.AG)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2022] The Strominger system in the square of a Kähler class
  - arxiv: `2211.03784` (math.DG)
  - authors: Tristan C. Collins, Sebastien Picard, Shing-Tung Yau

- [2022] Cross-Section Continuity of Definitions of Angular Momentum
  - arxiv: `2207.04590` (gr-qc)
  - authors: Po-Ning Chen, Daniel Paraizo, Robert M. Wald, Mu-Tao Wang, Ye-Kai Wang

- [2022] Global exterior stability of the Minkowski space: coupled Einstein-Yang-Mills perturbation
  - arxiv: `2211.03167` (gr-qc)
  - authors: Puskar Mondal, Shing-Tung Yau

- [2022] Conserved quantities in general relativity -- the view from null infinity
  - arxiv: `2204.04010` (gr-qc)
  - authors: Po-Ning Chen, Mu-Tao Wang, Ye-Kai Wang, Shing-Tung Yau

- [2022] Einstein-Yang-Mills equations in the double null framework
  - arxiv: `2205.01101` (gr-qc)
  - authors: Puskar Mondal, Shing-Tung Yau

- [2022] Stable regular solution of Einstein-Yang-Mills equation
  - arxiv: `2210.09861` (gr-qc)
  - authors: Yuewen Chen, Shing-Tung Yau

- [2022] Supertranslation invariance of angular momentum at null infinity in double null gauge
  - arxiv: `2204.03182` (gr-qc)
  - authors: Po-Ning Chen, Mu-Tao Wang, Ye-Kai Wang, Shing-Tung Yau

- [2021] Soft noncommutative schemes via toric geometry and morphisms from an Azumaya scheme with a
  - arxiv: `2108.05328` (math.AG)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2021] Stability of the tangent bundle through conifold transitions
  - arxiv: `2102.11170` (math.DG)
  - authors: Tristan C. Collins, Sebastien Picard, Shing-Tung Yau

- [2021] Non-Holomorphic Cycles and Non-BPS Black Branes
  - arxiv: `2104.06420` (hep-th)
  - authors: Cody Long, Artan Sheshmani, Cumrun Vafa, Shing-Tung Yau

- [2021] Supertranslation invariance of angular momentum
  - arxiv: `2102.03235` (gr-qc)
  - authors: Po-Ning Chen, Mu-Tao Wang, Ye-Kai Wang, Shing-Tung Yau

- [2021] Discrete Morse Theory on Digraphs
  - arxiv: `2102.10518` (math.CO)
  - authors: Yong Lin, Chong Wang, Shing-Tung Yau

- [2021] Special Lagrangian cycles and Calabi-Yau transitions
  - arxiv: `2111.10355` (math.DG)
  - authors: Tristan C. Collins, Sergei Gukov, Sebastien Picard, Shing-Tung Yau

- [2021] Ricci-flat graphs with maximum degree at most 4
  - arxiv: `2103.00941` (math.DG)
  - authors: Shuliang Bai, Linyuan Lu, Shing-Tung Yau

- [2021] A new flow solving the LYZ equation in Kähler geometry
  - arxiv: `2105.13576` (math.DG)
  - authors: Jixiang Fu, Shing-Tung Yau, Dekai Zhang

- [2020] Elliptic stable envelopes and hypertoric loop spaces
  - arxiv: `2010.00670` (math.AG)
  - authors: Michael McBreen, Artan Sheshmani, Shing-Tung Yau

- [2020] Grothendieck meeting [Wess & Bagger]: [Supersymmetry and supergravity: IV, V, VI, VII, XXI
  - arxiv: `2002.11868` (math.AG)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2020] Twisted Quasimaps and Symplectic Duality for Hypertoric Spaces
  - arxiv: `2004.04508` (math.AG)
  - authors: Michael McBreen, Artan Sheshmani, Shing-Tung Yau

- [2020] Super quantum cohomology I: Super stable maps of genus zero with Neveu-Schwarz punctures
  - arxiv: `2010.15634` (math.DG)
  - authors: Enno Keßler, Artan Sheshmani, Shing-Tung Yau

- [2020] Graph Laplacians, Riemannian Manifolds and their Machine-Learning
  - arxiv: `2006.16619` (math.CO)
  - authors: Yang-Hui He, Shing-Tung Yau

- [2020] Green's Functions for Vladimirov Derivatives and Tate's Thesis
  - arxiv: `2001.01721` (hep-th)
  - authors: An Huang, Bogdan Stoica, Shing-Tung Yau, Xiao Zhong

- [2020] Computing Harmonic Maps and Conformal Maps on Point Clouds
  - arxiv: `2009.09383` (math.DG)
  - authors: Tianqi Wu, Shing-Tung Yau

- [2020] Global stability of spacetimes with supersymmetric compactifications
  - arxiv: `2006.00824` (math.AP)
  - authors: Lars Andersson, Pieter Blue, Zoe Wyatt, Shing-Tung Yau

- [2020] Positive Scalar Curvature on Noncompact Manifolds and the Liouville Theorem
  - arxiv: `2009.12618` (math.DG)
  - authors: Martin Lesourd, Ryan Unger, Shing-Tung Yau

- [2020] Torsion of digraphs and path complexes
  - arxiv: `2012.07302` (math.CO)
  - authors: Alexander Grigor'yan, Yong Lin, Shing-Tung Yau

- [2020] Global shifted potentials for moduli stacks of sheaves on Calabi-Yau four-folds
  - arxiv: `2007.13194` (math.AG)
  - authors: Dennis Borisov, Ludmil Katzarkov, Artan Sheshmani, Shing-Tung Yau

- [2020] Stable Surfaces and Free Boundary Marginally Outer Trapped Surfaces
  - arxiv: `2009.07933` (math.DG)
  - authors: Aghil Alaee, Martin Lesourd, Shing-Tung Yau

- [2019] Physicists' $d=3+1$, $N=1$ superspace-time and supersymmetric QFTs from a tower constructi
  - arxiv: `1902.06246` (hep-th)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2019] Singularity, Sasaki-Einstein manifold, Log del Pezzo surface and $\mathcal{N}=1$ AdS/CFT c
  - arxiv: `1903.00150` (hep-th)
  - authors: Dan Xie, Shing-Tung Yau

- [2019] Quantum Statistics and Spacetime Topology: Quantum Surgery Formulas
  - arxiv: `1901.11537` (quant-ph)
  - authors: Juven Wang, Xiao-Gang Wen, Shing-Tung Yau

- [2019] General relativity from $p$-adic strings
  - arxiv: `1901.02013` (hep-th)
  - authors: An Huang, Bogdan Stoica, Shing-Tung Yau

- [2019] Higher rank flag sheaves on Surfaces and Vafa-Witten invariants
  - arxiv: `1911.00124` (math.AG)
  - authors: Artan Sheshmani, Shing-Tung Yau

- [2019] Strictification and gluing of Lagrangian distributions on derived schemes with shifted sym
  - arxiv: `1908.00651` (math.AG)
  - authors: Dennis Borisov, Ludmil Katzarkov, Artan Sheshmani, Shing-Tung Yau

- [2019] Super $J$-holomorphic Curves: Construction of the Moduli Space
  - arxiv: `1911.05607` (math.DG)
  - authors: Enno Keßler, Artan Sheshmani, Shing-Tung Yau

- [2019] Quasi-local mass at null infinity in Bondi-Sachs coordinates
  - arxiv: `1901.06952` (gr-qc)
  - authors: Po-Ning Chen, Mu-Tao Wang, Ye-Kai Wang, Shing-Tung Yau

- [2019] Positive mass theorem for initial data sets with corners along a hypersurface
  - arxiv: `1906.08796` (math.DG)
  - authors: Aghil Alaee, Shing-Tung Yau

- [2019] Quasi-local mass at axially symmetric null infinity
  - arxiv: `1901.06948` (gr-qc)
  - authors: Po-Ning Chen, Mu-Tao Wang, Ye-Kai Wang, Shing-Tung Yau

- [2019] Quasi-local mass on unit spheres at spatial infinity
  - arxiv: `1901.06954` (gr-qc)
  - authors: Po-Ning Chen, Mu-Tao Wang, Ye-Kai Wang, Shing-Tung Yau

- [2019] Non-Abelian Gauged Fracton Matter Field Theory: New Sigma Models, Superfluids and Vortices
  - arxiv: `1912.13485` (cond-mat.str-el)
  - authors: Juven Wang, Shing-Tung Yau

- [2019] Gauss-Manin connection in disguise: Genus two curves
  - arxiv: `1910.07624` (math.AG)
  - authors: Jin Cao, Hossein Movasati, Shing-Tung Yau

- [2019] Higher-Rank Tensor Non-Abelian Field Theory: Higher-Moment or Subdimensional Polynomial Gl
  - arxiv: `1911.01804` (hep-th)
  - authors: Juven Wang, Kai Xu, Shing-Tung Yau

- [2018] $N=1$ fermionic D3-branes in RNS formulation I. $C^\infty$-Algebrogeometric foundations of
  - arxiv: `1808.05011` (math.DG)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2018] Atiyah class and sheaf counting on local Calabi Yau fourfolds
  - arxiv: `1810.09382` (math.AG)
  - authors: Duiliu-Emanuel Diaconescu, Artan Sheshmani, Shing-Tung Yau

- [2018] Moment maps, nonlinear PDE, and stability in mirror symmetry
  - arxiv: `1811.04824` (math.DG)
  - authors: Tristan C. Collins, Shing-Tung Yau

- [2018] Hasse-Witt matrices, unit roots and period integrals
  - arxiv: `1801.01189` (math.AG)
  - authors: An Huang, Bong Lian, Shing-Tung Yau, Chenglong Yu

- [2018] Tunneling Topological Vacua via Extended Operators: (Spin-)TQFT Spectra and Boundary Decon
  - arxiv: `1801.05416` (cond-mat.str-el)
  - authors: Juven Wang, Kantaro Ohmori, Pavel Putrov, Yunqin Zheng, Zheyan Wan

- [2017] Dynamics of D-branes II. The standard action --- an analogue of the Polyakov action for (f
  - arxiv: `1704.03237` (hep-th)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2017] Further studies of the notion of differentiable maps from Azumaya/matrix supermanifolds I.
  - arxiv: `1709.08927` (math.DG)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2017] The deformed Hermitian-Yang-Mills equation in geometry and physics
  - arxiv: `1712.00893` (math.DG)
  - authors: Tristan C. Collins, Dan Xie, Shing-Tung Yau

- [2017] Weil-Petersson geometry on the space of Bridgeland stability conditions
  - arxiv: `1708.02161` (math.AG)
  - authors: Yu-Wei Fan, Atsushi Kanazawa, Shing-Tung Yau

- [2017] ADE String Chains and Mirror Symmetry
  - arxiv: `1705.05199` (hep-th)
  - authors: Babak Haghighat, Wenbin Yan, Shing-Tung Yau

- [2017] Mirror of Atiyah flop in symplectic geometry and stability conditions
  - arxiv: `1706.02942` (math.SG)
  - authors: Yu-Wei Fan, Hansol Hong, Siu-Cheong Lau, Shing-Tung Yau

- [2017] Calabi-Yau Volumes and Reflexive Polytopes
  - arxiv: `1704.03462` (hep-th)
  - authors: Yang-Hui He, Rak-Kyeong Seong, Shing-Tung Yau

- [2017] Mordell-Weil Torsion, Anomalies, and Phase Transitions
  - arxiv: `1712.02337` (hep-th)
  - authors: Mboyo Esole, Monica Jinwoo Kang, Shing-Tung Yau

- [2017] 4d N=2 SCFT and singularity theory Part III: Rigid singularity
  - arxiv: `1712.00464` (hep-th)
  - authors: Bingyi Chen, Dan Xie, Stephen S. -T. Yau, Shing-Tung Yau, Huaiqing Zuo

- [2016] More on the admissible condition on differentiable maps $\varphi: (X^{\!A\!z},E;\nabla)\ri
  - arxiv: `1611.09439` (hep-th)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2016] Dynamics of D-branes I. The non-Abelian Dirac-Born-Infeld action, its first variation, and
  - arxiv: `1606.08529` (hep-th)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2016] Chiral algebra of Argyres-Douglas theory from M5 brane
  - arxiv: `1604.02155` (hep-th)
  - authors: Dan Xie, Wenbin Yan, Shing-Tung Yau

- [2016] Braiding Statistics and Link Invariants of Bosonic/Fermionic Topological Quantum Matter in
  - arxiv: `1612.09298` (cond-mat.str-el)
  - authors: Pavel Putrov, Juven Wang, Shing-Tung Yau

- [2016] Quantum Statistics and Spacetime Surgery
  - arxiv: `1602.05951` (cond-mat.str-el)
  - authors: Juven Wang, Xiao-Gang Wen, Shing-Tung Yau

- [2016] K stability and stability of chiral ring
  - arxiv: `1606.09260` (hep-th)
  - authors: Tristan C. Collins, Dan Xie, Shing-Tung Yau

- [2016] 4d N=2 SCFT and singularity theory Part II: Complete intersection
  - arxiv: `1604.07843` (hep-th)
  - authors: Bingyi Chen, Dan Xie, Shing-Tung Yau, Stephen S. -T. Yau, Huaiqing Zuo

- [2016] Sharp Davies-Gaffney-Grigor'yan Lemma on Graphs
  - arxiv: `1604.01911` (math.DG)
  - authors: Frank Bauer, Bobo Hua, Shing-Tung Yau

- [2015] Further studies on the notion of differentiable maps from Azumaya/matrix manifolds, I. The
  - arxiv: `1508.02347` (math.DG)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2015] D-branes and synthetic/$C^{\infty}$-algebraic symplectic/calibrated geometry, I: Lemma on 
  - arxiv: `1504.01841` (math.SG)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2015] Airy Equation for the Topological String Partition Function in a Scaling Limit
  - arxiv: `1506.01375` (hep-th)
  - authors: Murad Alim, Shing-Tung Yau, Jie Zhou

- [2015] Negative Holomorphic curvature and positive canonical bundle
  - arxiv: `1505.05802` (math.DG)
  - authors: Damin Wu, Shing-Tung Yau

- [2015] Semicontinuity of 4d N=2 spectrum under renormalization group flow
  - arxiv: `1510.06036` (hep-th)
  - authors: Dan Xie, Shing-Tung Yau

- [2015] (1,1) forms with specified Lagrangian phase: A priori estimates and algebraic obstructions
  - arxiv: `1508.01934` (math.DG)
  - authors: Tristan C. Collins, Adam Jacob, Shing-Tung Yau

- [2015] Calabi-Yau modular forms in limit: Elliptic Fibrations
  - arxiv: `1511.01310` (math.AG)
  - authors: Babak Haghighat, Hossein Movasati, Shing-Tung Yau

- [2015] 4d N=2 SCFT and singularity theory Part I: Classification
  - arxiv: `1510.01324` (hep-th)
  - authors: Dan Xie, Shing-Tung Yau

- [2014] D-branes and Azumaya/matrix noncommutative differential geometry,II: Azumaya/matrix superm
  - arxiv: `1412.0771` (hep-th)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2014] D-branes and Azumaya/matrix noncommutative differential geometry, I: D-branes as fundament
  - arxiv: `1406.0929` (math.DG)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2014] Cohomology and Hodge Theory on Symplectic Manifolds: III
  - arxiv: `1402.0427` (math.SG)
  - authors: Chung-Jun Tsai, Li-Sheng Tseng, Shing-Tung Yau

- [2014] Gauss-Manin connection in disguise: Calabi-Yau threefolds
  - arxiv: `1410.1889` (math.AG)
  - authors: Murad Alim, Hossein Movasati, Emanuel Scheidegger, Shing-Tung Yau

- [2014] Non-Kaehler SYZ mirror symmetry
  - arxiv: `1409.2765` (math.DG)
  - authors: Siu-Cheong Lau, Li-Sheng Tseng, Shing-Tung Yau

- [2014] Heterotic String Compactification and New Vector Bundles
  - arxiv: `1412.8000` (hep-th)
  - authors: Hai Lin, Baosen Wu, Shing-Tung Yau

- [2014] Invariant Solutions to the Strominger System on Complex Lie Groups and Their Quotients
  - arxiv: `1407.7641` (math-ph)
  - authors: Teng Fei, Shing-Tung Yau

- [2014] A New Model for Elliptic Fibrations with a Rank One Mordell-Weil Group: I. Singular Fibers
  - arxiv: `1410.0003` (hep-th)
  - authors: Mboyo Esole, Monica Jinwoo Kang, Shing-Tung Yau

- [2014] Volume doubling, Poincaré inequality and Guassian heat kernel estimate for nonnegative cur
  - arxiv: `1411.5087` (math.DG)
  - authors: Paul Horn, Yong Lin, Shuang Liu, Shing-Tung Yau

- [2014] Extremal Bundles on Calabi-Yau Threefolds
  - arxiv: `1403.1268` (hep-th)
  - authors: Peng Gao, Yang-Hui He, Shing-Tung Yau

- [2014] Singularities and Gauge Theory Phases II
  - arxiv: `1407.1867` (hep-th)
  - authors: Mboyo Esole, Shu-Heng Shao, Shing-Tung Yau

- [2014] Singularities and Gauge Theory Phases
  - arxiv: `1402.6331` (hep-th)
  - authors: Mboyo Esole, Shu-Heng Shao, Shing-Tung Yau

- [2014] On cohomology theory of (di)graphs
  - arxiv: `1409.6194` (math.CO)
  - authors: An Huang, Shing-Tung Yau

- [2014] On the validity of the definition of angular momentum in general relativity
  - arxiv: `1401.0597` (math.DG)
  - authors: Po-Ning Chen, Lan-Hsuan Huang, Mu-Tao Wang, Shing-Tung Yau

- [2013] Special Polynomial Rings, Quasi Modular Forms and Duality of Topological Strings
  - arxiv: `1306.0002` (hep-th)
  - authors: Murad Alim, Emanuel Scheidegger, Shing-Tung Yau, Jie Zhou

- [2013] A mathematical theory of D-string world-sheet instantons, I: Compactness of the stack of $
  - arxiv: `1302.2054` (math.AG)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2013] A mathematical theory of D-string world-sheet instantons, II: Moduli stack of $Z$-(semi)st
  - arxiv: `1310.5195` (math.AG)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2013] On the Holonomic Rank Problem
  - arxiv: `1302.4481` (math.AG)
  - authors: Spencer Bloch, An Huang, Bong H. Lian, Vasudevan Srinivas, Shing-Tung Yau

- [2013] Nodal geometry of graphs on surfaces
  - arxiv: `1307.3226` (math.CO)
  - authors: Yong Lin, Gabor Lippner, Dan Mangoubi, Shing-Tung Yau

- [2013] Li-Yau inequality on graphs
  - arxiv: `1306.2561` (math.AP)
  - authors: Frank Bauer, Paul Horn, Yong Lin, Gabor Lippner, Dan Mangoubi

- [2013] Minimizing properties of critical points of quasi-local energy
  - arxiv: `1302.5321` (math.DG)
  - authors: PoNing Chen, Mu-Tao Wang, Shing-Tung Yau

- [2013] Simplicial Ricci Flow
  - arxiv: `1302.0804` (math.DG)
  - authors: Warner A. Miller, Jonathan R. McDonald, Paul M. Alsing, David Gu, Shing-Tung Yau

- [2012] A brief review on geometry and spectrum of graphs
  - arxiv: `1204.3168` (math.CO)
  - authors: Yong Lin, Shing-Tung Yau

- [2012] Hodge Bundles on Smooth Compactifications of Siegel Varieties and Applications
  - arxiv: `1201.3784` (math.AG)
  - authors: Shing-Tung Yau, Yi Zhang

- [2012] The Geometry on Smooth Toroidal Compactifications of Siegel varieties
  - arxiv: `1201.3785` (math.AG)
  - authors: Shing-Tung Yau, Yi Zhang

- [2012] Homologies of path complexes and digraphs
  - arxiv: `1207.2834` (math.CO)
  - authors: Alexander Grigor'yan, Yong Lin, Yuri Muranov, Shing-Tung Yau

- [2011] Immersed Lagrangian deformations of a branched covering of a special Lagrangian 3-sphere i
  - arxiv: `1109.1878` (math.DG)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2011] Algebraic cobordism of filtered vector bundles on varieties: Notes on a work of Lee and Pa
  - arxiv: `1104.0280` (math.AG)
  - authors: Chien-Hao Liu, Yu-jong Tzeng, Shing-Tung Yau

- [2011] Generalized Cohomologies and Supersymmetry
  - arxiv: `1111.6968` (hep-th)
  - authors: Li-Sheng Tseng, Shing-Tung Yau

- [2011] Period Integrals of CY and General Type Complete Intersections
  - arxiv: `1105.4872` (math.AG)
  - authors: Bong H. Lian, Shing-Tung Yau

- [2011] D0-brane realizations of the resolution of a reduced singular curve
  - arxiv: `1111.4707` (math.AG)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2011] Small resolutions of SU(5)-models in F-theory
  - arxiv: `1107.0733` (hep-th)
  - authors: Mboyo Esole, Shing-Tung Yau

- [2011] Period Integrals and Tautological Systems
  - arxiv: `1105.2984` (math.AG)
  - authors: Bong H. Lian, Ruifang Song, Shing-Tung Yau

- [2011] D5 elliptic fibrations: non-Kodaira fibers and new orientifold limits of F-theory
  - arxiv: `1110.6177` (hep-th)
  - authors: Mboyo Esole, James Fullwood, Shing-Tung Yau

- [2011] Quantum tunneling on graphs
  - arxiv: `1101.2660` (quant-ph)
  - authors: Yong Lin, Gabor Lippner, Shing-Tung Yau

- [2010] D-branes and Azumaya noncommutative geometry: From Polchinski to Grothendieck
  - arxiv: `1003.1178` (math.SG)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2010] Cohomology and Hodge Theory on Symplectic Manifolds: II
  - arxiv: `1011.1250` (math.SG)
  - authors: Li-Sheng Tseng, Shing-Tung Yau

- [2010] D-branes of A-type, their deformations, and Morse cobordism of A-branes on Calabi-Yau 3-fo
  - arxiv: `1012.0525` (math.SG)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2010] Evaluating quasilocal energy and solving optimal embedding equation at null infinity
  - arxiv: `1002.0927` (math.DG)
  - authors: PoNing Chen, Mu-Tao Wang, Shing-Tung Yau

- [2010] Finiteness of Subfamilies of Calabi-Yau n-Folds over Curves with Maximal Length of Yukawa-
  - arxiv: `1010.4141` (math.AG)
  - authors: Kefeng Liu, Andrey Todorov, Shing-Tung Yau, Kang Zuo

- [2009] Azumaya structure on D-branes and resolution of ADE orbifold singularities revisited: Doug
  - arxiv: `0901.0342` (math.AG)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2009] Recent Development on the Geometry of the Teichmuller and Moduli Spaces of Riemann Surface
  - arxiv: `0912.5471` (math.DG)
  - authors: Kefeng Liu, Xiaofeng Sun, Shing-Tung Yau

- [2009] Azumaya structure on D-branes and deformations and resolutions of a conifold revisited: Kl
  - arxiv: `0907.0268` (math.AG)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2009] Nontrivial Azumaya noncommutative schemes, morphisms therefrom, and their extension by the
  - arxiv: `0909.2291` (math.AG)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2009] Global Torelli Theorem for Teichmuller Spaces of Polarized Calabi-Yau manifolds
  - arxiv: `0912.5239` (math.AG)
  - authors: Kefeng Liu, Andrey Todorov, Xiaofeng Sun, Shing-Tung Yau

- [2009] Cohomology and Hodge Theory on Symplectic Manifolds: I
  - arxiv: `0909.5418` (math.SG)
  - authors: Li-Sheng Tseng, Shing-Tung Yau

- [2009] Limit of quasilocal mass at spatial infinity
  - arxiv: `0906.0200` (math.DG)
  - authors: Mu-Tao Wang, Shing-Tung Yau

- [2009] Gap of the First Two Eigenvalues of the Schrödinger Operator with Nonconvex Potential
  - arxiv: `0902.2253` (math.DG)
  - authors: Shing-Tung Yau

- [2009] An Estimate of the Gap of the First Two Eigenvalues in the Schrödinger Operator
  - arxiv: `0902.2250` (math.DG)
  - authors: Shing-Tung Yau

- [2008] Balanced metrics on non-Kahler Calabi-Yau threefolds
  - arxiv: `0809.4748` (math.DG)
  - authors: Jixiang Fu, Jun Li, Shing-Tung Yau

- [2008] Isometric embeddings into the Minkowski space and new quasi-local mass
  - arxiv: `0805.1370` (math.DG)
  - authors: Mu-Tao Wang, Shing-Tung Yau

- [2008] Quasilocal mass in general relativity
  - arxiv: `0804.1174` (gr-qc)
  - authors: Mu-Tao Wang, Shing-Tung Yau

- [2008] A new geometric approach to problems in birational geometry
  - arxiv: `0811.2965` (math.AG)
  - authors: Chen-Yu Chi, Shing-Tung Yau

- [2007] Azumaya-type noncommutative spaces and morphisms therefrom: Polchinski's D-branes in strin
  - arxiv: `0709.1515` (math.AG)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2007] Taming symplectic forms and the Calabi-Yau equation
  - arxiv: `math/0703773` (math.DG)
  - authors: Valentino Tosatti, Ben Weinkove, Shing-Tung Yau

- [2006] Branes, Bundles and Attractors: Bogomolov and Beyond
  - arxiv: `math/0604597` (math.AG)
  - authors: Michael R. Douglas, Rene Reinbacher, Shing-Tung Yau

- [2006] Degeneration and gluing of Kuranishi structures in Gromov-Witten theory and the degenerati
  - arxiv: `math/0609483` (math.SG)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2006] Obstructions to the Existence of Sasaki-Einstein Metrics
  - arxiv: `hep-th/0607080` (hep-th)
  - authors: Jerome P. Gauntlett, Dario Martelli, James Sparks, Shing-Tung Yau

- [2006] A generalization of Liu-Yau's quasi-local mass
  - arxiv: `math/0602321` (math.DG)
  - authors: Mu-Tao Wang, Shing-Tung Yau

- [2006] Sasaki-Einstein Manifolds and Volume Minimisation
  - arxiv: `hep-th/0603021` (hep-th)
  - authors: Dario Martelli, James Sparks, Shing-Tung Yau

- [2005] Transformation of algebraic Gromov-Witten invariants of three-folds under flops and small 
  - arxiv: `math/0505084` (math.AG)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2005] The Geometric Dual of a-maximisation for Toric Sasaki-Einstein Manifolds
  - arxiv: `hep-th/0503183` (hep-th)
  - authors: Dario Martelli, James Sparks, Shing-Tung Yau

- [2004] Affine Manifolds, SYZ Geometry, and the "Y" Vertex
  - arxiv: `math/0405061` (math.DG)
  - authors: John Loftin, Shing-Tung Yau, Eric Zaslow

- [2004] Topological String Partition Functions as Polynomials
  - arxiv: `hep-th/0406078` (hep-th)
  - authors: Satoshi Yamaguchi, Shing-Tung Yau

- [2004] $S^1$-fixed-points in hyper-Quot-schemes and an exact mirror formula for flag manifolds fr
  - arxiv: `math/0401367` (math.AG)
  - authors: Chien-Hao Liu, Kefeng Liu, Shing-Tung Yau

- [2004] A degeneration formula of Gromov-Witten invariants with respect to a curve class for degen
  - arxiv: `math/0408147` (math.AG)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2004] Positivity of quasi-local mass II
  - arxiv: `math/0412292` (math.DG)
  - authors: Chiu-Chu Melissa Liu, Shing-Tung Yau

- [2004] Canonical Metrics on the Moduli Space of Riemann Surfaces II
  - arxiv: `math/0409220` (math.DG)
  - authors: Kefeng Liu, Xiaofeng Sun, Shing-Tung Yau

- [2004] Extracting Gromov-Witten invariants of a conifold from semi-stable reduction and relative 
  - arxiv: `math/0411038` (math.AG)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2003] Counting Unimodular Lattices in $\R^{r,s}$
  - arxiv: `math/0301095` (math.QA)
  - authors: Shinobu Hosono, Bong H. Lian, Keiji Oguiso, Shing-Tung Yau

- [2002] Autoequivalences of Derived Category of A K3 Surface and Monodromy Transformations
  - arxiv: `math/0201047` (math.AG)
  - authors: Shinobu Hosono, Bong H. Lian, Keiji Oguiso, Shing-Tung Yau

- [2002] c=2 Rational Toroidal Conformal Field Theories via the Gauss Product
  - arxiv: `hep-th/0211230` (hep-th)
  - authors: Shinobu Hosono, Bong H. Lian, Keiji Oguiso, Shing-Tung Yau

- [2002] On A-twisted moduli stack for curves from Witten's gauged linear sigma models
  - arxiv: `math/0212316` (math.AG)
  - authors: Chien-Hao Liu, Kefeng Liu, Shing-Tung Yau

- [2002] Duality and Fibrations on G_2 Manifolds
  - arxiv: `hep-th/0203217` (hep-th)
  - authors: Sergei Gukov, Shing-Tung Yau, Eric Zaslow

- [2001] Fibrewise T-Duality for D-Branes on Elliptic Calabi-Yau
  - arxiv: `hep-th/0101129` (hep-th)
  - authors: Bjorn Andreas, Gottfried Curio, Daniel Hernandez Ruiperez, Shing-Tung Yau

- [2001] Decay Rates and Probability Estimates for Massive Dirac Particles in the Kerr-Newman Black
  - arxiv: `gr-qc/0107094` (gr-qc)
  - authors: Felix Finster, Niky Kamran, Joel Smoller, Shing-Tung Yau

- [2001] The $S^1$ fixed points in Quot-schemes and mirror principle computations
  - arxiv: `math/0111256` (math.AG)
  - authors: Bong H. Lian, Chien-Hao Liu, Kefeng Liu, Shing-Tung Yau

- [2000] From Special Lagrangian to Hermitian-Yang-Mills via Fourier-Mukai Transform
  - arxiv: `math/0005118` (math.DG)
  - authors: Naichung Conan Leung, Shing-Tung Yau, Eric Zaslow

- [2000] The Interaction of Dirac Particles with Non-Abelian Gauge Fields and Gravity - Bound State
  - arxiv: `gr-qc/0001067` (gr-qc)
  - authors: Felix Finster, Joel Smoller, Shing-Tung Yau

- [2000] On the Splitting Type of an Equivariant Vector Bundle over a Toric Manifold
  - arxiv: `math/0002031` (math.AG)
  - authors: Chien-Hao Liu, Shing-Tung Yau

- [2000] A reconstruction of Euler data
  - arxiv: `math/0003071` (math.AG)
  - authors: Bong H. Lian, Chien-Hao Liu, Shing-Tung Yau

- [2000] Absence of Static, Spherically Symmetric Black Hole Solutions for Einstein-Dirac-Yang/Mill
  - arxiv: `gr-qc/0005028` (gr-qc)
  - authors: Felix Finster, Joel Smoller, Shing-Tung Yau

- [2000] Fourier-Mukai Transform and Mirror Symmetry for D-Branes on Elliptic Calabi-Yau
  - arxiv: `math/0012196` (math.AG)
  - authors: Bjorn Andreas, Gottfried Curio, Daniel Hernandez Ruiperez, Shing-Tung Yau

- [2000] The Long-Time Dynamics of Dirac Particles in the Kerr-Newman Black Hole Geometry
  - arxiv: `gr-qc/0005088` (gr-qc)
  - authors: Felix Finster, Niky Kamran, Joel Smoller, Shing-Tung Yau

- [2000] Maximal Unipotent Monodromy for Complete Intersection CY Manifolds
  - arxiv: `math/0008061` (math.AG)
  - authors: Bong H. Lian, Andrey Todorov, Shing-Tung Yau

- [2000] Toric morphisms and fibrations of toric Calabi-Yau hypersurfaces
  - arxiv: `math/0010082` (math.AG)
  - authors: Yi Hu, Chien-Hao Liu, Shing-Tung Yau

- [1999] The Interaction of Dirac Particles with Non-Abelian Gauge Fields and Gravity - Black Holes
  - arxiv: `gr-qc/9910047` (gr-qc)
  - authors: Felix Finster, Joel Smoller, Shing-Tung Yau

- [1999] Non-Existence of Time-Periodic Solutions of the Dirac Equation in an Axisymmetric Black Ho
  - arxiv: `gr-qc/9905047` (gr-qc)
  - authors: Felix Finster, Niky Kamran, Joel Smoller, Shing-Tung Yau

- [1999] The Einstein-Dirac-Maxwell Equations - Black Hole Solutions
  - arxiv: `gr-qc/9910030` (gr-qc)
  - authors: Felix Finster, Joel Smoller, Shing-Tung Yau

- [1996] Mirror Symmetry is T-Duality
  - arxiv: `hep-th/9606040` (hep-th)
  - authors: Andrew Strominger, Shing-Tung Yau, Eric Zaslow

- [1995] BPS States, String Duality, and Nodal Curves on K3
  - arxiv: `hep-th/9512121` (hep-th)
  - authors: Shing-Tung Yau, Eric Zaslow

- [1994] Mirror Symmetry, Mirror Map and Applications to Complete Intersection Calabi-Yau Spaces
  - arxiv: `hep-th/9406055` (hep-th)
  - authors: S. Hosono, A. Klemm, S. Theisen, Shing-Tung Yau

- [1994] Arithmetic Properties of Mirror Map and Quantum Coupling
  - arxiv: `hep-th/9411234` (hep-th)
  - authors: Bong H. Lian, Shing-Tung Yau


## you-lei (en=Lei You) — 1 candidates not in yaml

- [2025] Thermodynamic properties and Joule-Thomson expansion of AdS black hole with Gaussian distr
  - arxiv: `2503.12363` (gr-qc)
  - authors: Rui-Bo Wang, Lei You, Shi-Jie Ma, Jian-Bo Deng, Xian-Ru Hu


## zagier (en=Don Zagier) — 9 candidates not in yaml

- [2020] Information thermodynamics of financial markets: the Glosten-Milgrom model
  - arxiv: `2010.01905` (cond-mat.stat-mech)
  - authors: Léo Touzo, Matteo Marsili, Don Zagier

- [2019] Dynamics of geodesics, and Maass cusp forms
  - arxiv: `1906.01067` (math.DS)
  - authors: A. Pohl, D. Zagier

- [2004] Numerical verification of Beilinson's conjecture for K2 of hyperelliptic curves
  - arxiv: `math/0405040` (math.AG)
  - authors: Tim Dokchitser, Rob de Jeu, Don Zagier

- [2002] Crossing Probabilities and Modular Forms
  - arxiv: `math-ph/0209023` (math-ph)
  - authors: Peter Kleban, Don Zagier

- [2001] Period functions for Maass wave forms. I
  - arxiv: `math/0101270` (math.NT)
  - authors: J. Lewis, D. Zagier

- [2000] Finite Size XXZ Spin Chain with Anisotropy Parameter $Δ= {1/2}$
  - arxiv: `nlin/0010021` (nlin.SI)
  - authors: V. Fridkin, Yu. Stroganov, D. Zagier

- [1999] Ground State of the Quantum Symmetric Finite Size XXZ Spin Chain with Anisotropy Parameter
  - arxiv: `hep-th/9912252` (hep-th)
  - authors: V. Fridkin, Yu. Stroganov, D. Zagier

- [1996] Jacobi forms and the structure of Donaldson invariants for 4-manifolds with b_+=1
  - arxiv: `alg-geom/9612020` (math.AG)
  - authors: Lothar Göttsche, Don Zagier

- [1996] Higher Weil-Petersson Volumes of Moduli Spaces of Stable $n$-pointed Curves
  - arxiv: `alg-geom/9604001` (math.AG)
  - authors: R. Kaufmann, Yu. Manin, D. Zagier


## zhang-bin (en=Bin Zhang) — 15 candidates not in yaml

- [2022] Contrastive Learning of Coarse-Grained Force Fields
  - arxiv: `2205.10861` (physics.chem-ph)
  - authors: Xinqiang Ding, Bin Zhang

- [2020] Computing Absolute Free Energy with Deep Generative Models
  - arxiv: `2005.00638` (cond-mat.stat-mech)
  - authors: Xinqiang Ding, Bin Zhang

- [2015] Shape Transitions and Chiral Symmetry Breaking in the Energy Landscape of the Mitotic Chro
  - arxiv: `1511.03300` (physics.bio-ph)
  - authors: Bin Zhang, Peter G. Wolynes

- [2013] Work distribution of an expanding gas and transverse energy production in relativistic hea
  - arxiv: `1308.3748` (nucl-th)
  - authors: Bin Zhang, Jay P. Mayfield

- [2013] Structure controllability of complex network based on preferential matching
  - arxiv: `1307.2642` (math-ph)
  - authors: Xizhe Zhang, Tianyang Lv, Xueying Yang, Bin Zhang

- [2012] E-Characteristic Polynomials of Tensors
  - arxiv: `1208.1607` (math.SP)
  - authors: An-Min Li, Liqun Qi, Bin Zhang

- [2010] Spontaneous Symmetry Breaking during Formation of ZnO Nanocrystals
  - arxiv: `1012.5891` (cond-mat.mes-hall)
  - authors: Yan Zhou, Junyan Zhang, Jiangong Li, Bin Zhang

- [2006] Transition-Event Durations in One Dimensional Activated Processes
  - arxiv: `cond-mat/0609741` (cond-mat.stat-mech)
  - authors: Bin W. Zhang, David Jasnow, Daniel M. Zuckerman

- [2006] Renormalization of multiple zeta values
  - arxiv: `math/0606076` (math.NT)
  - authors: Li Guo, Bin Zhang

- [2006] A Stringy Product on Twisted Orbifold K-theory
  - arxiv: `math/0605534` (math.AT)
  - authors: Alejandro Adem, Yongbin Ruan, Bin Zhang

- [2003] Equivariant Todd Classes for Toric Varieties
  - arxiv: `math/0311318` (math.AG)
  - authors: Jean-Luc Brylinski, Bin Zhang

- [2003] K-twisted K-theory for SU(N)
  - arxiv: `math/0311298` (math.KT)
  - authors: Bin Zhang

- [2003] Equivariant gerbes over compact simple Lie groups
  - arxiv: `math/0306183` (math.SG)
  - authors: Kai Behrend, Ping Xu, Bin Zhang

- [1999] Equivariant Singular Riemann-Roch Theorem
  - arxiv: `math/9906152` (math.AG)
  - authors: Bin Zhang

- [1997] Equivariant K-Theory of Simply Connected Lie Groups
  - arxiv: `dg-ga/9710035` (math.DG)
  - authors: Jean-Luc Brylinski, Bin Zhang


## zhang-ning (en=Ning Zhang) — 17 candidates not in yaml

- [2025] A solution to Banach conjecture
  - arxiv: `2512.04628` (math.FA)
  - authors: Ning Zhang

- [2024] Spectral Clustering for Directed Graphs via Likelihood Estimation on Stochastic Block Mode
  - arxiv: `2403.19516` (stat.ML)
  - authors: Ning Zhang, Xiaowen Dong, Mihai Cucuringu

- [2019] Conditional variable screening via ordinary least squares projection
  - arxiv: `1910.11291` (math.ST)
  - authors: Ning Zhang, Wenxin Jiang, Yuting Lan

- [2018] Riemann-Hilbert method and soliton solutions in the system of two-component Hirota equatio
  - arxiv: `1809.07035` (math.AP)
  - authors: Fang Fang, Beibei Hu, Ling Zhang, Ning Zhang

- [2018] The Novel Symmetry Constraint and Binary Nonlinearization of the Super Generalized Broer-K
  - arxiv: `1810.08331` (math.AP)
  - authors: Beibei Hu, Fang Fang, Ning Zhang

- [2018] On the sure screening properties of iteratively sure independence screening algorithms
  - arxiv: `1812.01367` (math.ST)
  - authors: Ning Zhang, Wenxin Jiang, Yuting Lan

- [2018] Riemann-Hilbert approach for a mixed coupled nonlinear Schrödinger system and its soliton 
  - arxiv: `1809.09472` (math.AP)
  - authors: Fang Fang, Beibei Hu, Ling Zhang, Ning Zhang

- [2017] The $p$-capacitary Orlicz-Hadamard variational formula and Orlicz-Minkowski problems
  - arxiv: `1703.01458` (math.MG)
  - authors: Han Hong, Deping Ye, Ning Zhang

- [2017] Strong limit theorems for weighted sums of negatively associated random variables in nonli
  - arxiv: `1706.05788` (math.PR)
  - authors: Yuting Lan, Ning Zhang

- [2017] Convergence of ground state solutions for nonlinear Schrödinger equations on graphs
  - arxiv: `1705.03981` (math.AP)
  - authors: Ning Zhang, Liang Zhao

- [2017] A comparison theorem under sublinear expectations and related limit theorems
  - arxiv: `1710.01624` (math.PR)
  - authors: Ning Zhang, Yuting Lan

- [2015] Existence of solutions for a higher order Kirchhoff type problem with exponential critical
  - arxiv: `1507.05280` (math.AP)
  - authors: Liang Zhao, Ning Zhang

- [2013] Isocapacity Estimates for Hessian Operators
  - arxiv: `1305.0721` (math.FA)
  - authors: Jie Xiao, Ning Zhang

- [2012] Limiting Weak Type Estimate for Capacitary Maximal Function
  - arxiv: `1211.5076` (math.FA)
  - authors: Jie Xiao, Ning Zhang

- [2006] The Picard group of the loop space of the Riemann sphere
  - arxiv: `math/0602667` (math.CV)
  - authors: Ning Zhang

- [2004] Dolbeault cohomology of a loop space
  - arxiv: `math/0403405` (math.CV)
  - authors: Laszlo Lempert, Ning Zhang

- [2002] Holomorphic line bundles on the loop space of the Riemann sphere
  - arxiv: `math/0210017` (math.CV)
  - authors: Ning Zhang


## zhang-qing (en=Qing Zhang) — 4 candidates not in yaml

- [2025] Doping-induced Polyamorphic Transitions in Fluorite Oxides
  - arxiv: `2506.18333` (cond-mat.mtrl-sci)
  - authors: Hao Yang, Qiaotong Luan, Qing Zhang, Yuhao Yue, Yawen Xu

- [2023] Optimal Strategies for Round-Trip Pairs Trading Under Geometric Brownian Motions
  - arxiv: `2310.15803` (math.OC)
  - authors: Emily Crawford Das, Jingzhi Tie, Qing Zhang

- [2017] A local converse theorem for $\textrm{Sp}_{2r}$
  - arxiv: `1705.01692` (math.RT)
  - authors: Qing Zhang

- [2013] Weak Convergence Methods for Approximation of Path-dependent Functionals
  - arxiv: `1302.4278` (math.PR)
  - authors: Qingshuo Song, George Yin, Qing Zhang


## zhang-wei (en=Wei Zhang) — 118 candidates not in yaml

- [2026] Arithmetic volumes of moduli stacks of Shtukas
  - arxiv: `2601.18557` (math.NT)
  - authors: Tony Feng, Zhiwei Yun, Wei Zhang

- [2026] Helicoidal surfaces of non-lightlike frontals in Lorentz-Minkowski 3-space
  - arxiv: `2604.03268` (math.DG)
  - authors: Kaixin Yao, Wei Zhang

- [2025] More regular formal moduli spaces and arithmetic transfer conjectures: the ramified quadra
  - arxiv: `2507.01395` (math.NT)
  - authors: Yu Luo, Michael Rapoport, Wei Zhang

- [2025] Unitary Friedberg-Jacquet periods and their twists: Fundamental lemmas
  - arxiv: `2503.09500` (math.NT)
  - authors: Spencer Leslie, Jingwei Xiao, Wei Zhang

- [2025] Unitary Friedberg-Jacquet periods and their twists: Relative trace formulas
  - arxiv: `2503.09664` (math.NT)
  - authors: Spencer Leslie, Jingwei Xiao, Wei Zhang

- [2025] Survey on bounding Selmer groups for Rankin--Selberg motives
  - arxiv: `2509.16881` (math.NT)
  - authors: Yifeng Liu, Yichao Tian, Liang Xiao, Wei Zhang, Xinwen Zhu

- [2025] Higher derivative corrections to Kerr-AdS black hole thermodynamics
  - arxiv: `2504.21724` (hep-th)
  - authors: Wei Guo, Xiyao Guo, Xin Lan, Hongbao Zhang, Wei Zhang

- [2025] Finite-Time Splash in Free Boundary Problem of 3D Neo-Hookean Elastodynamics
  - arxiv: `2508.08751` (math.AP)
  - authors: Wei Zhang, Jie Fu, Chengchun Hao

- [2025] Black hole thermodynamics is around the corner
  - arxiv: `2510.04499` (hep-th)
  - authors: Gerui Chen, Wei Guo, Xin Lan, Hongbao Zhang, Wei Zhang

- [2025] Power convexity of solutions to complex Monge-Ampère equation in $\mathbb{C}^2$
  - arxiv: `2505.11002` (math.AP)
  - authors: Wei Zhang, Qi Zhou

- [2025] Background subtraction method is not only much simpler, but also as applicable as covarian
  - arxiv: `2501.08214` (hep-th)
  - authors: Wei Guo, Xiyao Guo, Xin Lan, Hongbao Zhang, Wei Zhang

- [2025] Distance spectral radius for a graph to be k-critical with respect to [1,b]-odd factor
  - arxiv: `2511.17679` (math.CO)
  - authors: Sufang Wang, Wei Zhang

- [2025] A Liouville theorem for the $2$-Hessian equation on the Heisenberg group
  - arxiv: `2509.08415` (math.AP)
  - authors: Wei Zhang, Qi Zhou

- [2025] The log-concavity of eigenfunction to complex Monge-Ampère operator in $\mathbb{C}^2$
  - arxiv: `2505.12817` (math.AP)
  - authors: Wei Zhang, Qi Zhou

- [2025] Quadratic curvature corrections to 5-dimensional Kerr-AdS black hole thermodynamics by bac
  - arxiv: `2508.18171` (hep-th)
  - authors: Gerui Chen, Xiyao Guo, Xin Lan, Hongbao Zhang, Wei Zhang

- [2025] Phase transitions and crtical exponents in the six-vertex model on kagome lattices
  - arxiv: `2506.00804` (cond-mat.stat-mech)
  - authors: Wei Zhang, Wanzhou Zhang, Jie Zhang, Chengxiang Ding, Youjin Deng

- [2025] Distributional Control of Ensemble Systems
  - arxiv: `2504.04570` (math.OC)
  - authors: Jr-Shin Li, Wei Zhang

- [2024] Quasi-canonical AFL and Arithmetic Transfer conjectures at parahoric levels
  - arxiv: `2404.02214` (math.NT)
  - authors: Chao Li, Michael Rapoport, Wei Zhang

- [2024] High dimensional Gross--Zagier formula: a survey
  - arxiv: `2402.17656` (math.NT)
  - authors: Wei Zhang

- [2024] Gan--Gross--Prasad cycles and derivatives of $p$-adic $L$-functions
  - arxiv: `2410.08401` (math.NT)
  - authors: Daniel Disegni, Wei Zhang

- [2024] Toughness and spectral radius in graphs
  - arxiv: `2406.08224` (math.CO)
  - authors: Sufang Wang, Wei Zhang

- [2024] Global well-posedness of the free boundary problem for incompressible viscous resistive MH
  - arxiv: `2408.15279` (math.AP)
  - authors: Wei Zhang, Jie Fu, Chengchun Hao, Siqi Yang

- [2024] Spanning trees and signless Laplacian spectral radius in graphs
  - arxiv: `2406.07132` (math.CO)
  - authors: Sufang Wang, Wei Zhang

- [2024] Gaussian Approximations for the $k$th coordinate of sums of random vectors
  - arxiv: `2408.03039` (math.ST)
  - authors: Yixi Ding, Qizhai Li, Yuke Shi, Wei Zhang

- [2023] Arithmetic Fundamental Lemma for the spherical Hecke algebra
  - arxiv: `2305.14465` (math.NT)
  - authors: Chao Li, Michael Rapoport, Wei Zhang

- [2023] Vanishing results for the modified diagonal cycles II: Shimura curves
  - arxiv: `2310.19707` (math.AG)
  - authors: Congling Qiu, Wei Zhang

- [2023] Modularity of higher theta series I: cohomology of the generic fiber
  - arxiv: `2308.10979` (math.NT)
  - authors: Tony Feng, Zhiwei Yun, Wei Zhang

- [2023] Analyzing multimodal probability measures with autoencoders
  - arxiv: `2310.03492` (physics.chem-ph)
  - authors: Tony Lelièvre, Thomas Pigeon, Gabriel Stoltz, Wei Zhang

- [2023] A note on simple zeros related to Dedekind zeta functions
  - arxiv: `2310.07360` (math.NT)
  - authors: Wei Zhang

- [2023] On a variant of the prime number theorem
  - arxiv: `2303.12347` (math.NT)
  - authors: Wei Zhang

- [2023] On general divisor functions over Piatetski-Shapiro sequences
  - arxiv: `2304.10119` (math.NT)
  - authors: Wei Zhang

- [2023] EPR-Net: Constructing non-equilibrium potential landscape via a variational force projecti
  - arxiv: `2301.01946` (physics.bio-ph)
  - authors: Yue Zhao, Wei Zhang, Tiejun Li

- [2022] Twisted linear periods and a new relative trace formula
  - arxiv: `2209.08366` (math.NT)
  - authors: Hang Xue, Wei Zhang

- [2022] Vanishing results in Chow groups for the modified diagonal cycles
  - arxiv: `2209.09736` (math.AG)
  - authors: Congling Qiu, Wei Zhang

- [2022] On an exponential sum related to the Möbius function
  - arxiv: `2204.04613` (math.NT)
  - authors: Wei Zhang

- [2022] Averages of exponential twists of the von Mangoldt function
  - arxiv: `2203.12168` (math.NT)
  - authors: Xiumin Ren, Wei Zhang

- [2022] On $k$-free numbers over Beatty sequences
  - arxiv: `2210.16828` (math.NT)
  - authors: Wei Zhang

- [2022] On fractional sums of the divisor functions
  - arxiv: `2207.00923` (math.NT)
  - authors: Wei Zhang

- [2022] On squares associated to the Piatetski-Shapiro sequences
  - arxiv: `2212.05274` (math.NT)
  - authors: Wei Zhang

- [2022] Controllability Canonical Forms of Linear Ensemble Systems
  - arxiv: `2211.02975` (math.OC)
  - authors: Wei Zhang, Jr-Shin Li

- [2022] Koopman Bilinearization of Nonlinear Control Systems
  - arxiv: `2211.07112` (math.OC)
  - authors: Wei Zhang, Jr-Shin Li

- [2022] On primes in special sequences with applications to Carmichael numbers
  - arxiv: `2207.02378` (math.NT)
  - authors: Wei Zhang

- [2022] On sums of $k$-th powers with almost equal primes
  - arxiv: `2204.07715` (math.NT)
  - authors: Wei Zhang

- [2022] On density of the zeros of Dedekind zeta-functions
  - arxiv: `2203.08384` (math.NT)
  - authors: Wei Zhang

- [2021] On the arithmetic Siegel--Weil formula for GSpin Shimura varieties
  - arxiv: `2106.15038` (math.NT)
  - authors: Chao Li, Wei Zhang

- [2021] Higher Siegel--Weil formula for unitary groups: the non-singular terms
  - arxiv: `2103.11514` (math.NT)
  - authors: Tony Feng, Zhiwei Yun, Wei Zhang

- [2021] More Arithmetic Fundamental Lemma conjectures: the case of Bessel subgroups
  - arxiv: `2108.02086` (math.NT)
  - authors: Wei Zhang

- [2021] A note on Tate's conjectures for abelian varieties
  - arxiv: `2112.15164` (math.NT)
  - authors: Chao Li, Wei Zhang

- [2021] Higher theta series for unitary groups over function fields
  - arxiv: `2110.07001` (math.NT)
  - authors: Tony Feng, Zhiwei Yun, Wei Zhang

- [2021] On general sums involving the floor function with applications to $k$-free numbers
  - arxiv: `2112.06156` (math.NT)
  - authors: Wei Zhang

- [2021] On the Arithmetic Fundamental Lemma conjecture over a general $p$-adic field
  - arxiv: `2104.02779` (math.NT)
  - authors: Andreas Mihatsch, Wei Zhang

- [2021] Deformation of rigid conjugate self-dual Galois representations
  - arxiv: `2108.06998` (math.NT)
  - authors: Yifeng Liu, Yichao Tian, Liang Xiao, Wei Zhang, Xinwen Zhu

- [2021] Distance-based regression analysis for measuring associations
  - arxiv: `2105.10145` (math.ST)
  - authors: Yuke Shi, Wei Zhang, Aiyi Liu, Qizhai Li

- [2021] The Cauchy Combination Test under Arbitrary Dependence Structures
  - arxiv: `2107.06040` (stat.ME)
  - authors: Mingya Long, Zhengbang Li, Wei Zhang, Qizhai Li

- [2020] Some new results on relative entropy production, time reversal, and optimal control of tim
  - arxiv: `2006.11212` (math.PR)
  - authors: Wei Zhang

- [2020] Non-reversible sampling schemes on submanifolds
  - arxiv: `2011.02835` (math.NA)
  - authors: Upanshu Sharma, Wei Zhang

- [2020] Ensemble Control on Lie Groups
  - arxiv: `2008.03243` (math.OC)
  - authors: Jr-Shin Li, Wei Zhang

- [2019] Kudla--Rapoport cycles and derivatives of local densities
  - arxiv: `1908.01701` (math.NT)
  - authors: Chao Li, Wei Zhang

- [2019] Weil representation and Arithmetic Fundamental Lemma
  - arxiv: `1909.02697` (math.NT)
  - authors: Wei Zhang

- [2019] On Shimura varieties for unitary groups
  - arxiv: `1906.12346` (math.NT)
  - authors: Michael Rapoport, Brian Smithling, Wei Zhang

- [2019] On the Beilinson-Bloch-Kato conjecture for Rankin-Selberg motives
  - arxiv: `1912.11942` (math.NT)
  - authors: Yifeng Liu, Yichao Tian, Liang Xiao, Wei Zhang, Xinwen Zhu

- [2019] Isolation of cuspidal spectrum, with application to the Gan--Gross--Prasad conjecture
  - arxiv: `1912.07169` (math.NT)
  - authors: Raphaël Beuzart-Plessis, Yifeng Liu, Wei Zhang, Xinwen Zhu

- [2019] Flat-band Ferromagnetism of the SU$(N)$ Hubbard Model on the Tasaki Lattice
  - arxiv: `1901.07004` (cond-mat.str-el)
  - authors: Rui-Jin Liu, Wenxing Nie, Wei Zhang

- [2018] Pathwise estimates for effective dynamics: the case of nonlinear vectorial reaction coordi
  - arxiv: `1805.01928` (math.PR)
  - authors: Tony Lelièvre, Wei Zhang

- [2018] Jarzynski's equality, fluctuation theorems, and variance reduction: Mathematical analysis 
  - arxiv: `1803.09347` (math-ph)
  - authors: Carsten Hartmann, Christof Schuette, Wei Zhang

- [2018] Moderate deviation and central limit theorem for SDDEs with plynomial growth
  - arxiv: `1806.11003` (math.PR)
  - authors: Yongqiang Suo, Jin Tao, Wei Zhang

- [2018] Pseudo-Harmonic Maps From Complete Noncompact Pseudo-Hermitian Manifolds To Regular Balls
  - arxiv: `1802.08034` (math.DG)
  - authors: Tian Chong, Yuxin Dong, Yibin Ren, Zhang Wei

- [2017] Arithmetic diagonal cycles on unitary Shimura varieties
  - arxiv: `1710.06962` (math.NT)
  - authors: Michael Rapoport, Brian Smithling, Wei Zhang

- [2017] Statistical analysis of the first passage path ensemble of jump processes
  - arxiv: `1701.04270` (math.PR)
  - authors: Max von Kleist, Christof Schütte, Wei Zhang

- [2017] Periods, cycles, and $L$-functions: a relative trace formula approach
  - arxiv: `1712.08844` (math.NT)
  - authors: Wei Zhang

- [2017] Ergodic SDEs on submanifolds and related numerical sampling schemes
  - arxiv: `1702.08064` (math.PR)
  - authors: Wei Zhang

- [2017] Shtukas and the Taylor expansion of $L$-functions (II)
  - arxiv: `1712.08026` (math.NT)
  - authors: Zhiwei Yun, Wei Zhang

- [2017] Multi-window dilation-and-modulation frames on the half real line
  - arxiv: `1708.05941` (math.FA)
  - authors: Yun-Zhang Li, Wei Zhang

- [2016] Regular formal moduli spaces and arithmetic transfer conjectures
  - arxiv: `1604.02419` (math.NT)
  - authors: Michael Rapoport, Brian Smithling, Wei Zhang

- [2016] Liouville Theorems for critical points of the p-Ginzburg-Landau type functional
  - arxiv: `1610.06301` (math.DG)
  - authors: Tian Chong, Bofeng Cheng, Yuxin Dong, Wei Zhang

- [2016] Ferromagnetic ground state of SU(3) Hubbard model on the Lieb lattice
  - arxiv: `1607.08618` (cond-mat.str-el)
  - authors: Wenxing Nie, Deping Zhang, Wei Zhang

- [2016] Comparison theorems in pseudo-Hermitian geometry and applications
  - arxiv: `1611.00539` (math.DG)
  - authors: Yuxin Dong, Wei Zhang

- [2015] On the arithmetic transfer conjecture for exotic smooth formal moduli spaces
  - arxiv: `1503.06520` (math.NT)
  - authors: Michael Rapoport, Brian Smithling, Wei Zhang

- [2015] Shtukas and the Taylor expansion of $L$-functions
  - arxiv: `1512.02683` (math.NT)
  - authors: Zhiwei Yun, Wei Zhang

- [2015] Asymptotic Analysis of Multiscale Markov Chain
  - arxiv: `1512.08944` (math.PR)
  - authors: Wei Zhang

- [2015] Importance sampling in path space for diffusion processes with slow-fast variables
  - arxiv: `1502.07899` (math.PR)
  - authors: Carsten Hartmann, Christof Schütte, Marcus Weber, Wei Zhang

- [2015] On $p$-adic Waldspurger formula
  - arxiv: `1511.08172` (math.NT)
  - authors: Yifeng Liu, Shouwu Zhang, Wei Zhang

- [2015] A Unified Stochastic Hybrid System Approach to Aggregate Modeling of Responsive Loads
  - arxiv: `1503.06911` (eess.SY)
  - authors: Lin Zhao, Wei Zhang

- [2015] Zhu's Algebra of a C1-cofinite Vertex Algebra
  - arxiv: `1508.06351` (math.QA)
  - authors: Lu Ding, Wei Jiang, Wei Zhang

- [2014] Tracial state space with non-compact extreme boundary
  - arxiv: `1403.6788` (math.OA)
  - authors: Wei Zhang

- [2014] Indivisibility of Heegner points in the multiplicative case
  - arxiv: `1407.1099` (math.NT)
  - authors: Christopher Skinner, Wei Zhang

- [2014] A majority of elliptic curves over $\mathbb Q$ satisfy the Birch and Swinnerton-Dyer conje
  - arxiv: `1407.1826` (math.NT)
  - authors: Manjul Bhargava, Christopher Skinner, Wei Zhang

- [2013] The Petrov-like boundary condition at finite cutoff surface in Gravity/Fluid duality
  - arxiv: `1306.5633` (gr-qc)
  - authors: Yi Ling, Chao Niu, Yu Tian, Xiao-Ning Wu, Wei Zhang

- [2013] Bond and Site Percolation in Three Dimensions
  - arxiv: `1302.0421` (cond-mat.stat-mech)
  - authors: Junfeng Wang, Zongzheng Zhou, Wei Zhang, Timothy M. Garoni, Youjin Deng

- [2012] On the Arithmetic Fundamental Lemma in the minuscule case
  - arxiv: `1203.5827` (math.NT)
  - authors: Michael Rapoport, Ulrich Terstiege, Wei Zhang

- [2012] Convergence of Yang-Mills-Higgs flow for twist Higgs pairs on Riemann surfaces
  - arxiv: `1209.3907` (math.DG)
  - authors: Wei Zhang

- [2012] Automorphic period and the central value of Rankin--Selberg L-function
  - arxiv: `1208.6280` (math.NT)
  - authors: Wei Zhang

- [2012] Skew $N$-Derivations on Semiprime Rings
  - arxiv: `1206.3396` (math.RA)
  - authors: Xiaowei Xu, Yang Liu, Wei Zhang

- [2011] Cotangent bundles of toric varieties and coverings of toric hyperkähler manifolds
  - arxiv: `1101.5050` (math.DG)
  - authors: Craig van Coevering, Wei Zhang

- [2011] Holomorphic Lagrangian fibrations of toric hyperkahler manifolds
  - arxiv: `1110.0269` (math.DG)
  - authors: Craig van Coevering, Wei Zhang

- [2010] Fibred toric varieties in toric hyperkähler varieties
  - arxiv: `1012.2427` (math.AG)
  - authors: Craig van Coevering, Wei Zhang

- [2010] Convexity of the smallest principal curvature of the convex level sets of some quasi-linea
  - arxiv: `1005.1515` (math.AP)
  - authors: Kun Huang, Wei Zhang

- [2010] Gaussian Curvature estimates for the convex level sets of solutions for some nonlinear ell
  - arxiv: `1003.2057` (math.AP)
  - authors: Pei-He Wang, Wei Zhang

- [2009] Some geometric critical exponents for percolation and the random-cluster model
  - arxiv: `0904.3448` (cond-mat.stat-mech)
  - authors: Youjin Deng, Wei Zhang, Timothy M. Garoni, Alan D. Sokal, Andrea Sportiello

- [2009] Tomography of correlation functions for ultracold atoms via time-of-flight images
  - arxiv: `0906.0250` (cond-mat.quant-gas)
  - authors: Wei Zhang, L. -M. Duan

- [2008] Biharmonic space-like hypersurfaces in pseudo-Riemannian space
  - arxiv: `0808.1346` (math.DG)
  - authors: Wei Zhang

- [2008] Characteristics of Bose-Einstein condensation in an optical lattice
  - arxiv: `0802.0700` (cond-mat.supr-con)
  - authors: G. -D. Lin, Wei Zhang, L. -M. Duan

- [2008] Rational vertex operator algebras are finitely generated
  - arxiv: `0806.2346` (math.QA)
  - authors: Chongying Dong, Wei Zhang

- [2008] Binomial coefficients and the ring of p-adic integers
  - arxiv: `0812.3089` (math.NT)
  - authors: Zhi-Wei Sun, Wei Zhang

- [2008] A worm algorithm for the fully-packed loop model
  - arxiv: `0811.2042` (cond-mat.stat-mech)
  - authors: Wei Zhang, Timothy M. Garoni, Youjin Deng

- [2008] On the integers of the form $p^2+b^2+2^n$ and $b_1^2+b_2^2+2^{n^2}$
  - arxiv: `0812.1259` (math.NT)
  - authors: Hao Pan, Wei Zhang

- [2008] A Monte Carlo study of the triangular lattice gas with the first- and the second-neighbor 
  - arxiv: `0803.3334` (cond-mat.stat-mech)
  - authors: Wei Zhang, Youjin Deng

- [2007] On the Gauss Map with Vanishing Biharmonic stress-energy tensor
  - arxiv: `0709.3355` (math.DG)
  - authors: Wei Zhang

- [2007] Bernstein Type Results for Lagrangian Graphs with Partially Harmonic Gauss Map
  - arxiv: `0707.0183` (math.DG)
  - authors: Wei Zhang

- [2007] New Examples of Biharmonic Submanifolds in $CP^n$ and $S^{2n+1}$
  - arxiv: `0705.3961` (math.DG)
  - authors: Wei Zhang

- [2006] Logistic regression with unknown sizes
  - arxiv: `math/0609579` (math.ST)
  - authors: Wei Zhang

- [2006] Semiparametric logistic regression with unknown sizes, and its application to bioassays
  - arxiv: `math/0609582` (math.ST)
  - authors: Wei Zhang

- [2006] Double-mixing semiparametric logistic regression with unknown sizes
  - arxiv: `math/0609581` (math.ST)
  - authors: Wei Zhang

- [2005] Vortices and Dissipation in a Bilayer Thin Film Superconductor
  - arxiv: `cond-mat/0502402` (cond-mat.supr-con)
  - authors: Wei Zhang, H. A. Fertig

- [2003] Diffusion Entropy Approach to Dynamical Characteristics of a Hodgkin-Huxley Neuron
  - arxiv: `q-bio/0312004` (q-bio.NC)
  - authors: Huijie Yang, Fangcui Zhao, Zhongnan Li, Wei Zhang

- [1998] On Schwarzschild Black Hole in Large N Matrix theory
  - arxiv: `hep-th/9806242` (hep-th)
  - authors: Yi-hong Gao, Wei Zhang

- [1998] Evaporation of Schwarzschild Black Hole in the Large N Matrix Theory
  - arxiv: `hep-th/9806245` (hep-th)
  - authors: Yi-hong Gao, Wei Zhang

- [1998] On Torsion and Nieh-Yan Form
  - arxiv: `hep-th/9805037` (hep-th)
  - authors: Han-Ying Guo, Ke Wu, Wei Zhang


## zhang-xuhui (en=Xuhui Zhang) — 5 candidates not in yaml

- [2024] Electric Field Induced Associations in the Double Layer of Salt-in-Ionic-Liquid Electrolyt
  - arxiv: `2402.04039` (physics.chem-ph)
  - authors: Daniel M. Markiewitz, Zachary A. H. Goodwin, Michael McEldrew, J. Pedro de Souza, Xuhui Zhang

- [2023] Wasserstein-based Minimax Estimation of Dependence in Multivariate Regularly Varying Extre
  - arxiv: `2312.09862` (math.ST)
  - authors: Xuhui Zhang, Jose Blanchet, Youssef Marzouk, Viet Anh Nguyen, Sven Wang

- [2022] Distributionally Robust Gaussian Process Regression and Bayesian Inverse Problems
  - arxiv: `2205.13111` (math.OC)
  - authors: Xuhui Zhang, Jose Blanchet, Youssef Marzouk, Viet Anh Nguyen, Sven Wang

- [2020] Minimax Efficient Finite-Difference Stochastic Gradient Estimators Using Black-Box Functio
  - arxiv: `2007.04443` (math.ST)
  - authors: Henry Lam, Haidong Li, Xuhui Zhang

- [2020] Distributionally Robust Parametric Maximum Likelihood Estimation
  - arxiv: `2010.05321` (stat.ML)
  - authors: Viet Anh Nguyen, Xuhui Zhang, Jose Blanchet, Angelos Georghiou


## zhang-youjin (en=Youjin Zhang) — 13 candidates not in yaml

- [2005] Bihamiltonian Systems of Hydrodynamic Type and Reciprocal Transformations
  - arxiv: `math/0510250` (math.DG)
  - authors: Ting Xue, Youjin Zhang

- [2005] A 2-Component Generalization of the Camassa-Holm Equation and Its Solutions
  - arxiv: `nlin/0501028` (nlin.SI)
  - authors: Ming Chen, Si-Qi Liu, Youjin Zhang

- [2005] On Quasitriviality and Integrability of a Class of Scalar Evolutionary PDEs
  - arxiv: `nlin/0510019` (nlin.SI)
  - authors: Si-Qi Liu, Youjin Zhang

- [2005] Extended affine Weyl groups and Frobenius manifolds -- II
  - arxiv: `math/0502365` (math.DG)
  - authors: Boris Dubrovin, Youjin Zhang, Dafeng Zuo

- [2004] On the Quasitriviality of Deformations of Bihamiltonian Structures of Hydrodynamic Type
  - arxiv: `math/0406626` (math.DG)
  - authors: Si-Qi Liu, Youjin Zhang

- [2004] Deformations of Semisimple Bihamiltonian Structures of Hydrodynamic Type
  - arxiv: `math/0405146` (math.DG)
  - authors: Si-Qi Liu, Youjin Zhang

- [2004] On Hamiltonian perturbations of hyperbolic systems of conservation laws
  - arxiv: `math/0410027` (math.DG)
  - authors: Boris Dubrovin, Si-Qi Liu, Youjin Zhang

- [2003] The Extended Toda Hierarchy
  - arxiv: `nlin/0306060` (nlin.SI)
  - authors: Guido Carlet, Boris Dubrovin, Youjin Zhang

- [2003] Virasoro Symmetries of the Extended Toda Hierarchy
  - arxiv: `math/0308152` (math.DG)
  - authors: Boris Dubrovin, Youjin Zhang

- [2001] Normal forms of hierarchies of integrable PDEs, Frobenius manifolds and Gromov - Witten in
  - arxiv: `math/0108160` (math.DG)
  - authors: Boris Dubrovin, Youjin Zhang

- [1998] Frobenius Manifolds And Virasoro Constraints
  - arxiv: `math/9808048` (math.AG)
  - authors: Boris Dubrovin, Youjin Zhang

- [1997] Bihamiltonian Hierarchies in 2D Topological Field Theory At One-Loop Approximation
  - arxiv: `hep-th/9712232` (hep-th)
  - authors: Boris Dubrovin, Youjin Zhang

- [1996] Extended affine Weyl groups and Frobenius manifolds
  - arxiv: `hep-th/9611200` (hep-th)
  - authors: Boris Dubrovin, Youjin Zhang


## zhou-chunhui (en=Chunhui Zhou) — 5 candidates not in yaml

- [2025] Structure stability of steady supersonic shear flow with inflow boundary conditions
  - arxiv: `2503.10001` (math.AP)
  - authors: Song Jiang, Chunhui Zhou

- [2024] Zero Viscosity Limit of Steady Compressible Shear Flow with Navier-Slip Boundary
  - arxiv: `2406.04700` (math.AP)
  - authors: Wenbin Li, Chunhui Zhou

- [2022] Stability and related zero viscosity limit of steady plane Poiseuille-Couette flows with n
  - arxiv: `2210.15389` (math.AP)
  - authors: Song Jiang, Chunhui Zhou

- [2017] Stationary Inviscid Limit to Shear Flows
  - arxiv: `1711.05664` (math.AP)
  - authors: Sameer Iyer, Chunhui Zhou

- [2011] On the existence of weak solutions to the three-dimensional steady compressible Navier-Sto
  - arxiv: `1107.5701` (math.AP)
  - authors: Song Jiang, Chunhui Zhou


## zhou-jian (en=Jian Zhou) — 88 candidates not in yaml

- [2026] Cusp Form Dimensions, Lattice Uniqueness, and LP Sharpness for Sphere Packing in Dimension
  - arxiv: `2604.10914` (math.CO)
  - authors: Jian Zhou

- [2024] On Phase Transition of Two-Dimensional Topological Gravity
  - arxiv: `2401.02085` (hep-th)
  - authors: Jian Zhou

- [2024] Existence of solutions for a class of Kirchhoff-type equations with indefinite potential
  - arxiv: `2403.19284` (math.AP)
  - authors: Linlian Xiao, Jiaqian Yuan, Jian Zhou, Yunshun Wu

- [2021] On Some Mathematics Related to the Interpolating Statistics
  - arxiv: `2108.10514` (math-ph)
  - authors: Jian Zhou

- [2020] On Emergent Geometry of the Gromov-Witten Theory of Quintic Calabi-Yau Threefold
  - arxiv: `2008.03407` (math-ph)
  - authors: Jian Zhou

- [2020] Virasoro Constraints of Curves as Residues
  - arxiv: `2009.00882` (math-ph)
  - authors: Jian Zhou

- [2019] Grothendieck's Dessins d'Enfants in a Web of Dualities
  - arxiv: `1905.10773` (math-ph)
  - authors: Jian Zhou

- [2019] Emergent Geometry of Matrix Models with Even Couplings
  - arxiv: `1903.10767` (math-ph)
  - authors: Jian Zhou

- [2019] Grothendieck's Dessins d'Enfants in a Web of Dualities. II
  - arxiv: `1907.00357` (math-ph)
  - authors: Jian Zhou

- [2018] Hessian Geometry and Phase Change of Gibbons-Hawking Metrics
  - arxiv: `1801.02755` (math.DG)
  - authors: Jian Zhou

- [2018] K-Theory of Hilbert Schemes as a Formal Quantum Field Theory
  - arxiv: `1803.06080` (math.AG)
  - authors: Jian Zhou

- [2018] Hessian Geometry and Phase Changes of Multi-Taub-NUT Metrics
  - arxiv: `1801.06631` (math.DG)
  - authors: Jian Zhou

- [2018] On Quasimodularity of Some Equivariant Intersection Numbers on the Hilbert Schemes
  - arxiv: `1801.09090` (math.AG)
  - authors: Jian Zhou

- [2018] Hermitian One-Matrix Model and KP Hierarchy
  - arxiv: `1809.07951` (math-ph)
  - authors: Jian Zhou

- [2018] Fat and Thin Emergent Geometries of Hermitian One-Matrix Models
  - arxiv: `1810.03883` (math-ph)
  - authors: Jian Zhou

- [2018] Genus Expansions of Hermitian One-Matrix Models: Fat Graphs vs. Thin Graphs
  - arxiv: `1809.10870` (math-ph)
  - authors: Jian Zhou

- [2018] Noether's problem for some subgroups of $S_{14}$: the modular case
  - arxiv: `1805.05678` (math.AG)
  - authors: Hang Fu, Ming-chang Kang, Baoshan Wang, Jian Zhou

- [2018] Standing waves for quasilinear Schröinger equations with indefinite potentials
  - arxiv: `1801.01976` (math.AP)
  - authors: Shibo Liu, Jian Zhou

- [2017] On Geometry and Symmetry of Kepler Systems. I
  - arxiv: `1708.05504` (math-ph)
  - authors: Jian Zhou

- [2017] Noether's Problem for Some Semidirect Products
  - arxiv: `1703.01010` (math.NT)
  - authors: Ming-chang Kang, Jian Zhou

- [2016] Information Theory and Statistical Mechanics Revisited
  - arxiv: `1604.08739` (math-ph)
  - authors: Jian Zhou

- [2015] Frobenius Manifolds, Spectral Curves, and Integrable Hierarchies
  - arxiv: `1512.05466` (math-ph)
  - authors: Jian Zhou

- [2015] On Equivariant Elliptic Genera of Toric Calabi-Yau 3-folds
  - arxiv: `1510.08528` (math.AG)
  - authors: Jian Zhou

- [2015] Emergent Geometry and Mirror Symmetry of A Point
  - arxiv: `1507.01679` (math-ph)
  - authors: Jian Zhou

- [2015] On a Mean Field Theory of Topological 2D Gravity
  - arxiv: `1503.08546` (math.AG)
  - authors: Jian Zhou

- [2015] Emergent Geometry of KP Hierarchy. II
  - arxiv: `1512.03196` (math-ph)
  - authors: Jian Zhou

- [2015] Fermionic Computations for Integrable Hierarchies
  - arxiv: `1508.01999` (math-ph)
  - authors: Jian Zhou

- [2015] On Regularized Elliptic Genera of ALE Spaces
  - arxiv: `1511.01191` (math-ph)
  - authors: Jian Zhou

- [2015] Emergent Geometry of KP Hierarchy
  - arxiv: `1511.08257` (math-ph)
  - authors: Jian Zhou

- [2014] Quantum Deformation Theory of the Airy Curve and Mirror Symmetry of a Point
  - arxiv: `1405.5296` (math.AG)
  - authors: Jian Zhou

- [2014] On Topological 1D Gravity. I
  - arxiv: `1412.1604` (math-ph)
  - authors: Jian Zhou

- [2014] Rationality problem for transitive subgroups of S_8
  - arxiv: `1402.1675` (math.AG)
  - authors: Baoshan Wang, Jian Zhou

- [2014] Quantum McKay correspondence for disc invariants of orbifold vertex
  - arxiv: `1410.4374` (math-ph)
  - authors: Hua-Zhong Ke, Jian Zhou

- [2014] Quantum McKay correspondence for disc invariants of toric Calabi-Yau 3-orbifolds
  - arxiv: `1410.4376` (math-ph)
  - authors: Hua-Zhong Ke, Jian Zhou

- [2013] Solution of W-Constraints for R-Spin Intersection Numbers
  - arxiv: `1305.6991` (math-ph)
  - authors: Jian Zhou

- [2013] Explicit Formula for Witten-Kontsevich Tau-Function
  - arxiv: `1306.5429` (math.AG)
  - authors: Jian Zhou

- [2013] Rationality for subgroups of S_6
  - arxiv: `1308.0409` (math.AG)
  - authors: Jian Zhou

- [2013] Invariants of wreath products and subgroups of S_6
  - arxiv: `1308.0885` (math.AG)
  - authors: Ming-chang Kang, Baoshan Wang, Jian Zhou

- [2012] Quantum Mirror Curves for ${\mathbb C}^3$ and the Resolved Confiold
  - arxiv: `1207.0598` (math.AG)
  - authors: Jian Zhou

- [2012] Intersection numbers on Deligne-Mumford moduli spaces and quantum Airy curve
  - arxiv: `1206.5896` (math.AG)
  - authors: Jian Zhou

- [2012] On fermionic representation of the Gromov-Witten invariants of the resolved Conifold
  - arxiv: `1201.2500` (math.AG)
  - authors: Fusheng Deng, Jian Zhou

- [2012] Fermionic gluing principle of the topological vertex
  - arxiv: `1204.5067` (math.AG)
  - authors: Fusheng Deng, Jian Zhou

- [2011] On fermionic representation of the framed topological vertex
  - arxiv: `1111.0415` (math.AG)
  - authors: Fusheng Deng, Jian Zhou

- [2011] Noether's problem for the groups with a cyclic subgroup of index 4
  - arxiv: `1108.3379` (math.AC)
  - authors: Ming-chang Kang, Ivo M. Michailov, Jian Zhou

- [2010] Some integrality properties in local mirror symmetry
  - arxiv: `1005.3243` (math.AG)
  - authors: Jian Zhou

- [2010] Open String Invariants and Mirror Curve of the Resolved Conifold
  - arxiv: `1001.0447` (math.AG)
  - authors: Jian Zhou

- [2010] A Proof of the Full Marino-Vafa Conjecture
  - arxiv: `1001.2092` (math.AG)
  - authors: Jian Zhou

- [2010] Integrality Properties of Variations of Mahler Measures
  - arxiv: `1006.2428` (math.AG)
  - authors: Jian Zhou

- [2010] Integrality Properties of Open-Closed Mirror Maps
  - arxiv: `1006.5266` (math.AG)
  - authors: Jian Zhou

- [2010] Noether's problem for some 2-groups
  - arxiv: `1009.2299` (math.AG)
  - authors: Ming-chang Kang, Ivo M. Michailov, Jian Zhou

- [2010] Noether's problem for \hat{S}_4 and \hat{S}_5
  - arxiv: `1006.1158` (math.AG)
  - authors: Ming-chang Kang, Jian Zhou

- [2010] The rationality problem for finite subgroups of GL_4(Q)
  - arxiv: `1006.1156` (math.AG)
  - authors: Ming-chang Kang, Jian Zhou

- [2009] Local Mirror Symmetry for the Topological Vertex
  - arxiv: `0911.2343` (math.AG)
  - authors: Jian Zhou

- [2009] Crepant Resolutions, Quivers and GW/NCDT Duality
  - arxiv: `0907.0135` (math.AG)
  - authors: Jian Zhou

- [2009] Local Mirror Symmetry for One-Legged Topological Vertex
  - arxiv: `0910.4320` (math.AG)
  - authors: Jian Zhou

- [2008] Crepant resolution conjecture in all genera for type A singularities
  - arxiv: `0811.2023` (math.AG)
  - authors: Jian Zhou

- [2008] Arithmetic McKay correspondence
  - arxiv: `0812.4202` (math.AG)
  - authors: Jian Zhou

- [2007] On computations of Hurwitz-Hodge integrals
  - arxiv: `0710.1679` (math.AG)
  - authors: Jian Zhou

- [2005] On a deformed topological vertex
  - arxiv: `math/0504460` (math.AG)
  - authors: Jian Zhou

- [2004] Elliptic Genera of Complete Intersections
  - arxiv: `math/0411081` (math.AG)
  - authors: Xiaoguang Ma, Jian Zhou

- [2004] A Mathematical Theory of the Topological Vertex
  - arxiv: `math/0408426` (math.AG)
  - authors: Jun Li, Chiu-Chu Melissa Liu, Kefeng Liu, Jian Zhou

- [2004] Topological String Partition Functions as Equivariant Indices
  - arxiv: `math/0412089` (math.AG)
  - authors: Jun Li, Kefeng Liu, Jian Zhou

- [2004] $K$-theory associated to vertex operator algebras
  - arxiv: `math/0403547` (math.DG)
  - authors: Chongying Dong, Kefeng Liu, Xiaonan Ma, Jian Zhou

- [2003] A Conjecture on Hodge Integrals
  - arxiv: `math/0310282` (math.AG)
  - authors: Jian Zhou

- [2003] Localizations on Moduli Spaces and Free Field Realizations of Feynman Rules
  - arxiv: `math/0310283` (math.AG)
  - authors: Jian Zhou

- [2003] Curve counting and instanton counting
  - arxiv: `math/0311237` (math.AG)
  - authors: Jian Zhou

- [2003] Hodge integrals, Hurwitz numbers, and Symmetric Groups
  - arxiv: `math/0308024` (math.AG)
  - authors: Jian Zhou

- [2003] Hodge Integrals and Integrable Hierarchies
  - arxiv: `math/0310408` (math.AG)
  - authors: Jian Zhou

- [2003] Mariño-Vafa Formula and Hodge Integral Identities
  - arxiv: `math/0308015` (math.AG)
  - authors: Chiu-Chu Melissa Liu, Kefeng Liu, Jian Zhou

- [2003] A Formula of Two-Partition Hodge Integrals
  - arxiv: `math/0310272` (math.AG)
  - authors: Chiu-Chu Melissa Liu, Kefeng Liu, Jian Zhou

- [2003] On a Proof of a Conjecture of Marino-Vafa on Hodge Integrals
  - arxiv: `math/0306257` (math.AG)
  - authors: Chiu-Chu Melissa Liu, Kefeng Liu, Jian Zhou

- [2003] A Proof of a Conjecture of Marino-Vafa on Hodge Integrals
  - arxiv: `math/0306434` (math.AG)
  - authors: Chiu-Chu Melissa Liu, Kefeng Liu, Jian Zhou

- [2000] Orbifold Hodge numbers of the wreath product orbifolds
  - arxiv: `math/0005124` (math.AG)
  - authors: Weiqiang Wang, Jian Zhou

- [2000] Superconformal vertex algebras in differential geometry. I
  - arxiv: `math/0006201` (math.DG)
  - authors: Jian Zhou

- [2000] DGBV Algebras and Mirror Symmetry
  - arxiv: `math/0006123` (math.DG)
  - authors: Huai-Dong Cao, Jian Zhou

- [1999] Homological perturbation theory and mirror symmetry
  - arxiv: `math/9906096` (math.DG)
  - authors: Jian Zhou

- [1999] Rational homotopy types of mirror manifolds
  - arxiv: `math/9910027` (math.DG)
  - authors: Jian Zhou

- [1999] Hodge theory and $A_{\infty}$ structures on cohomology
  - arxiv: `math/9903154` (math.DG)
  - authors: Jian Zhou

- [1999] Calculations of the Hirzebruch $χ_y$ genera of symmetric products by the holomorphic Lefsc
  - arxiv: `math/9910029` (math.DG)
  - authors: Jian Zhou

- [1999] Delocalized equivariant coholomogy of symmetric products
  - arxiv: `math/9910028` (math.DG)
  - authors: Jian Zhou

- [1999] On quasi-isomorphic DGBV algebras
  - arxiv: `math/9904168` (math.DG)
  - authors: Huai-Dong Cao, Jian Zhou

- [1999] Formal Frobenius manifold structure on equivariant cohomology
  - arxiv: `math/9903024` (math.DG)
  - authors: Huai-Dong Cao, Jian Zhou

- [1998] Degenerate Chern-Weil Theory and Equivariant Cohomology
  - arxiv: `math/9804135` (math.DG)
  - authors: Huai-Dong Cao, Jian Zhou

- [1998] Frobenius Manifold Structure on Dolbeault Cohomology and Mirror Symmetry
  - arxiv: `math/9805094` (math.DG)
  - authors: Huai-Dong Cao, Jian Zhou

- [1998] On Quantum de Rham Cohomology
  - arxiv: `math/9806157` (math.DG)
  - authors: Huai-Dong Cao, Jian Zhou

- [1998] On Quantum de Rham Cohomology Theory
  - arxiv: `math/9804145` (math.DG)
  - authors: Huai-Dong Cao, Jian Zhou

- [1998] Identification of Two Frobenius Manifolds In Mirror Symmetry
  - arxiv: `math/9805095` (math.DG)
  - authors: Huai-Dong Cao, Jian Zhou

- [1998] Equivariant Cohomology and Wall Crossing Formulas in Seiberg-Witten Theory
  - arxiv: `math/9804134` (math.DG)
  - authors: Huai-Dong Cao, Jian Zhou
