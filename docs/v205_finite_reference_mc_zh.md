# v2.05：有限独立标定的三档 Monte Carlo 比较

**研究日期：2026-11-17。研究等级：数学/合成统计方法学，不是实际光学实验，不是永久光子身份的预测或验证。** 复现：[GitHub 模型](../models/identity_evidence_v202_v211.py)；[十项测试](../tests/test_identity_evidence_v202_v211.py)。Python/NumPy/SciPy，Monte Carlo 固定随机种子 20261117，每种场景重复 3000 次。

主实验 n=5000，p_main=0.08；独立参考 p_ref=0.06，m=1000/5000/20000。单侧 pooled two-proportion z 检验、α=.05，每档 3000 次重复。模拟检验功效依次为 **0.7176667、0.9910000、0.9993333**；近似 Monte Carlo 95% 半宽依次为 0.016108、0.003380、0.000924。零假设（两组概率都为 0.06）拒绝率分别为 0.051667、0.047667、0.050000。该检验基于渐近 z 近似而非精确双样本检验；参考样本量不足会造成明显功效损失。

**研究背景文献：** Englbrecht et al. PRL 132,050201 (2024), https://doi.org/10.1103/PhysRevLett.132.050201 ；Fleischhauer & Lukin PRA 65,022314 (2002), https://doi.org/10.1103/PhysRevA.65.022314 ；Pollock et al. PRA 97,012127 (2018), https://doi.org/10.1103/PhysRevA.97.012127 。
