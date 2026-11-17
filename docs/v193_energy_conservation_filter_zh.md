# v1.93：守恒律作为机制筛选第一道门槛

**研究日期：2026-11-17。** 本批次为标准量子模型的可证伪性方法论与合成 Bernoulli 检验，不是光子永久身份的实测结果或完整 QED 预测。实际本地 Python/NumPy/SciPy 运行 10 项测试全部通过。GitHub 复现：[计算代码](../models/identity_synthesis_v192_v201.py)；[十项测试](../tests/test_identity_synthesis_v192_v201.py)。

封闭模型设入射能量为 3，出射光子仍保持能量 3，同时靶物质净增激发能量 2，则出态能量 5、比入态多 2。若无外场、介质初始储能等来源，该具体方案不满足能量守恒。若候选改为光子降能 1、靶增能 2，则总能量可守恒，但这是普通非弹性过程也允许的形式；不能由守恒本身证明永久身份。

**有关研究：** Englbrecht et al., *Indistinguishability of Identical Bosons from a Quantum Information Theory Perspective*, PRL 132,050201 (2024), https://doi.org/10.1103/PhysRevLett.132.050201 ；Suzuki et al., *Quantum state estimation with nuisance parameters*, J. Phys. A 53,453001 (2020), https://doi.org/10.1088/1751-8121/ab8b78。
