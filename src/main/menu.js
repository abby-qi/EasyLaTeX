const { Menu, dialog, shell, app, BrowserWindow } = require('electron');

/**
 * 应用中文菜单栏
 *
 * CHANGELOG 0.1.1 里宣称"实现完整的中文菜单栏系统"，但 main/index.js 中
 * 从来没有创建过 Menu，preload 暴露的 onNewFile / onOpenFile / onSaveFile
 * 三个监听器永远等不到事件，菜单相关的功能全是死的。这里补齐。
 *
 * 菜单项通过 webContents.send 把事件派发给渲染进程，事件名统一使用
 * 'menu:*' 前缀，避免和 IPC invoke 通道混淆。
 */

function sendToRenderer(eventName, ...args) {
  const win = BrowserWindow.getFocusedWindow() || BrowserWindow.getAllWindows()[0];
  if (win && win.webContents) {
    win.webContents.send(eventName, ...args);
  }
}

function buildMenu() {
  const isMac = process.platform === 'darwin';

  const template = [
    // ---------------- 文件 ----------------
    {
      label: '文件',
      submenu: [
        {
          label: '新建',
          accelerator: 'CmdOrCtrl+N',
          click: () => sendToRenderer('menu:new-file'),
        },
        {
          label: '从模板新建…',
          accelerator: 'CmdOrCtrl+Shift+N',
          click: () => sendToRenderer('menu:new-from-template'),
        },
        {
          label: '打开…',
          accelerator: 'CmdOrCtrl+O',
          click: () => sendToRenderer('menu:open-file'),
        },
        {
          label: '保存',
          accelerator: 'CmdOrCtrl+S',
          click: () => sendToRenderer('menu:save-file'),
        },
        { type: 'separator' },
        {
          label: '导出 PDF…',
          accelerator: 'CmdOrCtrl+E',
          click: () => sendToRenderer('menu:export-pdf'),
        },
        {
          label: '导出 Word…',
          accelerator: 'CmdOrCtrl+Shift+W',
          click: () => sendToRenderer('menu:export-word'),
        },
        {
          label: '导出 LaTeX 源码…',
          accelerator: 'CmdOrCtrl+Shift+E',
          click: () => sendToRenderer('menu:export-tex'),
        },
        { type: 'separator' },
        isMac ? { role: 'close' } : { role: 'quit', label: '退出' },
      ],
    },

    // ---------------- 编辑 ----------------
    {
      label: '编辑',
      submenu: [
        { role: 'undo', label: '撤销' },
        { role: 'redo', label: '重做' },
        { type: 'separator' },
        { role: 'cut', label: '剪切' },
        { role: 'copy', label: '复制' },
        { role: 'paste', label: '粘贴' },
        { role: 'selectAll', label: '全选' },
        { type: 'separator' },
        {
          label: '查找…',
          accelerator: 'CmdOrCtrl+F',
          click: () => sendToRenderer('menu:find'),
        },
      ],
    },

    // ---------------- 视图 ----------------
    {
      label: '视图',
      submenu: [
        {
          label: '编译预览',
          accelerator: 'CmdOrCtrl+R',
          click: () => sendToRenderer('menu:compile'),
        },
        {
          label: '自动编译预览',
          type: 'checkbox',
          checked: false,
          click: (item) => sendToRenderer('menu:toggle-auto-compile', item.checked),
        },
        { type: 'separator' },
        {
          label: '高级模式',
          accelerator: 'CmdOrCtrl+Shift+A',
          click: () => sendToRenderer('menu:toggle-advanced'),
        },
        { type: 'separator' },
        { role: 'reload', label: '重新加载' },
        { role: 'toggleDevTools', label: '开发者工具' },
        { type: 'separator' },
        { role: 'resetZoom', label: '实际大小' },
        { role: 'zoomIn', label: '放大' },
        { role: 'zoomOut', label: '缩小' },
        { type: 'separator' },
        { role: 'togglefullscreen', label: '全屏' },
      ],
    },

    // ---------------- 帮助 ----------------
    {
      label: '帮助',
      submenu: [
        {
          label: '检查 LaTeX 环境',
          click: () => sendToRenderer('menu:check-env'),
        },
        {
          label: '打开模板目录',
          click: () => {
            const dir = require('./template_manager').TEMPLATE_DIR;
            shell.openPath(dir);
          },
        },
        { type: 'separator' },
        {
          label: '关于 EasyLaTeX',
          click: () => {
            const win = BrowserWindow.getFocusedWindow();
            dialog.showMessageBox(win || null, {
              type: 'info',
              title: '关于 EasyLaTeX',
              message: 'EasyLaTeX',
              detail: [
                '版本: ' + app.getVersion(),
                '极简可视化 LaTeX 编辑器',
                '',
                '为不懂 LaTeX 的用户提供 Word 式可视化操作，零配置生成学术 PDF。',
              ].join('\n'),
              buttons: ['确定'],
            });
          },
        },
      ],
    },
  ];

  return Menu.buildFromTemplate(template);
}

function setupMenu() {
  Menu.setApplicationMenu(buildMenu());
}

module.exports = { setupMenu, buildMenu, sendToRenderer };
