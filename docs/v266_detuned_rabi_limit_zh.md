# v2.66：失谐抑制光—物质最大转移

**日期：2026-11-18。** 这是标准 Jaynes–Cummings 型单激发空间数值计算，未进行真实实验，不是完整量子电动力学，也未提出永久光子身份的独有动力学。Python/NumPy 本地运行 10 项测试全部通过。[研究模型](../models/identity_light_matter_v262_v271.py) · [十项测试](../tests/test_identity_light_matter_v262_v271.py)。

在每个二态交换子空间，H=[[0,g],[g,Δ]]，从光学初态出发，物质激发概率 P_m(t)=[g²/(g²+(Δ/2)²)]sin²(√(g²+(Δ/2)²)t)。设 g=1,Δ=.8，转移上界 1/1.16=0.8620689655172413，最优首次时刻 t=π/(2√1.16)=1.4584477755572458；数值矩阵指数验证 0.862068965517241。它完全是标准失谐 Rabi 动力学。

**基础文献：** [Fleischhauer & Lukin, Quantum memory for photons: Dark-state polaritons (2002)](https://doi.org/10.1103/PhysRevA.65.022314)；[Storage and retrieval of single photons transmitted between remote quantum memories (Nature 2006)](https://www.nature.com/articles/nature04315)；[Jaynes–Cummings model and detuning](https://pmc.ncbi.nlm.nih.gov/articles/PMC12840198/)。
