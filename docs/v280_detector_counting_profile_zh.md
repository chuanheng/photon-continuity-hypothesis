# v2.80：探测器和有限样本的复合标准模型轮廓

**研究日期：2026-11-19。** 本轮是四维单激发光—物质写入/读取与二能级探针的有限维量子信息模拟，**不是 QED 场论、真实光学实验或永久光子身份验证**。本地 NumPy 计算及对应 10 项回归测试均已实际执行通过。统一代码：[GitHub 计算模型](../models/identity_full_sequence_v272_v281.py)，[GitHub 回归测试](../tests/test_identity_full_sequence_v272_v281.py)。

把 v2.75 的光学 X+ 概率 p=.7806141091 经普通探测效率 η=.9 和暗计数 d=.01 映射为点击概率 q=.7055271711807368。NumPy RNG seed=20261119、n=10000 次 binomial 合成抽样得到 7071 次点击。若错误固定“无额外退相干”的 c=.85,s=1，则基准点击概率 q0=.7680339639759212，KL(Bern(q)||Bern(q0))=.010368707254628726 nat/事件。但允许标准模型设置 c_eff=.68，点击概率逐点一致、最小 KL=0。**固定基准的显著性不意味着永久身份新物理。**

**标准参考：** Fleischhauer & Lukin (2002), [Quantum memory for photons: Dark-state polaritons](https://doi.org/10.1103/PhysRevA.65.022314)；[Quantum measurement and POVM lecture notes](https://cleve.iqc.uwaterloo.ca/resources/QIC-710-F24/Qic710QuantumInformationTheory2024V3.pdf)。
