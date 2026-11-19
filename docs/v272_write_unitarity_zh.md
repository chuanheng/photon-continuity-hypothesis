# v2.72：写入操作的酉性与物质存储

**研究日期：2026-11-19。** 本轮是四维单激发光—物质写入/读取与二能级探针的有限维量子信息模拟，**不是 QED 场论、真实光学实验或永久光子身份验证**。本地 NumPy 计算及对应 10 项回归测试均已实际执行通过。统一代码：[GitHub 计算模型](../models/identity_full_sequence_v272_v281.py)，[GitHub 回归测试](../tests/test_identity_full_sequence_v272_v281.py)。

构造 H=Σ_i g_i(|p_i><m_i|+|m_i><p_i|)+ΔΣ_i|m_i><m_i|，在 g0=g1=1,Δ=0,t=π/2 下计算写入 W=exp(−iHt)。数值酉性最大矩阵元误差 4.4408920985×10^-16。初态 (|p0>+|p1>)/√2 的物质子空间占据概率为 0.9999999999999993。结论：理想模型的可逆信息存储由标准量子理论解释；存储不提供永久光子编号。

**标准参考：** Fleischhauer & Lukin (2002), [Quantum memory for photons: Dark-state polaritons](https://doi.org/10.1103/PhysRevA.65.022314)；[Quantum measurement and POVM lecture notes](https://cleve.iqc.uwaterloo.ca/resources/QIC-710-F24/Qic710QuantumInformationTheory2024V3.pdf)。
