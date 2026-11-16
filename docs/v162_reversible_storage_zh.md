# v1.62：可逆光—物质写入的酉性

**日期：2026-11-16。** 本轮为有限维光—物质量子态映射与统计辨识的合成数学研究，**不是**完整量子电动力学（QED）计算、真实光学实验或永久光子身份的验证。使用单激发四维 Hilbert 空间，基底为 |p0>,|p1>,|m0>,|m1>；NumPy 模型与十项测试见：[模型](../models/identity_memory_v162_v171.py)、[测试](../tests/test_identity_memory_v162_v171.py)。

定义四维耦合酉矩阵 U(θ)，对 (p0,m0) 及 (p1,m1) 分别实施同一实旋转。θ=π/2 时，将两光学基态完全映射到两物质基态。数值核查 ||U†U−I||max=0（浮点计算结果）。这只是允许的单激发数学编码，不是实物存储器。**结论：** 满足酉性不要求存在可跨零光子状态的永久个体编号。

**对照文献：** Fleischhauer & Lukin (2002), *Quantum memory for photons: Dark-state polaritons*, https://doi.org/10.1103/PhysRevA.65.022314；Ma, Slattery & Tang (2017), *Optical quantum memory based on electromagnetically induced transparency*, https://doi.org/10.1088/2040-8986/19/4/043001 。
