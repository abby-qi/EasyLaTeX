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
