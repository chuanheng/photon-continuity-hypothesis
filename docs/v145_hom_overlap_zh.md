# v1.45：HOM 符合由模式重叠决定

**日期：2026-11-16；研究类型：** 两粒子两模式有限维玻色子模型、理想 HOM 与矩阵数值核查。不是全量子电动力学（QED）模型、真实实验或永久光子身份的物理证明。

**复现代码：** [统一模型](../models/identity_permutation_v142_v151.py) · [10 项测试](../tests/test_identity_permutation_v142_v151.py)。独立本地脚本使用 Python 3/NumPy，在 2026-11-16 执行 10 项测试，全部通过。

理想 50:50 分束器、双单光子分别入两个输入端口、无多光子背景和探测损耗时，P_coinc=(1−|〈φ1|φ2〉|²)/2。实际计算：重叠 0→0.5；重叠 0.6→0.32；重叠 1→0。这是标准量子光学已知效应。单纯观察 HOM 凹陷不能证明永久个体身份。

参考： [Identical particles — graduate QM notes](https://etneil.github.io/grad_qm_lec_notes/identical_particles.html)；[Stanford Encyclopedia — Quantum Field Theory](https://plato.stanford.edu/entries/quantum-field-theory/)。
