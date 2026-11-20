# v3.02–v3.11 十轮研究：永久光子身份的条件性操作不可辨识性工作论文

**2026-11-20 | 工作论文及理论/数学审查 | 未同行评审 | 无真实光子实验**

## 十轮成果

| 版本 | 研究题目 | 独立研究报告 |
|---|---|---|
| v3.02 | 玻色交换与物理身份的界限 | [查看](./v302_scope_and_exchange_zh.md) |
| v3.03 | 条件性不可辨识性定理及归纳证明 | [查看](./v303_conditional_operational_no_go_zh.md) |
| v3.04 | HOM 隐藏标签的标准模式等价 | [查看](./v304_HOM_reparameterization_zh.md) |
| v3.05 | Fisher 信息秩亏证明 | [查看](./v305_fisher_rank_theorem_zh.md) |
| v3.06 | 四测量设置的模型再参数化 | [查看](./v306_multiple_settings_standard_fit_zh.md) |
| v3.07 | 200 次精确二项检验 | [查看](./v307_exact_binomial_significance_audit_zh.md) |
| v3.08 | 缺乏物理依据的标准模型边界 | [查看](./v308_restricted_nuisance_boundary_zh.md) |
| v3.09 | 量子过程层析的表示规范自由度 | [查看](./v309_tomographic_gauge_zh.md) |
| v3.10 | 混合态、噪声和非线性反例 | [查看](./v310_adversarial_counterexamples_zh.md) |
| v3.11 | 论文主张、限制和审稿检查清单 | [查看](./v311_manuscript_and_peer_review_gate_zh.md) |

## 中文论文初稿

[《光子“永久身份”假说的操作不可辨识性：条件定理、HOM 反例与实验门槛》](./v311_operational_no_go_paper_draft_zh.md)

论文涵盖摘要、研究对象、条件性定理和证明、交换对称性、HOM 重参数化、Fisher 信息、精确统计检验、环境与探测反例、过程规范自由度、物理和实验门槛、局限及来源。**不是新物理发现论文；不能声称实验发现永久身份。**

## 数值复核结果

- 两二能级相同玻色子的对称子空间 rank=3。
- 沉默身份标签：100 组随机可见态和标签态及可访问 POVM 测试，最大概率差3.33e−16。
- HOM 候选可见重叠q=.81、隐藏重叠s=.64，符合概率.2408；普通内模式重叠q_eff=.5184也给.2408，差0。
- 单设置HOM参数(q,s)的Fisher矩阵解析秩1；多设置若允许每组普通模式变化仍可精确拟合。
- 简单H0:p=.095 vs H1:p=.2408，n=200的单侧精确二项检验拒绝阈值≥27，size=.04027344834、power=.99992920176、固定KL=.09059719559。标准模型有效模式重拟合后**profile KL=0**。
- 若人为规定标准重叠≥.7，候选和允许标准概率边界的 KL=.028210545，但该额外界限**无独立物理依据**。
- 线性过程表示相似变换 k=0..7 最大概率差5.55e−16；这是规范表示，**不是合法新物理动力学**。
- 混合内部态ρ=diag(.7,.3)、σ=diag(.2,.8)得HOM=.31。加入η=.85、暗计数d=.02，候选及标准重拟合的点击概率均为.2205864。
- 不可访问性的命题只在标签没有任何到可访问仪器的反馈时有效，不能据此普遍排除所有可能新耦合。

## 复现资源

[Python 数值模型](../models/identity_paper_audit_v302_v311.py) · [十项回归测试](../tests/test_identity_paper_audit_v302_v311.py)

```bash
python -m models.identity_paper_audit_v302_v311
python -m unittest discover -s tests -p 'test_identity_paper_audit_v302_v311.py' -v
```

依赖NumPy和SciPy。**本地独立原始代码已实际运行并通过10/10测试**，含结果JSON、CSV、测试日志、较长中文论文稿的ZIP在本次会话下载。GitHub代码为数学等价的整理版，尚未单独执行仓库CI，不宣称逐字节同源。

## 主要可信文献

- [Englbrecht et al. (2024), PRL 132,050201](https://doi.org/10.1103/PhysRevLett.132.050201)：相同玻色子操作不可区分性
- [HOM review (2022)](https://doi.org/10.1140/epjd/s10053-022-00525-0)：模式重叠与符合概率
- [Nielsen et al., Gate Set Tomography (2021)](https://research.ibm.com/publications/gate-set-tomography)：规范自由度与操作可区分性
- [Simon et al., PRL 87,170405 (2001)](https://doi.org/10.1103/PhysRevLett.87.170405)：无信号和动力学线性性
- [Quantum Statistics of Identical Particles (2022)](https://link.springer.com/article/10.1007/s10701-022-00596-4)

## 下一阶段审稿检查

真正值得优先解决的是：是否能构造一个没有普通内部模式或环境替代表示的、可在吸收—再发射期间操作追踪的身份动力学？在此之前，论文应强调有限操作集合下的**条件性no-go/不可辨识性结论**，把负结果与未完成证明写得同样明确。
