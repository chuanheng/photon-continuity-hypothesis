# v4.62–v4.71 场耦合与普通光学响应

部分检查点。已执行 v4.62–v4.64，下一轮 v4.65。完整批次版本仍为 v4.61。

| 版本 | 报告 | 结论 |
|---|---|---|
| v4.62 | [规范一致性](v462_zh.md) | 只增加局域裸矢势耦合时源必须守恒 |
| v4.63 | [偏振旋转](v463_zh.md) | 正下界依赖独立偏置校准，放开偏置可近精确拟合 |
| v4.64 | [开放腔](v464_zh.md) | 普通内部损耗给出未观测到的激发份额 |

```bash
python -m v462_v471.model
python -m unittest -v v462_v471.test_model v452_v461.test_model v442_v451.test_model v432_v441.test_model
```

[输出](results.json) · [验证记录](verification.json) · [后续路线](../docs/research_roadmap.md)
