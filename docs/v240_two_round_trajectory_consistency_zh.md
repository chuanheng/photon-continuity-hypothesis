# v2.40：连续两次通道与分支平均一致

**版本批次：v2.32–v2.41；日期：2026-11-18。** 标准有限维振幅阻尼/量子轨迹数学模拟，不是永久光子身份理论、真实光学实验或完整相对论 QED。使用 NumPy，固定种子 20261118。实际本地测试 10/10 通过。复现：[GitHub 模型](../models/identity_trajectories_v232_v241.py)、[GitHub 十项测试](../tests/test_identity_trajectories_v232_v241.py)。

对同一初始 |+> 态，先应用标准振幅阻尼 E，再应用 E，直接得到 E²(ρ)。另一计算按第一次跳跃/未跳跃结果枚举各条件态、按真实概率加权后再施加 E。两条计算路径的输出迹距离约 1.39e-17；两次通道之后的 X 正端口概率为 0.82。此处默认每次均使用同一个固定的 Markov CPTP 通道，**不能由这个例子推断所有有记忆环境都满足两步半群条件**。

**标准理论参照：** [Quantum trajectory framework for general time-local master equations, Nature Communications (2022)](https://doi.org/10.1038/s41467-022-31533-8)；[Quantum trajectories in monitored systems, PTEP (2026)](https://academic.oup.com/ptep/article/2026/5/052A01/8530537)。
