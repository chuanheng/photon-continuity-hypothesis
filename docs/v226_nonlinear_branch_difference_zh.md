# v2.26：非线性逐分支演化使相同态输出不同

**研究日期：2026-11-17。** 本轮属于两量子比特 Bell 态、远端 POVM 和非线性 Bloch 玩具规则的解析与合成数值研究。**不是光学实验、超光速通信实验证据或永久光子身份理论。** 已在独立 Python/NumPy/SciPy 环境运行并通过 10 项测试。代码：[模型](../models/identity_remote_steering_v222_v231.py)、[回归测试](../tests/test_identity_remote_steering_v222_v231.py)。

继续采用 v2.14 的候选规则 N_λ:(x,y,z)→(c x,c y,z)，c=1−2λx²，λ=0.4。假定此规则分别作用于 Bob 被远端制备的每一个条件纯态，然后不依赖 Alice 结果地对输出取平均。方案 A 的输出 Bloch=(0,0,0)；方案 B 的输出 Bloch=(−0.2,0,0)。因此 Bob 的 X 正端口概率依次为 0.50、0.40，输出态迹距离为 0.10。**这一步是非线性模型假设，不是标准量子力学的预言。**

**相关已发表理论：** Simon, Bužek & Gisin (2001), [No-Signaling Condition and Quantum Dynamics](https://doi.org/10.1103/PhysRevLett.87.170405)；Halvorson (2004), [Remote preparation of arbitrary ensembles and quantum bit commitment](https://arxiv.org/abs/quant-ph/0310001)；[IBM Quantum: Hughston–Jozsa–Wootters theorem](https://qiskit.qotlabs.org/learning/courses/general-formulation-of-quantum-information/purifications-and-fidelity/purifications)。
