# v2.30：避免超光速信号的两类修正及代价

**研究日期：2026-11-17。** 本轮属于两量子比特 Bell 态、远端 POVM 和非线性 Bloch 玩具规则的解析与合成数值研究。**不是光学实验、超光速通信实验证据或永久光子身份理论。** 已在独立 Python/NumPy/SciPy 环境运行并通过 10 项测试。代码：[模型](../models/identity_remote_steering_v222_v231.py)、[回归测试](../tests/test_identity_remote_steering_v222_v231.py)。

修正方案一：让 N_λ 仅依赖 Bob 的无条件密度算符 ρ_B=I/2，而不是 Alice 远端制备的每个条件纯态。则两组输出都为 N_λ(I/2)=I/2，正端口同为 0.5，当前远端信号消失。**但** 它与先本地经典随机混合纯态、逐支演化再取平均的操作结果不同：方案 B 的逐支演化为正端口 0.4，混合一致性问题仍存在。方案二：要求演化满足全部系综分解的仿射一致性，则本批次 A、B 的输出必须相同；任意公共输出与该玩具模型两种目标输出的最大迹距离至少为 0.05。**结论**：修复必须给出完整且自洽的状态和测量操作理论，不能简单改变演化施加对象却保留所有原预测。

**相关已发表理论：** Simon, Bužek & Gisin (2001), [No-Signaling Condition and Quantum Dynamics](https://doi.org/10.1103/PhysRevLett.87.170405)；Halvorson (2004), [Remote preparation of arbitrary ensembles and quantum bit commitment](https://arxiv.org/abs/quant-ph/0310001)；[IBM Quantum: Hughston–Jozsa–Wootters theorem](https://qiskit.qotlabs.org/learning/courses/general-formulation-of-quantum-information/purifications-and-fidelity/purifications)。
