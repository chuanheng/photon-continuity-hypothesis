# v2.70：显著差异被普通失谐参数重新拟合

**日期：2026-11-18。** 这是标准 Jaynes–Cummings 型单激发空间数值计算，未进行真实实验，不是完整量子电动力学，也未提出永久光子身份的独有动力学。Python/NumPy 本地运行 10 项测试全部通过。[研究模型](../models/identity_light_matter_v262_v271.py) · [十项测试](../tests/test_identity_light_matter_v262_v271.py)。

取 Δ=.8，g=1，t=1.4584477755572458。真实候选激发概率 p_det=0.862068965517241；错误固定 Δ=0 的标准基准 p_res=0.9874308203577848。Bernoulli KL(p_det||p_res)=0.21337052010623392 nats/event。但允许标准 JC 模型将 Δ 自由拟合到真实 .8，就会得到完全相同激发概率及完整单激发模型，轮廓 KL=0。**拒绝一个错误固定的共振基准不是对标准量子光学的否证。**

**基础文献：** [Fleischhauer & Lukin, Quantum memory for photons: Dark-state polaritons (2002)](https://doi.org/10.1103/PhysRevA.65.022314)；[Storage and retrieval of single photons transmitted between remote quantum memories (Nature 2006)](https://www.nature.com/articles/nature04315)；[Jaynes–Cummings model and detuning](https://pmc.ncbi.nlm.nih.gov/articles/PMC12840198/)。
