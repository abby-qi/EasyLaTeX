const { ipcMain } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

const pythonScriptPath = path.join(__dirname, '../backend');

function runPythonScript(scriptName, args) {
  return new Promise((resolve, reject) => {
    const python = spawn('python', [
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

    python.on('close', (code) => {
      if (code === 0) {
        try {
          const result = JSON.parse(output);
          resolve(result);
        } catch (e) {
          resolve({ success: true, data: output });
        }
      } else {
        reject(new Error(error || 'Script execution failed'));
      }
    });
  });
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

ipcMain.handle('compile-latex', async (event, texContent) => {
  try {
    const result = await runPythonScript('compiler/tex_compiler.py', [
      JSON.stringify({ content: texContent })
    ]);
    return { success: true, pdfPath: result.pdf_path };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

ipcMain.handle('export-pdf', async (event, data, outputPath) => {
  try {
    const result = await runPythonScript('exporter/pdf_exporter.py', [
      JSON.stringify(data),
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