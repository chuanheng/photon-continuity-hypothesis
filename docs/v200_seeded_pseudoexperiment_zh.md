# v2.00：固定种子合成试验与事前规则演示

**研究日期：2026-11-17。** 本批次为标准量子模型的可证伪性方法论与合成 Bernoulli 检验，不是光子永久身份的实测结果或完整 QED 预测。实际本地 Python/NumPy/SciPy 运行 10 项测试全部通过。GitHub 复现：[计算代码](../models/identity_synthesis_v192_v201.py)；[十项测试](../tests/test_identity_synthesis_v192_v201.py)。

设真实合成概率 p_A=0.08、N=5000，使用 numpy.random.default_rng(seed=20261117).binomial(N,p_A)，本次得到 383 次点击；对 q≤0.06 最不利边界的单侧二项 p 值 1.1130892427544515e-06。此结果在假定标定上界确实成立时会拒绝有界零假设。**但这是模拟数据，分析并未真实预注册，不能作为真实新物理检验；如边界不存在，则标准模型取 q=0.08 即可解释数据。**

**有关研究：** Englbrecht et al., *Indistinguishability of Identical Bosons from a Quantum Information Theory Perspective*, PRL 132,050201 (2024), https://doi.org/10.1103/PhysRevLett.132.050201 ；Suzuki et al., *Quantum state estimation with nuisance parameters*, J. Phys. A 53,453001 (2020), https://doi.org/10.1088/1751-8121/ab8b78。
