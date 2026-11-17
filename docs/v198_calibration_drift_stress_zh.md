# v1.98：独立标定漂移使可辨识性崩塌

**研究日期：2026-11-17。** 本批次为标准量子模型的可证伪性方法论与合成 Bernoulli 检验，不是光子永久身份的实测结果或完整 QED 预测。实际本地 Python/NumPy/SciPy 运行 10 项测试全部通过。GitHub 复现：[计算代码](../models/identity_synthesis_v192_v201.py)；[十项测试](../tests/test_identity_synthesis_v192_v201.py)。

允许标准概率上界从 0.06 发生绝对漂移 δ=0、0.005、0.01、0.015、0.02。对应最小 KL 分别为 0.003228857、0.001732119、0.000736469、0.000176620、0。δ≥0.02 时，上界达到候选 p_A=0.08，标准模型再次可以精确拟合候选数据。**结论**：跨实验共享参数及漂移边界是不可跳过的前提；不能以高统计功效弥补未经验证的系统误差。

**有关研究：** Englbrecht et al., *Indistinguishability of Identical Bosons from a Quantum Information Theory Perspective*, PRL 132,050201 (2024), https://doi.org/10.1103/PhysRevLett.132.050201 ；Suzuki et al., *Quantum state estimation with nuisance parameters*, J. Phys. A 53,453001 (2020), https://doi.org/10.1088/1751-8121/ab8b78。
