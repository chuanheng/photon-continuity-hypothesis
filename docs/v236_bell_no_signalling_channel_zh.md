# v2.36：纠缠态上的非选择性局域通道与无信号

**版本批次：v2.32–v2.41；日期：2026-11-18。** 标准有限维振幅阻尼/量子轨迹数学模拟，不是永久光子身份理论、真实光学实验或完整相对论 QED。使用 NumPy，固定种子 20261118。实际本地测试 10/10 通过。复现：[GitHub 模型](../models/identity_trajectories_v232_v241.py)、[GitHub 十项测试](../tests/test_identity_trajectories_v232_v241.py)。

取 |Φ+>=(|00>+|11>)/sqrt2，在 Bob 子系统施加标准振幅阻尼 E。Alice 的未条件化约化态在施加通道前后迹距离为 0；Bob 结果等于对他原先 I/2 态直接施加 E，数值迹距离约 1.11e-16。这是非选择性局域 CPTP 通道的标准无信号性质。与上一批次逐纯态分支的非线性 toy rule 不同，此处没有可利用的远端条件态区别。

**标准理论参照：** [Quantum trajectory framework for general time-local master equations, Nature Communications (2022)](https://doi.org/10.1038/s41467-022-31533-8)；[Quantum trajectories in monitored systems, PTEP (2026)](https://academic.oup.com/ptep/article/2026/5/052A01/8530537)。
