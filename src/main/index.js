const { app, BrowserWindow } = require('electron');
const path = require('path');
const fs = require('fs');

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
 *
 * 历史问题：vite build 的产物输出在 src/dist，而主进程一直加载
 * src/frontend/index.html。那份 index.html 里是
 * <script type="module" src="./main.js">，main.js 又写了裸导入
 * import { createApp } from 'vue'，浏览器根本解析不了 ——
 * 于是 CHANGELOG 里宣称"修复了启动白屏"，实际上生产模式必然白屏。
 *
 * 现在按优先级选择：dev 地址 -> 构建产物 -> 源码入口（并给出明确警告）。
 */
function resolveEntry() {
  const isDev = process.argv.includes('--dev');
  if (isDev) {
    return { type: 'url', target: 'http://localhost:5173' };
  }

  const distIndex = path.join(__dirname, '../dist/index.html');
  if (fs.existsSync(distIndex)) {
    return { type: 'file', target: distIndex };
  }

  const srcIndex = path.join(__dirname, '../frontend/index.html');
  return { type: 'file', target: srcIndex, warn: true };
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
    mainWindow.loadURL(entry.target);
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(entry.target);
    if (entry.warn) {
      console.warn(
        '[EasyLaTeX] 未找到构建产物 src/dist/index.html，已回退到源码入口。\n' +
        '如果页面空白，请先执行 npm run build 再启动，或使用 npm run dev。'
      );
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

app.on('ready', () => {
  setupMenu();
  createWindow();
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', function () {
  if (mainWindow === null) createWindow();
});
