# v2.08：探测器效率与暗计数的全局参数混淆

**研究日期：2026-11-17。研究等级：数学/合成统计方法学，不是实际光学实验，不是永久光子身份的预测或验证。** 复现：[GitHub 模型](../models/identity_evidence_v202_v211.py)；[十项测试](../tests/test_identity_evidence_v202_v211.py)。Python/NumPy/SciPy，Monte Carlo 固定随机种子 20261117，每种场景重复 3000 次。

仅观测一项 Bernoulli 点击概率 p_obs=d+(1-d)ηb，其中 b 是普通软光子出射概率，η 是探测效率，d 是独立暗计数概率。参数组合 (b,η,d)=(0.08,0.7,0.01) 给 p_obs=0.06544；(0.05795918367,0.8,0.02) 给出完全相同的 p_obs=0.06544。单一点击观测无论重复多少次都不能区分它们；必须引入独立效率、暗计数及光子通道标定。这个反例属于标准仪器混淆，不代表身份的发现。

**研究背景文献：** Englbrecht et al. PRL 132,050201 (2024), https://doi.org/10.1103/PhysRevLett.132.050201 ；Fleischhauer & Lukin PRA 65,022314 (2002), https://doi.org/10.1103/PhysRevA.65.022314 ；Pollock et al. PRA 97,012127 (2018), https://doi.org/10.1103/PhysRevA.97.012127 。
