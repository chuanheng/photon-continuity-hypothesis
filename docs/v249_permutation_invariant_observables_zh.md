# v2.49：粒子编号与允许物理测量算符

**研究日期：2026-11-18。** 理想双光子 HOM 分束器、纯态内模式与隐藏二能级标签的合成数学研究。**不是实际实验，也不是永久光子身份的验证。** Python/NumPy 本地运行并通过 10/10 单元测试。可复现文件：[统一模型](../models/identity_label_hom_v242_v251.py) · [十项测试](../tests/test_identity_label_hom_v242_v251.py)。

在两个计算槽位的二能级标签空间令交换算符 S 交换中间 |01> 与 |10>。随意指定“第一个粒子 Z”的算符 O=Z⊗I，与 S 的对易子 Frobenius 范数 ||[O,S]||=2.8284271247；对称化算符 O_sym=(Z⊗I+I⊗Z)/2 与 S 对易，范数 0。这说明对相同玻色子，纯粹依赖任意粒子编号的单体槽位算符不是物理上可区分的独立观测量。**但** 模式选择性探测、光子与物质耦合、带物理内部态的对称测量仍可允许；不能把“不可编号”误解为“不可观察内部模式差异”。

**理论参照**：[Hong、Ou、Mandel (1987)](https://doi.org/10.1103/PhysRevLett.59.2044)；[Englbrecht 等 (2024)，PRL 132,050201](https://doi.org/10.1103/PhysRevLett.132.050201)；[Indistinguishability Theory for Identical Particles with Invariant Degrees of Freedom (2026 预印本)](https://arxiv.org/abs/2609.14428)。
