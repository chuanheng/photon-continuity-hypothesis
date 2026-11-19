# v2.88：四个探针角度仍可被标准环境可见度重标记

**日期：2026-11-19。研究类型：** 五参数二项统计模型的独立参考、Fisher 可辨识性、有限样本和漂移审计。**全属合成数据；不是实际光学测量、永久光子身份的新动力学或 QED 检验。** 本地 NumPy 实际运行 10/10 项测试通过。模型：[GitHub 计算代码](../models/identity_calibration_v282_v291.py)；[GitHub 测试](../tests/test_identity_calibration_v282_v291.py)。参考： [Gate Set Tomography, Quantum 5,557 (2021)](https://quantum-journal.org/papers/q-2021-10-05-557/)；[Tomography of Optical Single-Qubit Quantum Memory (2022)](https://link.springer.com/article/10.1134/S0021364022600951)。

令 θ 取 0、.3、.6、.9，候选主光学输出 P=(1+v c s cosθ)/2。四个概率分别 .823、.80857368599、.76658340362、.70078001975。若标准模型允许普通额外环境可见度 r=s=.8，表达式 P_standard=(1+v c r cosθ)/2，四项逐一完全相同，最大绝对差 0。若改写 v_eff=v s 也是数学上等价的，但只有当 v 未被独立、可信约束时才应把 v_eff 当作自由输入参数。**即使 v、c 已独立标定，允许另一个标准物理环境系数 r 仍能复制 s。**
