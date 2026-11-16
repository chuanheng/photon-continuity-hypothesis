# v1.69：独立 HOM 标定恢复局部参数可辨识

**日期：2026-11-16。** 本轮为有限维光—物质量子态映射与统计辨识的合成数学研究，**不是**完整量子电动力学（QED）计算、真实光学实验或永久光子身份的验证。使用单激发四维 Hilbert 空间，基底为 |p0>,|p1>,|m0>,|m1>；NumPy 模型与十项测试见：[模型](../models/identity_memory_v162_v171.py)、[测试](../tests/test_identity_memory_v162_v171.py)。

假设独立 HOM 参考可以测到主实验同一个 μ，理想符合概率 (1−μ²)/2。主实验采用 1 次理想正端口测量作为 Fisher 信息单位，HOM 参考计数 1000 次。联合信息矩阵特征值约 0.7052324 与 3291.88008，行列式 2321.5405>0，局部满秩。**重要限制：** 这里只对一个主实验单位加 1000 个 HOM 参考计数，不是实验最佳样本分配，也没有有限样本置信覆盖率。不能把统计意义的 s 与真实永久身份等同。

**对照文献：** Fleischhauer & Lukin (2002), *Quantum memory for photons: Dark-state polaritons*, https://doi.org/10.1103/PhysRevA.65.022314；Ma, Slattery & Tang (2017), *Optical quantum memory based on electromagnetically induced transparency*, https://doi.org/10.1088/2040-8986/19/4/043001 。
