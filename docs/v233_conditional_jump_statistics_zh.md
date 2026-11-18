# v2.33：归一化条件态与量子跳跃概率

**版本批次：v2.32–v2.41；日期：2026-11-18。** 标准有限维振幅阻尼/量子轨迹数学模拟，不是永久光子身份理论、真实光学实验或完整相对论 QED。使用 NumPy，固定种子 20261118。实际本地测试 10/10 通过。复现：[GitHub 模型](../models/identity_trajectories_v232_v241.py)、[GitHub 十项测试](../tests/test_identity_trajectories_v232_v241.py)。

取初始 |+>=(|0>+|1>)/sqrt2。结果 i 的发生概率 p_i=Tr(K_iρK_i†)，条件态 ρ_i=K_iρK_i†/p_i。实际计算：p_jump=0.18、p_no_jump=0.82，两者之和为 1（数值误差约 2.2e-16）；两个已发生结果的条件态迹均为 1。因 p_i 依赖输入态，归一化后的条件更新对 ρ 一般是非线性的；这种非线性是标准量子测量的条件化，不是新动力学。

**标准理论参照：** [Quantum trajectory framework for general time-local master equations, Nature Communications (2022)](https://doi.org/10.1038/s41467-022-31533-8)；[Quantum trajectories in monitored systems, PTEP (2026)](https://academic.oup.com/ptep/article/2026/5/052A01/8530537)。
