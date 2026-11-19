# v2.93：不同的算符是否真的可操作

**研究日期：2026-11-19。证据等级：** NumPy 有限维量子信息计算与局域 U(1) 规范代数的数值一致性检查。**不是完整 QED、真实实验，亦不是永久光子身份的证明。** 本地原始代码已完成 10/10 自动测试。GitHub 整理版模型：[Python](../models/identity_theory_audit_v292_v301.py)；[测试](../tests/test_identity_theory_audit_v292_v301.py)。

对两槽位 qubit，令 O_slot=Z⊗I，O_sym=(Z⊗I+I⊗Z)/2。显式计算交换对易子 Frobenius 范数 ||[O_slot,S]||_F=2√2≈2.8284271247，而 ||[O_sym,S]||_F=0。对 |01> 等输入先用 P₊ 对称化，可得到满足 S|ψ>=|ψ> 的合法纯态（范数误差0）。**判断**：物理内部模式测量可以有集体对称版本；把算符强行写成“原来第一颗光子的性质”不是对同种玻色子不可辨识性的解决办法。此检验不排除通过空间模式或源标签进行可操作的条件寻址。

参考：[Quantum Statistics of Identical Particles (2022)](https://link.springer.com/article/10.1007/s10701-022-00596-4)；[Englbrecht et al., PRL 132, 050201 (2024)](https://doi.org/10.1103/PhysRevLett.132.050201)；[Low-energy photon-photon scattering EFT, PRD 57, 2443 (1998)](https://doi.org/10.1103/PhysRevD.57.2443)；[Identity and Individuality in Quantum Theory (SEP)](https://plato.sydney.edu.au/entries/qt-idind/)。
