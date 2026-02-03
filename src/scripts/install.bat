@echo off
echo 正在配置npm镜像...
echo registry=https://registry.npmmirror.com > .npmrc
echo strict-ssl=false >> .npmrc
echo.
echo 正在安装Node.js依赖...
call npm install
echo.
echo 正在下载并安装TinyTeX...
if not exist "tinytex" mkdir tinytex
cd tinytex

rem 下载TinyTeX for Windows
powershell -Command "Invoke-WebRequest -Uri 'https://yihui.org/tinytex/TinyTeX-1.zip' -OutFile 'TinyTeX.zip'"

rem 解压TinyTeX
powershell -Command "Expand-Archive -Path 'TinyTeX.zip' -DestinationPath '.'"

rem 清理安装包
del TinyTeX.zip

rem 返回项目根目录
cd ..
echo.
echo 配置git SSL验证...
call git config --global http.sslVerify false
echo.
echo 安装完成！
pause
