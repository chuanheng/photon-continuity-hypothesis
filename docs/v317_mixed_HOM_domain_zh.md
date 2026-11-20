# v3.17：HOM公式应明确混合态和器件适用条件

**日期：2026-11-20。反方审稿阶段：v3.12–v3.21。** 全部是标准量子信息有限维数学、合成统计和文献比对。**不包含真实光子实验、完整 QED，也不是永久光子身份发现。** 本地独立模型已运行10/10项测试。复现：[GitHub模型](../models/identity_referee_v312_v321.py)、[GitHub回归测试](../tests/test_identity_referee_v312_v321.py)。

理想50:50无损分束器，每端输入独立单光子，探测器不分辨内态，对单光子内态密度算符ρ、σ，符合概率P_coin=[1−Tr(ρσ)]/2。取ρ=diag(.7,.3)、σ=diag(.2,.8)，Tr(ρσ)=.38，故P=.31。纯态内标签示例q=.81,s=.64得到P=.2408，可由普通内模式重叠q_eff=.5184精确复现。理论审查须明确适用条件：输入单光子数、两源独立、理想分束器、探测器不分辨所建模的内部态；不能无条件用于含高阶多光子、相关源或非平衡装置。

**核查文献：** [Gate Set Tomography (Nielsen et al., 2021)](https://quantum-journal.org/papers/q-2021-10-05-557/)；[HOM interference for mixed states](https://doi.org/10.1139/cjp-2023-0312)；[Experimental GST gauge freedom (2017)](https://www.nature.com/articles/ncomms14485)；[Realistic HOM source limitations (2026)](https://www.mdpi.com/2304-6732/13/9/846)。
