# v2.55：集体耦合满足混合态的量子通道线性性

**日期：2026-11-18。研究性质：** 两个相同玻色子的二维内部标签与单量子比特探针的有限维玩具模型；不是完整光子 QED、实际实验、永久个体身份的证据。** 本地 Python/NumPy 实际执行 10/10 单元测试通过。复现：[统一模型](../models/identity_operator_v252_v261.py)、[十项回归测试](../tests/test_identity_operator_v252_v261.py)。参数 θ=0.8，固定 NumPy RNG 种子 20261118。

输入等权统计混合 ρ_mix=[|00><00|+|11><11|]/2。先混合再耦合并偏迹、与分别耦合后按权重混合，探针两种结果的密度矩阵数值完全相等，矩阵元最大差 0；单次 |00> 输入的探针输出迹约 1。没有 v2.22–v2.31 确定性逐系综非线性模型的仿射性冲突。**局限：** 仅确认本模型标准线性量子动力学，不验证全 QED 守恒或微因果。

**相关文献：** [Quantum Statistics of Identical Particles](https://link.springer.com/article/10.1007/s10701-022-00596-4)；[Second quantization, Scholarpedia](https://www.scholarpedia.org/article/Second_quantization)；[HOM experiment review](https://link.springer.com/article/10.1140/epjd/s10053-022-00525-0)。
