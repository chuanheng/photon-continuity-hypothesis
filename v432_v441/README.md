# v4.32–v4.41 量子因果切断与校准

十轮模型和测试均完成。结果是标准理论下的条件性证明及确定性模型计算，无光学实测数据。

| 轮次 | 报告 | 结果 |
|---|---|---|
| v4.32 | [近似因果切断](v432_zh.md) | 全域半钻石范数约束记录变化；局域重置无法保证清除普通环境记录 |
| v4.33 | [相干校准](v433_zh.md) | Z 布居相同的两个标准通道，可由相位制备或辅助系区分 |

| v4.34 | [交叉重置](v434_zh.md) | 普通串联通路产生交互，时序混叠可抬高差异 |
| v4.35 | [路线交换](v435_zh.md) | 普通模式损耗足以改变读出 |
| v4.36 | [相干容量](v436_zh.md) | 四阶子式排除三态及以下指定经典通路 |
| v4.37 | [相关样本](v437_zh.md) | 独立假设失配会放大误报 |
| v4.38 | [谱混合重拟合](v438_zh.md) | 背景边界决定可否拟合 |
| v4.39 | [玻色对称](v439_zh.md) | 交换奇算符在对称空间投影为零 |
| v4.40 | [普通相位旁路](v440_zh.md) | 指定操作下普通失谐混合精确重拟合 |
| v4.41 | [否证条件](v441_zh.md) | 先验证校准，再检验显著性 |

[修订稿](manuscript_zh.md) · [反方审稿](review_zh.md) · [已运行的 Jupyter 笔记本](reproduce.ipynb) · [数值输出](results.json)

```bash
python -m v432_v441.model
python -m unittest -v v432_v441.test_model
```

理论对照：[Pollock 等](https://doi.org/10.1103/PhysRevLett.120.040405) · [Watrous](https://johnwatrous.com/wp-content/uploads/TQI.pdf) · [Gorshkov 等](https://doi.org/10.1103/PhysRevLett.98.123601)
