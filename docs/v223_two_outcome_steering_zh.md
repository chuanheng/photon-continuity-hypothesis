# v2.23：方案 A 的两结果远端投影测量

**研究日期：2026-11-17。** 本轮属于两量子比特 Bell 态、远端 POVM 和非线性 Bloch 玩具规则的解析与合成数值研究。**不是光学实验、超光速通信实验证据或永久光子身份理论。** 已在独立 Python/NumPy/SciPy 环境运行并通过 10 项测试。代码：[模型](../models/identity_remote_steering_v222_v231.py)、[回归测试](../tests/test_identity_remote_steering_v222_v231.py)。

方案 A 选择 Bob 的 X 本征纯态 |+>、|−>，目标权重分别 1/2。对于 |Φ+>，Alice 使用效果算符 E_i=2w_iρ_i^T，即 |+><+| 与 |−><−|，满足 ΣE_i=I、各效果正定（半正定）。联合密度矩阵计算 Alice 测量后 Bob 的未归一化条件态，得到 0.5ρ_+ 与 0.5ρ_-，条件态误差 0。忽略 Alice 测量结果后，Bob 的态为 I/2。

**相关已发表理论：** Simon, Bužek & Gisin (2001), [No-Signaling Condition and Quantum Dynamics](https://doi.org/10.1103/PhysRevLett.87.170405)；Halvorson (2004), [Remote preparation of arbitrary ensembles and quantum bit commitment](https://arxiv.org/abs/quant-ph/0310001)；[IBM Quantum: Hughston–Jozsa–Wootters theorem](https://qiskit.qotlabs.org/learning/courses/general-formulation-of-quantum-information/purifications-and-fidelity/purifications)。
