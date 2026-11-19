# v2.86：Fisher 精度与蒙特卡洛覆盖率复核

**日期：2026-11-19。研究类型：** 五参数二项统计模型的独立参考、Fisher 可辨识性、有限样本和漂移审计。**全属合成数据；不是实际光学测量、永久光子身份的新动力学或 QED 检验。** 本地 NumPy 实际运行 10/10 项测试通过。模型：[GitHub 计算代码](../models/identity_calibration_v282_v291.py)；[GitHub 测试](../tests/test_identity_calibration_v282_v291.py)。参考： [Gate Set Tomography, Quantum 5,557 (2021)](https://quantum-journal.org/papers/q-2021-10-05-557/)；[Tomography of Optical Single-Qubit Quantum Memory (2022)](https://link.springer.com/article/10.1134/S0021364022600951)。

在上述五通道模型里，利用完整 Fisher 信息矩阵逆元得到 s 的局部标准误 sqrt[(F^-1)_ss]=.0206025977100884。另用 RNG 同种子串行运行 2000 组独立合成试验及解析反演，s 估计的样本标准差为 .020485795226444874；以理论 s=.8 为真值、使用固定 Fisher 标准误的对称 ±1.96 SE 覆盖率为 .953（2000 次）。**这不是对所有参数边界、SPAM 或真实漂移情形的置信区间有效性保证**，只是模型内有限样本一致性检查。
