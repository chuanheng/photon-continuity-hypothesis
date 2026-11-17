# v2.02–v2.11 十轮连续研究：光子身份可检验性论文综合审查

**日期：2026-11-17。批次状态：** 十项独立研究分析、Python/NumPy/SciPy 数值运行、十项本地单元测试全部完成。**不是实际物理实验，没有发现永久光子身份的新证据。**

| 版本 | 研究主题 | 独立报告 |
|---|---|---|
| v2.02 | 历史候选机制证据台账 | [阅读](./v202_historical_mechanism_ledger_zh.md) |
| v2.03 | 惰性身份标签操作不可辨识 | [阅读](./v203_observational_no_go_zh.md) |
| v2.04 | 已知参考的精确二项检验 | [阅读](./v204_exact_known_reference_zh.md) |
| v2.05 | 有限参考校准 Monte Carlo | [阅读](./v205_finite_reference_mc_zh.md) |
| v2.06 | 共享零假设联合似然分离度 | [阅读](./v206_joint_profile_information_zh.md) |
| v2.07 | 未建模漂移的虚假拒绝 | [阅读](./v207_unmodeled_drift_zh.md) |
| v2.08 | 效率与暗计数的参数混淆 | [阅读](./v208_efficiency_dark_rate_aliasing_zh.md) |
| v2.09 | 零假设拒绝率模拟核验 | [阅读](./v209_empirical_null_size_zh.md) |
| v2.10 | 功效与系统偏差综合 | [阅读](./v210_empirical_power_and_drift_zh.md) |
| v2.11 | 论文主张与证据等级 | [阅读](./v211_manuscript_claim_gate_zh.md) |

## 正式研究论文初稿

**[《光子连续性假说的操作可辨识性：标准模型等价、独立标定与系统漂移》](./v211_operational_identifiability_paper_draft_zh.md)**

本稿结构完整，包含摘要、研究问题、统计和量子方法学、有限参考及漂移模拟结果、讨论与局限、结论及独立文献。该稿是**方法学/否定性结果初稿**，不是已经符合期刊发表标准的光子永久身份发现论文。

## 复现资源

- [GitHub Python 计算模型](../models/identity_evidence_v202_v211.py)
- [GitHub 十项测试](../tests/test_identity_evidence_v202_v211.py)
- 完整独立本地运行快照（`batch.py`、`test_batch.py`、`results.json`、`summary.csv`、`paper_draft_zh.md`）可从本次对话提供的 ZIP 下载；GitHub 提交的是相同统计计算的结构化整理版本，**并非本地原稿逐字节相同**。

```bash
python -m models.identity_evidence_v202_v211
python -m unittest discover -s tests -p 'test_identity_evidence_v202_v211.py' -v
```

Python 依赖 NumPy 与 SciPy；本地批次运行代码的 10 项测试通过。GitHub CI 尚未单独核验。

## 本批次三个关键结果

1. **有限参考直接影响功效。** 主实验 n=5000、合成 p_main=.08、参考 p_ref=.06、名义 α=.05、3000 次重复。参考 m=1000/5000/20000 时双样本 z 检验拒绝率为 71.7667%/99.10%/99.9333%。如果参考 p_ref=.06 真正精确已知，单样本精确检验的功效为 99.9936%，两者不能混用。
2. **错误参数共享导致虚假归因。** 假设没有新效应，只是普通主实验背景比参考提高 .02，仍错误采用共享参数零假设，模拟拒绝率达 98.73%。这是错误模型被拒绝，不能说成标准物理被拒绝。
3. **仪器参数不可辨识。** 只记录点击时，d+(1-d)ηb 的三项不同组合可产生相同概率，无法从单一观测反推出“新身份耦合”。

## 论文科学判定

尚无“永久身份”独有的、可由实际实验否证且无法由标准 QED 含合理干扰参数的模型解释的物理预测；也没有真实光学实验数据。本批次完成的是**理论研究的证据审计和标定可靠性评估**，而非光子永久身份的验证。后续最关键的工作不是继续增加版本号，而是提出具体新动力学并接受标准模型全套反例和真实测量检验。

## 已核查基础文献

- Englbrecht et al. (2024), https://doi.org/10.1103/PhysRevLett.132.050201
- Fleischhauer & Lukin (2002), https://doi.org/10.1103/PhysRevA.65.022314
- Pollock et al. (2018), https://doi.org/10.1103/PhysRevA.97.012127
