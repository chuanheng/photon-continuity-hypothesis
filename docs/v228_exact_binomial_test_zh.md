# v2.28：有限样本精确二项检验的理论能力

**研究日期：2026-11-17。** 本轮属于两量子比特 Bell 态、远端 POVM 和非线性 Bloch 玩具规则的解析与合成数值研究。**不是光学实验、超光速通信实验证据或永久光子身份理论。** 已在独立 Python/NumPy/SciPy 环境运行并通过 10 项测试。代码：[模型](../models/identity_remote_steering_v222_v231.py)、[回归测试](../tests/test_identity_remote_steering_v222_v231.py)。

把方案 A 的正端口概率 0.5 视为完全指定的零假设、方案 B 的 0.4 视为备择；N=1000 次独立测量，采用单侧拒绝低计数、显著性目标 α≤0.05。严格二项分布穷举得到拒绝阈值 K≤473，真实第一类错误概率 0.04684364573775；备择下理论检验功效 0.99999874518。NumPy seed=20261117 的各 1000 次合成计数为 A:485、B:377。**这些是玩具模型的统计能力，不证明理论合法或真实仪器可操作；不能用高功效回避超光速信号冲突。**

**相关已发表理论：** Simon, Bužek & Gisin (2001), [No-Signaling Condition and Quantum Dynamics](https://doi.org/10.1103/PhysRevLett.87.170405)；Halvorson (2004), [Remote preparation of arbitrary ensembles and quantum bit commitment](https://arxiv.org/abs/quant-ph/0310001)；[IBM Quantum: Hughston–Jozsa–Wootters theorem](https://qiskit.qotlabs.org/learning/courses/general-formulation-of-quantum-information/purifications-and-fidelity/purifications)。
