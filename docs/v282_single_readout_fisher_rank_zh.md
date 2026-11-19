# v2.82：单一主读出的五参数秩亏

**日期：2026-11-19。研究类型：** 五参数二项统计模型的独立参考、Fisher 可辨识性、有限样本和漂移审计。**全属合成数据；不是实际光学测量、永久光子身份的新动力学或 QED 检验。** 本地 NumPy 实际运行 10/10 项测试通过。模型：[GitHub 计算代码](../models/identity_calibration_v282_v291.py)；[GitHub 测试](../tests/test_identity_calibration_v282_v291.py)。参考： [Gate Set Tomography, Quantum 5,557 (2021)](https://quantum-journal.org/papers/q-2021-10-05-557/)；[Tomography of Optical Single-Qubit Quantum Memory (2022)](https://link.springer.com/article/10.1134/S0021364022600951)。

定义待估 (v,c,s,η,d)，主实验 p=d+(1−d)η[1+vcs cosθ]/2。设置 (v,c,s,η,d,θ)=(.95,.85,.8,.9,.01,.6)。数值 p=0.693025812621701，光学可见度乘积 vcs=0.646。主实验重复 10000 次的 Fisher 矩阵 F=N∇p∇pᵀ/[p(1−p)]，秩=1，不能分别确定五项参数。这是明确的操作不可辨识性，不论样本量增加多少，单一设置下都无法打破乘积和探测参数的混淆。
