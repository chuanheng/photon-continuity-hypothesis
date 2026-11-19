# v2.79：多时长与失谐、模式选择性的标准解释

**研究日期：2026-11-19。** 本轮是四维单激发光—物质写入/读取与二能级探针的有限维量子信息模拟，**不是 QED 场论、真实光学实验或永久光子身份验证**。本地 NumPy 计算及对应 10 项回归测试均已实际执行通过。统一代码：[GitHub 计算模型](../models/identity_full_sequence_v272_v281.py)，[GitHub 回归测试](../tests/test_identity_full_sequence_v272_v281.py)。

设普通时长依赖退相干 c(t)=exp(−0.3t)，身份候选含常数 s=.8，θ=.6。在 t=.5、1、2 时，光学 X+ 概率分别为 0.7841491787921748、0.7445694646810546、0.6811815156580988。**完全标准**的初始模式可见度 v=.8 加同一 c(t)，预测三点的最大误差 1.22×10^-15。另以写入模型 Δ=.8 产生的读取后剩余光学总占据约 0.9885801，以 g1=.7 的模式选择性读取得到约 0.9926918；这些是读取不完全造成的剩余物质激发，不能直接当成探测器损耗或身份消失。多时长本身不解决这个已明示的初始可见度混淆。

**标准参考：** Fleischhauer & Lukin (2002), [Quantum memory for photons: Dark-state polaritons](https://doi.org/10.1103/PhysRevA.65.022314)；[Quantum measurement and POVM lecture notes](https://cleve.iqc.uwaterloo.ca/resources/QIC-710-F24/Qic710QuantumInformationTheory2024V3.pdf)。
