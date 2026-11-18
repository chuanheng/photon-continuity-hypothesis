# v2.62：建立四态单激发光—物质动力学

**日期：2026-11-18。** 这是标准 Jaynes–Cummings 型单激发空间数值计算，未进行真实实验，不是完整量子电动力学，也未提出永久光子身份的独有动力学。Python/NumPy 本地运行 10 项测试全部通过。[研究模型](../models/identity_light_matter_v262_v271.py) · [十项测试](../tests/test_identity_light_matter_v262_v271.py)。

**模型**：选择基底 |p0>,|p1>,|m0>,|m1>，标准单激发耦合矩阵 H=Σ_i g_i(|p_i><m_i|+|m_i><p_i|)+ΔΣ_i|m_i><m_i|，取 ħ=1、能量参考光学模式为零。数值检查共振 g_i=1 的 H=H†、酉演化 U(t)=exp(−itH) 满足 U†U=I，最大酉性误差 4.44×10^-16。**物理边界**：矩阵是标准旋转波近似的简化版本，没有完整多光子场、相对论或规范自由度。

**基础文献：** [Fleischhauer & Lukin, Quantum memory for photons: Dark-state polaritons (2002)](https://doi.org/10.1103/PhysRevA.65.022314)；[Storage and retrieval of single photons transmitted between remote quantum memories (Nature 2006)](https://www.nature.com/articles/nature04315)；[Jaynes–Cummings model and detuning](https://pmc.ncbi.nlm.nih.gov/articles/PMC12840198/)。
