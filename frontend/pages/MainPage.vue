<template>
  <div class="main-page">
    <div class="sidebar">
      <FormulaPanel @formula-inserted="handleFormulaInserted" />
      <TableEditor @table-generated="handleTableGenerated" />
    </div>

    <div class="editor-area">
      <div class="editor-header">
        <h2>EasyLaTeX 编辑器</h2>
        <div class="header-actions">
          <button @click="exportWord" class="btn-word">导出Word</button>
          <button @click="exportTex" class="btn-tex">导出LaTeX</button>
          <button @click="showAdvancedMode" class="btn-advanced">高级模式</button>
        </div>
      </div>

      <div class="editor-content">
        <textarea
          v-model="texContent"
          placeholder="在此输入LaTeX代码，或使用左侧工具栏插入公式和表格..."
          @input="handleContentChange"
        ></textarea>
      </div>

      <PreviewPanel :tex-content="texContent" />
    </div>
  </div>
</template>

<script>
import FormulaPanel from '../components/FormulaPanel.vue';
import TableEditor from '../components/TableEditor.vue';
import PreviewPanel from '../components/PreviewPanel.vue';

export default {
  name: 'MainPage',
  components: {
    FormulaPanel,
    TableEditor,
    PreviewPanel
  },
  data() {
    return {
      texContent: ''
    };
  },
  methods: {
    handleFormulaInserted(latexCode) {
      this.texContent += latexCode + '\n';
    },
    handleTableGenerated(latexCode) {
      this.texContent += latexCode + '\n';
    },
    handleContentChange() {
      this.texContent = this.texContent;
    },
    async exportWord() {
      try {
        const result = await window.electronAPI.exportWord(
          { content: this.texContent },
          'output.docx'
        );
        if (result.success) {
          alert('Word文档导出成功!');
        } else {
          alert(`导出失败: ${result.error}`);
        }
      } catch (error) {
        alert(`导出失败: ${error.message}`);
      }
    },
    async exportTex() {
      try {
        const result = await window.electronAPI.exportTex(
          { content: this.texContent },
          'output.tex'
        );
        if (result.success) {
          alert('LaTeX文件导出成功!');
        } else {
          alert(`导出失败: ${result.error}`);
        }
      } catch (error) {
        alert(`导出失败: ${error.message}`);
      }
    },
    showAdvancedMode() {
      alert('高级模式功能开发中...');
    }
  }
};
</script>

<style scoped>
.main-page {
  display: flex;
  height: 100vh;
  background: #f0f2f5;
}

.sidebar {
  width: 300px;
  padding: 20px;
  background: white;
  border-right: 1px solid #dee2e6;
  overflow-y: auto;
}

.editor-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
  gap: 20px;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 15px 20px;
  border-radius: 8px;
}

.editor-header h2 {
  margin: 0;
  font-size: 20px;
  color: #333;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.btn-word,
.btn-tex,
.btn-advanced {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.btn-word {
  background: #007bff;
  color: white;
}

.btn-tex {
  background: #6c757d;
  color: white;
}

.btn-advanced {
  background: #17a2b8;
  color: white;
}

.editor-content {
  flex: 1;
  background: white;
  border-radius: 8px;
  padding: 20px;
}

.editor-content textarea {
  width: 100%;
  height: 100%;
  padding: 15px;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  resize: none;
  line-height: 1.6;
}

.editor-content textarea:focus {
  outline: 2px solid #007bff;
  border-color: transparent;
}
</style>