const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  generateFormula: (formulaData) => ipcRenderer.invoke('generate-formula', formulaData),
  generateTable: (tableData) => ipcRenderer.invoke('generate-table', tableData),
  compileLatex: (texContent) => ipcRenderer.invoke('compile-latex', texContent),
  exportPDF: (data, outputPath) => ipcRenderer.invoke('export-pdf', data, outputPath),
  exportWord: (data, outputPath) => ipcRenderer.invoke('export-word', data, outputPath),
  exportTex: (data, outputPath) => ipcRenderer.invoke('export-tex', data, outputPath),
  onCompileProgress: (callback) => ipcRenderer.on('compile-progress', callback),
  onCompileError: (callback) => ipcRenderer.on('compile-error', callback),
  onNewFile: (callback) => ipcRenderer.on('new-file', callback),
  onOpenFile: (callback) => ipcRenderer.on('open-file', callback),
  onSaveFile: (callback) => ipcRenderer.on('save-file', callback),
  openFileDialog: () => ipcRenderer.invoke('open-file-dialog'),
  saveFileDialog: (content) => ipcRenderer.invoke('save-file-dialog', content),
});