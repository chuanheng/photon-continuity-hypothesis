# v2.38：相同输入密度矩阵的不同系综不再分叉

**版本批次：v2.32–v2.41；日期：2026-11-18。** 标准有限维振幅阻尼/量子轨迹数学模拟，不是永久光子身份理论、真实光学实验或完整相对论 QED。使用 NumPy，固定种子 20261118。实际本地测试 10/10 通过。复现：[GitHub 模型](../models/identity_trajectories_v232_v241.py)、[GitHub 十项测试](../tests/test_identity_trajectories_v232_v241.py)。

构造 I/2 的两种纯态系综：Z 本征态 |0>、|1> 各 1/2，以及 X 本征态 |+>、|−> 各 1/2。对各分支施加同一振幅阻尼量子通道后按权重平均，两个输出态迹距离约 1.11e-16。不同于被 v2.31 判定存在无信号冲突的非线性分支规则，固定线性量子通道满足仿射律 E(Σw_iρ_i)=Σw_iE(ρ_i)。这恰恰说明当前“修复后的模型”仍属于普通量子理论。

**标准理论参照：** [Quantum trajectory framework for general time-local master equations, Nature Communications (2022)](https://doi.org/10.1038/s41467-022-31533-8)；[Quantum trajectories in monitored systems, PTEP (2026)](https://academic.oup.com/ptep/article/2026/5/052A01/8530537)。
