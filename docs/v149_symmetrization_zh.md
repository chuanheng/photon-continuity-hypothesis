# v1.49：身份耦合对称化后退化为普通模式耦合

**日期：2026-11-16；研究类型：** 两粒子两模式有限维玻色子模型、理想 HOM 与矩阵数值核查。不是全量子电动力学（QED）模型、真实实验或永久光子身份的物理证明。

**复现代码：** [统一模型](../models/identity_permutation_v142_v151.py) · [10 项测试](../tests/test_identity_permutation_v142_v151.py)。独立本地脚本使用 Python 3/NumPy，在 2026-11-16 执行 10 项测试，全部通过。

对上轮 H_label 做群平均 H_avg=(H_label+S H_label S)/2=(Z⊗I+I⊗Z)/2。数值验证 P+H_label P+=P+H_avg P+，差为 0；物理子空间投影后的耦合范数为 1.4142135623730951。其非零效应可解释为普通对称模式算符，未产生可追踪的永久身份标签。**重点：** 对称化不代表哈密顿量作用变为零，只代表失去任意槽位专属意义。

参考： [Identical particles — graduate QM notes](https://etneil.github.io/grad_qm_lec_notes/identical_particles.html)；[Stanford Encyclopedia — Quantum Field Theory](https://plato.stanford.edu/entries/quantum-field-theory/)。
