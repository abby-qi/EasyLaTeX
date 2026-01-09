# EasyLaTeX 项目部署与依赖优化计划

## 📋 问题分析

### 🔍 当前项目配置状态

1. **LaTeX编译环境**

   * 当前使用`spawn('python', ...)`调用Python脚本

   * 依赖本地Python环境和LaTeX编译器

   * 没有内嵌TinyTeX或MiKTeX

2. **Node.js依赖**

   * package.json已配置完整依赖

   * 需要运行`npm install`安装

3. **npm镜像配置**

   * 需要配置国内npm镜像源

   * 加速依赖下载

4. **SSL证书验证**

   * 需要禁用或配置SSL证书验证

   * 避免网络连接问题

5. **项目打包**

   * 当前未将LaTeX环境打包进应用

   * 需要用户本地安装编译器

## 🎯 解决方案

### 方案一：配置npm国内镜像（推荐）

#### 创建.npmrc配置文件

在项目根目录创建`.npmrc`文件：

```ini
registry=https://registry.npmmirror.com
strict-ssl=false
```

**说明：**

* `registry`: 使用淘宝npm镜像

* `strict-ssl=false`: 禁用SSL证书验证

#### 配置git取消SSL验证

```bash
git config --global http.sslVerify false
```

### 方案二：更新README.md部署说明

#### 添加LaTeX环境要求说明

在README.md中明确说明：

**LaTeX编译器安装要求：**

1. **Windows用户**：

   * 下载并安装MiKTeX（推荐）或TinyTeX

   * 或使用在线编译服务（如Overleaf）

2. **macOS用户**：

   * 使用MacTeX或安装MiKTeX

   * 或使用在线编译服务

3. **Linux用户**：

   * 安装TeX Live或MiKTeX

   * 或使用在线编译服务

**在线编译服务推荐：**

* Overleaf: <https://www.overleaf.com/>

* TeXLive: <https://www.texlive.net/>

### 方案三：提供一键安装脚本

#### 创建install.bat（Windows）

```batch
@echo off
echo 正在配置npm镜像...
echo registry=https://registry.npmmirror.com > .npmrc
echo strict-ssl=false >> .npmrc
echo.
echo 正在安装Node.js依赖...
call npm install
echo.
echo 配置git SSL验证...
call git config --global http.sslVerify false
echo.
echo 安装完成！
pause
```

#### 创建install.sh（Linux/macOS）

```bash
#!/bin/bash
echo "正在配置npm镜像..."
echo "registry=https://registry.npmmirror.com" > .npmrc
echo "strict-ssl=false" >> .npmrc
echo ""
echo "正在安装Node.js依赖..."
npm install
echo ""
echo "配置git SSL验证..."
git config --global http.sslVerify false
echo ""
echo "安装完成！"
```

### 方案四：更新CHANGELOG.md

添加部署相关说明：

```markdown
### 部署优化

#### npm镜像配置
* ✅ 添加.npmrc配置文件
  * 使用淘宝npm镜像加速依赖下载
  * 禁用SSL证书验证

#### Git配置
* ✅ 配置git取消SSL验证
  * 避免证书验证失败问题

#### 安装脚本
* ✅ 提供Windows一键安装脚本
* ✅ 提供Linux/macOS一键安装脚本
* ✅ 自动配置所有必要的环境变量

#### LaTeX环境说明
* ✅ 明确LaTeX编译器安装要求
  * Windows: MiKTeX或TinyTeX
  * macOS: MacTeX或MiKTeX
  * Linux: TeX Live或MiKTeX
* ✅ 推荐在线编译服务
  * Overleaf
  * TeXLive
```

### 方案五：创建部署文档

创建`docs/DEPLOYMENT.md`文件，包含：

* 详细的安装步骤

* 常见问题解决方案

* 环境配置说明

* 故障排查指南

## 📝 执行步骤

1. **创建.npmrc配置文件**
2. **创建install.bat安装脚本**
3. **创建install.sh安装脚本**
4. **更新README.md添加部署说明**
5. **更新CHANGELOG.md添加部署优化**
6. **提交所有更改到Git**

## ✅ 预期结果

* npm依赖下载速度提升

* SSL证书验证问题解决

* 用户安装体验改善

* 部署文档完善

* 项目可维护性提升

