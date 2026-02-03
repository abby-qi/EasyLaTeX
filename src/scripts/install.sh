#!/bin/bash
echo "正在配置npm镜像..."
echo "registry=https://registry.npmmirror.com" > .npmrc
echo "strict-ssl=false" >> .npmrc
echo ""
echo "正在安装Node.js依赖..."
npm install
echo ""
echo "正在下载并安装TinyTeX..."
mkdir -p tinytex
cd tinytex

# 下载TinyTeX
if [[ "$(uname)" == "Darwin" ]]; then
    # macOS
    curl -LO "https://yihui.org/tinytex/TinyTeX-1.tgz"
    tar -xzf TinyTeX-1.tgz
else
    # Linux
    curl -LO "https://yihui.org/tinytex/TinyTeX-1.tgz"
    tar -xzf TinyTeX-1.tgz
fi

# 清理安装包
rm -f TinyTeX-1.tgz

# 返回项目根目录
cd ..
echo ""
echo "配置git SSL验证..."
git config --global http.sslVerify false
echo ""
echo "安装完成！"
