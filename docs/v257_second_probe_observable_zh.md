# v2.57：相同平均集体量但不同分布可被区分

**日期：2026-11-18。研究性质：** 两个相同玻色子的二维内部标签与单量子比特探针的有限维玩具模型；不是完整光子 QED、实际实验、永久个体身份的证据。** 本地 Python/NumPy 实际执行 10/10 单元测试通过。复现：[统一模型](../models/identity_operator_v252_v261.py)、[十项回归测试](../tests/test_identity_operator_v252_v261.py)。参数 θ=0.8，固定 NumPy RNG 种子 20261118。

比较合法对称纯态 |ψ+>=(|01>+|10>)/sqrt2 与等权混合态 ρ_mix=[|00><00|+|11><11|]/2。二者集体期望值 <A> 都为 0，因此探针 X+ 概率均为 0.5。然而探针 Z+ 概率不同：|ψ+> 为 1，混合态为 (1+cos0.8)/2=0.848353354673582。两者差 0.151646645326417。这体现探针可检测内部量**分布的二阶信息**，但它仍属于标准集体自旋/内部模式统计。

**相关文献：** [Quantum Statistics of Identical Particles](https://link.springer.com/article/10.1007/s10701-022-00596-4)；[Second quantization, Scholarpedia](https://www.scholarpedia.org/article/Second_quantization)；[HOM experiment review](https://link.springer.com/article/10.1140/epjd/s10053-022-00525-0)。
