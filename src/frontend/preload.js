const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
  // 公式生成
  generateFormula: (formulaData) => ipcRenderer.invoke('generate-formula', formulaData),
  // 表格生成
  generateTable: (tableData) => ipcRenderer.invoke('generate-table', tableData),
  // 导出功能
  exportWord: (data, outputPath) => ipcRenderer.invoke('export-word', data, outputPath),
  exportTex: (data, outputPath) => ipcRenderer.invoke('export-tex', data, outputPath),
  exportPdf: (data, outputPath) => ipcRenderer.invoke('export-pdf', data, outputPath),
  // 文件操作
  openFileDialog: () => ipcRenderer.invoke('open-file-dialog'),
  saveFileDialog: (content) => ipcRenderer.invoke('save-file-dialog', content),
  exportFileDialog: (exportType) => ipcRenderer.invoke('export-file-dialog', exportType),
  // 菜单事件
  onNewFile: (callback) => ipcRenderer.on('new-file', callback),
  onOpenFile: (callback) => ipcRenderer.on('open-file', callback),
  onSaveFile: (callback) => ipcRenderer.on('save-file', callback),
  // 新增：来自主进程菜单栏的事件（menu:* 前缀）
  onMenu: (eventName, callback) => {
    ipcRenderer.on(eventName, (event, ...args) => callback(...args));
  },
  // 模板
  getTemplates: () => ipcRenderer.invoke('get-templates'),
  renderTemplate: (templateId, major, fields) => ipcRenderer.invoke('render-template', templateId, major, fields),
  // 编译与预览
  compileLatex: (texContent, options) => ipcRenderer.invoke('compile-latex', texContent, options),
  checkLatexEnv: () => ipcRenderer.invoke('check-latex-env'),
  readPdfData: (filePath) => ipcRenderer.invoke('read-pdf-data', filePath)
})
