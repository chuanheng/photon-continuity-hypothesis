# v1.48：动力学必须通过交换对称性检验

**日期：2026-11-16；研究类型：** 两粒子两模式有限维玻色子模型、理想 HOM 与矩阵数值核查。不是全量子电动力学（QED）模型、真实实验或永久光子身份的物理证明。

**复现代码：** [统一模型](../models/identity_permutation_v142_v151.py) · [10 项测试](../tests/test_identity_permutation_v142_v151.py)。独立本地脚本使用 Python 3/NumPy，在 2026-11-16 执行 10 项测试，全部通过。

构造 H_sym=X⊗I+I⊗X+0.35 Z⊗Z，得到 ||[H_sym,S]||=0。构造 H_label=Z⊗I，得到 ||[H_label,S]||=2.8284271247461903。后者把任意计算槽位当成物理上受特殊对待的粒子，不符合所用相同玻色子表示。**限定：** 正确的带内部自由度或外部场模型须让完整单粒子自由度一同交换；不能以这里的简化槽位对易式代替完整场论一致性审查。

参考： [Identical particles — graduate QM notes](https://etneil.github.io/grad_qm_lec_notes/identical_particles.html)；[Stanford Encyclopedia — Quantum Field Theory](https://plato.stanford.edu/entries/quantum-field-theory/)。
