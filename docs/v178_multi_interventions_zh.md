# v1.78：四种中间量子操作与完整过程对照

**日期：2026-11-17。研究性质：** 本批次使用两能级相位退相干的合成量子信息模型（θ=0.6）；并非完整光子吸收/再发射实验，不是永久光子身份的证据。所有概率为模型计算，不是实测。完整运行见 [Python 复现代码](../models/identity_process_v172_v181.py) 与 [测试](../tests/test_identity_process_v172_v181.py)。

计算 I、X、Y、Z 四种中间酉控制操作下的两曝光输出密度矩阵。隐藏寄存器的 Z 扇区保持不变，迹掉寄存器所得映射与“每次实验内固定同一个经典随机符号”的模型逐项完全相等，最大矩阵元误差 0。**范围：** 验证的四种中间酉操作是测试集；其受控结构允许进一步解析推广到任意只作用系统的中间操作，但此脚本未实现完整过程张量层析。

**参考：** Pollock et al. (2018), *Non-Markovian quantum processes: Complete framework and efficient characterization*, https://doi.org/10.1103/PhysRevA.97.012127 。
