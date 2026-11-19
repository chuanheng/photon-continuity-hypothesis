# v2.74：普通存储退相干与附加身份参数的合成

**研究日期：2026-11-19。** 本轮是四维单激发光—物质写入/读取与二能级探针的有限维量子信息模拟，**不是 QED 场论、真实光学实验或永久光子身份验证**。本地 NumPy 计算及对应 10 项回归测试均已实际执行通过。统一代码：[GitHub 计算模型](../models/identity_full_sequence_v272_v281.py)，[GitHub 回归测试](../tests/test_identity_full_sequence_v272_v281.py)。

以普通物质存储的相干系数 c=.85，假设额外“身份因子”s=.8。模型定义整体退相干通道 D_{cs}(ρ)=[(1+cs)ρ+(1−cs)Z_modeρZ_mode]/2，其有效参数 cs=.68。因为 cs∈[−1,1]，该随机酉通道 CPTP。完成探针及读取后，全系统归一化迹为 0.9999999999999984。关键是此处没有独立的身份作用，它只在数值上乘进普通退相干系数；这会形成严格的参数混淆。

**标准参考：** Fleischhauer & Lukin (2002), [Quantum memory for photons: Dark-state polaritons](https://doi.org/10.1103/PhysRevA.65.022314)；[Quantum measurement and POVM lecture notes](https://cleve.iqc.uwaterloo.ca/resources/QIC-710-F24/Qic710QuantumInformationTheory2024V3.pdf)。
