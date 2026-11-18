# v2.64：逆酉操作重建原始量子态

**日期：2026-11-18。** 这是标准 Jaynes–Cummings 型单激发空间数值计算，未进行真实实验，不是完整量子电动力学，也未提出永久光子身份的独有动力学。Python/NumPy 本地运行 10 项测试全部通过。[研究模型](../models/identity_light_matter_v262_v271.py) · [十项测试](../tests/test_identity_light_matter_v262_v271.py)。

承接 v2.63 的存储态，对它执行理想 U(−π/2)=U(π/2)†。原光学态恢复保真度 0.9999999999999991，态向量 2 范数误差约 3.17×10^-16。**限制**：现实光学量子存储须考虑损耗、噪声、有效能级、带宽和外部控制；理想的态恢复不等于某个不可区分玻色子个体的同一性。

**基础文献：** [Fleischhauer & Lukin, Quantum memory for photons: Dark-state polaritons (2002)](https://doi.org/10.1103/PhysRevA.65.022314)；[Storage and retrieval of single photons transmitted between remote quantum memories (Nature 2006)](https://www.nature.com/articles/nature04315)；[Jaynes–Cummings model and detuning](https://pmc.ncbi.nlm.nih.gov/articles/PMC12840198/)。
