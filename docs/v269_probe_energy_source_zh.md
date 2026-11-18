# v2.69：探针耦合与能量来源审查

**日期：2026-11-18。** 这是标准 Jaynes–Cummings 型单激发空间数值计算，未进行真实实验，不是完整量子电动力学，也未提出永久光子身份的独有动力学。Python/NumPy 本地运行 10 项测试全部通过。[研究模型](../models/identity_light_matter_v262_v271.py) · [十项测试](../tests/test_identity_light_matter_v262_v271.py)。

令 H_probe=I_4⊗Z_probe、H_int=A⊗Y_probe。数值 Frobenius 范数 ||[H_int,H_probe]||_F=4，故探针自由能不在耦合作用下单独守恒。可将其理解为外部驱动的有效相互作用，但**不能在未给出驱动、物质、探针的完整能量账本之前宣称孤立装置总能量守恒**。当前离规范不变的光学 QED 微观相互作用还存在明确缺口。

**基础文献：** [Fleischhauer & Lukin, Quantum memory for photons: Dark-state polaritons (2002)](https://doi.org/10.1103/PhysRevA.65.022314)；[Storage and retrieval of single photons transmitted between remote quantum memories (Nature 2006)](https://www.nature.com/articles/nature04315)；[Jaynes–Cummings model and detuning](https://pmc.ncbi.nlm.nih.gov/articles/PMC12840198/)。
