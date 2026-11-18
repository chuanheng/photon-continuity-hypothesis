# v2.54：探针读取集体内部标签的显式概率

**日期：2026-11-18。研究性质：** 两个相同玻色子的二维内部标签与单量子比特探针的有限维玩具模型；不是完整光子 QED、实际实验、永久个体身份的证据。** 本地 Python/NumPy 实际执行 10/10 单元测试通过。复现：[统一模型](../models/identity_operator_v252_v261.py)、[十项回归测试](../tests/test_identity_operator_v252_v261.py)。参数 θ=0.8，固定 NumPy RNG 种子 20261118。

取探针初始 |0>，施加 U=exp[−iθ A⊗Y/2]，θ=0.8，然后测探针 X+。标签 |00> 对应 A 本征值 +1，得到 P_X+=(1+sinθ)/2=0.858678045449761；|11> 对应 -1，得到 P=0.141321954550239；对称 |ψ+>=(|01>+|10>)/sqrt2 对应 0，得到 P=0.5。8×8 酉矩阵数值计算与闭式关系差低于 1e−15。**这是一项普通的内部量条件控制测量，不能由其读数反推出“原来是哪一个光子”。**

**相关文献：** [Quantum Statistics of Identical Particles](https://link.springer.com/article/10.1007/s10701-022-00596-4)；[Second quantization, Scholarpedia](https://www.scholarpedia.org/article/Second_quantization)；[HOM experiment review](https://link.springer.com/article/10.1140/epjd/s10053-022-00525-0)。
