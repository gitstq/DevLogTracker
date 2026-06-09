<div align="center">

# 🚀 DevLogTracker

**Intelligent Developer Log Tracker - Auto-capture, analyze and visualize your development workflow**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange)](https://github.com/gitstq/DevLogTracker/releases)

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

<a name="english"></a>
## 🎉 Project Introduction

DevLogTracker is an **intelligent developer activity tracking tool** that automatically monitors file changes in your project, records development behavior, and provides beautiful data analysis and visualization reports.

### 💡 Inspiration

As developers, we spend countless hours coding every day, but rarely have a clear picture of our own development patterns. DevLogTracker was born to solve this pain point - it silently records every file change, then generates intuitive reports to help you understand your coding habits, peak productivity periods, and project hotspots.

### ✨ Key Differentiators
- **Zero Configuration**: Works out of the box with sensible defaults
- **Real-time Monitoring**: File system watcher captures changes instantly
- **Rich Analytics**: Daily summaries, weekly reports, productivity scoring
- **Beautiful Terminal UI**: Powered by Rich for stunning CLI output
- **HTML Reports**: Export professional reports for sharing
- **Smart Ignore**: Automatically filters build artifacts and dependencies

---

## ✨ Core Features

| Feature | Description | Emoji |
|---------|-------------|-------|
| 👁️ **Real-time Watch** | Monitor file changes across multiple paths | 🟢 Active |
| 📊 **Daily Summary** | Event counts, peak hours, activity span | 📈 |
| 📈 **Weekly Report** | Visual bar charts showing daily breakdown | 📅 |
| 🏆 **Productivity Score** | AI-powered scoring with personalized suggestions | 🎯 |
| 🔥 **Hot Files** | Identify most frequently edited files | 🔥 |
| 📄 **HTML Export** | Generate beautiful reports for sharing | 🌐 |
| 🧹 **Auto Cleanup** | Remove old entries to keep logs lean | ✨ |
| ⚙️ **Customizable** | YAML config for watch paths and ignore patterns | 🔧 |

---

## 🚀 Quick Start

### Requirements
- **Python** >= 3.8
- **pip** package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/gitstq/DevLogTracker.git
cd DevLogTracker

# Install dependencies
pip install -e .

# Or install directly
pip install devlog-tracker
```

### Basic Usage

```bash
# Initialize configuration (optional)
devlog init

# Start watching current directory
devlog watch

# View today's summary
devlog summary

# View weekly report
devlog week

# View productivity stats
devlog stats

# Generate HTML report
devlog report -o my_report.html

# Clean up entries older than 30 days
devlog cleanup -d 30
```

---

## 📖 Detailed Usage Guide

### Watch Multiple Directories

```bash
devlog watch -p ./src -p ./tests -o my_project.json
```

### Custom Configuration

Create `.devlog.yml` in your project root:

```yaml
watch_paths:
  - "./src"
  - "./lib"

ignore_patterns:
  - "*.pyc"
  - "__pycache__"
  - "node_modules"
  - ".git"

log_file: "devlog.json"

categories:
  code: [".py", ".js", ".ts"]
  config: [".json", ".yaml"]
```

### Productivity Score Algorithm

The productivity score (0-100) is calculated based on:
- **Daily average events** × 5 points
- **Unique files touched** × 2 points
- Capped at 100

Levels:
- 🔥 **Prolific** (80-100): Amazing output!
- ⚡ **Productive** (50-79): Solid work
- 🌱 **Steady** (20-49): Consistent progress
- 💤 **Quiet** (0-19): Time to code!

---

## 💡 Design Philosophy

### Why DevLogTracker?

1. **Non-intrusive**: Runs in background, no UI to distract you
2. **Privacy-first**: All data stays local, no cloud upload
3. **Developer-centric**: Built by developers, for developers
4. **Extensible**: Modular architecture for easy customization

### Tech Stack

| Component | Technology | Reason |
|-----------|-----------|--------|
| CLI Framework | Click | Mature, intuitive command design |
| Terminal UI | Rich | Beautiful tables, panels, progress bars |
| File Watching | Watchdog | Cross-platform, reliable |
| Config | PyYAML | Human-readable configuration |
| Templating | Jinja2 | Flexible HTML report generation |

---

## 📦 Packaging & Deployment

### Build Distribution

```bash
# Build wheel and source distribution
python setup.py sdist bdist_wheel

# The generated files will be in dist/
```

### Run Tests

```bash
python -m pytest tests/ -v
```

### Install in Development Mode

```bash
pip install -e .
```

---

## 🤝 Contributing Guide

We welcome contributions! Please follow these guidelines:

1. **Fork** the repository
2. Create a **feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'feat: add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. Open a **Pull Request**

### Commit Convention

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation update
- `refactor:` Code refactoring
- `test:` Test additions/changes

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<a name="简体中文"></a>
## 🎉 项目介绍

DevLogTracker 是一款**智能开发者活动追踪工具**，自动监控项目中的文件变更，记录开发行为，并提供精美的数据分析与可视化报告。

### 💡 灵感来源

作为开发者，我们每天花费无数小时编写代码，却很少对自己的开发模式有清晰的认知。DevLogTracker 正是为了解决这一痛点而生——它静默记录每一次文件变更，然后生成直观的报告，帮助你了解自己的编码习惯、高效时段和项目热点。

### ✨ 差异化亮点
- **零配置开箱即用**：内置合理的默认配置
- **实时监控**：文件系统监听器即时捕获变更
- **丰富分析**：每日摘要、周报、生产力评分
- **精美终端UI**：基于 Rich 的惊艳命令行界面
- **HTML报告**：导出专业报告便于分享
- **智能过滤**：自动忽略构建产物和依赖项

---

## ✨ 核心特性

| 特性 | 描述 | 状态 |
|---------|-------------|-------|
| 👁️ **实时监控** | 监控多个路径的文件变更 | 🟢 运行中 |
| 📊 **每日摘要** | 事件统计、高峰时段、活动跨度 | 📈 |
| 📈 **周报** | 可视化柱状图展示每日数据 | 📅 |
| 🏆 **生产力评分** | AI驱动的评分与个性化建议 | 🎯 |
| 🔥 **热点文件** | 识别最频繁编辑的文件 | 🔥 |
| 📄 **HTML导出** | 生成精美报告便于分享 | 🌐 |
| 🧹 **自动清理** | 删除旧记录保持日志精简 | ✨ |
| ⚙️ **可定制** | YAML配置监控路径和忽略规则 | 🔧 |

---

## 🚀 快速开始

### 环境要求
- **Python** >= 3.8
- **pip** 包管理器

### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/DevLogTracker.git
cd DevLogTracker

# 安装依赖
pip install -e .

# 或直接安装
pip install devlog-tracker
```

### 基本用法

```bash
# 初始化配置（可选）
devlog init

# 开始监控当前目录
devlog watch

# 查看今日摘要
devlog summary

# 查看周报
devlog week

# 查看生产力统计
devlog stats

# 生成HTML报告
devlog report -o my_report.html

# 清理30天前的记录
devlog cleanup -d 30
```

---

## 📖 详细使用指南

### 监控多个目录

```bash
devlog watch -p ./src -p ./tests -o my_project.json
```

### 自定义配置

在项目根目录创建 `.devlog.yml`：

```yaml
watch_paths:
  - "./src"
  - "./lib"

ignore_patterns:
  - "*.pyc"
  - "__pycache__"
  - "node_modules"
  - ".git"

log_file: "devlog.json"

categories:
  code: [".py", ".js", ".ts"]
  config: [".json", ".yaml"]
```

### 生产力评分算法

生产力评分（0-100）基于以下因素计算：
- **日均事件数** × 5 分
- **触及的唯一文件数** × 2 分
- 上限 100 分

等级划分：
- 🔥 **高产** (80-100)：惊人的产出！
- ⚡ **高效** (50-79)：扎实的工作
- 🌱 **稳健** (20-49)：持续进步
- 💤 **安静** (0-19)：该写代码了！

---

## 💡 设计思路

### 为什么选择 DevLogTracker？

1. **无侵入式**：后台运行，无干扰界面
2. **隐私优先**：所有数据本地存储，不上传云端
3. **开发者导向**：由开发者打造，为开发者服务
4. **可扩展**：模块化架构，易于定制

### 技术栈

| 组件 | 技术 | 选型理由 |
|-----------|-----------|--------|
| CLI 框架 | Click | 成熟、直观的命令设计 |
| 终端 UI | Rich | 精美的表格、面板、进度条 |
| 文件监控 | Watchdog | 跨平台、可靠 |
| 配置管理 | PyYAML | 人类可读的配置格式 |
| 模板引擎 | Jinja2 | 灵活的 HTML 报告生成 |

---

## 📦 打包与部署

### 构建分发包

```bash
# 构建 wheel 和源码分发
python setup.py sdist bdist_wheel

# 生成的文件位于 dist/ 目录
```

### 运行测试

```bash
python -m pytest tests/ -v
```

### 开发模式安装

```bash
pip install -e .
```

---

## 🤝 贡献指南

欢迎贡献！请遵循以下规范：

1. **Fork** 本仓库
2. 创建**功能分支** (`git checkout -b feature/amazing-feature`)
3. **提交** 更改 (`git commit -m 'feat: add amazing feature'`)
4. **推送** 到分支 (`git push origin feature/amazing-feature`)
5. 发起 **Pull Request**

### 提交规范

- `feat:` 新功能
- `fix:` 修复问题
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试相关

---

## 📄 开源协议

本项目采用 **MIT 协议** 开源 - 详见 [LICENSE](LICENSE) 文件。

---

<a name="繁體中文"></a>
## 🎉 專案介紹

DevLogTracker 是一款**智慧開發者活動追蹤工具**，自動監控專案中的檔案變更，記錄開發行為，並提供精美的資料分析與視覺化報告。

### 💡 靈感來源

作為開發者，我們每天花費無數小時編寫程式碼，卻很少對自己的開發模式有清晰的認知。DevLogTracker 正是為了解決這一痛點而生——它靜默記錄每一次檔案變更，然後生成直觀的報告，幫助你了解自己的編碼習慣、高效時段和專案熱點。

### ✨ 差異化亮點
- **零配置開箱即用**：內建合理的預設配置
- **即時監控**：檔案系統監聽器即時捕獲變更
- **豐富分析**：每日摘要、週報、生產力評分
- **精美終端UI**：基於 Rich 的驚豔命令列介面
- **HTML報告**：匯出專業報告便於分享
- **智慧過濾**：自動忽略建置產物和依賴項

---

## ✨ 核心特性

| 特性 | 描述 | 狀態 |
|---------|-------------|-------|
| 👁️ **即時監控** | 監控多個路徑的檔案變更 | 🟢 執行中 |
| 📊 **每日摘要** | 事件統計、高峰時段、活動跨度 | 📈 |
| 📈 **週報** | 視覺化柱狀圖展示每日資料 | 📅 |
| 🏆 **生產力評分** | AI驅動的評分與個人化建議 | 🎯 |
| 🔥 **熱點檔案** | 識別最頻繁編輯的檔案 | 🔥 |
| 📄 **HTML匯出** | 生成精美報告便於分享 | 🌐 |
| 🧹 **自動清理** | 刪除舊記錄保持日誌精簡 | ✨ |
| ⚙️ **可客製化** | YAML配置監控路徑和忽略規則 | 🔧 |

---

## 🚀 快速開始

### 環境要求
- **Python** >= 3.8
- **pip** 套件管理器

### 安裝

```bash
# 克隆倉庫
git clone https://github.com/gitstq/DevLogTracker.git
cd DevLogTracker

# 安裝依賴
pip install -e .

# 或直接安裝
pip install devlog-tracker
```

### 基本用法

```bash
# 初始化配置（可選）
devlog init

# 開始監控目前目錄
devlog watch

# 查看今日摘要
devlog summary

# 查看週報
devlog week

# 查看生產力統計
devlog stats

# 生成HTML報告
devlog report -o my_report.html

# 清理30天前的記錄
devlog cleanup -d 30
```

---

## 📖 詳細使用指南

### 監控多個目錄

```bash
devlog watch -p ./src -p ./tests -o my_project.json
```

### 自訂配置

在專案根目錄建立 `.devlog.yml`：

```yaml
watch_paths:
  - "./src"
  - "./lib"

ignore_patterns:
  - "*.pyc"
  - "__pycache__"
  - "node_modules"
  - ".git"

log_file: "devlog.json"

categories:
  code: [".py", ".js", ".ts"]
  config: [".json", ".yaml"]
```

### 生產力評分演算法

生產力評分（0-100）基於以下因素計算：
- **日均事件數** × 5 分
- **觸及的獨特檔案數** × 2 分
- 上限 100 分

等級劃分：
- 🔥 **高產** (80-100)：驚人的產出！
- ⚡ **高效** (50-79)：扎實的工作
- 🌱 **穩健** (20-49)：持續進步
- 💤 **安靜** (0-19)：該寫程式碼了！

---

## 💡 設計思路

### 為什麼選擇 DevLogTracker？

1. **無侵入式**：背景執行，無干擾介面
2. **隱私優先**：所有資料本地儲存，不上傳雲端
3. **開發者導向**：由開發者打造，為開發者服務
4. **可擴展**：模組化架構，易於客製化

### 技術棧

| 元件 | 技術 | 選型理由 |
|-----------|-----------|--------|
| CLI 框架 | Click | 成熟、直觀的命令設計 |
| 終端 UI | Rich | 精美的表格、面板、進度條 |
| 檔案監控 | Watchdog | 跨平台、可靠 |
| 配置管理 | PyYAML | 人類可讀的配置格式 |
| 模板引擎 | Jinja2 | 靈活的 HTML 報告生成 |

---

## 📦 打包與部署

### 建構分發包

```bash
# 建構 wheel 和原始碼分發
python setup.py sdist bdist_wheel

# 生成的檔案位於 dist/ 目錄
```

### 執行測試

```bash
python -m pytest tests/ -v
```

### 開發模式安裝

```bash
pip install -e .
```

---

## 🤝 貢獻指南

歡迎貢獻！請遵循以下規範：

1. **Fork** 本倉庫
2. 建立**功能分支** (`git checkout -b feature/amazing-feature`)
3. **提交** 更改 (`git commit -m 'feat: add amazing feature'`)
4. **推送** 到分支 (`git push origin feature/amazing-feature`)
5. 發起 **Pull Request**

### 提交規範

- `feat:` 新功能
- `fix:` 修復問題
- `docs:` 文件更新
- `refactor:` 程式碼重構
- `test:` 測試相關

---

## 📄 開源協議

本專案採用 **MIT 協議** 開源 - 詳見 [LICENSE](LICENSE) 文件。
