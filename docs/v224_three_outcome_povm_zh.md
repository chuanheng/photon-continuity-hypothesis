# v2.24：方案 B 的三结果 POVM 与合法性

**研究日期：2026-11-17。** 本轮属于两量子比特 Bell 态、远端 POVM 和非线性 Bloch 玩具规则的解析与合成数值研究。**不是光学实验、超光速通信实验证据或永久光子身份理论。** 已在独立 Python/NumPy/SciPy 环境运行并通过 10 项测试。代码：[模型](../models/identity_remote_steering_v222_v231.py)、[回归测试](../tests/test_identity_remote_steering_v222_v231.py)。

方案 B 选择三个纯态，其 Bloch 向量分别为 (1,0,0)、(−1/2,0,√3/2)、(−1/2,0,−√3/2)，权重各为 1/3。构造 Alice 的三结果效果算符 E_i=(2/3)ρ_i^T。每个 E_i 均半正定，其最小特征值数值约为 0，ΣE_i=I 的最大矩阵元误差 1.11×10^-16。通过显式 Bell 关联计算得到 Bob 的三个未归一化条件态 w_iρ_i，误差 0。故它不是人为写出无法由纠缠测量实现的系综，而是一组数学上合法的远端制备 POVM。

**相关已发表理论：** Simon, Bužek & Gisin (2001), [No-Signaling Condition and Quantum Dynamics](https://doi.org/10.1103/PhysRevLett.87.170405)；Halvorson (2004), [Remote preparation of arbitrary ensembles and quantum bit commitment](https://arxiv.org/abs/quant-ph/0310001)；[IBM Quantum: Hughston–Jozsa–Wootters theorem](https://qiskit.qotlabs.org/learning/courses/general-formulation-of-quantum-information/purifications-and-fidelity/purifications)。
