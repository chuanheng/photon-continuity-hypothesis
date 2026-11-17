# v2.22：Bell 态作为远端制备的严格起点

**研究日期：2026-11-17。** 本轮属于两量子比特 Bell 态、远端 POVM 和非线性 Bloch 玩具规则的解析与合成数值研究。**不是光学实验、超光速通信实验证据或永久光子身份理论。** 已在独立 Python/NumPy/SciPy 环境运行并通过 10 项测试。代码：[模型](../models/identity_remote_steering_v222_v231.py)、[回归测试](../tests/test_identity_remote_steering_v222_v231.py)。

取 |Φ+>=(|00>+|11>)/√2，联合态归一化范数在浮点精度内为 1。对 Alice 求偏迹，Bob 的初始约化态为 I/2。此时 Alice 位于任意远端并选择局域测量，而 Bob 在未知 Alice 结果时只拥有最大混合态。这个构造是标准量子信息模型，并未引入真实光子的永久标签。后续所有“远端信号”判断均明确依赖 Alice 可以选择 POVM、Bob 未获知她的结果、但候选非线性演化逐条件纯态分支作用的假设。

**相关已发表理论：** Simon, Bužek & Gisin (2001), [No-Signaling Condition and Quantum Dynamics](https://doi.org/10.1103/PhysRevLett.87.170405)；Halvorson (2004), [Remote preparation of arbitrary ensembles and quantum bit commitment](https://arxiv.org/abs/quant-ph/0310001)；[IBM Quantum: Hughston–Jozsa–Wootters theorem](https://qiskit.qotlabs.org/learning/courses/general-formulation-of-quantum-information/purifications-and-fidelity/purifications)。
