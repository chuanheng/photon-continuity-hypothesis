# v2.50：有限采样可以拒绝固定基准但不能拒绝标准模型族

**研究日期：2026-11-18。** 理想双光子 HOM 分束器、纯态内模式与隐藏二能级标签的合成数学研究。**不是实际实验，也不是永久光子身份的验证。** Python/NumPy 本地运行并通过 10/10 单元测试。可复现文件：[统一模型](../models/identity_label_hom_v242_v251.py) · [十项测试](../tests/test_identity_label_hom_v242_v251.py)。

对候选 q=0.81、s=0.64 的 HOM 符合概率 p=0.2408，NumPy default_rng(seed=20261118) 的 N=10000 次合成 Bernoulli 二项抽样得到 2403 次符合。若错误地把标准重叠固定为 q=0.81 且 s=1，则基准概率 P0=(1−0.81)/2=0.095，得到简单假设 KL(Bern(.2408)||Bern(.095))≈0.0905972 nat/次。不过标准模型可采用不含身份的有效内部重叠 0.5184，精确预测 0.2408，profile KL=0。**合成数据的明显差异不是永久身份独有的证据。**

**理论参照**：[Hong、Ou、Mandel (1987)](https://doi.org/10.1103/PhysRevLett.59.2044)；[Englbrecht 等 (2024)，PRL 132,050201](https://doi.org/10.1103/PhysRevLett.132.050201)；[Indistinguishability Theory for Identical Particles with Invariant Degrees of Freedom (2026 预印本)](https://arxiv.org/abs/2609.14428)。
