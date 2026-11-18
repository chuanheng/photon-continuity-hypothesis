# v2.43：直接从分束器输出振幅计算 HOM 符合

**研究日期：2026-11-18。** 理想双光子 HOM 分束器、纯态内模式与隐藏二能级标签的合成数学研究。**不是实际实验，也不是永久光子身份的验证。** Python/NumPy 本地运行并通过 10/10 单元测试。可复现文件：[统一模型](../models/identity_label_hom_v242_v251.py) · [十项测试](../tests/test_identity_label_hom_v242_v251.py)。

两个纯态内模式矢量 u_i、v_i 通过理想 50:50 平衡分束器，光子数分辨且探测器不读内部态。输出分别各有一光子的内部指标 (i,j) 振幅为 (u_i v_j−v_i u_j)/2。将每个 (i,j) 的模平方求和得到 P_coin=0.2408；与闭式关系 (1−|<u|v>|²)/2=0.2408 的误差 2.78e-17。**解释：** 额外内部标签降低 HOM 可见度，符合标准光子不可区分性理论，无需假设永久身份。

**理论参照**：[Hong、Ou、Mandel (1987)](https://doi.org/10.1103/PhysRevLett.59.2044)；[Englbrecht 等 (2024)，PRL 132,050201](https://doi.org/10.1103/PhysRevLett.132.050201)；[Indistinguishability Theory for Identical Particles with Invariant Degrees of Freedom (2026 预印本)](https://arxiv.org/abs/2609.14428)。
