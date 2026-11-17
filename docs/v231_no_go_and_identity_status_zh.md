# v2.31：候选机制的一致性判决及永久身份状态

**研究日期：2026-11-17。** 本轮属于两量子比特 Bell 态、远端 POVM 和非线性 Bloch 玩具规则的解析与合成数值研究。**不是光学实验、超光速通信实验证据或永久光子身份理论。** 已在独立 Python/NumPy/SciPy 环境运行并通过 10 项测试。代码：[模型](../models/identity_remote_steering_v222_v231.py)、[回归测试](../tests/test_identity_remote_steering_v222_v231.py)。

v2.22–v2.30 构造了标准合法的 Alice 远端两种 POVM，Bob 的输入都是 I/2；如果同时要求 v2.14 的确定性非线性规则逐远端制备的纯态分支演化，Bob 的结果可以识别 Alice 的测量选择，因而违反通常无超光速信号原则。**在这一组明确假设下，拒绝该候选作为自洽物理理论。** 这个结论不会自动排除所有非线性或随机量子理论，更不会证明任何“永久身份”机制不存在。v2.14 映射从未由光子身份微观动力学推导；目前没有新的、物理一致且身份专属的可证伪预测，也无真实光学实验数据。后续重点应转向一致性优先的替代机制，而不是继续统计优化这个已暴露严重冲突的规则。

**相关已发表理论：** Simon, Bužek & Gisin (2001), [No-Signaling Condition and Quantum Dynamics](https://doi.org/10.1103/PhysRevLett.87.170405)；Halvorson (2004), [Remote preparation of arbitrary ensembles and quantum bit commitment](https://arxiv.org/abs/quant-ph/0310001)；[IBM Quantum: Hughston–Jozsa–Wootters theorem](https://qiskit.qotlabs.org/learning/courses/general-formulation-of-quantum-information/purifications-and-fidelity/purifications)。
