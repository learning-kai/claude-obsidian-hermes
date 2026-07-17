# claude-obsidian-hermes

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/learning-kai/claude-obsidian-hermes?display_name=tag)](https://github.com/learning-kai/claude-obsidian-hermes/releases/latest)
[![Hermes](https://img.shields.io/badge/runtime-Hermes%20Agent-blue)](https://hermes-agent.nousresearch.com/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)](https://github.com/learning-kai/claude-obsidian-hermes)
[![Upstream](https://img.shields.io/badge/upstream-claude--obsidian-6f42c1)](https://github.com/AgriciDaniel/claude-obsidian)

> **一句话：** 把 [AgriciDaniel/claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) 的第二大脑工作流移植到 **Hermes Agent**——保留 `.raw/` + `wiki/`、skills、检索与 lint，不依赖 Claude Code。

**语言：** [English](README.md) | 简体中文

## 为什么做

上游 claude-obsidian 在 Claude Code + Obsidian 上很完整。
很多 Hermes 用户想要同一套 vault 架构，但不想绑定 Claude Code。本仓库提供 Hermes 适配 skills、vault 模板、脚本与 `co` CLI。

## 核心特性

- **15 个上游 skill** 的 Hermes 适配版（`adapted/skills/`）
- **上游 vault 布局**：不可变 `.raw/`、生成式 `wiki/`、hot/index/log/manifest
- **`bin/co` 命令行**：ingest · ingest-url · query · lint · save · fold · mode · doctor · reindex · mirror
- **BM25 检索**（无需 GPU）
- **干净 vault 模板**（不含私人笔记）
- **完整文档**：差距矩阵、验收说明、可选 Obsidian 镜像

## 截图与演示

本项目是 CLI/Agent 工具链（无独立 GUI）。典型闭环：

```text
co ingest note.md  ->  .raw/ + wiki/sources/  ->  co query "关键词"  ->  co lint/doctor
```

可选：用 Obsidian 打开 vault，浏览 `wiki/` 与双链。

## 快速开始

### 一行安装（macOS / Linux）

```bash
curl -fsSL https://raw.githubusercontent.com/learning-kai/claude-obsidian-hermes/master/scripts/bootstrap.sh | bash
```

### 一行安装（Windows PowerShell）

```powershell
irm https://raw.githubusercontent.com/learning-kai/claude-obsidian-hermes/master/scripts/bootstrap.ps1 | iex
```

### 手动安装

```bash
git clone https://github.com/learning-kai/claude-obsidian-hermes.git
cd claude-obsidian-hermes
cp -a vault-template "$HOME/claude-obsidian-vault"
export CLAUDE_OBSIDIAN_VAULT="$HOME/claude-obsidian-vault"
export CLAUDE_OBSIDIAN_PORT="$PWD"

mkdir -p ~/.hermes/skills/note-taking
for d in adapted/skills/*; do
  name=$(basename "$d")
  rm -rf "$HOME/.hermes/skills/note-taking/claude-obsidian-$name"
  cp -a "$d" "$HOME/.hermes/skills/note-taking/claude-obsidian-$name"
done

./bin/co status
./bin/co ingest ./README.md "readme-seed"
./bin/co query "claude-obsidian"
./bin/co doctor
```

在 Hermes 对话中加载 skill **`claude-obsidian`**（需先装到 skills 目录）。

## 工程质量

无标准 Node/Rust 应用构建。验证以 Python/Shell hermetic 测试 + CLI 冒烟（`co doctor`）为准。

- `adapted/tests/` 下 hermetic 脚本测试
- 可选 Windows 镜像脚本的路径白名单
- 发布前密钥/大文件检查
- 仓库不包含私人 live vault

```bash
cd adapted
python3 tests/test_wiki_mode.py
python3 tests/test_retrieve.py
bash tests/test_wiki_lock.sh
```

无 Node/Rust 应用构建。质量证据以 Python/Shell 测试与 CLI 冒烟为主。

## 项目文档

| 文档 | 用途 |
|---|---|
| [docs/scope.md](docs/scope.md) | 范围与非目标 |
| [docs/GAP-MATRIX.md](docs/GAP-MATRIX.md) | 与上游差距 |
| [docs/FINAL-ACCEPTANCE.md](docs/FINAL-ACCEPTANCE.md) | 验收记录 |
| [docs/OBSIDIAN-MIRROR.md](docs/OBSIDIAN-MIRROR.md) | Obsidian 镜像 |
| [docs/SECURITY.md](docs/SECURITY.md) | 路径白名单 |

## 隐私与安全边界

- 不要提交私人 vault、`.env`、凭据
- 镜像助手（若使用）只能写明确授权的新文件夹
- `.raw/**` 入库后不可改
- 本仓库仅提供模板 vault

## 发布与更新

- Release：https://github.com/learning-kai/claude-obsidian-hermes/releases
- 安装脚本建议固定 Release / tag
- 也可用 `master` 跟踪最新

## 路线图

- [x] Hermes skill 适配 + `co` CLI
- [x] 无 GPU 的 BM25 检索
- [x] vault 模板与文档
- [ ] 可选 skill 打包安装
- [ ] defuddle-cli 更优 URL 清洗
- [ ] 大内存主机上的 Ollama 重排指南

## 贡献

欢迎 Issue / PR：
1. 不要带私人笔记
2. 改脚本请跑相关测试
3. 用户可见变更请同步 README 中英

## 故障排查

| 现象 | 处理 |
|---|---|
| 新页面搜不到 | `./bin/co reindex` |
| doctor 缺目录 | 重新复制 `vault-template` 或 `co scaffold` |
| retrieve 报 ollama | 无 Ollama 时正常；BM25 仍可用 |
| Windows 镜像失败 | 检查 SSH 与白名单目标文件夹 |

## License

MIT - 见 [LICENSE](./LICENSE)。

## 归属

上游：[AgriciDaniel/claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian)（MIT）
详见 `adapted/LICENSE`、`adapted/ATTRIBUTION.md`。
