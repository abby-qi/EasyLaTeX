# EasyLaTeX - 极简可视化LaTeX编辑器

<div align="center">

![EasyLaTeX Logo](frontend/assets/icons/icon.png)

**为不懂LaTeX的用户提供Word式可视化操作，零配置生成学术PDF**

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Electron](https://img.shields.io/badge/Electron-28.0.0-blue)](https://www.electronjs.org/)
[![Python](https://img.shields.io/badge/Python-3.9+-green)](https://www.python.org/)

</div>

## 📖 项目简介

EasyLaTeX是一款专为研究生、中小学老师等非专业用户设计的可视化LaTeX编辑器。通过直观的图形界面，用户可以像使用Word一样轻松创建专业的学术论文、试卷和报告，无需学习复杂的LaTeX语法。

### ✨ 核心特性

- **🎨 可视化编辑**: 点击按钮插入公式符号，无需记忆LaTeX命令
- **📊 三线表支持**: 专业的学术表格编辑器，自动生成booktabs格式
- **📄 多格式导出**: 支持导出PDF、Word和LaTeX源码
- **🚀 零配置运行**: 内置TinyTeX，无需安装LaTeX环境
- **🔄 实时预览**: 编译后立即查看PDF效果（基于 pdf.js）
- **🧩 高级模式**: 透明编辑层 + 语法高亮 + 编译错误定位，可直编LaTeX源码
- **📦 跨平台**: 支持Windows、macOS和Linux

## 🛠️ 技术栈

- **前端**: Electron + Vue 3
- **后端**: Python 3.9+
- **构建/打包**: Vite + electron-builder（Docker 为可选方案，非主要构建方式）
- **LaTeX编译**: 集成TinyTeX（一键安装脚本自动下载到项目根 `tinytex/`）
- **核心依赖**: python-docx（Word 导出）、pdf.js（PDF 预览）、TinyTeX（PDF 编译引擎）

## 📦 安装与运行

### 方式一: 使用一键安装脚本(推荐)

安装脚本位于 `src/scripts/` 目录。

#### Windows用户

双击运行 `src/scripts/install.bat` 脚本即可自动完成以下配置：

* 配置npm淘宝镜像（加速依赖下载）
* 禁用SSL证书验证（避免网络问题）
* 安装所有Node.js依赖
* 下载并安装TinyTeX（LaTeX编译引擎）
* 配置git取消SSL验证

#### Linux/macOS用户

运行 `src/scripts/install.sh` 脚本即可自动完成以下配置：

* 配置npm淘宝镜像（加速依赖下载）
* 禁用SSL证书验证（避免网络问题）
* 安装所有Node.js依赖
* 下载并安装TinyTeX（LaTeX编译引擎）
* 配置git取消SSL验证

### 方式二: 手动配置

如果需要手动配置，请按以下步骤操作：

#### 配置npm镜像

创建 `.npmrc` 文件：

```ini
registry=https://registry.npmmirror.com
strict-ssl=false
```

#### 配置git取消SSL验证

```bash
git config --global http.sslVerify false
```

#### 安装依赖

```bash
npm install
```

### 方式三: 从源码运行

#### 前置要求

- Node.js 18+
- Python 3.9+
- npm 或 yarn
- 本机已安装 MiKTeX / TinyTeX / TeX Live（用于LaTeX编译，或运行安装脚本自动拉取 TinyTeX）

#### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/abby-qi/EasyLaTeX.git
cd EasyLaTeX
```

2. 安装依赖
```bash
npm install
pip install -r src/backend/requirements.txt
```

3. 启动应用
```bash
npm start
```

> ⚠️ 启动命令说明：请使用 `npm start`（等价于「构建前端 + 启动 Electron」）。**不要单独双击 `run.bat`**——`run.bat` 只会拉起 Electron，但前端 `src/dist/` 尚未构建时会白屏。

### 方式四: 使用Docker构建

```bash
docker build -t easylatex -f docker/Dockerfile .
docker run -it easylatex
```

## 📚 使用教程

### 快速开始

1. **创建文档**: 点击"新建文档"按钮，使用文档向导选择文档类型和专业
2. **插入公式**: 点击左侧公式符号面板,选择需要的符号
3. **编辑表格**: 使用表格编辑器创建三线表
4. **编译预览**: 点击"编译"按钮生成PDF效果
5. **导出文档**: 选择导出格式(PDF/Word/LaTeX)

### 插入公式示例

点击公式符号面板中的"积分"按钮,会自动插入:
```latex
\int_{}^{}
```
然后手动填写上下限和被积函数即可。

### 创建三线表示例

1. 设置行数和列数
2. 点击"创建表格"
3. 在表格单元格中输入内容
4. 点击"生成LaTeX"按钮

### 使用文档向导

文档向导可以帮助您快速创建适合特定专业的文档：

1. **步骤1: 选择文档类型**
   - 毕业论文: 适用于本科生、研究生的学位论文
   - 试卷: 适用于各类考试的试卷模板

2. **步骤2: 选择专业**
   - 数学专业: 包含数学公式和符号支持
   - 物理专业: 包含物理公式和单位支持
   - 计算机专业: 包含代码和算法支持
   - 其他专业: 通用模板，适用于其他专业

3. **创建文档**
   - 点击"创建文档"按钮，系统会自动生成适合您选择的模板
   - 模板会根据专业自动配置相应的LaTeX包和格式

### 高级模式（直接编辑LaTeX源码）

点击"高级模式"可切换为源码视图：
- 透明文本编辑层叠加在语法高亮层之上，所见即所得
- 左侧行号可点击，跳转到对应行
- 编译后若报错，错误定位器会解析引擎日志（`l.NNN` / `NNN:` / `line NN`）并自动跳转到出错行

## 🏗️ 项目结构

```
EasyLaTeX/
├── src/
│   ├── frontend/            # Electron + Vue 3 前端
│   │   ├── components/       # 可复用 UI 组件（含 AdvancedPanel 高级模式）
│   │   ├── pages/            # 核心页面（MainPage）
│   │   ├── assets/           # 图标、静态资源
│   │   └── styles/           # 全局样式
│   ├── backend/             # Python 后端核心逻辑
│   │   ├── latex_generator/  # LaTeX 代码生成模块
│   │   ├── compiler/         # LaTeX 编译模块（调用 TinyTeX）
│   │   └── exporter/         # PDF / Word / TeX 导出模块
│   ├── main/                # Electron 主进程（index.js / ipc_handlers.js / menu.js）
│   ├── config/
│   │   └── templates/        # 预设文档模板
│   ├── scripts/             # 安装 / 构建 / 测试脚本（install.bat / install.sh / run_tests.bat）
│   ├── tests/               # 后端测试（pytest）
│   └── dist/                # vite 生产构建产物（index.html + assets/）
├── docker/                  # 可选 Docker 构建配置（Dockerfile / docker-compose.yml）
├── node_modules/
├── package.json
├── vite.config.js
├── install.bat / install_deps.bat / run.bat
└── PORTABLE_SETUP.md
```

> 注：旧文档曾把根目录写成 `latex-gui-editor/` 并列出不存在的 `backend/utils/`、`frontend/config/`，以上结构为当前真实布局。

## 🧪 测试

运行后端测试:
```bash
pytest src/tests/
```

运行前端测试:
```bash
npm test
```

## ⚠️ 已知限制 / Known Limitations

- **Word 导出中的公式**: python-docx 没有原生公式（OMML）写入 API，因此导出的 `.docx` 里公式会降级为 *斜体等宽文本*（即 LaTeX 源码形式）。对公式保真度要求高的场景，建议优先导出 PDF。
- **PDF 预览/导出依赖 LaTeX 引擎**: 实时预览与 PDF 导出需要本机已安装 TinyTeX / TeX Live / MiKTeX。`install.bat` / `install.sh` 会自动下载 TinyTeX 到项目根 `tinytex/`；若跳过安装则需手动配置编译引擎路径。
- **GUI 未做自动化端到端验证**: 当前无显示（headless）环境下无法自动点击验证完整图形界面流程。构建产物（`src/dist`）与编译链路已验证可正常产出，但首次启动请在带显示器的机器上跑一次 `npm start` 确认交互无误。
- **PDF 预览依赖 pdf.js 原生包**: 预览面板使用 `pdfjs-dist`（v6.x）。该原生二进制包在某些网络/环境下 `npm install` 可能下载不完整（表现为预览空白）。若遇此情况，优先执行 `npm install pdfjs-dist --no-cache` 重装。

## 📝 更新日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解详细的版本更新历史。

## 📚 常见问题 (FAQ)

### Q: 编译LaTeX时出现错误怎么办？

A: 检查以下几点：
1. 确保公式语法正确（括号匹配、符号使用等）
2. 检查表格格式是否正确（行列数是否匹配）
3. 查看错误提示，通常会给出具体的错误位置和建议
4. 使用高级模式时，错误定位器会自动跳转到出错行

### Q: 导出的Word文档格式不对？

A: Word导出功能使用python-docx库，可能存在以下限制：
1. 复杂公式无法完美转换（会降级为斜体等宽文本，见"已知限制"）
2. 表格样式可能与LaTeX略有不同
3. 建议使用PDF导出以获得最佳效果

### Q: 软件启动慢怎么办？

A: 尝试以下优化：
1. 关闭不必要的后台应用
2. 增加系统内存
3. 清理缓存文件
4. 使用最新版本的软件

### Q: 如何自定义LaTeX模板？

A: 目前版本支持以下方式：
1. 使用高级模式直接编辑LaTeX源码
2. 修改 `src/config/templates/` 目录下的模板文件
3. 后续版本将提供可视化模板编辑器

### Q: 预览面板空白 / PDF 不显示？

A: 优先排查 pdf.js 原生包是否安装完整：
1. 检查 `node_modules/pdfjs-dist/build/pdf.worker.min.mjs` 是否存在
2. 若不存在或大小异常，执行 `npm install pdfjs-dist --no-cache` 重装
3. 确认本机已安装 LaTeX 引擎（TinyTeX / TeX Live / MiKTeX），否则无 PDF 可预览

### Q: npm install失败怎么办？

A: 如果npm install失败，请尝试：
1. 使用一键安装脚本（src/scripts/install.bat 或 src/scripts/install.sh）
2. 手动配置npm镜像和SSL验证
3. 检查网络连接
4. 清理npm缓存：`npm cache clean --force`
5. 使用管理员权限运行终端

## 📝 开发计划

- [x] 项目初始化和骨架搭建
- [x] 后端核心功能实现
- [x] 前端UI完善
- [x] 高级模式（AdvancedPanel）实现
- [x] 生产构建验证（vite build 通过，无白屏）
- [x] 用户文档完善
- [ ] 端到端 GUI 自动化测试
- [ ] Word 公式（OMML）原生支持
- [ ] 可视化模板编辑器

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议!

### 贡献流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request
6. **签署 CLA**: 在您的首次 Pull Request 中添加一条评论，表明您同意 CLA 的条款

### 签署 CLA (Contributor License Agreement)

所有贡献者必须签署贡献者许可协议 (CLA)，以确保项目的知识产权清晰。签署方式：

- **个人贡献者**: 在首次 Pull Request 中添加评论：
  ```
  I hereby agree to the terms of the Contributor License Agreement.
  ```

- **企业贡献者**: 在首次 Pull Request 中添加评论，指明代表的企业：
  ```
  I hereby agree to the terms of the Contributor License Agreement on behalf of [公司/组织名称].
  ```

详细信息请参阅 [CLA.md](CLA.md) 文件。

## 📄 许可证

本项目采用 GNU Affero General Public License v3.0 (AGPLv3) - 详见 [LICENSE](LICENSE) 文件

## 👥 作者

EasyLaTeX Team

## 🙏 致谢

- [Electron](https://www.electronjs.org/) - 跨平台桌面应用框架
- [Vue.js](https://vuejs.org/) - 渐进式JavaScript框架
- [TinyTeX](https://yihui.org/tinytex/) - 轻量级LaTeX发行版
- [python-docx](https://python-docx.readthedocs.io/) - Python Word文档库
- [pdf.js](https://mozilla.github.io/pdf.js/) - PDF 预览引擎

## 📮 联系方式

- 项目主页: [https://github.com/abby-qi/EasyLaTeX](https://github.com/abby-qi/EasyLaTeX)
- 问题反馈: [Issues](https://github.com/abby-qi/EasyLaTeX/issues)

---

<div align="center">

如果这个项目对你有帮助,请给个⭐️支持一下!

Made with ❤️ by EasyLaTeX Team

</div>
