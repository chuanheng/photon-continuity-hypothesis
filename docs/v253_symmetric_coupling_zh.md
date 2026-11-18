# v2.53：符合交换对称性的集体内部量耦合

**日期：2026-11-18。研究性质：** 两个相同玻色子的二维内部标签与单量子比特探针的有限维玩具模型；不是完整光子 QED、实际实验、永久个体身份的证据。** 本地 Python/NumPy 实际执行 10/10 单元测试通过。复现：[统一模型](../models/identity_operator_v252_v261.py)、[十项回归测试](../tests/test_identity_operator_v252_v261.py)。参数 θ=0.8，固定 NumPy RNG 种子 20261118。

定义交换算符 S，单槽位 O=Z⊗I，与 S 的对易子 Frobenius 范数为 2.8284271247461903；集体量 A=(Z⊗I+I⊗Z)/2 满足 [A,S]=0。探针哈密顿量的无量纲耦合 H_int=A⊗Y_probe 也满足 [H_int,S⊗I_probe]=0。这说明可以合法构造**交换不变的内部量探针**，但其中 A 是常规集体二能级内部量，不是永久粒子编号。

**相关文献：** [Quantum Statistics of Identical Particles](https://link.springer.com/article/10.1007/s10701-022-00596-4)；[Second quantization, Scholarpedia](https://www.scholarpedia.org/article/Second_quantization)；[HOM experiment review](https://link.springer.com/article/10.1140/epjd/s10053-022-00525-0)。
