# v2.62–v2.71：十轮真实光—物质动力学模型与永久身份审查

**2026-11-18。状态：** 十轮数学研究、实际 Python/NumPy 计算、本地对应 10 个回归测试全部通过。**仅为标准 JC 型有效模型，不是实际光学实验、完整 QED 证明或永久光子身份发现。**

## 十轮详细研究目录

| 版本 | 研究内容 | 报告 |
|---|---|---|
| v2.62 | 四态 JC 有效哈密顿量 | [阅读](./v262_jc_hamiltonian_zh.md) |
| v2.63 | 理想共振吸收与物质存储 | [阅读](./v263_resonant_absorption_zh.md) |
| v2.64 | 逆演化光学态读取 | [阅读](./v264_inverse_readout_zh.md) |
| v2.65 | 激发数、自由能与总能量账本 | [阅读](./v265_excitation_energy_bookkeeping_zh.md) |
| v2.66 | 失谐 Rabi 转移上界 | [阅读](./v266_detuned_rabi_limit_zh.md) |
| v2.67 | 普通模式选择性耦合 | [阅读](./v267_selection_rule_nuisance_zh.md) |
| v2.68 | 物质内部态探针读取 | [阅读](./v268_matter_probe_readout_zh.md) |
| v2.69 | 探针自由能与外部驱动 | [阅读](./v269_probe_energy_source_zh.md) |
| v2.70 | 标准失谐参数重拟合 | [阅读](./v270_standard_detuning_profile_zh.md) |
| v2.71 | 永久身份独有性与 QED 一致性审查 | [阅读](./v271_identity_qed_gap_zh.md) |

## 核心模型与结果

选取单激发四维子空间 |p0>,|p1>,|m0>,|m1>，令 H=Σ_i g_i(|p_i><m_i|+|m_i><p_i|)+ΔΣ_i|m_i><m_i|（ħ=1，在光学模旋转参考架），用矩阵对角化求 U(t)=exp(−itH)。

- v2.62: 厄米性误差 0；U(π/2) 酉性误差约 4.44×10^-16。
- v2.63: g0=g1=1、Δ=0、t=π/2，(p0+p1)/√2 完全进入物质双模式子空间；物质概率 0.9999999999999996。
- v2.64: 逆操作 U† 完全恢复原输入态，态保真度 0.9999999999999991。
- v2.65: 总单激发数 N=1 守恒；若 Δ=0.8，自由项 H0=diag(0,0,.8,.8) 与总 H 的对易子 Frobenius 范数 1.6，自由能单独不守恒；时间不变全哈密顿量 H 自身为守恒量。尚未验证场论完整能动量守恒。
- v2.66: Δ=.8、g=1 时最大物质转移概率 g²/(g²+(Δ/2)²)=0.8620689655172413，数值矩阵指数给 0.862068965517241，最优时间约 1.45844777556。
- v2.67: g0=1、g1=.7，同 t=π/2 造成两个物质激发概率 1.0 与 0.7938926261，差约 0.2061。属于标准耦合强度/选择规则。
- v2.68: 物质内部态 |m0>、|m1> 经辅助探针 U=exp[−iθ (|m0><m0|−|m1><m1|)⊗Y/2]、θ=.8，得到探针 X+ 概率 0.85867804545、0.14132195455，标准内部态读取。
- v2.69: 这一探针相互作用与独立探针自由能 I⊗Z 不对易，||[H_int,H_probe]||_F=4，需考虑外部控制驱动及完整能量账本。
- v2.70: p_det=0.8620689655 与**错误固定** Δ=0 的 p_res=0.9874308204 有 KL=0.2133705201 nat/事件；标准 JC 模型允许拟合 Δ=.8 后，profile KL=0。
- v2.71: 未构造可在吸收—物质存储—再发射中保留且可独立访问的永久光子个体标签；未产生独有预测和真实数据。**标准 JC 有效模型即可解释全批次计算。**

## 复现

- [GitHub 模型代码](../models/identity_light_matter_v262_v271.py)
- [GitHub 十项回归测试](../tests/test_identity_light_matter_v262_v271.py)

```bash
python -m models.identity_light_matter_v262_v271
python -m unittest discover -s tests -p 'test_identity_light_matter_v262_v271.py' -v
```

需 Python3 与 NumPy。本轮另附本地实际执行的源码、JSON 结果、CSV、完整测试日志 ZIP；GitHub 代码是同数学模型的结构化版，但与本地文件并非逐字节一致。GitHub CI 尚未单独核验。

## 文献和审查标准

- [Fleischhauer & Lukin (2002), Quantum memory for photons: Dark-state polaritons](https://doi.org/10.1103/PhysRevA.65.022314).
- [Chanelière et al. (2005/2006), Storage and retrieval of single photons transmitted between remote quantum memories](https://www.nature.com/articles/nature04315).
- [The Physical Spectrum of a Driven Jaynes–Cummings Model (2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12840198/).

**下一轮建议 v2.72–v2.81：** 在可实现的原子跃迁选择规则、真正独立校准的探针读数和光学输出联合实验中检验可观测分布。严格区分可逆的信息传递、常规物质内部态标签和没有物理观测定义的永久粒子编号；所有正结果应对标准量子光学全模型作 nuisance profiling。
