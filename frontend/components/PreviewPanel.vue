<template>
  <div class="preview-panel">
    <div class="panel-header">
      <h3>PDF预览</h3>
      <div class="controls">
        <button @click="compile" class="btn-compile" :disabled="isCompiling">
          {{ isCompiling ? '编译中...' : '编译' }}
        </button>
        <button @click="exportPDF" class="btn-export">导出PDF</button>
      </div>
    </div>

    <div class="preview-content">
      <div v-if="pdfUrl" class="pdf-viewer">
        <iframe :src="pdfUrl" width="100%" height="100%"></iframe>
      </div>
      <div v-else class="placeholder">
        <p>点击"编译"按钮生成PDF预览</p>
      </div>
    </div>

    <div v-if="compileError" class="error-message">
      <h4>编译错误</h4>
      <p>{{ compileError }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PreviewPanel',
  props: {
    texContent: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      pdfUrl: null,
      isCompiling: false,
      compileError: null
    };
  },
  watch: {
    texContent() {
      this.compileError = null;
    }
  },
  methods: {
    async compile() {
      if (!this.texContent) {
        this.compileError = '请先输入LaTeX内容';
        return;
      }

      this.isCompiling = true;
      this.compileError = null;

      try {
        const result = await window.electronAPI.compileLatex(this.texContent);
        if (result.success) {
          this.pdfUrl = `file://${result.pdfPath}`;
        } else {
          this.compileError = result.error;
        }
      } catch (error) {
        this.compileError = `编译失败: ${error.message}`;
      } finally {
        this.isCompiling = false;
      }
    },
    async exportPDF() {
      if (!this.pdfUrl) {
        alert('请先编译生成PDF');
        return;
      }

      try {
        const result = await window.electronAPI.exportPDF(
          { content: this.texContent },
          'output.pdf'
        );
        if (result.success) {
          alert('PDF导出成功!');
        } else {
          alert(`导出失败: ${result.error}`);
        }
      } catch (error) {
        alert(`导出失败: ${error.message}`);
      }
    }
  }
};
</script>

<style scoped>
.preview-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.panel-header h3 {
  margin: 0;
  font-size: 16px;
}

.controls {
  display: flex;
  gap: 10px;
}

.btn-compile,
.btn-export {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.btn-compile {
  background: #007bff;
  color: white;
}

.btn-compile:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.btn-export {
  background: #28a745;
  color: white;
}

.preview-content {
  flex: 1;
  overflow: hidden;
}

.pdf-viewer {
  width: 100%;
  height: 100%;
}

.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #6c757d;
}

.error-message {
  padding: 15px 20px;
  background: #f8d7da;
  border-top: 1px solid #f5c6cb;
}

.error-message h4 {
  margin: 0 0 10px 0;
  color: #721c24;
  font-size: 14px;
}

.error-message p {
  margin: 0;
  color: #721c24;
  font-size: 13px;
}
</style>