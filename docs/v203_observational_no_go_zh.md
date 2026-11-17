# v2.03：惰性身份标签的操作不可辨识性

**研究日期：2026-11-17。研究等级：数学/合成统计方法学，不是实际光学实验，不是永久光子身份的预测或验证。** 复现：[GitHub 模型](../models/identity_evidence_v202_v211.py)；[十项测试](../tests/test_identity_evidence_v202_v211.py)。Python/NumPy/SciPy，Monte Carlo 固定随机种子 20261117，每种场景重复 3000 次。

设 P(D|θ,L) 对 L 不依赖，或 L 与系统始终张量独立且所有实验操作为 E_sys⊗I_L。将 L 求和/偏迹，得到所有允许操作的可访问概率 P(D|θ)；分布总变差和 KL 都为 0。此时标签本身既不能被否证，也不能被确认。**限制**：若提出新的可访问耦合，须重新建模并比较完整量子操作集合，而不是把“无耦合零效应”误当成所有身份理论必然的结论。

**研究背景文献：** Englbrecht et al. PRL 132,050201 (2024), https://doi.org/10.1103/PhysRevLett.132.050201 ；Fleischhauer & Lukin PRA 65,022314 (2002), https://doi.org/10.1103/PhysRevA.65.022314 ；Pollock et al. PRA 97,012127 (2018), https://doi.org/10.1103/PhysRevA.97.012127 。
