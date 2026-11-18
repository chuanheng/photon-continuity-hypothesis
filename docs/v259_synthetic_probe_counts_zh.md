# v2.59：1000 次合成探针计数与理论可区分性

**日期：2026-11-18。研究性质：** 两个相同玻色子的二维内部标签与单量子比特探针的有限维玩具模型；不是完整光子 QED、实际实验、永久个体身份的证据。** 本地 Python/NumPy 实际执行 10/10 单元测试通过。复现：[统一模型](../models/identity_operator_v252_v261.py)、[十项回归测试](../tests/test_identity_operator_v252_v261.py)。参数 θ=0.8，固定 NumPy RNG 种子 20261118。

取 v2.54 的两组完全指定标签输入：|00> 与 |11>，其探针 X+ 概率分别为 0.858678045449761、0.141321954550239。NumPy default_rng(seed=20261118)，每组分别进行 N=1000 的 binomial 抽样，得到 X+ 次数 858 和 153。两指定模型的单次 Bernoulli KL(D(P_00)||P_11)=1.2943638995390043 nats。这个巨大的统计差异说明能测量普通集体内部量，**绝非永久身份独有证据，也不代表真实光学样本**。

**相关文献：** [Quantum Statistics of Identical Particles](https://link.springer.com/article/10.1007/s10701-022-00596-4)；[Second quantization, Scholarpedia](https://www.scholarpedia.org/article/Second_quantization)；[HOM experiment review](https://link.springer.com/article/10.1140/epjd/s10053-022-00525-0)。
