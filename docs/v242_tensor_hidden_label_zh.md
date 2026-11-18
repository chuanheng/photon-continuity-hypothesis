# v2.42：可见模式与独立隐藏标签的张量模型

**研究日期：2026-11-18。** 理想双光子 HOM 分束器、纯态内模式与隐藏二能级标签的合成数学研究。**不是实际实验，也不是永久光子身份的验证。** Python/NumPy 本地运行并通过 10/10 单元测试。可复现文件：[统一模型](../models/identity_label_hom_v242_v251.py) · [十项测试](../tests/test_identity_label_hom_v242_v251.py)。

令单光子内部 Hilbert 空间为 H_visible⊗H_label，每个因子均为二维。两光子分别具有内部态 |u>=|v1>⊗|l1>、|v>=|v2>⊗|l2>；可见态重叠平方 q=|<v1|v2>|²=0.81，标签重叠平方 s=|<l1|l2>|²=0.64，则联合重叠平方 |<u|v>|²=q s=0.5184（浮点误差 1.11e-16）。**关键区分：** 这里构造的是单光子的额外内部量子数，两个光子整体仍须服从玻色子交换对称性；其数学存在不证明跨吸收/再发射的永久个体身份。

**理论参照**：[Hong、Ou、Mandel (1987)](https://doi.org/10.1103/PhysRevLett.59.2044)；[Englbrecht 等 (2024)，PRL 132,050201](https://doi.org/10.1103/PhysRevLett.132.050201)；[Indistinguishability Theory for Identical Particles with Invariant Degrees of Freedom (2026 预印本)](https://arxiv.org/abs/2609.14428)。
