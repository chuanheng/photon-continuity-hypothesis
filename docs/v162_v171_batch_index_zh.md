# v1.62–v1.71：十轮光子存储、物质转移与永久身份可证伪性研究

**研究日期：2026-11-16。状态：** 完成十轮分析、十项本地自动化测试，属于标准量子信息的有限维合成模型。**没有永久光子身份的新预测或实验验证。**

| 版本 | 研究主题 | 独立研究报告 |
|---|---|---|
| v1.62 | 可逆光物质写入 | [查看](./v162_reversible_storage_zh.md) |
| v1.63 | 零光子阶段的量子信息 | [查看](./v163_zero_photon_memory_zh.md) |
| v1.64 | 逆操作与读取保真度 | [查看](./v164_retrieval_fidelity_zh.md) |
| v1.65 | 隐藏指针造成退相干 | [查看](./v165_pointer_visibility_zh.md) |
| v1.66 | 普通环境通道的精确等价 | [查看](./v166_standard_environment_zh.md) |
| v1.67 | 模式依赖读取效率 | [查看](./v167_mode_dependent_retrieval_zh.md) |
| v1.68 | 乘积可见度局部秩亏 | [查看](./v168_product_degeneracy_zh.md) |
| v1.69 | HOM 参考恢复统计可辨识 | [查看](./v169_hom_reference_zh.md) |
| v1.70 | 有限样本与基线重新拟合 | [查看](./v170_finite_sample_nuisance_zh.md) |
| v1.71 | 永久身份独有预测审查 | [查看](./v171_identity_falsifiability_zh.md) |

## 复现

[计算模型](../models/identity_memory_v162_v171.py) · [10 项测试](../tests/test_identity_memory_v162_v171.py)

```bash
python3 models/identity_memory_v162_v171.py
python3 -m unittest discover -s tests -p 'test_identity_memory_v162_v171.py' -v
```

依赖 Python 3 和 NumPy。独立本地测试已运行，10/10 通过。GitHub 代码已上传但 GitHub CI 未核验。会话提供 ZIP，包含本地运行的 model.py、test_model.py、results.json；文件与仓库中代码组织略有不同，核心参数、数学公式和结果相同。

## 研究核心

- 使用四维单激发态空间 |p0>,|p1>,|m0>,|m1>，双旋转 U(π/2) 把光学双模式叠加完全写入物质子空间，U† 理想逆变换完整恢复；酉性误差 0，读取保真度约 1。
- 在零光子存储阶段，物质携带原来光学量子态的信息，但信息的连续性**并不蕴含**不可区分玻色子的永久个体编号。
- 隐藏指针重叠 s=0.6，普通模式重叠 μ=0.75，正端口概率 P+=(1+sμ)/2=0.725。身份指针的约化通道与标准环境退相干通道严格相同，系统迹距离 0。
- 单次主实验的两参数 Fisher 秩为 1；若独立 HOM 参考真正测同一 μ，联合信息局部满秩。不过这只区分两个有效统计参数，**不等于测得“永久身份”**。
- 种子 20261116、10000 次 Bernoulli 合成采样：7314 次正端口。与错误固定 s=1 的基准 KL≈0.08049；标准模型允许其物理环境或有效模式参数重拟合后 KL=0。
- 当前三条候选机制：零光子存储、身份指针相干作用、身份影响再发射选择，都被当前有限维标准模型覆盖。**没有得到 QED 之外的新机制证据。**

## 下一阶段必要工作

独立物理机制必须具有具体哈密顿量及可访问可观测量，遵守交换统计、能量动量守恒、局域性、规范与洛伦兹对称性的相应条件，并给出标准 QED 及其合理干扰参数族无法重拟合的明确分布差。未通过这些标准之前，不应只靠增加版本号宣称接近发现。

## 参考文献

- Fleischhauer & Lukin (2002), [Quantum memory for photons: Dark-state polaritons](https://doi.org/10.1103/PhysRevA.65.022314)
- Ma, Slattery & Tang (2017), [Optical quantum memory based on electromagnetically induced transparency](https://doi.org/10.1088/2040-8986/19/4/043001)
- Vernaz-Gris et al. (2018), [High-efficiency quantum memory for single-photon polarization qubits](https://www.nature.com/articles/s41566-019-0368-8)
