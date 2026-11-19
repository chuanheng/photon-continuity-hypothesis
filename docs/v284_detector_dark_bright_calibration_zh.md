# v2.84：暗计数与探测效率的两项额外标定

**日期：2026-11-19。研究类型：** 五参数二项统计模型的独立参考、Fisher 可辨识性、有限样本和漂移审计。**全属合成数据；不是实际光学测量、永久光子身份的新动力学或 QED 检验。** 本地 NumPy 实际运行 10/10 项测试通过。模型：[GitHub 计算代码](../models/identity_calibration_v282_v291.py)；[GitHub 测试](../tests/test_identity_calibration_v282_v291.py)。参考： [Gate Set Tomography, Quantum 5,557 (2021)](https://quantum-journal.org/papers/q-2021-10-05-557/)；[Tomography of Optical Single-Qubit Quantum Memory (2022)](https://link.springer.com/article/10.1134/S0021364022600951)。

增加暗参考 p_dark=d=.01，及理想明亮参考 p_bright=d+(1−d)η=.901，均 5000 次。现在五项 Bernoulli 观测对应五参数雅可比满秩，完整 Fisher 矩阵正特征值依次约 2286.27997、20212.49286、51607.36385、87193.66201、510895.55150，因而在给定模型和所有标定独立、可共享条件下局部可辨识。这是形式统计结论，不能排除被遗漏的其他普通物理衰减参数。
