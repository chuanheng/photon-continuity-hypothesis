# v2.97：物质存储与逆读取不保证实体个体同一性

**研究日期：2026-11-19。证据等级：** NumPy 有限维量子信息计算与局域 U(1) 规范代数的数值一致性检查。**不是完整 QED、真实实验，亦不是永久光子身份的证明。** 本地原始代码已完成 10/10 自动测试。GitHub 整理版模型：[Python](../models/identity_theory_audit_v292_v301.py)；[测试](../tests/test_identity_theory_audit_v292_v301.py)。

取四维单激发空间 |p0>,|p1>,|m0>,|m1>，哈密顿量 H 将每个光学模式与对应物质激发等强度耦合。U=exp(−iπH/2) 把输入 (|p0>+|p1>)/√2 转为物质激发，概率0.9999999999999996；U† 逆演化后的原态保真度0.9999999999999991。整个过程限制在固定一激发子空间，数值上没有额外激发产生。**关键论证**：可逆的信息态转移及恢复属于普通量子存储，无法由末态重建单独推导最初“那一个光子”的跨吸收个体同一性。

参考：[Quantum Statistics of Identical Particles (2022)](https://link.springer.com/article/10.1007/s10701-022-00596-4)；[Englbrecht et al., PRL 132, 050201 (2024)](https://doi.org/10.1103/PhysRevLett.132.050201)；[Low-energy photon-photon scattering EFT, PRD 57, 2443 (1998)](https://doi.org/10.1103/PhysRevD.57.2443)；[Identity and Individuality in Quantum Theory (SEP)](https://plato.sydney.edu.au/entries/qt-idind/)。
