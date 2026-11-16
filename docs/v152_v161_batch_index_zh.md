# v1.52–v1.61 十轮研究：永久光子身份的场论一致性审查

**日期：2026-11-16。研究性质：** 10 项互相关联的有限维/格点理论演示及回归测试。**不是完整 QED 的计算，也不是新物理现象的发现。**

| 版本 | 主题 | 独立报告 |
|---|---|---|
| v1.52 | 对称态与编号 | [查看](./v152_exchange_projection_zh.md) |
| v1.53 | 两格点 U(1) 规范协变 | [查看](./v153_lattice_gauge_covariance_zh.md) |
| v1.54 | Wilson 环路不变性 | [查看](./v154_wilson_loop_zh.md) |
| v1.55 | 独立子系统对易 | [查看](./v155_tensor_locality_zh.md) |
| v1.56 | 局域操作与相互作用 | [查看](./v156_operational_local_action_zh.md) |
| v1.57 | 离散连续性方程 | [查看](./v157_discrete_continuity_zh.md) |
| v1.58 | 真空无质量壳条件 | [查看](./v158_mass_shell_offset_zh.md) |
| v1.59 | 场激发数与吸收 | [查看](./v159_absorption_fock_zh.md) |
| v1.60 | 路径指针和模式可见度 | [查看](./v160_pointer_interference_zh.md) |
| v1.61 | 永久身份的观测等价 | [查看](./v161_new_physics_gate_zh.md) |

## 可复现代码

- [Python/NumPy 模型](../models/identity_qft_gates_v152_v161.py)
- [十项回归测试](../tests/test_identity_qft_gates_v152_v161.py)

```bash
python3 models/identity_qft_gates_v152_v161.py
python3 -m unittest discover -s tests -p 'test_identity_qft_gates_v152_v161.py' -v
```

本次同时在独立的本地 Python/NumPy 脚本运行 10 项测试，全部通过，保存 JSON 数值结果及 ZIP；仓库中的精简脚本为相同数学测试的对应版本，但不是本地脚本的字节完全相同副本。GitHub CI 尚未核验。

## 关键数值与解释

1. 玻色对称投影 rank=3；编号交换后的投影差为 0。
2. 两格点规范协变误差 1.11e-16，三格点环路相位不变性误差 1.24e-16。
3. 独立张量因子对易子范数为 0，而特定双体耦合与远端算符的对易子范数为 4；前者**不能**替代相对论类空间隔微因果性。
4. 对 Bell 态只作用一个局域幺正，另一子系统的局域统计不变；允许直接相互作用后，期望可改变约 0.1861。
5. 格点跃迁满足局部连续性方程。人为的常数能量偏移使无质量光子的 E²−p² 在四个动量点分别变为 0.1344、0.2544、0.4944、0.9744。
6. 单激发 JC 子空间中，t=0.4 的物质激发概率为 0.1516466，光子数可变，但总激发数不变。
7. 不可访问二值身份寄存器被求和后，与标准模型全部观测概率完全相同，KL=0。

## 仍未解决的核心问题

没有写出带有新永久光子身份可观测量的**洛伦兹协变、规范一致、局域且符合玻色统计**的完整动力学；也未得到标准理论无法通过其物理干扰参数重拟合的非零最小 KL。该问题是新假说后续被独立检验之前的必要门槛。不能继续以增加版本号代替通过这一门槛。

## 参考资料

- UCSD Advanced Quantum Mechanics (identical particles): https://mcgreevy.physics.ucsd.edu/s23/2023-212C-lectures.pdf
- Heidelberg QFT lecture notes (local observables and microcausality): https://www.thphys.uni-heidelberg.de/courses/weigand/QFT1-12-13.pdf
- UvA Quantum Field Theory notes: https://staff.fnwi.uva.nl/j.smit/qft07.pdf
