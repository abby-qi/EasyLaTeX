# EasyLaTeX - 极简可视化LaTeX编辑器

<div align="center">

![EasyLaTeX Logo](frontend/assets/icons/icon.png)

**为不懂LaTeX的用户提供Word式可视化操作，零配置生成学术PDF**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
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
- **🔄 实时预览**: 编译后立即查看PDF效果
- **📦 跨平台**: 支持Windows、macOS和Linux

## 🛠️ 技术栈

- **前端**: Electron + Vue 3
- **后端**: Python 3.9+
- **构建**: Docker
- **LaTeX编译**: MiKTeX / TinyTeX
- **核心依赖**: python-docx、pylatex

## 📦 安装与运行

### 方式一: 使用预编译安装包(推荐)

从 [GitHub Releases](https://github.com/abby-qi/EasyLaTeX/releases) 下载对应平台的安装包:

- Windows: `EasyLaTeX-Setup-x.x.x.exe`
- macOS: `EasyLaTeX-x.x.x.dmg`
- Linux: `EasyLaTeX-x.x.x.AppImage`

双击安装包即可安装使用。

### 方式二: 从源码运行

#### 前置要求

- Node.js 18+
- Python 3.9+
- npm 或 yarn
- MiKTeX 或 TinyTeX (用于LaTeX编译)

#### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/abby-qi/EasyLaTeX.git
cd EasyLaTeX
```

2. 安装依赖
```bash
npm install
pip install -r requirements.txt
```

3. 启动应用
```bash
npm start
```

### 方式三: 使用Docker构建

```bash
docker build -t easylatex -f docker/Dockerfile .
docker run -it easylatex
```

## 📚 使用教程

### 快速开始

1. **创建文档**: 选择预设模板(课程论文/试卷/实验报告)
2. **插入公式**: 点击左侧公式符号面板,选择需要的符号
3. **编辑表格**: 使用表格编辑器创建三线表
4. **编译预览**: 点击"编译"按钮生成PDF预览
5. **导出文档**: 选择导出格式(PDF/Word/LaTeX)

### 插入公式示例

点击公式符号面板中的"积分"按钮,会自动插入:
```latex
\int_{}^{}
```

然后手动填写上下限和被积函数即可。

### 创建三表示例

1. 设置行数和列数
2. 点击"创建表格"
3. 在表格单元格中输入内容
4. 点击"生成LaTeX"按钮

## 🏗️ 项目结构

```
latex-gui-editor/
├── backend/              # Python后端核心逻辑
│   ├── latex_generator/  # LaTeX代码生成模块
│   ├── compiler/         # LaTeX编译模块
│   ├── exporter/         # 导出模块
│   └── utils/           # 通用工具
├── frontend/            # Electron前端
│   ├── components/      # 可复用UI组件
│   ├── pages/          # 核心页面
│   └── styles/         # 全局样式
├── main/               # Electron主进程
├── config/             # 全局配置
│   └── templates/      # 预设文档模板
├── docker/             # Docker构建配置
└── test/              # 测试用例
```

## 🧪 测试

运行后端测试:
```bash
pytest tests/
```

运行前端测试:
```bash
npm test
```

## 📝 更新日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解详细的版本更新历史。

## 📚 常见问题 (FAQ)

### Q: 编译LaTeX时出现错误怎么办？

A: 检查以下几点：
1. 确保公式语法正确（括号匹配、符号使用等）
2. 检查表格格式是否正确（行列数是否匹配）
3. 查看错误提示，通常会给出具体的错误位置和建议

### Q: 导出的Word文档格式不对？

A: Word导出功能使用python-docx库，可能存在以下限制：
1. 复杂公式可能无法完美转换
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
2. 修改 `config/templates/` 目录下的模板文件
3. 后续版本将提供可视化模板编辑器

## 📝 开发计划

- [x] 项目初始化和骨架搭建
- [x] 后端核心功能实现
- [x] 前端UI完善
- [x] 集成测试
- [x] 性能优化
- [x] 用户文档完善

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议!

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 👥 作者

EasyLaTeX Team

## 🙏 致谢

- [Electron](https://www.electronjs.org/) - 跨平台桌面应用框架
- [Vue.js](https://vuejs.org/) - 渐进式JavaScript框架
- [TinyTeX](https://yihui.org/tinytex/) - 轻量级LaTeX发行版
- [python-docx](https://python-docx.readthedocs.io/) - Python Word文档库

## 📮 联系方式

- 项目主页: [https://github.com/abby-qi/EasyLaTeX](https://github.com/abby-qi/EasyLaTeX)
- 问题反馈: [Issues](https://github.com/abby-qi/EasyLaTeX/issues)

---

<div align="center">

如果这个项目对你有帮助,请给个⭐️支持一下!

Made with ❤️ by EasyLaTeX Team

</div>