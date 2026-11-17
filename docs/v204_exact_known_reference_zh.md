# v2.04：精确已知参考概率的理想检验

**研究日期：2026-11-17。研究等级：数学/合成统计方法学，不是实际光学实验，不是永久光子身份的预测或验证。** 复现：[GitHub 模型](../models/identity_evidence_v202_v211.py)；[十项测试](../tests/test_identity_evidence_v202_v211.py)。Python/NumPy/SciPy，Monte Carlo 固定随机种子 20261117，每种场景重复 3000 次。

合成主实验 N=5000，候选概率 0.08、精确已知标准概率 0.06。单侧二项检验 α≤.05，拒绝临界点击数≥329，真实检验大小 0.0463287715163；备择下精确检验功效 0.9999358296579。**不能将本项当成真实标定条件**：参考概率 0.06 精确已知是一个人为理想化假设。

**研究背景文献：** Englbrecht et al. PRL 132,050201 (2024), https://doi.org/10.1103/PhysRevLett.132.050201 ；Fleischhauer & Lukin PRA 65,022314 (2002), https://doi.org/10.1103/PhysRevA.65.022314 ；Pollock et al. PRA 97,012127 (2018), https://doi.org/10.1103/PhysRevA.97.012127 。
