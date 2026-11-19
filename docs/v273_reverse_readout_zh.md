# v2.73：再发射的逆酉演化

**研究日期：2026-11-19。** 本轮是四维单激发光—物质写入/读取与二能级探针的有限维量子信息模拟，**不是 QED 场论、真实光学实验或永久光子身份验证**。本地 NumPy 计算及对应 10 项回归测试均已实际执行通过。统一代码：[GitHub 计算模型](../models/identity_full_sequence_v272_v281.py)，[GitHub 回归测试](../tests/test_identity_full_sequence_v272_v281.py)。

令写入后存储态 ρ_m=Wρ_inW†，执行读取 W†ρ_mW。在没有探针和退相干的理想基准中，读取后状态与原光学输入态的迹距离 4.463374267×10^-16。该结果说明理想逆演化在单激发空间内恢复量子态；不能证明输出的场激发与输入光子是同一个永久个体。加入退相干和探针后回读不再完全恢复。

**标准参考：** Fleischhauer & Lukin (2002), [Quantum memory for photons: Dark-state polaritons](https://doi.org/10.1103/PhysRevA.65.022314)；[Quantum measurement and POVM lecture notes](https://cleve.iqc.uwaterloo.ca/resources/QIC-710-F24/Qic710QuantumInformationTheory2024V3.pdf)。
