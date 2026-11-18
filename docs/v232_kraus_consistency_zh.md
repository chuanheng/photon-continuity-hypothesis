# v2.32：测量仪器的 Kraus 完备性

**版本批次：v2.32–v2.41；日期：2026-11-18。** 标准有限维振幅阻尼/量子轨迹数学模拟，不是永久光子身份理论、真实光学实验或完整相对论 QED。使用 NumPy，固定种子 20261118。实际本地测试 10/10 通过。复现：[GitHub 模型](../models/identity_trajectories_v232_v241.py)、[GitHub 十项测试](../tests/test_identity_trajectories_v232_v241.py)。

使用标准双能级振幅阻尼 K0=diag(1,sqrt(1−γ))，K1=[[0,sqrtγ],[0,0]]，γ=0.36。直接计算 Σ_iK_i†K_i=I，最大矩阵元误差为 0。由此得到完全正、迹保持的非选择性量子通道。结论只表示该测量仪器模型数学合法，并不指向永久身份。

**标准理论参照：** [Quantum trajectory framework for general time-local master equations, Nature Communications (2022)](https://doi.org/10.1038/s41467-022-31533-8)；[Quantum trajectories in monitored systems, PTEP (2026)](https://academic.oup.com/ptep/article/2026/5/052A01/8530537)。
