# v3.12–v3.21：永久光子身份假说反方审稿与论文修订

**2026-11-20。研究状态：已完成十轮理论反例审查、本地独立数值计算和十项回归测试（10/10通过）；均为合成数据和标准量子信息模型，不是物理实验，也不是永久光子身份的验证。**

## 修订论文与独立审稿意见

- **[v3.21 中文修订版工作论文](./v321_revised_manuscript_zh.md)**：收紧条件性操作等价定理、补入系统—环境反馈反例，明确HOM及统计检验范围，删除无证据的原创性主张。
- **[v3.21 反方匿名审稿报告](./v321_adversarial_referee_report_zh.md)**：建议 Major Revision（大修后重新评估）。这是项目内部模拟反方审稿，**不是真实期刊或独立同行的审稿意见**。

## 十轮逐项独立报告

| 版本 | 审稿主题 | 独立报告 |
|---|---|---|
| v3.12 | 原创性与已知文献交叉 | [查看](./v312_originality_literature_audit_zh.md) |
| v3.13 | 封闭量子仪器的操作等价 | [查看](./v313_no_feedback_test_zh.md) |
| v3.14 | 系统—环境相关性反馈最大反例 | [查看](./v314_correlated_environment_counterexample_zh.md) |
| v3.15 | 制备相关量子通道的混淆 | [查看](./v315_preparation_dependent_channels_zh.md) |
| v3.16 | 固定CPTP通道与系综一致性 | [查看](./v316_fixed_CPTP_affinity_zh.md) |
| v3.17 | 混合内态HOM公式审查 | [查看](./v317_mixed_HOM_domain_zh.md) |
| v3.18 | 探测噪声下的等价性 | [查看](./v318_detector_noise_reparam_zh.md) |
| v3.19 | 200次精确二项检验复核 | [查看](./v319_exact_test_rechecked_zh.md) |
| v3.20 | 量子过程表示规范的限定 | [查看](./v320_GST_gauge_limit_zh.md) |
| v3.21 | 反方审稿最终大修意见 | [查看](./v321_referee_recommendation_zh.md) |

## 核心新增反例：局域态相同却可经环境反馈分叉

S、E两量子比特：ρ_A=(|00><00|+|11><11|)/2，ρ_B=(|01><01|+|10><10|)/2，Tr_Eρ_A=Tr_Eρ_B=I/2。因此初始S迹距离为0。施加E控制S的CNOT后，两个输出系统分别为|0><0|和|1><1|，迹距离**1**，共同CNOT严格酉，误差0。它是标准环境相关性反馈，不是光子永久身份信号。**原“无标签不可辨识”的表述必须明确后续操作对S闭合、不存在标签或相关性反馈的前提**。否则不能从初始边缘态相等推出未来所有概率相同。

## 其余数值复核

- 不含标签反馈、使用同一个固定通道：200组随机系统/环境态输入测试最大可访问输出差2.498e−16。
- 对相同|+>输入，恒等通道与完全Z退相干通道可产生迹距离0.5；装置设置相关误差需要控制。
- 共同固定CPTP通道作用于I/2的X、Z不同纯态系综，输出差1.110e−16。
- 混合内态HOM：ρ=diag(.7,.3)、σ=diag(.2,.8)，符合概率.31；纯态标签示例q=.81,s=.64，符合概率.2408，普通内部态q_eff=.5184完全复制。
- 加探测效率.85、暗点击.02后两模型都给点击概率.2205864。
- 错误固定基准 p0=.095 vs p1=.2408，n=200，拒绝阈值K≥27，精确检验size=.040273448344332406、power=.9999292017586787、简单KL=.09059719558758264，而标准内部态拟合的**profile KL=0**。
- 抽象过程表示的可逆相似变换，在12个序列长度上最大概率差1.110e−16；它不证明新表示独立符合CPTP条件。

## 本轮审稿判断

已知标准量子操作的条件性等价不是本项目已证实的原创普适no-go定理。建议修订论文定位为**具体假说的条件性操作辨识方法、明确反例与否定性数值案例**。没有QED新动力学、完整相对论一致性、真实实验或跨吸收/再发射的永久身份独有可访问算符。独立学术审稿和进一步查新尚未完成。

## 复现

- [GitHub 整理版Python模型](../models/identity_referee_v312_v321.py)
- [GitHub 十项回归测试](../tests/test_identity_referee_v312_v321.py)

```bash
python -m models.identity_referee_v312_v321
python -m unittest discover -s tests -p 'test_identity_referee_v312_v321.py' -v
```

需要Python/NumPy/SciPy。本次对话提供原始本地实际执行代码、JSON、CSV、测试日志、中文修订稿及审稿报告的ZIP。GitHub整理版采用相同物理反例和核心参数，但**不是本地脚本逐字节相同，仓库CI尚未单独核验**。

## 主要参考

- [Nielsen et al., Gate Set Tomography, Quantum 5,557 (2021)](https://quantum-journal.org/papers/q-2021-10-05-557/)
- [Mixed-state HOM spectral–temporal analysis](https://doi.org/10.1139/cjp-2023-0312)
- [Experimental gate-set gauge freedom, Nature Communications (2017)](https://www.nature.com/articles/ncomms14485)
- [Realistic HOM interference source limitations (2026)](https://www.mdpi.com/2304-6732/13/9/846)

**下一批次建议：** 考虑停止自动累加版本，先开展文献查新及由专业量子光学研究者进行独立评审。如果继续v3.22–v3.31，应只优先解决明确的新耦合构造或把条件性可辨识性审计变成可验证的研究方法，而不是重复标准模型的合成计数。
