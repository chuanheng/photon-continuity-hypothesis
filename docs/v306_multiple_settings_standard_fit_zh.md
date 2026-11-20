# v3.06：多设置 HOM 对标准模型的再参数化检验

**研究日期：2026-11-20。证据等级：理论/数学与合成数据；未开展真实实验，未完成 QED 新动力学，也无永久身份独有预测。** 本地原始代码运行 10/10 测试通过。GitHub 整理版：[模型](../models/identity_paper_audit_v302_v311.py) · [十项测试](../tests/test_identity_paper_audit_v302_v311.py)。研究结论对照文献：[Englbrecht et al., PRL 132, 050201 (2024)](https://doi.org/10.1103/PhysRevLett.132.050201)；[HOM Review, EPJD (2022)](https://doi.org/10.1140/epjd/s10053-022-00525-0)；[Gate Set Tomography (2021)](https://research.ibm.com/publications/gate-set-tomography)。

选可见内模式重叠 q=[.81,.64,.49,.36]，假设共同隐藏重叠 s=.64；得到四次符合概率 (1−q_i s)/2。普通标准内模式只需分别取 q_eff,i=q_i s，即可对四个观测逐一完全复现，最大概率差0。**限制：** 若独立实验已经把标准内模式在所有设置下的重叠和演化规律限制在更小的物理模型族，此具体自由重拟合可能不再成立，需要重新核验；不能先假定这种物理约束，再把数学上的非零差异当成发现。
