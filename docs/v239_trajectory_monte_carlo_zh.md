# v2.39：20,000 次量子轨迹标签的 Monte Carlo 检验

**版本批次：v2.32–v2.41；日期：2026-11-18。** 标准有限维振幅阻尼/量子轨迹数学模拟，不是永久光子身份理论、真实光学实验或完整相对论 QED。使用 NumPy，固定种子 20261118。实际本地测试 10/10 通过。复现：[GitHub 模型](../models/identity_trajectories_v232_v241.py)、[GitHub 十项测试](../tests/test_identity_trajectories_v232_v241.py)。

从 v2.33 的两条量子轨迹结局概率 (0.82,0.18)，采用 NumPy default_rng(seed=20261118) 进行 n=20000 的 multinomial 抽样。实际取得跳跃 3593 次、未跳跃 16407 次，对应跳跃率 0.17965；理论期望跳跃数为 3600。合成结果是可复现实验代码的随机性检验，不是光子探测器的真实计数。

**标准理论参照：** [Quantum trajectory framework for general time-local master equations, Nature Communications (2022)](https://doi.org/10.1038/s41467-022-31533-8)；[Quantum trajectories in monitored systems, PTEP (2026)](https://academic.oup.com/ptep/article/2026/5/052A01/8530537)。
