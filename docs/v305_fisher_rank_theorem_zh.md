# v3.05：乘积参数 Fisher 信息秩亏的解析证明

**研究日期：2026-11-20。证据等级：理论/数学与合成数据；未开展真实实验，未完成 QED 新动力学，也无永久身份独有预测。** 本地原始代码运行 10/10 测试通过。GitHub 整理版：[模型](../models/identity_paper_audit_v302_v311.py) · [十项测试](../tests/test_identity_paper_audit_v302_v311.py)。研究结论对照文献：[Englbrecht et al., PRL 132, 050201 (2024)](https://doi.org/10.1103/PhysRevLett.132.050201)；[HOM Review, EPJD (2022)](https://doi.org/10.1140/epjd/s10053-022-00525-0)；[Gate Set Tomography (2021)](https://research.ibm.com/publications/gate-set-tomography)。

HOM 符合 p(q,s)=(1−qs)/2，对参数梯度 ∇p=(−s/2,−q/2)。N 次独立 Bernoulli 观测，F=N∇p∇pᵀ/[p(1−p)]，解析上为秩1的非负外积矩阵。方向 (q,−s) 与梯度正交，因此在这一局部方向内 q 与 s 的一阶变化不能被区分。n=200、q=.81,s=.64，数值最小特征值在约1e−14量级，因浮点舍入略偏零。增加同一个设置下的 N 不会提升秩。若额外参考可测 q，可能恢复形式上对 s 的局部可辨识，但不能证明 s 的物理本体是永久个体身份。
