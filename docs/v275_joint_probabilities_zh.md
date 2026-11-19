# v2.75：输入—存储—探针—再发射的完整联合概率

**研究日期：2026-11-19。** 本轮是四维单激发光—物质写入/读取与二能级探针的有限维量子信息模拟，**不是 QED 场论、真实光学实验或永久光子身份验证**。本地 NumPy 计算及对应 10 项回归测试均已实际执行通过。统一代码：[GitHub 计算模型](../models/identity_full_sequence_v272_v281.py)，[GitHub 回归测试](../tests/test_identity_full_sequence_v272_v281.py)。

四维物质/光学系统附加二能级探针，先写入 W，再对模式施加 D_{cs}，然后以 U_p=exp[−i θ A⊗Y/2] 耦合探针，A=diag(0,0,1,−1)，θ=.6，最后用 W† 读取。计算输出：光学 X+ 概率 0.7806141090692893，探针 X+ 概率约 0.5，光学模式 0、1 的非条件概率各约 0.5，联合事件 P(光学 X+ 且探针 X+)≈0.39030705453464476。光学 X+ 解析式 P=(1+cs cosθ)/2 与数值相差约 1.3×10^-15。**这是标准量子仪器模型，非真实测量。**

**标准参考：** Fleischhauer & Lukin (2002), [Quantum memory for photons: Dark-state polaritons](https://doi.org/10.1103/PhysRevA.65.022314)；[Quantum measurement and POVM lecture notes](https://cleve.iqc.uwaterloo.ca/resources/QIC-710-F24/Qic710QuantumInformationTheory2024V3.pdf)。
