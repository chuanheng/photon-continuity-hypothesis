# v1.32–v1.41：十轮辅助身份动力学与标准量子模型等价性研究

**日期：2026-11-16；研究性质：** 无量纲、可复现的开放量子系统数学与数值实验。未进行光学实验，也没有建立永久光子身份的物理实在性。模型与 Jaynes–Cummings 旋波近似的单激发扇区相关，但不是完整 QED。

## 逐轮索引

| 版本 | 主题 | 报告 |
|---|---|---|
| v1.32 | 两态光子—物质交换基准 | [打开](./v132_two_state_baseline_zh.md) |
| v1.33 | 旁观身份标签无观测效应 | [打开](./v133_spectator_identity_zh.md) |
| v1.34 | 附加寄存器耦合改变动力学 | [打开](./v134_coupled_register_zh.md) |
| v1.35 | 与经典准静态失谐噪声的通道等价 | [打开](./v135_channel_equivalence_zh.md) |
| v1.36 | 单激发子空间的守恒约束 | [打开](./v136_excitation_symmetry_zh.md) |
| v1.37 | 双激发末态在守恒模型中的禁戒 | [打开](./v137_number_selection_zh.md) |
| v1.38 | 单一失谐对照拟合失败 | [打开](./v138_restricted_detuning_fit_zh.md) |
| v1.39 | 固定基准的 KL 信息量 | [打开](./v139_fixed_baseline_kl_zh.md) |
| v1.40 | 探测噪声的数据处理不等式 | [打开](./v140_detection_loss_zh.md) |
| v1.41 | 允许标准环境参数后 KL 归零 | [打开](./v141_profile_standard_environment_zh.md) |

## 可复现实验

[模型源代码](../models/identity_dynamics_v132_v141.py) · [十项测试](../tests/test_identity_dynamics_v132_v141.py)

```bash
python3 models/identity_dynamics_v132_v141.py
python3 -m unittest discover -s tests -p 'test_identity_dynamics_v132_v141.py' -v
```

无第三方依赖，Python 标准库。设计与测试覆盖：（1）两态概率归一与基准；（2）旁观身份；（3）耦合的可见效应；（4）对四个独立矩阵算符的显式 4×4 偏迹和经典随机酉信道比较；（5）单激发模型的守恒；（6）激发数选择规则；（7）受限单失谐拟合；（8）多时间点 KL；（9）损耗后信息减少；（10）全标准噪声参考的严格等价。十项本地回归测试通过，GitHub CI 状态尚未独立验证。

## 核心数值

- g=1、Δ=0.7、κ=0.45，十个时间点 0.4 至 4.0：辅助寄存器耦合相对固定无噪声基准的最大存留概率差 **0.15523230404573773**。
- 最佳单一失谐拟合 Δ'=0.962，十点平方残差 **0.06735796179307191**；这只能排除受限的单参数对照。
- 对四个 2×2 基算符逐一比较，辅助寄存器约化通道与普通二值准静态失谐噪声 `E_t(rho)=0.5 U_+rho U_+†+0.5 U_-rho U_-†` 的最大差 **0（浮点精度）**。
- 十个独立时间测量方案的 Bernoulli KL 总和：理想读出 **0.4208667588101611** nat；损耗 η=0.82、暗计数 0.015 后 **0.199423716902078** nat。
- 与标准量子环境噪声允许相同准静态分布后最小 KL **严格为零**；无法由当前系统读出判别永久身份与普通环境。

## 理论边界

不能把一个人为加入的可耦合二能级寄存器直接宣称为光子的固有永久身份。对系统整体包括寄存器的独立寻址能力、与真实 QED 的兼容性、洛伦兹对称性及粒子交换对称性都未构造。单激发守恒约束不能推广到全部光场动力学。下一批次应优先论证新的物理耦合/可观测操作，否则继续拟合现有曲线不具有独立新理论识别价值。

## 学术背景

- Jaynes–Cummings 激发数守恒综述：https://pmc.ncbi.nlm.nih.gov/articles/PMC13167814/
- Halataei, *Classical simulation of arbitrary quantum noise*, PRA 96, 042338 (2017): https://doi.org/10.1103/PhysRevA.96.042338
- Huang & Merkli, *Qubit dynamics with classical noise*, Physics Open (2020): https://doi.org/10.1016/j.physo.2020.100043
