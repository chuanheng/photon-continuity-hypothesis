# v1.65：身份指针与相干性损失

**日期：2026-11-16。** 本轮为有限维光—物质量子态映射与统计辨识的合成数学研究，**不是**完整量子电动力学（QED）计算、真实光学实验或永久光子身份的验证。使用单激发四维 Hilbert 空间，基底为 |p0>,|p1>,|m0>,|m1>；NumPy 模型与十项测试见：[模型](../models/identity_memory_v162_v171.py)、[测试](../tests/test_identity_memory_v162_v171.py)。

设物质两模式叠加与不可访问的两指针态纠缠，指针内积 s=0.6。将指针迹掉后，两模式非对角相干项缩小 s 倍。以原始最大相干性归一后，得到可见度 0.6。等效的 CPTP 相位翻转量子通道是 E(ρ)=(1+s)ρ/2+(1−s)ZρZ/2。**结论：** 可见度变化只说明发生了路径可区分性或退相干，不证明所谓身份指针是真实的光子永久标签。

**对照文献：** Fleischhauer & Lukin (2002), *Quantum memory for photons: Dark-state polaritons*, https://doi.org/10.1103/PhysRevA.65.022314；Ma, Slattery & Tang (2017), *Optical quantum memory based on electromagnetically induced transparency*, https://doi.org/10.1088/2040-8986/19/4/043001 。
