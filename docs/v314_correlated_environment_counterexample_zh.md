# v3.14：最大强度的系统—环境反馈反例

**日期：2026-11-20。反方审稿阶段：v3.12–v3.21。** 全部是标准量子信息有限维数学、合成统计和文献比对。**不包含真实光子实验、完整 QED，也不是永久光子身份发现。** 本地独立模型已运行10/10项测试。复现：[GitHub模型](../models/identity_referee_v312_v321.py)、[GitHub回归测试](../tests/test_identity_referee_v312_v321.py)。

定义S,E各一个量子比特。联合态A=0.5|00><00|+0.5|11><11|；B=0.5|01><01|+0.5|10><10|，两者Tr_E均为I/2，初始S边缘迹距离0，E边缘也同为I/2。施加以E为控制、S为目标的CNOT：|s,e>→|s⊕e,e>。计算A输出S=|0><0|，B输出S=|1><1|，迹距离1；CNOT酉性误差0。这是**当前假说审查最重要的失效边界**：不同的相关性虽不改变局部初态，一旦允许普通环境反馈即可让S结果完全不同。该效应是标准量子力学，不证明永久光子身份。

**核查文献：** [Gate Set Tomography (Nielsen et al., 2021)](https://quantum-journal.org/papers/q-2021-10-05-557/)；[HOM interference for mixed states](https://doi.org/10.1139/cjp-2023-0312)；[Experimental GST gauge freedom (2017)](https://www.nature.com/articles/ncomms14485)；[Realistic HOM source limitations (2026)](https://www.mdpi.com/2304-6732/13/9/846)。
