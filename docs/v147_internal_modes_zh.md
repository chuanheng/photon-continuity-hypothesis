# v1.47：可区分的内部态不等于永久身份

**日期：2026-11-16；研究类型：** 两粒子两模式有限维玻色子模型、理想 HOM 与矩阵数值核查。不是全量子电动力学（QED）模型、真实实验或永久光子身份的物理证明。

**复现代码：** [统一模型](../models/identity_permutation_v142_v151.py) · [10 项测试](../tests/test_identity_permutation_v142_v151.py)。独立本地脚本使用 Python 3/NumPy，在 2026-11-16 执行 10 项测试，全部通过。

两光子内部模式正交（重叠 0）时，理想 HOM 符合率 0.5；内部模式相同时（重叠 1），符合率 0。偏振、频率、时域波包可以产生真实可测的模式差异，但这些是标准态描述中的物理自由度，并不是一个能够跨吸收、散射、再发射全过程追踪的“永久个体编号”。

参考： [Identical particles — graduate QM notes](https://etneil.github.io/grad_qm_lec_notes/identical_particles.html)；[Stanford Encyclopedia — Quantum Field Theory](https://plato.stanford.edu/entries/quantum-field-theory/)。
