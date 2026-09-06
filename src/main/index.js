const { app, BrowserWindow } = require('electron');
const path = require('path');
const fs = require('fs');
const http = require('http');

// 生产构建产物是 ES module（<script type="module">）。
// 之前尝试过 file:// 和自定义 app:// 协议，但前者被 Chromium 的 module CORS 拦截，
// 后者 registerFileProtocol 返回的 .js 不一定带 text/javascript，module 脚本仍被拒执行，
// 都会表现为纯白屏、JS 一句都不跑。
//
// 最稳的做法：用 Node 内置 http 起一个本地静态服务器托管 src/dist，
// MIME 类型完全可控，ES module 在同源 http 下既无 CORS 也无 MIME 问题。
const DIST_DIR = path.join(__dirname, '../dist');

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.wasm': 'application/wasm',
};

// 生产环境静态服务器地址（app ready 后启动，端口随机避免冲突）
let PROD_URL = null;

function startStaticServer() {
  return new Promise((resolve, reject) => {
    const server = http.createServer((req, res) => {
      try {
        const reqPath = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
        const rel = reqPath === '/' ? '/index.html' : reqPath;
        const filePath = path.normalize(path.join(DIST_DIR, rel));
        // 防目录穿越：必须落在 DIST_DIR 之内
        if (filePath !== DIST_DIR && !filePath.startsWith(DIST_DIR + path.sep)) {
          res.writeHead(403);
          return res.end('Forbidden');
        }
        fs.stat(filePath, (err, stat) => {
          if (err || !stat.isFile()) {
            res.writeHead(404);
            return res.end('Not found');
          }
          const ext = path.extname(filePath).toLowerCase();
          res.writeHead(200, {
            'Content-Type': MIME[ext] || 'application/octet-stream',
            'Cache-Control': 'no-cache',
          });
          fs.createReadStream(filePath).pipe(res);
        });
      } catch (e) {
        res.writeHead(500);
        res.end('Internal error');
      }
    });
    server.listen(0, '127.0.0.1', () => {
      resolve(`http://127.0.0.1:${server.address().port}`);
    });
    server.on('error', reject);
  });
}

// 加载 IPC 处理函数与菜单栏
require('./ipc_handlers');
const { setupMenu } = require('./menu');

// 确保应用单实例
const gotTheLock = app.requestSingleInstanceLock();

if (!gotTheLock) {
  app.quit();
} else {
  app.on('second-instance', (event, commandLine, workingDirectory) => {
    // 当第二实例启动时，聚焦到现有窗口
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.focus();
    }
  });
}

let mainWindow;

function resolveIcon() {
  // 图标文件可能缺失（例如刚 clone 还没生成资源），
  // 缺失时不要让窗口创建失败，直接不带图标启动。
  const candidates = [
    path.join(__dirname, '../frontend/assets/icons/icon.png'),
    path.join(__dirname, '../assets/icons/icon.png'),
  ];
  for (const p of candidates) {
    if (fs.existsSync(p)) return p;
  }
  return undefined;
}

/**
 * 决定加载哪个页面。
 * - --dev：优先连 vite 开发服务器 (localhost:5173)，连不上就回退到本地静态服务器（已构建产物）。
 * - 其余：本地静态服务器托管的 src/dist/index.html。
 */
function resolveEntry() {
  const isDev = process.argv.includes('--dev');
  if (isDev) {
    return { type: 'url', target: 'http://localhost:5173', fallback: PROD_URL };
  }
  return { type: 'url', target: PROD_URL };
}

function createWindow() {
  const icon = resolveIcon();

  mainWindow = new BrowserWindow({
    width: 1280,
    height: 860,
    minWidth: 900,
    minHeight: 600,
    webPreferences: {
      preload: path.join(__dirname, '../frontend/preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
    },
    title: 'EasyLaTeX',
    icon: icon,
    show: false,
    backgroundColor: '#f0f2f5',
  });

  const entry = resolveEntry();

  if (entry.type === 'url') {
    // 开发模式连不上 5173 时，自动回退到已构建产物，避免白屏
    if (entry.fallback) {
      mainWindow.webContents.once('did-fail-load', () => {
        mainWindow.loadURL(entry.fallback);
      });
    }
    mainWindow.loadURL(entry.target);
    if (process.argv.includes('--dev')) {
      mainWindow.webContents.openDevTools();
    }
  }

  // 等页面渲染完再显示窗口，避免启动瞬间闪白屏
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  mainWindow.on('closed', function () {
    mainWindow = null;
  });
}

app.on('ready', async () => {
  // 先启动本地静态服务器，再建窗口
  try {
    PROD_URL = await startStaticServer();
  } catch (err) {
    console.error('[EasyLaTeX] 启动静态服务器失败:', err);
  }

  if (!PROD_URL) {
    console.error('[EasyLaTeX] 未启动静态服务器，且未找到可用的页面入口，应用可能无法显示内容。');
  }

  setupMenu();
  createWindow();
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', function () {
  if (mainWindow === null) createWindow();
});
