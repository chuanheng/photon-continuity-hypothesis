# v2.68：物质内部态可通过探针被读取

**日期：2026-11-18。** 这是标准 Jaynes–Cummings 型单激发空间数值计算，未进行真实实验，不是完整量子电动力学，也未提出永久光子身份的独有动力学。Python/NumPy 本地运行 10 项测试全部通过。[研究模型](../models/identity_light_matter_v262_v271.py) · [十项测试](../tests/test_identity_light_matter_v262_v271.py)。

定义内部存储模式差 A=|m0><m0|−|m1><m1|，辅助探针初始 |0>，施加 U=exp[−iθA⊗Y/2]，θ=.8；读探针 X+。物质态 |m0> 给出概率 (1+sin.8)/2=0.858678045449761，|m1> 给出 (1−sin.8)/2=0.14132195455023855。探针完整 8×8 酉性误差 4.44e−16。这代表标准物质内部态的受控探针读出，不能证明吸收前后的光子具有同一永久身份。

**基础文献：** [Fleischhauer & Lukin, Quantum memory for photons: Dark-state polaritons (2002)](https://doi.org/10.1103/PhysRevA.65.022314)；[Storage and retrieval of single photons transmitted between remote quantum memories (Nature 2006)](https://www.nature.com/articles/nature04315)；[Jaynes–Cummings model and detuning](https://pmc.ncbi.nlm.nih.gov/articles/PMC12840198/)。
