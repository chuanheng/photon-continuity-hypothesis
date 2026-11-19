# v2.94：完全沉默的永久标签为何不可检验

**研究日期：2026-11-19。证据等级：** NumPy 有限维量子信息计算与局域 U(1) 规范代数的数值一致性检查。**不是完整 QED、真实实验，亦不是永久光子身份的证明。** 本地原始代码已完成 10/10 自动测试。GitHub 整理版模型：[Python](../models/identity_theory_audit_v292_v301.py)；[测试](../tests/test_identity_theory_audit_v292_v301.py)。

给可见单量子比特系统附加独立二能级标签 L。准备相同可见态 |+>，隐藏标签分别为 |0>、|1>，测量只作用于可见系统：E_+=(I+X)/2⊗I_L。两组概率均为1，差为0。**更普遍的有限维命题**：若实验制备的可见边缘态相同，所有后续通道/测量的可访问算符均与 L 脱耦并且没有任何系统—L 初始关联可反馈给系统，那么对 L 求迹使所有实验统计与无标签模型相同。该条件下身份参数的所有观测 Fisher 信息为0，但**不能**推出任何可能有新耦合的身份理论都不成立。

参考：[Quantum Statistics of Identical Particles (2022)](https://link.springer.com/article/10.1007/s10701-022-00596-4)；[Englbrecht et al., PRL 132, 050201 (2024)](https://doi.org/10.1103/PhysRevLett.132.050201)；[Low-energy photon-photon scattering EFT, PRD 57, 2443 (1998)](https://doi.org/10.1103/PhysRevD.57.2443)；[Identity and Individuality in Quantum Theory (SEP)](https://plato.sydney.edu.au/entries/qt-idind/)。
