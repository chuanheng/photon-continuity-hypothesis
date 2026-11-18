# v2.47：独立参考 HOM 校准与局部可辨识性

**研究日期：2026-11-18。** 理想双光子 HOM 分束器、纯态内模式与隐藏二能级标签的合成数学研究。**不是实际实验，也不是永久光子身份的验证。** Python/NumPy 本地运行并通过 10/10 单元测试。可复现文件：[统一模型](../models/identity_label_hom_v242_v251.py) · [十项测试](../tests/test_identity_label_hom_v242_v251.py)。

假设使用独立参考源校准“可见模式重叠”q=0.81，且参考可保证隐藏标签重叠为 1，使其符合概率 P_ref=(1−q)/2=0.095。在主实验 N=10000 及参考 N_ref=10000 的理想 Bernoulli 采样条件下，联合 Fisher 矩阵的两个特征值约 7146.8569、36504.8107，行列式约 260894659，局部满秩。**重点限制：** 这只能统计识别两个有效重叠参数，不能证明 s 是“永久个体身份”。参考源如何保证标签相同本身是一个独立且未解决的物理前提。

**理论参照**：[Hong、Ou、Mandel (1987)](https://doi.org/10.1103/PhysRevLett.59.2044)；[Englbrecht 等 (2024)，PRL 132,050201](https://doi.org/10.1103/PhysRevLett.132.050201)；[Indistinguishability Theory for Identical Particles with Invariant Degrees of Freedom (2026 预印本)](https://arxiv.org/abs/2609.14428)。
