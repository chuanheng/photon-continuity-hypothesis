# v3.18：普通探测误差不会自动打破观测等价

**日期：2026-11-20。反方审稿阶段：v3.12–v3.21。** 全部是标准量子信息有限维数学、合成统计和文献比对。**不包含真实光子实验、完整 QED，也不是永久光子身份发现。** 本地独立模型已运行10/10项测试。复现：[GitHub模型](../models/identity_referee_v312_v321.py)、[GitHub回归测试](../tests/test_identity_referee_v312_v321.py)。

从候选HOM符合概率p=.2408和普通模式重拟合后的完全相同p出发，使用共同的仿射点击探测模型p_obs=d+(1−d)ηp，η=.85,d=.02，得到两者均为0.2205864，差严格0。只要两种模型预测相同的输入观测分布且共享同一后续探测器量子仪器，测量噪声不可能替它们创造区分信号。注意这个二项化探测映射是简化模型，真实双探测器符合需包括每路效率、暗计数窗口和高阶光子背景。

**核查文献：** [Gate Set Tomography (Nielsen et al., 2021)](https://quantum-journal.org/papers/q-2021-10-05-557/)；[HOM interference for mixed states](https://doi.org/10.1139/cjp-2023-0312)；[Experimental GST gauge freedom (2017)](https://www.nature.com/articles/ncomms14485)；[Realistic HOM source limitations (2026)](https://www.mdpi.com/2304-6732/13/9/846)。
