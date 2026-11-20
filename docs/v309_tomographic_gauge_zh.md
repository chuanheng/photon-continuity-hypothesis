# v3.09：相同实验概率可以对应不同的过程表示

**研究日期：2026-11-20。证据等级：理论/数学与合成数据；未开展真实实验，未完成 QED 新动力学，也无永久身份独有预测。** 本地原始代码运行 10/10 测试通过。GitHub 整理版：[模型](../models/identity_paper_audit_v302_v311.py) · [十项测试](../tests/test_identity_paper_audit_v302_v311.py)。研究结论对照文献：[Englbrecht et al., PRL 132, 050201 (2024)](https://doi.org/10.1103/PhysRevLett.132.050201)；[HOM Review, EPJD (2022)](https://doi.org/10.1140/epjd/s10053-022-00525-0)；[Gate Set Tomography (2021)](https://research.ibm.com/publications/gate-set-tomography)。

用有限状态线性模型写序列概率 p_k=eᵀG^kρ。对于任意可逆 B，取 e'ᵀ=eᵀB⁻¹，G'=BGB⁻¹，ρ'=Bρ，则全部 k 上 p'_k=p_k。数值选二维转移矩阵、非单位 B，对 k=0..7 验证最大概率差 5.551e−16。**重要约束：** B 的表示变换不是新的物理相互作用，也不保证变换后矩阵在原始表示中每一个都是合法独立 CPTP 过程；它只是表明必须使用操作等价类，而不是对任意拟合参数赋予本体解释。量子 gate-set tomography 的规范自由度与此相关。
