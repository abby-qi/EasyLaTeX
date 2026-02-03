# EasyLaTeX

极简可视化LaTeX编辑器

## 项目说明

这是 EasyLaTeX 项目的根目录。完整的项目文档和说明请查看 `src/docs/README.md` 文件。

## 快速开始

### 安装依赖

```bash
# 使用安装脚本
./src/scripts/install.bat  # Windows
./src/scripts/install.sh   # Linux/macOS

# 或手动安装
npm install
pip install -r src/backend/requirements.txt
```

### 运行项目

```bash
# 开发模式
npm run dev

# 生产模式
npm start
```

## 项目结构

```
EasyLaTeX/
├── src/                # 源代码目录
│   ├── backend/       # Python 后端代码
│   ├── frontend/       # Electron + Vue 前端代码
│   ├── main/           # Electron 主进程代码
│   ├── config/         # 配置文件和模板
│   ├── docs/           # 项目文档
│   ├── scripts/        # 脚本文件
│   └── tests/          # 测试文件
├── docker/             # Docker 相关配置
├── package.json        # npm 项目配置
└── vite.config.js      # Vite 构建配置
```

## 许可证

本项目采用 GNU Affero General Public License v3.0 (AGPLv3) - 详见 `src/docs/LICENSE` 文件。
