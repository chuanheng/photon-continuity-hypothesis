# v2.67：模式选择性耦合制造明显信号

**日期：2026-11-18。** 这是标准 Jaynes–Cummings 型单激发空间数值计算，未进行真实实验，不是完整量子电动力学，也未提出永久光子身份的独有动力学。Python/NumPy 本地运行 10 项测试全部通过。[研究模型](../models/identity_light_matter_v262_v271.py) · [十项测试](../tests/test_identity_light_matter_v262_v271.py)。

令 g0=1、g1=.7，Δ=0，固定曝光时间 t=π/2。两个正交光学模式分别准备时，物质激发概率 P0=sin²(π/2)=1，P1=sin²(.7π/2)=0.7938926261462366，差 0.206107373853763。普通偶极选择规则、耦合强度、空间模式匹配均可导致这一结果。**不能将两种模式的不同吸收概率重新命名为永久身份被识别。**

**基础文献：** [Fleischhauer & Lukin, Quantum memory for photons: Dark-state polaritons (2002)](https://doi.org/10.1103/PhysRevA.65.022314)；[Storage and retrieval of single photons transmitted between remote quantum memories (Nature 2006)](https://www.nature.com/articles/nature04315)；[Jaynes–Cummings model and detuning](https://pmc.ncbi.nlm.nih.gov/articles/PMC12840198/)。
