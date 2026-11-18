# v2.65：激发数守恒不等于自由能分别守恒

**日期：2026-11-18。** 这是标准 Jaynes–Cummings 型单激发空间数值计算，未进行真实实验，不是完整量子电动力学，也未提出永久光子身份的独有动力学。Python/NumPy 本地运行 10 项测试全部通过。[研究模型](../models/identity_light_matter_v262_v271.py) · [十项测试](../tests/test_identity_light_matter_v262_v271.py)。

本模型固定在总单激发数 N=1 子空间，故 [H,N]=0。共振时光学和物质相对自由能一致，交换可不改变自由项。失谐 Δ=0.8 时令 H0=diag(0,0,Δ,Δ)，交互 H_int=H−H0，数值 ||[H,H0]||_F=1.6，**自由能会在演化中交换**，但对时间不变的完整 H，严格有 [H,H]=0，总能量期望守恒。这里不能从一个完整哈密顿量的平凡对易关系推出相对论能动量张量守恒。

**基础文献：** [Fleischhauer & Lukin, Quantum memory for photons: Dark-state polaritons (2002)](https://doi.org/10.1103/PhysRevA.65.022314)；[Storage and retrieval of single photons transmitted between remote quantum memories (Nature 2006)](https://www.nature.com/articles/nature04315)；[Jaynes–Cummings model and detuning](https://pmc.ncbi.nlm.nih.gov/articles/PMC12840198/)。
