# v0.88 原创性审查与多时刻量子记忆示例

**结论：截至本轮，尚未发现证明“原始光子永久存在”的独立可检验物理效应，也尚未识别出能够宣称首次证明的数学定理。** 以下是有边界的文献审查，而非穷尽性系统综述。

## 一、逐项审查已有成果

| v0.50—v0.87 的研究问题 | 先前文献 | 目前原创性判断 |
|---|---|---|
| 相同玻色子的槽位编号不等于历史个体身份 | 量子不可区分性、对称化 | 现有理论的推论 |
| 不可访问身份辅助空间在局域测量下不可辨识 | 偏迹、标准量子信息 | 现有恒等式 |
| 最小 Stinespring 扩张酉等价 | Stinespring 1955、后续教材 | 已知定理 |
| 常数身份相位 δ 可被普通组偏置 b 吸收 | Rothenberg 1971；参数冗余理论 | 已知一般原理的具体应用 |
| 同一个单步信道可能有不同的多时刻统计 | 量子过程张量，Pollock 等 2018 | 已知理论与现有实验框架 |

光子永久存在作为本体论解释，可以被讨论；但数学上能够引入身份标签不代表自然界存在该自由度。观察到额外相位也并不能直接证明它是旧光子的个体身份，必须排除普通量子记忆、模式与环境效应，并从独立动力学推出预测。

## 二、一个可复现的多时刻差异实例

初态 \(\rho_0=|0\rangle\langle0|\)，单步信道

\[
\mathcal E(\rho)=\tfrac12\rho+\tfrac12X\rho X.
\]

模型 A 在两个时间步都使用同一个隐藏随机比特 r，并施加 \(X^r\)；模型 B 每次独立抽取 r1,r2，分别施加 \(X^{r_i}\)。两者的单步信道完全相同，但是在中间不操作的两步演化后：

\[
\rho_2^A=\tfrac12\sum_r X^rX^r\rho_0X^rX^r=\rho_0,\qquad
\rho_2^B=\mathcal E^2(\rho_0)=I/2.
\]

因此 \(D(\rho_2^A,\rho_2^B)=\frac12\|\rho_2^A-\rho_2^B\|_1=0.5\)，先验各为一半时最优单次模型判别成功率为 \(\frac12(1+D)=0.75\)。如在中间施加固定的 X 操作，模型 A 输出 |1>，而 B 仍输出 I/2。这体现**单时刻信道相同不足以确定多时刻环境记忆**。它是已有过程张量理论能刻画的效应，既不是 PCH-A 新预言，也不是永久光子身份的证据。

## 三、科学贡献的严格门槛

1. 写出测量时序、可控操作集合、可访问代数；分清单时刻信道、特定多时刻实验，以及完整过程张量之间的等价。
2. 不可只给一个未知身份标签；必须给出动力学，符合相同玻色统计、局域性、Lorentz 协变和规范结构。
3. 普通环境记忆模型必须公平地包含可能的组别相位、非马尔可夫性及探测器效应。新增的实验差异必须不能被其重新参数化复制。
4. 与已有 Stinespring、Rothenberg、过程张量文献比较后，才能讨论是否存在新的联合定理或新算法。
5. 若只有已知理论的新组合和教科书式数值例子，不应宣称原创物理发现。

## 四、本轮执行

Python NumPy 模型，25/25 个 unittest 本地执行成功。完整本地 ZIP 含报告、文献对应矩阵、模型、测试、实验脚本及计算出的 JSON。GitHub 提交本身不代表远程 CI 已执行。

## 五、参考与链接

1. *Identity and Individuality in Quantum Theory*, Stanford Encyclopedia of Philosophy. https://plato.stanford.edu/entries/qt-idind/
2. *Stinespring Representation* 讲义（最小扩张唯一性）. https://mathweb.ucsd.edu/~helton/247A10/completePosIntro.pdf
3. Rothenberg (1971), *Identification in Parametric Models*. https://pages.stern.nyu.edu/~dbackus/Identification/Rothenberg_id_Econometrica_71.pdf
4. *Parameter Identifiability and Redundancy: Theoretical Considerations*. https://pmc.ncbi.nlm.nih.gov/articles/PMC2811744/
5. Pollock et al. (2018), *Operational Markov Condition for Quantum Processes*. https://doi.org/10.1103/PhysRevLett.120.040405
6. *Non-Markovian Quantum Process Tomography* (2022). https://doi.org/10.1103/PRXQuantum.3.020344
7. *Demonstration of non-Markovian process characterisation and control on a quantum processor* (2020). https://www.nature.com/articles/s41467-020-20113-3

## 下一轮 v0.89

把可访问的多时刻干预集合精确定义成操作性等价类，对比两类普通环境记忆模型与所谓身份模型的过程张量。若无法证明模型存在不能被普通记忆过程解释的区别，则保持“未发现独立新物理”的研究结论。