# v1.92：历史候选机制审计与分类

**研究日期：2026-11-17。** 本批次为标准量子模型的可证伪性方法论与合成 Bernoulli 检验，不是光子永久身份的实测结果或完整 QED 预测。实际本地 Python/NumPy/SciPy 运行 10 项测试全部通过。GitHub 复现：[计算代码](../models/identity_synthesis_v192_v201.py)；[十项测试](../tests/test_identity_synthesis_v192_v201.py)。

对前期研究出现的 8 类机制做可重复的证据层级分类：silent_label（无操作效应）；energy_free_hard_photon（封闭系统守恒冲突）；ordinary_dephasing、ordinary_amplitude_damping、matter_memory、quasistatic_environment（标准量子环境可解释）；mode_overlap_shift（合理 nuisance 重新拟合）；soft_click_excess（仅在标准背景被独立约束的假设下可检验）。分类不是全量物理定理，仅覆盖此前明确构造过的八个简化候选。**结论**：尚未找到永久身份独有的物理机制。

**有关研究：** Englbrecht et al., *Indistinguishability of Identical Bosons from a Quantum Information Theory Perspective*, PRL 132,050201 (2024), https://doi.org/10.1103/PhysRevLett.132.050201 ；Suzuki et al., *Quantum state estimation with nuisance parameters*, J. Phys. A 53,453001 (2020), https://doi.org/10.1088/1751-8121/ab8b78。
