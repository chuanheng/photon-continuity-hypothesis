# v2.35：同一个量子通道的两种轨迹展开

**版本批次：v2.32–v2.41；日期：2026-11-18。** 标准有限维振幅阻尼/量子轨迹数学模拟，不是永久光子身份理论、真实光学实验或完整相对论 QED。使用 NumPy，固定种子 20261118。实际本地测试 10/10 通过。复现：[GitHub 模型](../models/identity_trajectories_v232_v241.py)、[GitHub 十项测试](../tests/test_identity_trajectories_v232_v241.py)。

将 Kraus 集合正交旋转为 L±=(K0±K1)/sqrt2。新展开在 |+> 输入下的两项概率分别为 0.80、0.20，而原来的未跳跃/跳跃概率为 0.82、0.18。两种展开中的第一个条件态迹距离约 0.20952909，**明显不同**；但两组所有条件态按各自概率加权后的平均态迹距离仅 5.55e-17。这表明轨迹标签与测量仪器的环境展开方式有关，不能仅从某条“光子轨迹的身份”推断永久个体身份。完整测量记录如果可访问，本来就可区分测量安排；这里比较的是被忽略记录后的同一通道。

**标准理论参照：** [Quantum trajectory framework for general time-local master equations, Nature Communications (2022)](https://doi.org/10.1038/s41467-022-31533-8)；[Quantum trajectories in monitored systems, PTEP (2026)](https://academic.oup.com/ptep/article/2026/5/052A01/8530537)。
