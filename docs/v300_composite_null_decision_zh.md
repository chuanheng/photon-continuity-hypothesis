# v3.00：错误固定对照与合理标准模型族之间的差异

**研究日期：2026-11-19。证据等级：** NumPy 有限维量子信息计算与局域 U(1) 规范代数的数值一致性检查。**不是完整 QED、真实实验，亦不是永久光子身份的证明。** 本地原始代码已完成 10/10 自动测试。GitHub 整理版模型：[Python](../models/identity_theory_audit_v292_v301.py)；[测试](../tests/test_identity_theory_audit_v292_v301.py)。

取 v2.96 的 HOM 实验，P_candidate=.2408。错误地固定标准模式重叠 q=.81 且断言没有其他内部模式差异，得到 P_fixed=.095，两个 Bernoulli 模型 KL=.09059719558758264 nats/事件。NumPy default_rng(seed=20261119) 在 n=10000 的候选分布生成合成符合计数2393。**但是** 标准模型允许 q_eff=.5184 后获得完全同样的概率分布，KL_profile=0。即使积累无限多仅此一类 HOM 样本，也无法通过该观测量辨别这两种参数解释。模拟点击数不是实验事实。

参考：[Quantum Statistics of Identical Particles (2022)](https://link.springer.com/article/10.1007/s10701-022-00596-4)；[Englbrecht et al., PRL 132, 050201 (2024)](https://doi.org/10.1103/PhysRevLett.132.050201)；[Low-energy photon-photon scattering EFT, PRD 57, 2443 (1998)](https://doi.org/10.1103/PhysRevD.57.2443)；[Identity and Individuality in Quantum Theory (SEP)](https://plato.sydney.edu.au/entries/qt-idind/)。
