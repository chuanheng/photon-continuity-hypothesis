# v2.83：可见度与存储相干的独立参考

**日期：2026-11-19。研究类型：** 五参数二项统计模型的独立参考、Fisher 可辨识性、有限样本和漂移审计。**全属合成数据；不是实际光学测量、永久光子身份的新动力学或 QED 检验。** 本地 NumPy 实际运行 10/10 项测试通过。模型：[GitHub 计算代码](../models/identity_calibration_v282_v291.py)；[GitHub 测试](../tests/test_identity_calibration_v282_v291.py)。参考： [Gate Set Tomography, Quantum 5,557 (2021)](https://quantum-journal.org/papers/q-2021-10-05-557/)；[Tomography of Optical Single-Qubit Quantum Memory (2022)](https://link.springer.com/article/10.1134/S0021364022600951)。

假设在同一器件状态下，有两个可信的独立 Bernoulli 标定设置：存储参考 p_c=(1+c)/2=.925；输入可见度参考 p_v=(1+v)/2=.975，每个参考测 5000 次。连同主测量，5 个参数的观测概率雅可比秩从 1 提升至 3。这里的参考通道形式和它们仅依赖一个参数，是强烈的实验假设：实际光源状态制备、测量误差、模式漂移可能违反这种独立性。标定只增加可估参数数目，并未验证身份物理含义。
