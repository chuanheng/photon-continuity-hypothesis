# v3.07：精确检验可以很显著，却没有新物理辨识力

**研究日期：2026-11-20。证据等级：理论/数学与合成数据；未开展真实实验，未完成 QED 新动力学，也无永久身份独有预测。** 本地原始代码运行 10/10 测试通过。GitHub 整理版：[模型](../models/identity_paper_audit_v302_v311.py) · [十项测试](../tests/test_identity_paper_audit_v302_v311.py)。研究结论对照文献：[Englbrecht et al., PRL 132, 050201 (2024)](https://doi.org/10.1103/PhysRevLett.132.050201)；[HOM Review, EPJD (2022)](https://doi.org/10.1140/epjd/s10053-022-00525-0)；[Gate Set Tomography (2021)](https://research.ibm.com/publications/gate-set-tomography)。

合成候选 Bernoulli p1=.2408，错误固定标准基准 p0=.095；n=200 的上尾精确二项检验，满足 α≤.05 的最小阈值为 K≥27。第一类错误率 P_{.095}(K≥27)=0.040273448344332406，备择下功效 P_{.2408}(K≥27)=0.9999292017586787。两固定分布 KL=.09059719558758264 nat/次。然而标准量子理论若允许 q_eff=.5184，零假设族本身包含 p1，故 **profile KL=0**。不能把只针对一个错误固定基准的高显著性用来证实“永久光子身份”。
