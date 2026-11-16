# v1.50：独有身份参数被模式标定吸收

**日期：2026-11-16；研究类型：** 两粒子两模式有限维玻色子模型、理想 HOM 与矩阵数值核查。不是全量子电动力学（QED）模型、真实实验或永久光子身份的物理证明。

**复现代码：** [统一模型](../models/identity_permutation_v142_v151.py) · [10 项测试](../tests/test_identity_permutation_v142_v151.py)。独立本地脚本使用 Python 3/NumPy，在 2026-11-16 执行 10 项测试，全部通过。

候选机制只将 HOM 内态重叠 r 从 0.6 改为 0.7。候选符合概率 (1−0.7²)/2=0.255，而标准模型只需把自己可自由调整的内态重叠也设为 0.7，即可逐项复现此 Bernoulli 测量，profile KL=0。相对固定 r=0.6 基准，KL(0.255||0.32)=0.010112458143995133。**结论：** 固定错误基准可以造成显著差异，但允许物理上合理的标准 nuisance 重新拟合后，差异消失。

参考： [Identical particles — graduate QM notes](https://etneil.github.io/grad_qm_lec_notes/identical_particles.html)；[Stanford Encyclopedia — Quantum Field Theory](https://plato.stanford.edu/entries/quantum-field-theory/)。
