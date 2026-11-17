# v2.10：统计功效与错误物理归因之间的区别

**研究日期：2026-11-17。研究等级：数学/合成统计方法学，不是实际光学实验，不是永久光子身份的预测或验证。** 复现：[GitHub 模型](../models/identity_evidence_v202_v211.py)；[十项测试](../tests/test_identity_evidence_v202_v211.py)。Python/NumPy/SciPy，Monte Carlo 固定随机种子 20261117，每种场景重复 3000 次。

合成候选 p_main=0.08、p_ref=0.06，在 m=1000、5000、20000 时的模拟检验功效为 71.77%、99.10%、99.93%。然而若普通物理背景在主实验中漂移 0.02，而参考仍维持 0.06，未建模共享检验错误拒绝率可达到 98.73%。因此提高统计样本数并不能自行排除系统漂移。若标准模型允许主实验与参考参数不同，则可重拟合同一概率分布，物理层面的独有预测差异仍为零。

**研究背景文献：** Englbrecht et al. PRL 132,050201 (2024), https://doi.org/10.1103/PhysRevLett.132.050201 ；Fleischhauer & Lukin PRA 65,022314 (2002), https://doi.org/10.1103/PhysRevA.65.022314 ；Pollock et al. PRA 97,012127 (2018), https://doi.org/10.1103/PhysRevA.97.012127 。
