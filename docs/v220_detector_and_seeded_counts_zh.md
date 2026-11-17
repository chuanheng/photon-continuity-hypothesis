# v2.20：探测噪声与固定种子两组采样

**日期：2026-11-17。科学边界：** 本报告属于有限维单量子比特非线性映射的数学反例审查。它**不是光子场论机制、真实实验或永久光子身份的预测/证据**。统一代码：[模型](../models/identity_nonlinear_v212_v221.py)；[十项测试](../tests/test_identity_nonlinear_v212_v221.py)。本地原始版本使用 Python 标准库、固定随机种子，10 项单元测试全部通过。

从 v2.17 的 X 正端口 pA=0.5、pB=0.4 出发，采用探测效率 η=0.85、暗点击 d=0.02，观测点击概率 q=d+(1−d)ηp，得 qA=0.4365，qB=0.3532，相差 0.0833。对应 D_KL(Bern(qB)||Bern(qA))≈0.01438270311。Python random.Random(seed=20261117)，两个组每组 n=1000、顺序采样，实际合成点击计数为 A:464、B:373；合并方差两比例 z≈4.12480863。**这只是单次种子可复现模拟**，不能当成仪器真实数据，也没有做预注册、多重比较和实验系统误差审计。

**参阅：** Simon, Bužek & Gisin (2001), https://doi.org/10.1103/PhysRevLett.87.170405；Hughston–Jozsa–Wootters ensemble theorem 的远端制备讨论 https://arxiv.org/abs/quant-ph/0310001。
