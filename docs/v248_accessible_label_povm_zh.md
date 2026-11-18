# v2.48：真正读取标签后，它成为普通内部自由度

**研究日期：2026-11-18。** 理想双光子 HOM 分束器、纯态内模式与隐藏二能级标签的合成数学研究。**不是实际实验，也不是永久光子身份的验证。** Python/NumPy 本地运行并通过 10/10 单元测试。可复现文件：[统一模型](../models/identity_label_hom_v242_v251.py) · [十项测试](../tests/test_identity_label_hom_v242_v251.py)。

若实验允许测量隐藏单光子内部标签的投影算符 |l1><l1|，对第二标签态 |l2> 测得“与第一标签相同”的概率 |<l1|l2>|²=s=0.64。这个额外 POVM 可独立约束标签态的区别；但它在数学上与测量偏振、频率或其他常规内部态一样，**不直接测量“这是不是原来那一个光子”**。如果标签是绝对不可读的，则该 POVM 不在物理操作集合内，不能用它当作实际实验提案。

**理论参照**：[Hong、Ou、Mandel (1987)](https://doi.org/10.1103/PhysRevLett.59.2044)；[Englbrecht 等 (2024)，PRL 132,050201](https://doi.org/10.1103/PhysRevLett.132.050201)；[Indistinguishability Theory for Identical Particles with Invariant Degrees of Freedom (2026 预印本)](https://arxiv.org/abs/2609.14428)。
