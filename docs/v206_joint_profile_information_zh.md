# v2.06：双样本共享零假设的期望轮廓似然信息

**研究日期：2026-11-17。研究等级：数学/合成统计方法学，不是实际光学实验，不是永久光子身份的预测或验证。** 复现：[GitHub 模型](../models/identity_evidence_v202_v211.py)；[十项测试](../tests/test_identity_evidence_v202_v211.py)。Python/NumPy/SciPy，Monte Carlo 固定随机种子 20261117，每种场景重复 3000 次。

取主实验 n=5000，p=0.08，参考 m∈{1000,5000,20000}，q=0.06。共享零假设最优概率 q*=(np+mq)/(n+m)。理论“期望计数”似然比分离度为 nKL(p||q*)+mKL(q||q*)，依次为 **2.496143、7.704998、12.669583 nats**。这与假设 q 精确知道时的 nKL(0.08||0.06)=16.144285 不同。它是固定真实参数的 Asimov 分离度，而不是实际观察样本的对数似然比或新物理证据。

**研究背景文献：** Englbrecht et al. PRL 132,050201 (2024), https://doi.org/10.1103/PhysRevLett.132.050201 ；Fleischhauer & Lukin PRA 65,022314 (2002), https://doi.org/10.1103/PhysRevA.65.022314 ；Pollock et al. PRA 97,012127 (2018), https://doi.org/10.1103/PhysRevA.97.012127 。
