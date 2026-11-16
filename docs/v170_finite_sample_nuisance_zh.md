# v1.70：合成采样与标准模型重拟合

**日期：2026-11-16。** 本轮为有限维光—物质量子态映射与统计辨识的合成数学研究，**不是**完整量子电动力学（QED）计算、真实光学实验或永久光子身份的验证。使用单激发四维 Hilbert 空间，基底为 |p0>,|p1>,|m0>,|m1>；NumPy 模型与十项测试见：[模型](../models/identity_memory_v162_v171.py)、[测试](../tests/test_identity_memory_v162_v171.py)。

在 s=0.6、μ=0.75 下 P+=0.725，固定 Python Random 种子 20261116、10000 次 Bernoulli 采样得到正端口次数 7314。错误将 s=1 固定时 P+=0.875，两个**完全指定**假设 KL(0.725||0.875)=0.0804879063 nat/轮；但允许普通退相干或有效 μ 重新拟合后可以严格取同一 P+=0.725，profile KL=0。**结论：** 固定基准上的显著差异不等于永久身份特有信号。

**对照文献：** Fleischhauer & Lukin (2002), *Quantum memory for photons: Dark-state polaritons*, https://doi.org/10.1103/PhysRevA.65.022314；Ma, Slattery & Tang (2017), *Optical quantum memory based on electromagnetically induced transparency*, https://doi.org/10.1088/2040-8986/19/4/043001 。
