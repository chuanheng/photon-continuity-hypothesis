# v2.34：所有量子跳跃的概率加权平均

**版本批次：v2.32–v2.41；日期：2026-11-18。** 标准有限维振幅阻尼/量子轨迹数学模拟，不是永久光子身份理论、真实光学实验或完整相对论 QED。使用 NumPy，固定种子 20261118。实际本地测试 10/10 通过。复现：[GitHub 模型](../models/identity_trajectories_v232_v241.py)、[GitHub 十项测试](../tests/test_identity_trajectories_v232_v241.py)。

非选择性系统演化为 E(ρ)=Σ_iK_iρK_i†=Σ_ip_iρ_i。对 |+> 输入，枚举跳跃与未跳跃两条分支，得到平均密度矩阵与直接计算标准通道的迹距离 0。对 X 正端口的输出概率为 0.9。数学上条件归一化是非线性的，但其按**发生概率**加权后恢复了固定线性 CPTP 量子通道，符合标准开放量子系统理论。

**标准理论参照：** [Quantum trajectory framework for general time-local master equations, Nature Communications (2022)](https://doi.org/10.1038/s41467-022-31533-8)；[Quantum trajectories in monitored systems, PTEP (2026)](https://academic.oup.com/ptep/article/2026/5/052A01/8530537)。
