# v4.52–v4.61 吸收再发射的标准通道与探测

| 轮次 | 报告 | 主要结果 |
|---|---|---|
| v4.52 | [效率乘积](v452_zh.md) | 无独立探测器标定时源与探测效率共线 |
| v4.53 | [死时间](v453_zh.md) | 普通硬件给出符号交替的协方差 |
| v4.54 | [后脉冲](v454_zh.md) | 单路和真实迟到光精确等价，需独立探测器 |
| v4.55 | [热损耗](v455_zh.md) | 普通热泄漏给出相同输出光子数分布 |
| v4.56 | [相干存储](v456_zh.md) | 共振物质存储可完美转移单激发及相位 |
| v4.57 | [时间门](v457_zh.md) | 延迟模条件重叠可为 1，完整脉冲为 .35345 |
| v4.58 | [高斯完全正性](v458_zh.md) | 给定收缩的附加噪声下限来自真空 |
| v4.59 | [相位参考](v459_zh.md) | 共同参考保留相对相干，独立相位平均使之消失 |
| v4.60 | [缺失试次](v460_zh.md) | 接受率已知时总体对比仍可跨零 |
| v4.61 | [边带能量](v461_zh.md) | 普通非均匀探测可使对称谱出现平均频移 |

```bash
python -m v452_v461.model
python -m unittest -v v452_v461.test_model v442_v451.test_model v432_v441.test_model
PYTHONPATH=. python -Xfrozen_modules=off tools/execute_research_notebook.py v452_v461/reproduce.ipynb
```

[修订稿](manuscript_zh.md) · [内部反方审稿](review_zh.md) · [复现笔记本](reproduce.ipynb) · [数值输出](results.json) · [执行验证记录](verification.json)

死时间模拟种子 452461。其余数值确定性。无本仓库新增光学实测。
