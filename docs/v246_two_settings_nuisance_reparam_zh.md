# v2.46：两组设置也可能被标准模式参数全部吸收

**研究日期：2026-11-18。** 理想双光子 HOM 分束器、纯态内模式与隐藏二能级标签的合成数学研究。**不是实际实验，也不是永久光子身份的验证。** Python/NumPy 本地运行并通过 10/10 单元测试。可复现文件：[统一模型](../models/identity_label_hom_v242_v251.py) · [十项测试](../tests/test_identity_label_hom_v242_v251.py)。

对相同隐藏标签重叠 s=0.64，令两次可见模式重叠平方分别 q1=0.81、q2=0.64，则候选 HOM 符合概率分别 0.2408、0.2952。标准理论若允许每个设置的有效内部模式重叠 q_eff,1=0.5184、q_eff,2=0.4096，可逐点完全复现，两个设置的总 profile KL=0。**条件：** 标准有效内部态可以随设置变化，且没有外部物理约束阻止这种变化。如果设置间有共同参数或独立可信校准，需重做具体辨识分析。

**理论参照**：[Hong、Ou、Mandel (1987)](https://doi.org/10.1103/PhysRevLett.59.2044)；[Englbrecht 等 (2024)，PRL 132,050201](https://doi.org/10.1103/PhysRevLett.132.050201)；[Indistinguishability Theory for Identical Particles with Invariant Degrees of Freedom (2026 预印本)](https://arxiv.org/abs/2609.14428)。
