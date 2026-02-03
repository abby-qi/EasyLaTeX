const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
  // 公式生成
  generateFormula: (formulaData) => ipcRenderer.invoke('generate-formula', formulaData),
  // 表格生成
  generateTable: (tableData) => ipcRenderer.invoke('generate-table', tableData),
  // LaTeX编译
  compileLatex: (texContent) => ipcRenderer.invoke('compile-latex', texContent),
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
  onSaveFile: (callback) => ipcRenderer.on('save-file', callback)
})
