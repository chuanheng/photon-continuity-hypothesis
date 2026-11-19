# v2.72–v2.81：输入、物质存储、辅助探针、再发射与探测的十轮综合研究

**2026-11-19。** 10 轮模型分析、实际 NumPy 本地计算、10/10 对应单元测试全部通过。**没有进行真实物理实验，没有构造完整 QED，也没有发现永久光子身份的独有证据。**

## 十轮报告

| 版本 | 主题 | 独立报告 |
|---|---|---|
| v2.72 | 写入酉性及物质存储 | [查看](./v272_write_unitarity_zh.md) |
| v2.73 | 逆操作读取保真度 | [查看](./v273_reverse_readout_zh.md) |
| v2.74 | 身份参数与退相干通道 | [查看](./v274_storage_dephasing_CPTP_zh.md) |
| v2.75 | 光学、探针及联合概率 | [查看](./v275_joint_probabilities_zh.md) |
| v2.76 | 探针反作用与测量信息 | [查看](./v276_probe_backaction_zh.md) |
| v2.77 | 完整读出的标准模型精确等价 | [查看](./v277_standard_environment_exact_equivalence_zh.md) |
| v2.78 | 单读出的 Fisher 信息秩亏 | [查看](./v278_fisher_rank_nuisance_zh.md) |
| v2.79 | 存储时间、失谐与选择性耦合 | [查看](./v279_storage_time_and_controls_zh.md) |
| v2.80 | 探测器点击与标准参数轮廓 | [查看](./v280_detector_counting_profile_zh.md) |
| v2.81 | 永久身份专属预测的否定性审查 | [查看](./v281_full_sequence_verdict_zh.md) |

## 核心模型

在 |p0>,|p1>,|m0>,|m1> 四维单激发空间，使用写入 W=exp(−iHπ/2)，H=Σ_i g_i(|pi><mi|+|mi><pi|)+ΔΣ_i|mi><mi|。输入 (|p0>+|p1>)/√2 完整转入物质态。写入后对内部两模式施加退相干 D_{cs}(ρ)=[(1+cs)ρ+(1−cs)ZρZ]/2；c=.85 为普通存储相干系数，s=.8 是待检验额外“身份”乘数。然后与初始化 |0> 的辅助探针耦合 U_p=exp(−iθA⊗Y/2)，A=diag(0,0,1,−1)、θ=.6。对光/物质部分施加 W† 读取，再对不同测量投影求迹。

本模型是标准量子理论里的一种有限维**合成量子仪器**。s 在定义中只作为普通相干系数的乘因子，并非独立物理身份的操作定义。

## 数值结果

- 写入酉性误差 4.44e−16，理想写入物质占据约 1。无探针和退相干条件下，逆读取的输入输出迹距离 4.46e−16。
- 有探针时光学 X+：0.7806141090692893；探针 X+：约 0.5；光学模式 0、1 非条件概率各约 0.5；联合 X+×X+：约 0.39030705453464476。
- 探针 θ=0.6 相对 θ=0 给光学 X+ 的影响为 −0.05938589093070945。这是普通探针反作用造成的可见相干损失。
- **完整观测等价**：候选 c=.85,s=.8 与无额外身份因子的标准模型 c_eff=.68,s=1 在所有本次计算的六个观测量上数值差严格为 0。由于它们在探针介入前的系统密度矩阵完全相同，在相同下游动力学下可推广至任何后续 POVM 的零差。
- 探测器 η=.9、暗计数 d=.01 的模型给候选点击概率 0.7055271711807368。错误固定无身份衰减基准给 0.7680339639759212，简单假设 KL=0.010368707254628726 nat/事件，标准模型重拟合 c_eff=.68 后 KL=0。
- seed=20261119、10000 次 Bernoulli 合成样本得到 7071 次点击。这是**模拟数据而非实验数据**。
- 单光学读出只依赖 cs；对 (c,s) 的 Fisher 信息矩阵秩为 1（非零特征值约 886.613），无法分辨参数来源。
- 另令普通存储 c(t)=exp(−0.3t)、候选常数 s=.8，t=.5,1,2 时的 X+ 概率依次为 0.7841491788、0.7445694647、0.6811815157。常规模式可见度 v=.8 与同样 c(t) 结合能精确复制三点，最大误差 1.22e−15。增加存储时长设置仍不足以构成身份独有预测。
- 偏离理想写入（Δ=.8 或单模式 g1=.7）时，读取后光学占据小于 1，是本四态单激发空间中的**残留物质激发**，不能直接当成真实光学损耗。

## 复现

[GitHub 结构化计算代码](../models/identity_full_sequence_v272_v281.py) · [GitHub 回归测试](../tests/test_identity_full_sequence_v272_v281.py)

```bash
python -m models.identity_full_sequence_v272_v281
python -m unittest discover -s tests -p 'test_identity_full_sequence_v272_v281.py' -v
```

Python3 + NumPy。当前会话独立提供本地**实际运行**的 `model.py`、`test_model.py`、`results.json`、`tests.log`、`summary.csv` ZIP。GitHub 文件是相同数学公式/参数/随机种子的整理实现，和本地脚本不完全逐字相同；**GitHub CI 尚未核验**。

## 科学判定

**本批次没有永久光子身份的独立预测。** 当前所谓身份因子 s 与普通存储退相干 c 或初始模式可见度 v 完全混淆。多时长或更高统计显著性不会自动解决这个物理机制辨识问题。真实下一步需要一个不能表示为现有环境/内部态/探测 nuisance 重新参数化的明确新相互作用，及其在相同玻色子交换统计、规范、洛伦兹及能量约束下的可行模型与独立实验标定。

## 参考文献

- Fleischhauer & Lukin (2002), [Quantum memory for photons: Dark-state polaritons](https://doi.org/10.1103/PhysRevA.65.022314)
- [POVM and quantum measurements, University of Waterloo lecture notes](https://cleve.iqc.uwaterloo.ca/resources/QIC-710-F24/Qic710QuantumInformationTheory2024V3.pdf)
