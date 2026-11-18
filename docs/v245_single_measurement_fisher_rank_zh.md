# v2.45：单次 HOM 观测的两参数 Fisher 秩亏

**研究日期：2026-11-18。** 理想双光子 HOM 分束器、纯态内模式与隐藏二能级标签的合成数学研究。**不是实际实验，也不是永久光子身份的验证。** Python/NumPy 本地运行并通过 10/10 单元测试。可复现文件：[统一模型](../models/identity_label_hom_v242_v251.py) · [十项测试](../tests/test_identity_label_hom_v242_v251.py)。

对 P_coin(q,s)=(1−qs)/2，参数梯度 ∇P=(-s/2,-q/2)。N 次独立 Bernoulli 测量对应的 Fisher 矩阵 F=N∇P∇Pᵀ/[P(1−P)]，解析上秩最多为 1，无法独立识别 q、s。取 q=0.81、s=0.64、N=10000，两个数值特征值约 -1.36×10^-12（浮点零）与 14573.447。数值 determinant 因舍入约 -2.58×10^-8，**不可把这一近零负数解释成 Fisher 不是正定意义上的半正定**；解析外积表达式保证 F 半正定且 det(F)=0。

**理论参照**：[Hong、Ou、Mandel (1987)](https://doi.org/10.1103/PhysRevLett.59.2044)；[Englbrecht 等 (2024)，PRL 132,050201](https://doi.org/10.1103/PhysRevLett.132.050201)；[Indistinguishability Theory for Identical Particles with Invariant Degrees of Freedom (2026 预印本)](https://arxiv.org/abs/2609.14428)。
