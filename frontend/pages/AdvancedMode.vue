<template>
  <div class="advanced-mode">
    <div class="header">
      <h2>高级模式 - LaTeX源码编辑</h2>
      <div class="actions">
        <button @click="backToMain" class="btn-back">返回主界面</button>
        <button @click="saveAndCompile" class="btn-compile">保存并编译</button>
      </div>
    </div>

    <div class="editor-container">
      <div class="editor-pane">
        <h3>LaTeX源码</h3>
        <textarea
          v-model="latexCode"
          placeholder="在此输入完整的LaTeX源码..."
          @input="handleCodeChange"
        ></textarea>
      </div>

      <div class="preview-pane">
        <h3>实时预览</h3>
        <div v-if="pdfUrl" class="pdf-viewer">
          <iframe :src="pdfUrl" width="100%" height="100%"></iframe>
        </div>
        <div v-else class="placeholder">
          <p>点击"保存并编译"查看预览</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdvancedMode',
  data() {
    return {
      latexCode: '',
      pdfUrl: null
    };
  },
  methods: {
    handleCodeChange() {
      this.latexCode = this.latexCode;
    },
    async saveAndCompile() {
      try {
        const result = await window.electronAPI.compileLatex(this.latexCode);
        if (result.success) {
          this.pdfUrl = `file://${result.pdfPath}`;
        } else {
          alert(`编译失败: ${result.error}`);
        }
      } catch (error) {
        alert(`编译失败: ${error.message}`);
      }
    },
    backToMain() {
      this.$emit('back-to-main');
    }
  }
};
</script>

<style scoped>
.advanced-mode {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #f0f2f5;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background: white;
  border-bottom: 1px solid #dee2e6;
}

.header h2 {
  margin: 0;
  font-size: 20px;
  color: #333;
}

.actions {
  display: flex;
  gap: 10px;
}

.btn-back,
.btn-compile {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.btn-back {
  background: #6c757d;
  color: white;
}

.btn-compile {
  background: #007bff;
  color: white;
}

.editor-container {
  flex: 1;
  display: flex;
  gap: 20px;
  padding: 20px;
}

.editor-pane,
.preview-pane {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.editor-pane h3,
.preview-pane h3 {
  margin: 0;
  padding: 15px 20px;
  background: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
  font-size: 16px;
}

.editor-pane textarea {
  flex: 1;
  padding: 15px;
  border: none;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  resize: none;
  line-height: 1.6;
}

.editor-pane textarea:focus {
  outline: none;
}

.preview-pane {
  flex: 1;
}

.pdf-viewer {
  flex: 1;
}

.placeholder {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6c757d;
}
</style>