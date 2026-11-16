# v1.46：相位重新标记不会揭示个体身份

**日期：2026-11-16；研究类型：** 两粒子两模式有限维玻色子模型、理想 HOM 与矩阵数值核查。不是全量子电动力学（QED）模型、真实实验或永久光子身份的物理证明。

**复现代码：** [统一模型](../models/identity_permutation_v142_v151.py) · [10 项测试](../tests/test_identity_permutation_v142_v151.py)。独立本地脚本使用 Python 3/NumPy，在 2026-11-16 执行 10 项测试，全部通过。

将内态重叠 z=0.6 乘 exp(i0.7)，|z|² 不变，HOM 符合概率差为 0；将二玻色子态整体乘 exp(i0.53)，密度矩阵外积变化 Frobenius 范数为 1.12e−16（浮点误差）。**警告：** 此例只涉及全局相位与单个两态重叠；三光子闭环 Bargmann 相位是规范不变的、可影响多体干涉，不能被错误地宣布完全不可测。

参考： [Identical particles — graduate QM notes](https://etneil.github.io/grad_qm_lec_notes/identical_particles.html)；[Stanford Encyclopedia — Quantum Field Theory](https://plato.stanford.edu/entries/quantum-field-theory/)。
