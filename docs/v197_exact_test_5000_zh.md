# v1.97：有界复合零假设下的精确二项检验

**研究日期：2026-11-17。** 本批次为标准量子模型的可证伪性方法论与合成 Bernoulli 检验，不是光子永久身份的实测结果或完整 QED 预测。实际本地 Python/NumPy/SciPy 运行 10 项测试全部通过。GitHub 复现：[计算代码](../models/identity_synthesis_v192_v201.py)；[十项测试](../tests/test_identity_synthesis_v192_v201.py)。

在仅允许 q≤0.06 且 N=5000 次独立 Bernoulli 的条件下，单侧 α≤0.05 的最小拒绝点击数 k=329。q=0.06 是该单调上尾检验的最不利零假设。实际第一类错误率=0.04632877151629593；候选 p_A=0.08 时精确检验功效=0.9999358296578974。候选分布期望 log-LR（相对最佳标准边界）=5000×0.0032288569928560565=16.14428496428028。**这不是实际光学实验；只检验统计方法与假设条件。**

**有关研究：** Englbrecht et al., *Indistinguishability of Identical Bosons from a Quantum Information Theory Perspective*, PRL 132,050201 (2024), https://doi.org/10.1103/PhysRevLett.132.050201 ；Suzuki et al., *Quantum state estimation with nuisance parameters*, J. Phys. A 53,453001 (2020), https://doi.org/10.1088/1751-8121/ab8b78。
