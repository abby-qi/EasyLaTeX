# 更新日志 (CHANGELOG)

本文档记录EasyLaTeX项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [0.1.1] - 2026-01-09

### 新增功能

#### 用户界面优化

* ✨ 实现完整的中文菜单栏系统

  * 文件菜单：新建、打开、保存、退出

  * 编辑菜单：撤销、重做、剪切、复制、粘贴、全选

  * 视图菜单：重新加载、开发者工具、缩放、全屏

  * 帮助菜单：关于EasyLaTeX

* ✨ 实现文件对话框功能

  * 支持打开LaTeX文件（.tex）

  * 支持保存LaTeX文件（.tex）

  * 支持文本文件（.txt）

* ✨ 实现前端事件监听

  * 监听菜单栏IPC消息

  * 实现新建、打开、保存功能

#### 技术实现

##### 构建系统优化

* ✅ 配置Vite构建工具

  * 创建vite.config.js配置文件

  * 配置ES模块导入方式

  * 设置正确的构建输出路径

* ✅ 修复Vue应用加载问题

  * 修改main.js使用ES模块导入

  * 修复HTML文件路径配置

  * 确保CSS和JS正确生成

##### Electron主进程优化

* ✅ 完善IPC处理器

  * 添加文件对话框处理器

  * 实现open-file-dialog和save-file-dialog

  * 集成fs.promises文件操作

##### 前端组件优化

* ✅ 完善MainPage.vue

  * 添加mounted生命周期钩子

  * 实现newFile、openFile、saveFile方法

  * 添加用户确认提示

#### Bug修复

* 🐛 修复应用启动后界面空白问题

  * 配置正确的HTML加载路径

  * 修复Vite构建配置

  * 确保Vue应用正确挂载

* 🐛 修复菜单栏功能不可用问题

  * 添加IPC事件监听

  * 实现文件操作功能

#### 依赖更新

* 📦 添加Vite构建依赖

  * vite@^7.3.1

  * @vitejs/plugin-vue@^6.0.3

* 📦 添加开发工具依赖

  * concurrently@latest

  * wait-on@latest

#### 项目清理

* 🧹 删除临时测试文件

  * 删除根目录8个测试文件

  * 删除test/目录2个测试文件

  * 删除tests/目录5个文件

---

## [0.1.0] - 2026-01-09