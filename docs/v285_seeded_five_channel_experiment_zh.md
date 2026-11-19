# v2.85：固定种子的五通道合成实验

**日期：2026-11-19。研究类型：** 五参数二项统计模型的独立参考、Fisher 可辨识性、有限样本和漂移审计。**全属合成数据；不是实际光学测量、永久光子身份的新动力学或 QED 检验。** 本地 NumPy 实际运行 10/10 项测试通过。模型：[GitHub 计算代码](../models/identity_calibration_v282_v291.py)；[GitHub 测试](../tests/test_identity_calibration_v282_v291.py)。参考： [Gate Set Tomography, Quantum 5,557 (2021)](https://quantum-journal.org/papers/q-2021-10-05-557/)；[Tomography of Optical Single-Qubit Quantum Memory (2022)](https://link.springer.com/article/10.1134/S0021364022600951)。

在主测量 10000 次，存储参考、可见度参考、暗/亮参考各 5000 次条件下，用 NumPy default_rng(seed=20261119) 采样，依次得到点击 [6947,4603,4875,49,4518]。使用解析反演：d_hat=p_dark；η_hat=(p_bright−d_hat)/(1−d_hat)；c_hat=2p_c−1；v_hat=2p_v−1；s_hat=[2(p_main−d_hat)/((1−d_hat)η_hat)−1]/(v_hat c_hat cosθ)。得到 v_hat=.9500,c_hat=.8412,s_hat=.80744537,η_hat=.90264593,d_hat=.0098。属于有限数据的估计，没有真实光子观测。
