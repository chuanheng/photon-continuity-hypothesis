# v2.92–v3.01：永久光子身份理论有效性十轮综合审查

**日期：2026-11-19。** 完成十轮实质性理论筛选与可运行反例；本地 NumPy 计算的 10 项回归测试已实际执行，**10/10 PASS**。本批次不是实际光学实验，也没有完成 QED 计算或证明光子永久身份。

## 十轮成果

| 版本 | 研究主题 | 独立报告 |
|---|---|---|
| v2.92 | 玻色对称子空间与 Fock 解释 | [阅读](./v292_boson_hilbert_gate_zh.md) |
| v2.93 | 个体槽位算符的交换限制 | [阅读](./v293_permutation_operator_selection_zh.md) |
| v2.94 | 沉默身份标签的条件性 no-go | [阅读](./v294_silent_label_conditional_no_go_zh.md) |
| v2.95 | 可访问集体标签探针的标准解释 | [阅读](./v295_probe_coupling_internal_zh.md) |
| v2.96 | HOM 的隐藏标签与内模式等价 | [阅读](./v296_hidden_hom_reparam_zh.md) |
| v2.97 | 物质存储与个体同一性 | [阅读](./v297_optical_matter_memory_individuality_zh.md) |
| v2.98 | 电磁规范变换的必要条件检查 | [阅读](./v298_gauge_transform_sanity_zh.md) |
| v2.99 | 规范不变标量场耦合不是光子编号 | [阅读](./v299_gauge_invariant_new_field_not_identity_zh.md) |
| v2.100 | 错误固定基准与标准模型轮廓 | [阅读](./v300_composite_null_decision_zh.md) |
| v3.01 | 阶段性理论有效性判定 | [阅读](./v301_conditional_theory_verdict_zh.md) |

## 核心结论：条件性操作不可辨识

(1) 在同种玻色子两槽位内部态 Hilbert 空间，交换投影 (I+S)/2 的秩为3；“第一颗粒子的 Z”槽位算符不与交换对易（范数2.828427），而对称集体 Z 算符与交换对易（范数0）。物理可观测量的粒子标签不能由任意槽位编号替代。

(2) 如附加“身份标签”与一切可访问操作脱耦，且无法借由系统—环境关联向系统输出反馈，则不同标签的可见测量概率完全相同。本轮双量子比特例子观测概率差为0。此 no-go **只在限定假设下成立**，不说明所有未知新物理必然不可检验。

(3) 可交换对称地耦合一个标签集体量至探针，X+ 读出概率可为0.858678/0.141322/0.5；但该模型已属于标准量子力学的内部态/受控测量解释，不能证明可追踪的永久个体身份。

(4) HOM 中隐藏重叠 q=.81,s=.64 预测符合概率0.2408，与标准内模式 q_eff=.5184 完全相同。N=10000、NumPy seed=20261119 的合成符合数2393。与**错误固定**可见重叠 q=.81（符合概率0.095）比较，KL=0.09059719558758264；允许普通内部态重拟合，profile KL=0。

(5) 有限四态单激发光—物质写/读模型中存储概率约1、逆读出保真度约1；这些是量子信息转移，与永久个体存续是不同命题。

(6) 最低限度的电磁规范代数检查：F_{μν}=∂_μ A_ν−∂_ν A_μ，在 A_ν→A_ν+∂_νχ 的对称二阶导数变换下保持不变，数值误差1.11e−16；F_{μν}F^{μν} 不变，而 A_μ A^μ 在特定规范移动下改变量0.18。这**不是完整 QED 的 Ward 恒等式或规范与洛伦兹一致性证明**。

(7) 引入新的中性标量 χ 时，可以考虑有效项 χ F_{μν}F^{μν}/Λ（电磁规范不变且洛伦兹指标已收缩）；它描述额外物理场，而不是永久光子个体编号，也不代表该场已存在或该理论已通过所有约束。已知 QED 的 Euler–Heisenberg 光子相互作用亦使用规范不变的场强组合。

## 科学证据等级

**可确认：** 给定模型内的置换、Hilbert 空间、统计等价和规范代数结果。

**仍未完成：** 可区分于全部合理标准 QED/物质/探测机制的新身份动力学，满足规范与洛伦兹一致的完整作用量，跨吸收—再发射的同一性算符，以及真实独立实验。

**最终审查：** 目前应将永久光子身份写作“未验证且在所检验操作中不可辨识的假说”，不能仅凭增加隐藏标签、场论允许额外自由度或模拟显著性宣称新物理。

## 复现

- [GitHub 整理版计算模型](../models/identity_theory_audit_v292_v301.py)
- [GitHub 十项测试](../tests/test_identity_theory_audit_v292_v301.py)

```bash
python -m models.identity_theory_audit_v292_v301
python -m unittest discover -s tests -p 'test_identity_theory_audit_v292_v301.py' -v
```

Python 3 + NumPy。本对话另有独立本地运行快照 ZIP，内有 model.py/test_model.py/results.json/summary.csv/tests.log/README.md/综合判定文稿。GitHub 是数学内容相同的整理版，但不是本地脚本逐字节相同的源码；CI 需独立验证。

## 参考

- [Quantum Statistics of Identical Particles (2022)](https://link.springer.com/article/10.1007/s10701-022-00596-4)
- [Indistinguishability of Identical Bosons from a Quantum Information Theory Perspective (2024)](https://doi.org/10.1103/PhysRevLett.132.050201)
- [Effective Lagrangians and low-energy photon-photon scattering (1998)](https://doi.org/10.1103/PhysRevD.57.2443)
- [Identity and Individuality in Quantum Theory, Stanford Encyclopedia of Philosophy](https://plato.sydney.edu.au/entries/qt-idind/)

**下一阶段建议：** 不将新版本数量当作证据增长。若不能提出不可由普通内部态和量子环境重新表述的具体身份作用项，优先完成严谨的不可辨识性与否定性结果论文，而不是继续发明无物理来源的可调参数。
