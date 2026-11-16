# v1.42：玻色子 Fock 对称态维数

**日期：2026-11-16；研究类型：** 两粒子两模式有限维玻色子模型、理想 HOM 与矩阵数值核查。不是全量子电动力学（QED）模型、真实实验或永久光子身份的物理证明。

**复现代码：** [统一模型](../models/identity_permutation_v142_v151.py) · [10 项测试](../tests/test_identity_permutation_v142_v151.py)。独立本地脚本使用 Python 3/NumPy，在 2026-11-16 执行 10 项测试，全部通过。

对两粒子、两个单粒子模式，带有计算槽位编号的张量空间维数 2²=4；交换对称投影 P+=(I+S)/2 的矩阵秩为 3，对应玻色子空间 |2,0>、|1,1>、|0,2>。数值计算 rank(P+)=3，对称归一态 (|01>+|10>)/√2 满足 S|ψ>=|ψ>，差范数为 0。**限定：** 这是固定光子数的有限维模型，不代表整个光子 Fock 空间只有三维。

参考： [Identical particles — graduate QM notes](https://etneil.github.io/grad_qm_lec_notes/identical_particles.html)；[Stanford Encyclopedia — Quantum Field Theory](https://plato.stanford.edu/entries/quantum-field-theory/)。
