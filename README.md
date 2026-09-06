# EasyLaTeX

> 极简可视化 LaTeX 编辑器 —— 为不懂 LaTeX 的用户提供 Word 式可视化操作，零配置生成学术 PDF。
> 本文是项目入口文档；完整使用教程、FAQ 与贡献指南见 [`src/docs/README.md`](src/docs/README.md)。

## 这个项目现在能用吗？

代码层面已补全，且 `vite build` 生产构建**已验证通过**。但首次使用前必须跑一次一键安装（会下载约 100MB 的 TinyTeX 并安装 Python 依赖）。本仓库的桌面 GUI 尚未在自动化环境实机点开验证，按下方步骤在本机装好后即可使用。

## 已实现的功能

- **可视化插入**：左侧公式符号面板、表格编辑器（三线表 / booktabs 风格）。
- **实时 PDF 预览**：基于 pdf.js，编译后即时渲染（内置状态机处理「无引擎 / 编译错误 / 加载中 / 就绪」）。
- **多格式导出**：
  - **PDF**：调用 TinyTeX / TeX Live / MiKTeX 的 `xelatex` / `pdflatex` / `lualatex`（中文文档自动选 `xelatex`）。
  - **Word**：基于 python-docx，生成**真正能被 Word 打开**的 `.docx`（公式降级为斜体等宽文本，见限制）。
  - **LaTeX 源码**：导出 `.tex`。
- **中文菜单栏**：文件 / 编辑 / 视图 / 帮助，与编辑区联动（新建、打开、保存、导出、编译、高级模式、环境检测等）。
- **模板系统**：4 类模板（论文 / 课程论文 / 报告 / 试卷）× 4 个专业（数学 / 物理 / 计算机 / 其他），由 `manifest.json` 驱动。
- **高级模式**：语法高亮源码编辑器 + 行号槽 + 编译错误定位（解析日志中的 `l.NNN` 跳转到对应行）。
- **LaTeX 引擎自动探测**：优先项目根 `tinytex/`，其次系统 PATH；中文文档自动选用 `xelatex`。

## 技术栈

- 前端：Electron + Vue 3 + Vite
- 后端：Python 3.9+（公式 / 表格生成、编译、导出）
- 预览：pdf.js（`pdfjs-dist`）
- Word 导出：python-docx
- 构建 / 打包：Vite + electron-builder（另有可选 Docker 方案）

## 安装与启动

### 方式一：一键安装（推荐）

Windows：

```bash
src\scripts\install.bat
```

Linux / macOS：

```bash
bash src/scripts/install.sh
```

脚本会：配置 npm 镜像 → `npm install` → `pip install -r src/backend/requirements.txt`（含 python-docx）→ 下载并解压 TinyTeX 到项目根 `tinytex\`。

### 启动（关键）

```bash
npm start          # = vite build + electron .  ← 正确方式：先构建再启动
```

> ⚠️ **不要只跑 `run.bat`**：`run.bat` 直接启动 electron 但**不先做生产构建**，若没有 `src/dist` 产物会回退到源码入口（而源码入口需要 Vite 编译 `.vue`，会失败）。统一用 `npm start`。

开发模式（热重载）：

```bash
npm run dev        # vite dev server + electron --dev
```

### 前置要求

- Node.js 18+（本机以 22 验证）
- Python 3.9+（Word 导出需要 `python-docx`，已在 `src/backend/requirements.txt`）
- 编译 PDF 需要 LaTeX 引擎：一键安装会自带 TinyTeX；也可使用系统已装的 TeX Live / MiKTeX

## 项目结构

```
EasyLaTeX/
├── src/
│   ├── main/              # Electron 主进程（窗口 / 菜单 / IPC）
│   ├── frontend/          # Vue 3 前端（components / pages / styles / assets）
│   ├── backend/           # Python 后端
│   │   ├── latex_generator/   # 公式 / 表格 LaTeX 生成
│   │   ├── compiler/          # tex_compiler.py：调用 LaTeX 引擎
│   │   └── exporter/          # word / pdf / tex 导出
│   ├── config/templates/  # 模板 manifest.json + .tex
│   └── scripts/           # install.bat / install.sh
├── docker/                # 可选 Docker 方案
├── package.json
└── vite.config.js
```

## 已知限制

- **Word 中的数学公式**：python-docx 没有原生公式（OMML）写入接口，公式降级为斜体等宽文本；需要精确排版的公式请导出 PDF。
- **PDF 编译依赖引擎**：未安装 TinyTeX / TeX Live / MiKTeX 时，预览与 PDF 导出会提示先安装。
- **GUI 端到端未自动验证**：构建与后端模块均已验证，但桌面窗口的实机交互需你在本机 `npm start` 后确认。
- 本机 `npm install` 偶发会把原生二进制包（如 `pdfjs-dist`、`esbuild`）装残，重装即可（详见开发者说明）。

## 开发者说明

- 生产构建：`npm run build`（产物在 `src/dist`，主进程解析 `src/dist/index.html`）。
- 打包发布：`npm run build:win` / `:mac` / `:linux`（electron-builder；`package.json` 的 `build.files` 已包含 `src/dist/**/*`）。
- 后端模块可用 CLI 单独验证，例如：
  ```bash
  python src/backend/latex_generator/formula_gen.py '{"formula_type":"integral"}'
  python src/backend/latex_generator/table_gen.py '{"data":[["a","b"],["1","2"]]}'
  ```

许可证：AGPL-3.0。完整文档见 [`src/docs/README.md`](src/docs/README.md)。
