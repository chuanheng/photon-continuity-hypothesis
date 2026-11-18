# v2.52：不可访问内部标签与可观测操作代数

**日期：2026-11-18。研究性质：** 两个相同玻色子的二维内部标签与单量子比特探针的有限维玩具模型；不是完整光子 QED、实际实验、永久个体身份的证据。** 本地 Python/NumPy 实际执行 10/10 单元测试通过。复现：[统一模型](../models/identity_operator_v252_v261.py)、[十项回归测试](../tests/test_identity_operator_v252_v261.py)。参数 θ=0.8，固定 NumPy RNG 种子 20261118。

两个标签的完整空间维数 4；对称玻色子子空间秩为 3。若制备及操作仅允许 I_label⊗O_probe，且没有标签—探针耦合，则无论标签处于 |00> 还是 |11>，初态 |0> 探针的约化密度矩阵相同，最大元素差 0。这是在**规定可访问操作代数下**的不可观测性陈述，不是“标签不存在”的证明；若扩展操作集，须重新判断。

**相关文献：** [Quantum Statistics of Identical Particles](https://link.springer.com/article/10.1007/s10701-022-00596-4)；[Second quantization, Scholarpedia](https://www.scholarpedia.org/article/Second_quantization)；[HOM experiment review](https://link.springer.com/article/10.1140/epjd/s10053-022-00525-0)。
