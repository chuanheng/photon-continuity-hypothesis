# v2.78：身份参数与普通存储参数在单读出上不可辨识

**研究日期：2026-11-19。** 本轮是四维单激发光—物质写入/读取与二能级探针的有限维量子信息模拟，**不是 QED 场论、真实光学实验或永久光子身份验证**。本地 NumPy 计算及对应 10 项回归测试均已实际执行通过。统一代码：[GitHub 计算模型](../models/identity_full_sequence_v272_v281.py)，[GitHub 回归测试](../tests/test_identity_full_sequence_v272_v281.py)。

在仅记录光学 X+ 点击事件且探测效率 η=.9、暗计数 d=.01 时，p_click=.01+.99·.9(1+cs cosθ)/2。对 (c,s) 的导数方向为比例于 (s,c)，N=1000 的 Fisher 矩阵为外积，解析秩为 1。数值特征值约 (−2.84×10^-14,886.613067276)，负的微小值仅为浮点舍入误差，并不意味着信息矩阵真正有负特征值。单读出不能分开 c 和 s；即使独立标定它们，也未必赋予 s 永久身份的物理含义。

**标准参考：** Fleischhauer & Lukin (2002), [Quantum memory for photons: Dark-state polaritons](https://doi.org/10.1103/PhysRevA.65.022314)；[Quantum measurement and POVM lecture notes](https://cleve.iqc.uwaterloo.ca/resources/QIC-710-F24/Qic710QuantumInformationTheory2024V3.pdf)。
