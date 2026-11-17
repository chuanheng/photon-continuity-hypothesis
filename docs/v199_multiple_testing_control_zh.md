# v1.99：三个预先选定终点的多重检验控制

**研究日期：2026-11-17。** 本批次为标准量子模型的可证伪性方法论与合成 Bernoulli 检验，不是光子永久身份的实测结果或完整 QED 预测。实际本地 Python/NumPy/SciPy 运行 10 项测试全部通过。GitHub 复现：[计算代码](../models/identity_synthesis_v192_v201.py)；[十项测试](../tests/test_identity_synthesis_v192_v201.py)。

仍在 N=5000、q≤0.06、p_A=0.08 的玩具模型，假定事前指定三个统计检验，共同控制家族错误率 α=0.05。用 Bonferroni 将每个检验 α 限制为 0.016666666666666666，得到单项点击阈值 k=337、实际误报概率 0.016063662149256176、精确功效 0.9996486825763494。该计算只针对每个检验的相同边际模型，并没有实际生成三个互相关联终点。若数据驱动筛选终点、反复看数据或多个模型搜索，则还需要更适当的多重比较调整。

**有关研究：** Englbrecht et al., *Indistinguishability of Identical Bosons from a Quantum Information Theory Perspective*, PRL 132,050201 (2024), https://doi.org/10.1103/PhysRevLett.132.050201 ；Suzuki et al., *Quantum state estimation with nuisance parameters*, J. Phys. A 53,453001 (2020), https://doi.org/10.1088/1751-8121/ab8b78。
