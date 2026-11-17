# v2.27：逐分支非线性解释下的无信号违背

**研究日期：2026-11-17。** 本轮属于两量子比特 Bell 态、远端 POVM 和非线性 Bloch 玩具规则的解析与合成数值研究。**不是光学实验、超光速通信实验证据或永久光子身份理论。** 已在独立 Python/NumPy/SciPy 环境运行并通过 10 项测试。代码：[模型](../models/identity_remote_steering_v222_v231.py)、[回归测试](../tests/test_identity_remote_steering_v222_v231.py)。

在 Alice 与 Bob 类空间隔、Alice 可选择方案 A 或 B，且无须向 Bob发送结果的前提下，若 Bob 的局部系统确实逐远端制备的纯态分支遵循 N_0.4，Bob 单独统计 X 正端口可以识别 Alice 选择：P(X+|A)=0.5、P(X+|B)=0.4。Bernoulli KL(B||A)=0.02013551355069 nat/次。只要他们事先共享试验时刻并可多次重复，这一可控统计差异按假设形成超光速信号通道。**谨慎限定：** 这不是已经建成相对论场论或证明现实存在超光速信号；它是在标准远端制备、Born 测量与逐分支确定性非线性规则共存时推导出的理论冲突。

**相关已发表理论：** Simon, Bužek & Gisin (2001), [No-Signaling Condition and Quantum Dynamics](https://doi.org/10.1103/PhysRevLett.87.170405)；Halvorson (2004), [Remote preparation of arbitrary ensembles and quantum bit commitment](https://arxiv.org/abs/quant-ph/0310001)；[IBM Quantum: Hughston–Jozsa–Wootters theorem](https://qiskit.qotlabs.org/learning/courses/general-formulation-of-quantum-information/purifications-and-fidelity/purifications)。
