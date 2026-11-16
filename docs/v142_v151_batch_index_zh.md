# v1.42–v1.51 十轮研究：相同玻色子、交换对称性与永久身份的可观测性

**2026-11-16，研究类型：** 二粒子二模式有限维数学模型与理想 HOM 双光子干涉计算。独立 Python 3/NumPy 数值脚本实际执行，10 项回归测试全部通过。**不是 QED 场论证明或真实光学实验；没有验证永久光子身份。**

| 版本 | 主题 | 详细报告 |
|---|---|---|
| v1.42 | 对称 Fock 子空间维数 | [查看](./v142_fock_space_zh.md) |
| v1.43 | 粒子编号的对称投影 | [查看](./v143_relabel_symmetry_zh.md) |
| v1.44 | 编号专属可观测算符 | [查看](./v144_slot_operator_zh.md) |
| v1.45 | HOM 模式重叠 | [查看](./v145_hom_overlap_zh.md) |
| v1.46 | 相位与规范不变性 | [查看](./v146_phase_gauge_zh.md) |
| v1.47 | 内部态与永久身份之别 | [查看](./v147_internal_modes_zh.md) |
| v1.48 | 哈密顿量交换对称性 | [查看](./v148_hamiltonian_exchange_zh.md) |
| v1.49 | 编号耦合群平均 | [查看](./v149_symmetrization_zh.md) |
| v1.50 | 模式标定的模型等价性 | [查看](./v150_overlap_nuisance_zh.md) |
| v1.51 | 新理论一致性门槛 | [查看](./v151_consistency_gate_zh.md) |

## 可复现文件

- [GitHub 模型](../models/identity_permutation_v142_v151.py)
- [GitHub 十项测试](../tests/test_identity_permutation_v142_v151.py)

运行命令：

```bash
python3 models/identity_permutation_v142_v151.py
python3 -m unittest discover -s tests -p 'test_identity_permutation_v142_v151.py' -v
```

NumPy 为运行依赖。完整本地实验快照（batch.py、test_batch.py、results.json）另外在对话中提供 ZIP 备份。GitHub 中简化模型保留同一核心验证和对应精确结论，并非原始脚本字节一致的副本；请分别验证。

## 关键结果

1. 两光子两模式时带槽位标签张量空间维数 4，玻色子对称空间维数 3；交换标签本身在对称空间不可辨识。
2. 槽位专属算符 O1=Z⊗I 不满足交换对称性：||[O1,S]||_F=2.828427；对称算符 A=(Z⊗I+I⊗Z)/2 满足交换对易关系。
3. 理想 HOM：Pcoinc=(1−|overlap|²)/2，重叠 0.6 时概率 0.32，重叠 0.7 时概率 0.255。若标准模型自由估计重叠值，同一候选测量 KL=0；固定错误的重叠基线时 KL≈0.01011246。
4. 交换对称动力学 Hsym=X⊗I+I⊗X+0.35Z⊗Z 的交换对易子范数为 0；单一槽位动力学 Hlabel=Z⊗I 的对应范数约 2.828427。
5. 当前没有构造洛伦兹协变或规范一致的身份新场，也没有超出标准量子光学的独有可证伪预测。将其视为待检验的假说，而不是已被证实的新物理。

## 为什么这很重要

Fock 空间计数激发数而非给无差别光子永久编号；具有可测内部模式差异并不能自然推出跨吸收/再发射的永久同一性。严格的新假说必须给出新可测自由度、物理上允许的交换对称耦合以及在标准 nuisance 被拟合后仍非零的观测概率差。

参考：
- https://etneil.github.io/grad_qm_lec_notes/identical_particles.html
- https://plato.stanford.edu/entries/quantum-field-theory/
- https://link.springer.com/article/10.1007/s10701-022-00596-4

下一批次 v1.52–v1.61 应重点检查局域场、规范冗余、洛伦兹协变、微因果性及可操作性判据，避免仅以模型命名制造所谓新物理。
