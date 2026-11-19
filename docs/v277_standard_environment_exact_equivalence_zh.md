# v2.77：完整读出下的标准量子环境等价

**研究日期：2026-11-19。** 本轮是四维单激发光—物质写入/读取与二能级探针的有限维量子信息模拟，**不是 QED 场论、真实光学实验或永久光子身份验证**。本地 NumPy 计算及对应 10 项回归测试均已实际执行通过。统一代码：[GitHub 计算模型](../models/identity_full_sequence_v272_v281.py)，[GitHub 回归测试](../tests/test_identity_full_sequence_v272_v281.py)。

把包含“身份因子”的模型设置为普通退相干 c=.85、s=.8，与完全不含身份的标准模型 c_eff=.68、s=1 比较。本次已计算的光学 X+、探针 X+、两光学模式概率、联合 X+×X+ 以及剩余光学总占据，**六项读数最大绝对差均为零**。由于两模型在探针之前的密度矩阵已经完全相同，后面施加相同的任意量子通道或 POVM 都不能把它们区分开；这比“一个 Bernoulli 概率凑巧相等”更强。要产生独有新物理必须引入与普通 D_{cs} 不同的明确动力学。

**标准参考：** Fleischhauer & Lukin (2002), [Quantum memory for photons: Dark-state polaritons](https://doi.org/10.1103/PhysRevA.65.022314)；[Quantum measurement and POVM lecture notes](https://cleve.iqc.uwaterloo.ca/resources/QIC-710-F24/Qic710QuantumInformationTheory2024V3.pdf)。
