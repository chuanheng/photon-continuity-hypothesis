# v2.90：统计满秩不等于物理实体得证

**日期：2026-11-19。研究类型：** 五参数二项统计模型的独立参考、Fisher 可辨识性、有限样本和漂移审计。**全属合成数据；不是实际光学测量、永久光子身份的新动力学或 QED 检验。** 本地 NumPy 实际运行 10/10 项测试通过。模型：[GitHub 计算代码](../models/identity_calibration_v282_v291.py)；[GitHub 测试](../tests/test_identity_calibration_v282_v291.py)。参考： [Gate Set Tomography, Quantum 5,557 (2021)](https://quantum-journal.org/papers/q-2021-10-05-557/)；[Tomography of Optical Single-Qubit Quantum Memory (2022)](https://link.springer.com/article/10.1134/S0021364022600951)。

五个形式参数的 Fisher 满秩，只说明在预先指定的五参数模型里它们可局部估计。在量子过程层析与 gate-set tomography 中，还要审查输入态制备、操作、测量（SPAM）和规范自由度，避免把表示自由度或普通环境耦合误读成新增物理量。重要参考 Nielsen 等 2021 的 Gate Set Tomography。当前缺少建立 s 等同于跨吸收再发射永久光子身份的微观守恒理论，也没有验证独立标定真的隔离其他环境自由度。
