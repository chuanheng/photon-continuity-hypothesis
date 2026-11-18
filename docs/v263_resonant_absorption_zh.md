# v2.63：理想共振吸收使光学激发完全转移

**日期：2026-11-18。** 这是标准 Jaynes–Cummings 型单激发空间数值计算，未进行真实实验，不是完整量子电动力学，也未提出永久光子身份的独有动力学。Python/NumPy 本地运行 10 项测试全部通过。[研究模型](../models/identity_light_matter_v262_v271.py) · [十项测试](../tests/test_identity_light_matter_v262_v271.py)。

从 (|p0>+|p1>)/√2 出发，g0=g1=1、Δ=0、t=π/2。解析 U 将每个 |pi> 映至 −i|mi>，物质子空间激发概率数值为 0.9999999999999996，光学子空间概率约 4.25×10^-33。**这说明量子信息可被物质承载，但不说明原光子还在某个隐藏地方作为永久个体存在。**

**基础文献：** [Fleischhauer & Lukin, Quantum memory for photons: Dark-state polaritons (2002)](https://doi.org/10.1103/PhysRevA.65.022314)；[Storage and retrieval of single photons transmitted between remote quantum memories (Nature 2006)](https://www.nature.com/articles/nature04315)；[Jaynes–Cummings model and detuning](https://pmc.ncbi.nlm.nih.gov/articles/PMC12840198/)。
