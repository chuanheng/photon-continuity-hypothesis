# v2.76：探针反作用是普通退相干，而非身份专属信号

**研究日期：2026-11-19。** 本轮是四维单激发光—物质写入/读取与二能级探针的有限维量子信息模拟，**不是 QED 场论、真实光学实验或永久光子身份验证**。本地 NumPy 计算及对应 10 项回归测试均已实际执行通过。统一代码：[GitHub 计算模型](../models/identity_full_sequence_v272_v281.py)，[GitHub 回归测试](../tests/test_identity_full_sequence_v272_v281.py)。

固定 c=.85、s=.8，只改变探针耦合角 θ，从 0 改到 0.6。光学 X+ 概率因探针平均反作用降低 0.05938589093070945。探针 X+ 概率 0.5，联合 X+ 与探针 X+ 概率相对边际概率乘积的差只有 7.22×10^-16，表示该特定对称制备与双 X 读数并无额外统计相关信息。**这一结果仅限所选择的探针基与观测设置，不说明所有探针测量都没有联合相关性。**

**标准参考：** Fleischhauer & Lukin (2002), [Quantum memory for photons: Dark-state polaritons](https://doi.org/10.1103/PhysRevA.65.022314)；[Quantum measurement and POVM lecture notes](https://cleve.iqc.uwaterloo.ca/resources/QIC-710-F24/Qic710QuantumInformationTheory2024V3.pdf)。
