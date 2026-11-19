# v2.87：标准存储参数漂移导致身份因子估计偏差

**日期：2026-11-19。研究类型：** 五参数二项统计模型的独立参考、Fisher 可辨识性、有限样本和漂移审计。**全属合成数据；不是实际光学测量、永久光子身份的新动力学或 QED 检验。** 本地 NumPy 实际运行 10/10 项测试通过。模型：[GitHub 计算代码](../models/identity_calibration_v282_v291.py)；[GitHub 测试](../tests/test_identity_calibration_v282_v291.py)。参考： [Gate Set Tomography, Quantum 5,557 (2021)](https://quantum-journal.org/papers/q-2021-10-05-557/)；[Tomography of Optical Single-Qubit Quantum Memory (2022)](https://link.springer.com/article/10.1134/S0021364022600951)。

模拟一种不存在新机制的普通参考漂移：参考通道仍测 c=.85，但主实验真正存储参数变为 .83，其余参数照旧。若估计过程仍错误假设共享 c=.85，2000 组蒙特卡洛的 s_hat 平均值约 .78220346，较真实 .8 低 .01779654。这说明即使标定样本量很大，错误的跨实验参数共享仍会使所谓身份参数带系统偏差。**必须交错参考测量、监控时间漂移和构建联合背景模型。**
