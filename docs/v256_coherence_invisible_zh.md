# v2.56：当前可访问操作不能读取隐藏相干性

**日期：2026-11-18。研究性质：** 两个相同玻色子的二维内部标签与单量子比特探针的有限维玩具模型；不是完整光子 QED、实际实验、永久个体身份的证据。** 本地 Python/NumPy 实际执行 10/10 单元测试通过。复现：[统一模型](../models/identity_operator_v252_v261.py)、[十项回归测试](../tests/test_identity_operator_v252_v261.py)。参数 θ=0.8，固定 NumPy RNG 种子 20261118。

比较合法对称纯态 (|00>+|11>)/sqrt2 与合法的混合态 [|00><00|+|11><11|]/2。它们的标签子系统确实不同，但 H_int=A⊗Y 在 A 本征基中对角，单独对标签求迹后，所有当前探针测量对应的输出状态迹距离约 1.25e−16。**证明范围：** 这一具体耦合及其探针读出不能读取 |00> 与 |11> 间的相干相位；它不是对任意未来耦合的普遍不可观测定理。

**相关文献：** [Quantum Statistics of Identical Particles](https://link.springer.com/article/10.1007/s10701-022-00596-4)；[Second quantization, Scholarpedia](https://www.scholarpedia.org/article/Second_quantization)；[HOM experiment review](https://link.springer.com/article/10.1140/epjd/s10053-022-00525-0)。
