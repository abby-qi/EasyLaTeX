# EasyLaTeX 便携版设置指南

本文档说明如何将 EasyLaTeX 配置为便携版，包含内置的 Node.js 和 TinyTeX，无需用户手动下载和配置路径。

## 步骤 1: 下载并放置 Node.js

1. 访问 [Node.js 官方网站](https://nodejs.org/en/download/) 下载 Windows 便携版（zip 格式）
2. 解压下载的 zip 文件到项目根目录，并重命名为 `nodejs`
3. 确保目录结构如下：
   ```
   EasyLaTeX/
   ├── nodejs/
   │   ├── node.exe
   │   └── ... 其他 Node.js 文件
   └── ... 其他项目文件
   ```

## 步骤 2: 下载并放置 TinyTeX

1. 访问 [TinyTeX 官方网站](https://yihui.org/tinytex/) 下载 Windows 版本
2. 解压下载的 zip 文件到项目根目录，确保目录名为 `tinytex`
3. 确保目录结构如下：
   ```
   EasyLaTeX/
   ├── tinytex/
   │   ├── bin/
   │   │   └── win32/
   │   │       ├── pdflatex.exe
   │   │       └── ... 其他 LaTeX 工具
   │   └── ... 其他 TinyTeX 文件
   └── ... 其他项目文件
   ```

## 步骤 3: 安装依赖

1. 运行 `install_deps.bat` 脚本安装项目依赖
   ```bash
   install_deps.bat
   ```

## 步骤 4: 启动应用

1. 运行 `run.bat` 脚本启动 EasyLaTeX
   ```bash
   run.bat
   ```

## 注意事项

- 便携版的 Node.js 和 TinyTeX 不会修改系统环境变量，因此不会影响系统其他应用
- 如果本地 Node.js 或 TinyTeX 不存在，应用会自动尝试使用系统安装的版本（如果有）
- 首次运行时，由于需要加载所有依赖，启动时间可能会稍长
- 便携版的体积会比标准版大，因为包含了 Node.js 和 TinyTeX 的完整副本

## 故障排除

### Node.js 相关问题
- 确保 `nodejs/node.exe` 文件存在且可执行
- 检查 `nodejs` 目录权限是否正确

### TinyTeX 相关问题
- 确保 `tinytex/bin/win32/pdflatex.exe` 文件存在
- 如果编译 LaTeX 时出现错误，检查 `tinytex` 目录结构是否正确

### 依赖安装问题
- 确保网络连接正常
- 如果 npm 安装失败，尝试修改 `.npmrc` 文件中的镜像源

## 目录结构

```
EasyLaTeX/
├── nodejs/           # 便携版 Node.js
├── tinytex/          # 便携版 TinyTeX
├── src/              # 源代码
├── node_modules/     # npm 依赖（运行 install_deps.bat 后生成）
├── install_deps.bat  # 依赖安装脚本
├── run.bat           # 启动脚本
└── ... 其他配置文件
```