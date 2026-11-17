# v2.29：非线性强度与远端可见差异的解析关系

**研究日期：2026-11-17。** 本轮属于两量子比特 Bell 态、远端 POVM 和非线性 Bloch 玩具规则的解析与合成数值研究。**不是光学实验、超光速通信实验证据或永久光子身份理论。** 已在独立 Python/NumPy/SciPy 环境运行并通过 10 项测试。代码：[模型](../models/identity_remote_steering_v222_v231.py)、[回归测试](../tests/test_identity_remote_steering_v222_v231.py)。

对本批次两组特殊系综，逐分支应用 N_λ 后解析得到 P_A(X+)=1/2，P_B(X+)=1/2−λ/4，所以两者的差为 λ/4。固定 λ=0、.05、.1、.2、.3、.4、.5 分别得到 B 概率 .5000、.4875、.4750、.4500、.4250、.4000、.3750。只要 λ>0 且其分支规则保留，理论上便有非零的信号容量（在该构造下）。λ→0 可消除冲突，但同时抹去本批次想利用的非线性系综差异；这不构成普遍性的所有非线性理论禁止定理。

**相关已发表理论：** Simon, Bužek & Gisin (2001), [No-Signaling Condition and Quantum Dynamics](https://doi.org/10.1103/PhysRevLett.87.170405)；Halvorson (2004), [Remote preparation of arbitrary ensembles and quantum bit commitment](https://arxiv.org/abs/quant-ph/0310001)；[IBM Quantum: Hughston–Jozsa–Wootters theorem](https://qiskit.qotlabs.org/learning/courses/general-formulation-of-quantum-information/purifications-and-fidelity/purifications)。
