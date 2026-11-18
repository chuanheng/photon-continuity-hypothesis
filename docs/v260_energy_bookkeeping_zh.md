# v2.60：探针驱动耦合的能量账本问题

**日期：2026-11-18。研究性质：** 两个相同玻色子的二维内部标签与单量子比特探针的有限维玩具模型；不是完整光子 QED、实际实验、永久个体身份的证据。** 本地 Python/NumPy 实际执行 10/10 单元测试通过。复现：[统一模型](../models/identity_operator_v252_v261.py)、[十项回归测试](../tests/test_identity_operator_v252_v261.py)。参数 θ=0.8，固定 NumPy RNG 种子 20261118。

取候选无量纲相互作用 H_int=A⊗Y_probe；探针自由能代理 H_probe=I_label⊗Z_probe。计算 ||[H_int,H_probe]||_F=4，不满足该探针自由能单独守恒。因此实现这一耦合需要在完整系统动力学中显式考虑外部驱动、介质交换能量或其它补偿，而不能因 H_int 是厄米且交换不变，就声称“所有能量动量守恒条件自动成立”。还未构造洛伦兹协变的局域相互作用密度、规范不变的光子场耦合或完整总能量预算。

**相关文献：** [Quantum Statistics of Identical Particles](https://link.springer.com/article/10.1007/s10701-022-00596-4)；[Second quantization, Scholarpedia](https://www.scholarpedia.org/article/Second_quantization)；[HOM experiment review](https://link.springer.com/article/10.1140/epjd/s10053-022-00525-0)。
