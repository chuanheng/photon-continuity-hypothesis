# v2.25：两种远端选择的无条件统计完全一致

**研究日期：2026-11-17。** 本轮属于两量子比特 Bell 态、远端 POVM 和非线性 Bloch 玩具规则的解析与合成数值研究。**不是光学实验、超光速通信实验证据或永久光子身份理论。** 已在独立 Python/NumPy/SciPy 环境运行并通过 10 项测试。代码：[模型](../models/identity_remote_steering_v222_v231.py)、[回归测试](../tests/test_identity_remote_steering_v222_v231.py)。

对方案 A 和 B，都将 Bob 的条件态按 Alice 测量结果加总：Σ_iw_iρ_i=I/2。两个无条件态之间的迹距离为 0，与 I/2 的数值误差约 1.11×10^-16。因此，在标准量子理论中，若 Alice 不将测量结果传给 Bob，Bob 无法仅用本地测量判断 Alice 选择 A 还是 B。这是本批次的关键对照条件。

**相关已发表理论：** Simon, Bužek & Gisin (2001), [No-Signaling Condition and Quantum Dynamics](https://doi.org/10.1103/PhysRevLett.87.170405)；Halvorson (2004), [Remote preparation of arbitrary ensembles and quantum bit commitment](https://arxiv.org/abs/quant-ph/0310001)；[IBM Quantum: Hughston–Jozsa–Wootters theorem](https://qiskit.qotlabs.org/learning/courses/general-formulation-of-quantum-information/purifications-and-fidelity/purifications)。
