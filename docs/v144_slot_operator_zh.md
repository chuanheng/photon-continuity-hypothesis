# v1.44：编号专属观测算符与交换对称性

**日期：2026-11-16；研究类型：** 两粒子两模式有限维玻色子模型、理想 HOM 与矩阵数值核查。不是全量子电动力学（QED）模型、真实实验或永久光子身份的物理证明。

**复现代码：** [统一模型](../models/identity_permutation_v142_v151.py) · [10 项测试](../tests/test_identity_permutation_v142_v151.py)。独立本地脚本使用 Python 3/NumPy，在 2026-11-16 执行 10 项测试，全部通过。

设槽位专属 O1=Z⊗I，交换算符 S，则 Frobenius 范数 ||[O1,S]||=2.8284271247461903。对称化算符 A=(Z⊗I+I⊗Z)/2 满足 [A,S]=0，且 P+O1P+=P+AP+（误差 0）。因此**不能在相同玻色子物理空间内独立测第 1 个无名粒子的 Z**。这个结论只排除靠任意槽位编号实现的独有测量，不能排除实际引入新的可测内部量子数。

参考： [Identical particles — graduate QM notes](https://etneil.github.io/grad_qm_lec_notes/identical_particles.html)；[Stanford Encyclopedia — Quantum Field Theory](https://plato.stanford.edu/entries/quantum-field-theory/)。
