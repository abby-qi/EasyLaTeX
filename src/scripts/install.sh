#!/bin/bash
# ============================================================
#  EasyLaTeX 一键安装脚本 (Linux / macOS)
#  TinyTeX 必须装到【项目根目录】下的 tinytex/，
#  因为后端 tex_compiler.py 是按项目根来探测的。
# ============================================================
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT" || exit 1

echo "项目根目录: $PROJECT_ROOT"
echo

echo "[1/4] 正在配置 npm 镜像..."
cat > "$PROJECT_ROOT/.npmrc" <<'EOF'
registry=https://registry.npmmirror.com
strict-ssl=false
EOF

echo
echo "[2/4] 正在安装 Node.js 依赖..."
npm install || echo "[警告] npm install 失败，请检查网络"

echo
echo "[3/4] 正在安装 Python 依赖..."
if command -v python3 >/dev/null 2>&1; then
    python3 -m pip install -r "$PROJECT_ROOT/src/backend/requirements.txt" \
        || echo "[警告] Python 依赖安装失败"
else
    echo "[警告] 未找到 python3，跳过 Python 依赖安装"
fi

echo
echo "[4/4] 正在下载并安装 TinyTeX..."
TINYTEX_DIR="$PROJECT_ROOT/tinytex"

# 按平台推断 TinyTeX 的 bin 目录，用于判断是否已安装
case "$(uname)" in
    Darwin) BIN_SUB="bin/universal-darwin" ;;
    *)      BIN_SUB="bin/x86_64-linux" ;;
esac

if [ -x "$TINYTEX_DIR/$BIN_SUB/xelatex" ]; then
    echo "TinyTeX 已存在，跳过下载。"
else
    mkdir -p "$TINYTEX_DIR"
    echo "下载 TinyTeX (约 100MB，请耐心等待)..."
    if curl -fL -o "$TINYTEX_DIR/TinyTeX-1.tgz" "https://yihui.org/tinytex/TinyTeX-1.tgz"; then
        echo "解压中..."
        tar -xzf "$TINYTEX_DIR/TinyTeX-1.tgz" -C "$TINYTEX_DIR"
        rm -f "$TINYTEX_DIR/TinyTeX-1.tgz"
        # 官方压缩包里多一层 .TinyTeX 目录，摊平到 tinytex/ 下
        if [ -d "$TINYTEX_DIR/.TinyTeX" ]; then
            cp -a "$TINYTEX_DIR/.TinyTeX/." "$TINYTEX_DIR/"
            rm -rf "$TINYTEX_DIR/.TinyTeX"
        fi
    else
        echo "[警告] TinyTeX 下载失败。你可以："
        echo "  1. 手动从 https://yihui.org/tinytex/ 下载并解压到 $TINYTEX_DIR"
        echo "  2. 或安装 TeX Live 并加入 PATH"
    fi
fi

echo
echo "安装完成！"
echo "  TinyTeX 路径: $TINYTEX_DIR"
echo
echo "运行 npm start 启动应用（它会先构建前端再启动 Electron）。"
echo "  注意：不要单独运行根目录的 run.bat，它不会构建前端，会导致界面白屏。"
