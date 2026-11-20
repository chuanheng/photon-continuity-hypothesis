# v3.04：HOM 隐藏标签和普通内模式完全等价

**研究日期：2026-11-20。证据等级：理论/数学与合成数据；未开展真实实验，未完成 QED 新动力学，也无永久身份独有预测。** 本地原始代码运行 10/10 测试通过。GitHub 整理版：[模型](../models/identity_paper_audit_v302_v311.py) · [十项测试](../tests/test_identity_paper_audit_v302_v311.py)。研究结论对照文献：[Englbrecht et al., PRL 132, 050201 (2024)](https://doi.org/10.1103/PhysRevLett.132.050201)；[HOM Review, EPJD (2022)](https://doi.org/10.1140/epjd/s10053-022-00525-0)；[Gate Set Tomography (2021)](https://research.ibm.com/publications/gate-set-tomography)。

理想两单光子平衡分束器、内态纯态且探测器不分辨内态时，符合概率 p=(1−|〈u|v〉|²)/2。让内态张量分解为可见部分和所谓身份标签，重叠平方分别 q=.81、s=.64，则 p=(1−qs)/2=.2408；完全标准、没有身份标签的内模式重叠 q_eff=qs=.5184，仍得 .2408，概率差0。对于该观测，两模型所有 Bernoulli 数据分布完全相同，统计实验无法判别其物理命名。与标准理论的内模式重新拟合进行竞争比拒绝一个固定 q=.81 的简化基准更重要。
