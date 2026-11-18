# v2.44：普通内部模式精确复现隐藏标签的 HOM

**研究日期：2026-11-18。** 理想双光子 HOM 分束器、纯态内模式与隐藏二能级标签的合成数学研究。**不是实际实验，也不是永久光子身份的验证。** Python/NumPy 本地运行并通过 10/10 单元测试。可复现文件：[统一模型](../models/identity_label_hom_v242_v251.py) · [十项测试](../tests/test_identity_label_hom_v242_v251.py)。

将标准（不含新标签）两光子的可见内部纯态重叠平方直接设置 q_eff=q*s=0.5184；采用同一个平衡分束器振幅公式，其符合概率仍为 0.2408。两模型输出概率数值差 5.55e-17。只观察这一个 HOM 符合计数时，Bernoulli 分布完全相等、最小 KL=0。**严谨边界：** 这里证明的是这一实验的等价性，不是全部可能联合作用与全场论动力学的等价。

**理论参照**：[Hong、Ou、Mandel (1987)](https://doi.org/10.1103/PhysRevLett.59.2044)；[Englbrecht 等 (2024)，PRL 132,050201](https://doi.org/10.1103/PhysRevLett.132.050201)；[Indistinguishability Theory for Identical Particles with Invariant Degrees of Freedom (2026 预印本)](https://arxiv.org/abs/2609.14428)。
