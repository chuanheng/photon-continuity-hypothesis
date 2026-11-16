# v1.43：永久编号重排不能产生独立态

**日期：2026-11-16；研究类型：** 两粒子两模式有限维玻色子模型、理想 HOM 与矩阵数值核查。不是全量子电动力学（QED）模型、真实实验或永久光子身份的物理证明。

**复现代码：** [统一模型](../models/identity_permutation_v142_v151.py) · [10 项测试](../tests/test_identity_permutation_v142_v151.py)。独立本地脚本使用 Python 3/NumPy，在 2026-11-16 执行 10 项测试，全部通过。

用 |01> 与 |10> 代表两个计算槽位的交换描述，数值验证 P+|01>−P+|10>=0。对称模式算符 (Z⊗I+I⊗Z)/2 对两者的期望也相同。**边界：** 这是纯标签交换，不能拿来否定不同偏振、时间模式等真正可测的内部态差异。

参考： [Identical particles — graduate QM notes](https://etneil.github.io/grad_qm_lec_notes/identical_particles.html)；[Stanford Encyclopedia — Quantum Field Theory](https://plato.stanford.edu/entries/quantum-field-theory/)。
