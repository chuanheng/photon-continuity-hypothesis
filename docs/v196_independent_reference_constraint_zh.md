# v1.96：独立标定将不可辨识变成条件可辨识

**研究日期：2026-11-17。** 本批次为标准量子模型的可证伪性方法论与合成 Bernoulli 检验，不是光子永久身份的实测结果或完整 QED 预测。实际本地 Python/NumPy/SciPy 运行 10 项测试全部通过。GitHub 复现：[计算代码](../models/identity_synthesis_v192_v201.py)；[十项测试](../tests/test_identity_synthesis_v192_v201.py)。

作为**纯统计方法例子**，假设独立参考确立标准点击概率 q∈[0.03,0.06]，而候选 p_A=0.08。由于 KL 对 q 在 q<p_A 时递减，最佳零假设位于上边界 q=0.06，最小 KL = 0.0032288569928560565 nat/event。**严重限制**：q≤0.06 目前不是依据 QED、真实仪器测量或带不确定性区间推得的物理边界；假设它真实可靠之前，不能声称发现标准模型无法解释的新效应。

**有关研究：** Englbrecht et al., *Indistinguishability of Identical Bosons from a Quantum Information Theory Perspective*, PRL 132,050201 (2024), https://doi.org/10.1103/PhysRevLett.132.050201 ；Suzuki et al., *Quantum state estimation with nuisance parameters*, J. Phys. A 53,453001 (2020), https://doi.org/10.1088/1751-8121/ab8b78。
