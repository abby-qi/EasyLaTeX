const { ipcMain, dialog, app } = require('electron');
const { spawn, spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs').promises;
const templateManager = require('./template_manager');

const pythonScriptPath = path.join(__dirname, '../backend');

// ---------------------------------------------------------------------------
// Python 解释器探测
// ---------------------------------------------------------------------------
// 原先写死 spawn('python')，在只提供 python3 的机器上会直接抛 ENOENT，
// 而且错误信息对普通用户毫无意义。改成按平台逐个试，并缓存结果。
let pythonCmd = null;

function resolvePython() {
  if (pythonCmd) return pythonCmd;

  const candidates = process.platform === 'win32'
    ? ['python', 'py', 'python3']
    : ['python3', 'python'];

  for (const cmd of candidates) {
    try {
      const probe = spawnSync(cmd, ['-c', 'print(1)'], { encoding: 'utf-8' });
      if (!probe.error && probe.status === 0) {
        pythonCmd = cmd;
        return cmd;
      }
    } catch (e) {
      // 继续尝试下一个候选
    }
  }
  return null;
}

function runPythonScript(scriptName, args) {
  return new Promise((resolve, reject) => {
    const cmd = resolvePython();
    if (!cmd) {
      reject(new Error(
        '未找到 Python 解释器。请安装 Python 3.9+ 并加入 PATH，' +
        '然后重新运行 src/scripts/install.bat'
      ));
      return;
    }

    const python = spawn(cmd, [
      path.join(pythonScriptPath, scriptName),
      ...args
    ]);

    let output = '';
    let error = '';

    python.stdout.on('data', (data) => {
      output += data.toString();
    });

    python.stderr.on('data', (data) => {
      error += data.toString();
    });

    python.on('error', (err) => {
      reject(new Error('无法启动 Python: ' + err.message));
    });

    python.on('close', (code) => {
      // 后端脚本在失败时也会以 0 退出并打印 {"success": false}，
      // 因此这里不能只看退出码，还要看 JSON 里的 success 字段。
      let parsed = null;
      let lastJson = null;

      // 日志里可能混入非 JSON 输出，取最后一行能解析的 JSON
      const lines = output.split('\n').map((l) => l.trim()).filter(Boolean);
      for (let i = lines.length - 1; i >= 0; i--) {
        try {
          lastJson = JSON.parse(lines[i]);
          break;
        } catch (e) { /* 不是 JSON，继续往上找 */ }
      }
      parsed = lastJson;

      if (parsed && parsed.success === false) {
        reject(new Error(parsed.error || '后端执行失败'));
        return;
      }
      if (parsed) {
        resolve(parsed);
        return;
      }
      if (code === 0) {
        resolve({ success: true, data: output });
        return;
      }
      reject(new Error(error || output || 'Script execution failed'));
    });
  });
}

// PDF 等产物需要一个持久目录，不能落在会被清理的临时目录里
function getBuildDir() {
  try {
    return path.join(app.getPath('userData'), 'build');
  } catch (e) {
    return path.join(require('os').tmpdir(), 'easylatex-build');
  }
}

ipcMain.handle('generate-formula', async (event, formulaData) => {
  try {
    const result = await runPythonScript('latex_generator/formula_gen.py', [
      JSON.stringify(formulaData)
    ]);
    return { success: true, latexCode: result.latex_code };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

ipcMain.handle('generate-table', async (event, tableData) => {
  try {
    const result = await runPythonScript('latex_generator/table_gen.py', [
      JSON.stringify(tableData)
    ]);
    return { success: true, latexCode: result.latex_code };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// 项目根目录下的 tinytex（install.bat 会把 TinyTeX 装到这里）
function getTinytexPath() {
  return path.join(__dirname, '../../tinytex');
}

ipcMain.handle('compile-latex', async (event, texContent, options) => {
  try {
    const opts = options || {};
    const result = await runPythonScript('compiler/tex_compiler.py', [
      JSON.stringify({
        content: texContent,
        tinytex_path: opts.tinytexPath || getTinytexPath(),
        output_dir: opts.outputDir || getBuildDir(),
        engine: opts.engine || null,
      })
    ]);
    return {
      success: true,
      pdfPath: result.pdf_path,
      engine: result.engine || '',
      warnings: result.warnings || [],
      log: result.log || '',
      timestamp: Date.now(),
    };
  } catch (error) {
    return { success: false, error: error.message, needSetup: /未找到 LaTeX 引擎/.test(error.message) };
  }
});

// LaTeX 环境自检：前端据此决定是显示预览还是显示安装引导
ipcMain.handle('check-latex-env', async () => {
  try {
    const result = await runPythonScript('compiler/tex_compiler.py', [
      JSON.stringify({ action: 'check', tinytex_path: getTinytexPath() })
    ]);
    return {
      success: true,
      available: !!result.success,
      engine: result.engine || '',
      enginePath: result.enginePath || '',
      source: result.source || 'none',
    };
  } catch (error) {
    return { success: true, available: false, error: error.message, source: 'none' };
  }
});

// 模板：列出 / 渲染
ipcMain.handle('get-templates', async () => {
  return templateManager.listTemplates();
});

ipcMain.handle('render-template', async (event, templateId, major, fields) => {
  return templateManager.renderTemplate(templateId, major, fields);
});

// 把编译出的 PDF 以 base64 读回，供预览面板渲染。
// 之所以走 IPC 而不是让前端直接 fetch file://，是因为 dev 模式下页面
// 源是 http://localhost，浏览器会拒绝跨源读取本地文件。
ipcMain.handle('read-pdf-data', async (event, filePath) => {
  try {
    const data = await fs.readFile(filePath, { encoding: 'base64' });
    return { success: true, data, mime: 'application/pdf' };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

ipcMain.handle('export-pdf', async (event, data, outputPath) => {
  try {
    // 计算 TinyTeX 的路径（根据install.bat脚本，应该在项目根目录）
    const tinytexPath = path.join(__dirname, '../../tinytex');
    
    const result = await runPythonScript('exporter/pdf_exporter.py', [
      JSON.stringify({
        ...data,
        tinytex_path: tinytexPath
      }),
      outputPath
    ]);
    return { success: true, pdfPath: result.pdf_path };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

ipcMain.handle('export-word', async (event, data, outputPath) => {
  try {
    const result = await runPythonScript('exporter/word_exporter.py', [
      JSON.stringify(data),
      outputPath
    ]);
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

ipcMain.handle('export-tex', async (event, data, outputPath) => {
  try {
    const result = await runPythonScript('exporter/tex_exporter.py', [
      JSON.stringify(data),
      outputPath
    ]);
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

ipcMain.handle('open-file-dialog', async () => {
  try {
    const result = await dialog.showOpenDialog({
      properties: ['openFile'],
      filters: [
        { name: 'LaTeX Files', extensions: ['tex'] },
        { name: 'Text Files', extensions: ['txt'] },
        { name: 'All Files', extensions: ['*'] }
      ]
    });

    if (result.canceled || result.filePaths.length === 0) {
      return null;
    }

    const filePath = result.filePaths[0];
    const content = await fs.readFile(filePath, 'utf-8');
    return { content };
  } catch (error) {
    throw new Error('打开文件失败: ' + error.message);
  }
});

ipcMain.handle('save-file-dialog', async (event, content) => {
  try {
    const result = await dialog.showSaveDialog({
      filters: [
        { name: 'LaTeX Files', extensions: ['tex'] },
        { name: 'Text Files', extensions: ['txt'] },
        { name: 'All Files', extensions: ['*'] }
      ],
      defaultPath: 'document.tex'
    });

    if (result.canceled || !result.filePath) {
      return { success: false };
    }

    await fs.writeFile(result.filePath, content, 'utf-8');
    return { success: true, filePath: result.filePath };
  } catch (error) {
    throw new Error('保存文件失败: ' + error.message);
  }
});

ipcMain.handle('export-file-dialog', async (event, exportType) => {
  try {
    let filters = [];
    let defaultPath = 'output';
    
    switch (exportType) {
      case 'word':
        filters = [
          { name: 'Word Documents', extensions: ['docx'] },
          { name: 'All Files', extensions: ['*'] }
        ];
        defaultPath = 'output.docx';
        break;
      case 'tex':
        filters = [
          { name: 'LaTeX Files', extensions: ['tex'] },
          { name: 'Text Files', extensions: ['txt'] },
          { name: 'All Files', extensions: ['*'] }
        ];
        defaultPath = 'output.tex';
        break;
      case 'pdf':
        filters = [
          { name: 'PDF Files', extensions: ['pdf'] },
          { name: 'All Files', extensions: ['*'] }
        ];
        defaultPath = 'output.pdf';
        break;
      default:
        filters = [
          { name: 'All Files', extensions: ['*'] }
        ];
    }

    const result = await dialog.showSaveDialog({
      filters: filters,
      defaultPath: defaultPath
    });

    if (result.canceled || !result.filePath) {
      return { success: false };
    }

    return { success: true, filePath: result.filePath };
  } catch (error) {
    throw new Error('选择文件路径失败: ' + error.message);
  }
});
