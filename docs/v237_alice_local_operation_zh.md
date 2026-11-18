# v2.37：远端局域控制与 Bob 无条件统计

**版本批次：v2.32–v2.41；日期：2026-11-18。** 标准有限维振幅阻尼/量子轨迹数学模拟，不是永久光子身份理论、真实光学实验或完整相对论 QED。使用 NumPy，固定种子 20261118。实际本地测试 10/10 通过。复现：[GitHub 模型](../models/identity_trajectories_v232_v241.py)、[GitHub 十项测试](../tests/test_identity_trajectories_v232_v241.py)。

继承 v2.36 的纠缠态及 Bob 振幅阻尼结果，再仅对 Alice 系统施加 X 酉操作，并重新对 Alice 求偏迹。Bob 的约化态变化迹距离为 0。若 Alice 测量并公开某一结果，Bob 的条件态可以不同，但读取 Alice 的结果需要经典通信；不能把事后筛选的子样本统计直接当作超光速信号。检验只覆盖此有限维方案，不是完整洛伦兹场论的微因果性证明。

**标准理论参照：** [Quantum trajectory framework for general time-local master equations, Nature Communications (2022)](https://doi.org/10.1038/s41467-022-31533-8)；[Quantum trajectories in monitored systems, PTEP (2026)](https://academic.oup.com/ptep/article/2026/5/052A01/8530537)。
