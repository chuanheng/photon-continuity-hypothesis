# v1.68：干涉可见度乘积与秩亏

**日期：2026-11-16。** 本轮为有限维光—物质量子态映射与统计辨识的合成数学研究，**不是**完整量子电动力学（QED）计算、真实光学实验或永久光子身份的验证。使用单激发四维 Hilbert 空间，基底为 |p0>,|p1>,|m0>,|m1>；NumPy 模型与十项测试见：[模型](../models/identity_memory_v162_v171.py)、[测试](../tests/test_identity_memory_v162_v171.py)。

取身份指针重叠 s=0.60、普通模式重叠 μ=0.75，在理想单个正端口读出下 P+=(1+sμ)/2=0.725。只观测此概率，允许 s、μ 联合变化时，局部 Fisher 信息秩为 1；两特征值约 5.55×10^-17 与 1.1567398（单次观测）。因此单档无限采样仍不能分别确定两个参数。**注意：** “身份”参数的数学可辨识不等于它具备物理上独立的身份含义。

**对照文献：** Fleischhauer & Lukin (2002), *Quantum memory for photons: Dark-state polaritons*, https://doi.org/10.1103/PhysRevA.65.022314；Ma, Slattery & Tang (2017), *Optical quantum memory based on electromagnetically induced transparency*, https://doi.org/10.1088/2040-8986/19/4/043001 。
