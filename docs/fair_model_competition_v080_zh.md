# v0.80：公平模型竞争与独立校准下的身份参数可辨识性

**状态：** 有限维统计模型的数学结果；不是 QED 新预测，也没有证明光子永久身份。

## 研究问题

当普通量子记忆模型拥有损耗、振幅、共用相位以及普通环境漂移等 nuisance 参数时，假定的“身份额外相位”是否仍可以从实验中单独识别？

## 概率模型

每次试验返回三个结果：loss、plus、minus。设有效损失 L、干涉振幅 A，0<L<1，0<A<1−L。相位扫描 x，开关 z∈{0,1}，公共相位 β、普通漂移 κ、假设的额外相位 δ：

\[
p_{\rm loss}=L,\qquad
p_\pm=\frac{1-L\pm A\cos\left[x+\beta+z\left(\kappa+\mathbf1_{\rm test}\delta\right)\right]}2.
\]

仅 test 实验时，数据只依赖 κ+δ，故变换 (κ,δ)→(κ+c,δ−c) 保持所有概率不变。Fisher 信息矩阵的 κ 和 δ 列相同，存在零特征值；无论重复多少次，δ 都结构性不可辨识。

假定增加独立 calibration，其普通相位偏移与 test 共用 κ，但不受 δ 影响，则 calibration 可约束 κ，使 δ 局部可识别。但**κ 在两类实验中必须相同**，否则辨识性不成立。若普通模型获准分别拥有 κ_test、κ_cal，令 κ_test=κ+δ、κ_cal=κ 就能对所有测量条件重现所谓“身份模型”的预测。

## 公平模型竞争与数值结果

设 θ=(L,A,β,κ,δ)=(0.35,0.49,0.13,0.11,0.20)，相位 x=(0.15,0.8,1.7,2.5)，每条件模拟的期望试验次数1000。

| 统计量 | test alone | test+calibration |
|---|---:|---:|
| Fisher 矩阵秩 | 4/5 | 5/5 |
| 最小特征值 | 约 4.33×10⁻¹⁴ | 312.1802 |
| δ 的条件 Fisher 信息（Schur 补） | 数值精度内为0 | 441.8438 |
| δ=0 时优化其余 nuisance 参数的 Asimov deviance | 约 0 | 17.6523 |

本研究使用预期数据（Asimov dataset）而非任何真实实验测量。17.6523 是相应参数与样本规模下的期望统计量，**不等价于实际发现显著性**；模型错设、独立校准误差和非正则统计分布均未评估。

## 关键数学命题

固定共享 κ 假设时，校准可打破 (κ,δ) 的连续退化；放松该假设后，普通记忆模型重建所有概率，因此身份效应的存在不是强制解释，而取决于未经证明的环境动态约束。

本轮并未提出具备物理根据的“光子身份开关”或独立 QED 相互作用。额外相位若被观测，也可能是普通量子存储器的环境漂移、材料相干或额外光学相位。

## 实测与复现

Python 3.10+、numpy、scipy。**本地真实执行 28 项 unittest，全部通过，0.774 s。**

仓库文件：
- models/fair_model_competition_v080.py
- tests/test_fair_model_competition_v080.py
- experiments/run_v080.py
- results/model_competition_v080.json
- results/test_results_v080.txt

执行：
\`\`\`bash
python -m unittest discover -s tests -p 'test_fair_model_competition_v080.py' -v
python -m experiments.run_v080
\`\`\`

本地 ZIP 包还保存完整测试日志及相应模型的本地命名版本。

## 下一步 v0.81

1. 模拟 test/calibration 之间的随机漂移与时间相关噪声。
2. 预注册 ordinary-memory null model 的 nuisance 空间；不允许事后任意删减普通机制。
3. 使用参数化 bootstrap 评估似然比在有限计数下的分布。
4. 真正建立光子身份对某种交互作用的独立场论预测，否则将结论定位为统计可辨识性研究。

## 参考

Rothenberg, T. J. (1971), *Identification in Parametric Models*, Econometrica 39(3), 577–591, https://doi.org/10.2307/1913267 。关于 Fisher 秩与局部可辨识的联系，该结论要求相应正则条件，不应用于证明全局可辨识。
