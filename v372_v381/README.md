# v3.72–v3.81 精确二项似然与弱可辨识性研究

**2026-11-22；本地NumPy/SciPy 10/10测试通过；全部合成数据；不是光子身份的实验发现。**

| 版本 | 主题 | 研究报告 |
|---|---|---|
| v3.72 | 精确Bernoulli观测模型 | [报告](v372_zh.md) |
| v3.73 | 多起点精确二项极大似然 | [报告](v373_zh.md) |
| v3.74 | 历史样本重新估计 | [报告](v374_zh.md) |
| v3.75 | 材料记忆精确目标的轮廓扫描 | [报告](v375_zh.md) |
| v3.76 | 有限次数的似然比零分布 | [报告](v376_zh.md) |
| v3.77 | Wald正态近似的粗检 | [报告](v377_zh.md) |
| v3.78 | 有限样本材料刷新率分位 | [报告](v378_zh.md) |
| v3.79 | 信息矩阵条件数复核 | [报告](v379_zh.md) |
| v3.80 | 完整标准HMM的最优KL | [报告](v380_zh.md) |
| v3.81 | 本批次审稿判定 | [报告](v381_zh.md) |

核心结果：20261122固定种子的五组计数[2340,3803,3315,4148,477]，MLE约[.19781,.50125,.89456,.14910,.04770]；18点材料参数剖面存在数值局部最优风险；30次零假设模拟样本过少，不足以校准置信阈值。标准环境模型包含全部观测，profile KL=0。

复现：`python -m v372_v381.model`，`python -m unittest -v v372_v381.test_model`；需numpy/scipy。本对话另提供完整本地实际执行的源码、JSON、CSV、日志和十份长报告ZIP，GitHub版本为整理实现，非逐字节同源。理论依据：Pollock等，PRL 120,040405 (2018)，https://pubmed.ncbi.nlm.nih.gov/29437441/ ；Profile-wise analysis (2023)，https://pmc.ncbi.nlm.nih.gov/articles/PMC10566698/ ；Boundary inference review (2024)，https://www.imstat.org/publications/sts/sts_39_2/sts_39_2.pdf 。
