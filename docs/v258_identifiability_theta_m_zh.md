# v2.58：耦合强度与内部极化混淆

**日期：2026-11-18。研究性质：** 两个相同玻色子的二维内部标签与单量子比特探针的有限维玩具模型；不是完整光子 QED、实际实验、永久个体身份的证据。** 本地 Python/NumPy 实际执行 10/10 单元测试通过。复现：[统一模型](../models/identity_operator_v252_v261.py)、[十项回归测试](../tests/test_identity_operator_v252_v261.py)。参数 θ=0.8，固定 NumPy RNG 种子 20261118。

假设当前探针 X+ 只依赖内部极化 m=<A> 及未知角度 θ，P+=(1+m sinθ)/2。单个设置下参数梯度为 (sinθ/2,m cosθ/2)，因此 Bernoulli Fisher 信息 F=N∇P ∇P^T/[P(1−P)] 为秩 1（N=1000、m=0.6、θ=0.8）。本次数值两个特征值为 0 和 846.0863466132039。不能仅由这个读数区分“标签分布改变”与“探针耦合标定漂移”；引入其他设置或独立标定是必要的，但也不能证明永久本体身份。

**相关文献：** [Quantum Statistics of Identical Particles](https://link.springer.com/article/10.1007/s10701-022-00596-4)；[Second quantization, Scholarpedia](https://www.scholarpedia.org/article/Second_quantization)；[HOM experiment review](https://link.springer.com/article/10.1140/epjd/s10053-022-00525-0)。
