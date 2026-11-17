# v2.09：双样本检验的零假设错误率验证

**研究日期：2026-11-17。研究等级：数学/合成统计方法学，不是实际光学实验，不是永久光子身份的预测或验证。** 复现：[GitHub 模型](../models/identity_evidence_v202_v211.py)；[十项测试](../tests/test_identity_evidence_v202_v211.py)。Python/NumPy/SciPy，Monte Carlo 固定随机种子 20261117，每种场景重复 3000 次。

在主实验/参考实验真实概率均为 0.06 时，仍按 n=5000、m=1000/5000/20000 做 3000 次 Monte Carlo 独立重复。单侧 pooled z 统计量大于标准正态 95% 分位点的比例依次为 5.1667%、4.7667%、5.0000%。在本数值条件下与名义 5% 大体相符，但 3000 次模拟的不确定度约为 0.8 个百分点，不能当作对所有小样本或有相关性数据的严格检验大小保证。

**研究背景文献：** Englbrecht et al. PRL 132,050201 (2024), https://doi.org/10.1103/PhysRevLett.132.050201 ；Fleischhauer & Lukin PRA 65,022314 (2002), https://doi.org/10.1103/PhysRevA.65.022314 ；Pollock et al. PRA 97,012127 (2018), https://doi.org/10.1103/PhysRevA.97.012127 。
