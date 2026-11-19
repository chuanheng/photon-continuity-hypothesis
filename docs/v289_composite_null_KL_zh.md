# v2.89：固定标准模型与完整标准环境族的 KL 对照

**日期：2026-11-19。研究类型：** 五参数二项统计模型的独立参考、Fisher 可辨识性、有限样本和漂移审计。**全属合成数据；不是实际光学测量、永久光子身份的新动力学或 QED 检验。** 本地 NumPy 实际运行 10/10 项测试通过。模型：[GitHub 计算代码](../models/identity_calibration_v282_v291.py)；[GitHub 测试](../tests/test_identity_calibration_v282_v291.py)。参考： [Gate Set Tomography, Quantum 5,557 (2021)](https://quantum-journal.org/papers/q-2021-10-05-557/)；[Tomography of Optical Single-Qubit Quantum Memory (2022)](https://link.springer.com/article/10.1134/S0021364022600951)。

对主实验 Bernoulli 点击概率 p=.69302581262，若错误地强制标准模型 s=1 并认为 c、v、η、d 和探针角 θ 都没有遗漏参数，会得到非零 KL=0.00901883647 nats/事件。可是标准量子模型可以完全不包含身份自由度，而容许一个未探测环境带来的普通额外可见度 r=.8，于是所有概率与候选 s=.8 精确一致，轮廓 KL=0。这个零差比任何固定基准显著性都更关键；身份解释没有独有辨识优势。
