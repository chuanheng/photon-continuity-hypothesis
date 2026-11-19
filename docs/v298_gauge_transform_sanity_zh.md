# v2.98：初步规范变换检验与不能过度宣称的部分

**研究日期：2026-11-19。证据等级：** NumPy 有限维量子信息计算与局域 U(1) 规范代数的数值一致性检查。**不是完整 QED、真实实验，亦不是永久光子身份的证明。** 本地原始代码已完成 10/10 自动测试。GitHub 整理版模型：[Python](../models/identity_theory_audit_v292_v301.py)；[测试](../tests/test_identity_theory_audit_v292_v301.py)。

把电磁四维势的局部一阶导数记为矩阵 G_{μν}=∂μAν，场强 F_{μν}=G_{μν}−G_{νμ}。施加 U(1) 规范变化 Aν→Aν+∂νχ，在同一点的导数变化为对称 Hessian H_{μν}=∂μ∂νχ，则 F'=F。对任意指定四维实矩阵 G 与对称 H，数值最大场强变化 1.11×10^-16，形式不变的二次标量 F_{μν}F^{μν} 的变化0。相比之下，直接使用单点四势平方 A_μA^μ 的值可因梯度改变，本次数值变化为0.18。**极其重要的限制**：这是局域线性化的规范代数检查，不是完整规范固定、Ward 恒等式、量子反常、场论重整化或洛伦兹协变 QED 验证。

参考：[Quantum Statistics of Identical Particles (2022)](https://link.springer.com/article/10.1007/s10701-022-00596-4)；[Englbrecht et al., PRL 132, 050201 (2024)](https://doi.org/10.1103/PhysRevLett.132.050201)；[Low-energy photon-photon scattering EFT, PRD 57, 2443 (1998)](https://doi.org/10.1103/PhysRevD.57.2443)；[Identity and Individuality in Quantum Theory (SEP)](https://plato.sydney.edu.au/entries/qt-idind/)。
