# v1.95：复合标准模型的自由参数与最小 KL

**研究日期：2026-11-17。** 本批次为标准量子模型的可证伪性方法论与合成 Bernoulli 检验，不是光子永久身份的实测结果或完整 QED 预测。实际本地 Python/NumPy/SciPy 运行 10 项测试全部通过。GitHub 复现：[计算代码](../models/identity_synthesis_v192_v201.py)；[十项测试](../tests/test_identity_synthesis_v192_v201.py)。

设置一个**人为构造的统计示例**：候选软点击概率 p_A=0.08；标准模型允许的 Bernoulli 参数 q∈[0.001,0.999]。它可取 q=0.08，因此 inf_q KL(Bern(0.08)||Bern(q))=0。若仅与固定 q=0.06 进行比较则非零，但那不能代表拒绝整个标准模型族。**物理含义**：除非参考数据约束了标准参数族，否则显著的固定基准拒绝不能产生新物理证据。

**有关研究：** Englbrecht et al., *Indistinguishability of Identical Bosons from a Quantum Information Theory Perspective*, PRL 132,050201 (2024), https://doi.org/10.1103/PhysRevLett.132.050201 ；Suzuki et al., *Quantum state estimation with nuisance parameters*, J. Phys. A 53,453001 (2020), https://doi.org/10.1088/1751-8121/ab8b78。
