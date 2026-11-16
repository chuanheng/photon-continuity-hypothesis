# v0.87 — 16 历史版本的本地原件核验索引

**注意：这个索引仅提供本地原始资料的审计清单，不代表原始源码已经全部上传 GitHub。**

v0.51—v0.66 共16个版本、78个本地历史文件。下表为每个版本中中文报告、模型、单元测试的 **SHA-256 前12位**（顺序：报告 / 模型 / 测试）；其余运行文件及全部64位 SHA-256 在本地完整 `photon_v087/results/historical_file_manifest.json` 中。

| 版本 | 研究主题（文件名关键词） | 历史文件数 | 报告 / 模型 / 测试 SHA-256 前缀 |
|---|---|---:|---|
| v0.51 | bosonic_identity | 3 | `139d7571e121` / `a98ce7269fc4` / `4c7be1d27d35` |
| v0.52 | fock_identity | 4 | `7163de444c95` / `fe115d0ed799` / `18a12ee9c9c1` |
| v0.53 | absorption_identity | 4 | `a2ef3491b720` / `f5f9a2e48fee` / `4d1c2412ed1e` |
| v0.54 | rabi_identity | 4 | `4add669c0548` / `dc1bc0c838aa` / `4c0e6e5f4795` |
| v0.55 | identity_readout | 6 | `140fcde3b21c` / `ada53c6abb39` / `b4c0b62b4ccf` |
| v0.56 | eft_constraints | 4 | `4f2ac5624287` / `4be04af21876` / `bc7d1e8faa67` |
| v0.57 | noether_identity | 4 | `f41101f628c0` / `45fcb5a11055` / `6f27c77d8015` |
| v0.58 | charge_transfer | 4 | `f943f45515b4` / `1f93b770aa4c` / `ea634b43400f` |
| v0.59 | local_charge_eft | 4 | `b2a47f4df7fb` / `cbaaa1b42d9b` / `2f683da52bd1` |
| v0.60 | competing_models | 6 | `97136b4e9cac` / `ba657ff47b97` / `5ab65d4dbdf5` |
| v0.61 | theory_audit | 5 | `ce1aaa64c635` / `9f86085ec834` / `87bd0575c08c` |
| v0.62 | no_go_theorem | 6 | `dc8349f74373` / `7ce7a6e451bf` / `c609a88af6c4` |
| v0.63 | environment_memory | 6 | `bdbfeb41c67c` / `f9b13f59ecdc` / `942e96b948e0` |
| v0.64 | information_backflow | 6 | `6ea652d0f82b` / `143fe75ce9a3` / `cd247a0b9652` |
| v0.65 | environment_comparison | 6 | `7d6afd9f56bd` / `d08ac9e350da` / `930b2c0da95e` |
| v0.66 | fock_identity | 6 | `4a997625b245` / `f99d669bc5a2` / `45e447bf71f5` |

完整历史字节仍保存在本地 `photon_v051_v066_backfill.zip`，并随本轮 `photon_v087_complete.zip` 的外部历史归档使用。待认证网络环境恢复后应提交目录 `backfill/photon_v051` … `backfill/photon_v066`，然后逐一检查完整哈希。

目前 v0.68、v0.75 的原始可执行测试材料缺失。研究文档并不等于原始代码、数据与运行记录。

测试状态：v0.50—v0.86 共37个版本；35个版本1,101项单元测试通过。测试仅证明指定程序断言成立，不证明原始光子永久存在。
