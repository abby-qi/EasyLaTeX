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
          <button @click="showDocumentWizard" class="btn-new">新建文档</button>
          <button @click="exportWord" class="btn-word">导出Word</button>
          <button @click="exportTex" class="btn-tex">导出LaTeX</button>
          <button @click="exportPdf" class="btn-pdf">导出PDF</button>
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
    
    <!-- 文档向导 -->
    <DocumentWizard 
      v-if="showWizard"
      @document-created="handleDocumentCreated"
      @close="showWizard = false"
    />
  </div>
</template>

<script>
import FormulaPanel from '../components/FormulaPanel.vue';
import TableEditor from '../components/TableEditor.vue';
import PreviewPanel from '../components/PreviewPanel.vue';
import DocumentWizard from '../components/DocumentWizard.vue';

export default {
  name: 'MainPage',
  components: {
    FormulaPanel,
    TableEditor,
    PreviewPanel,
    DocumentWizard
  },
  data() {
    return {
      texContent: '',
      showWizard: false
    };
  },
  mounted() {
    window.electronAPI.onNewFile(() => {
      this.newFile();
    });
    window.electronAPI.onOpenFile(() => {
      this.openFile();
    });
    window.electronAPI.onSaveFile(() => {
      this.saveFile();
    });
  },
  methods: {
    newFile() {
      if (this.texContent && !confirm('确定要新建文件吗？当前内容将被清空。')) {
        return;
      }
      this.texContent = '';
    },
    async openFile() {
      try {
        const result = await window.electronAPI.openFileDialog();
        if (result && result.content) {
          this.texContent = result.content;
        }
      } catch (error) {
          alert('打开文件失败: ' + error.message);
        }
    },
    async saveFile() {
      try {
        const result = await window.electronAPI.saveFileDialog(this.texContent);
        if (result && result.success) {
          alert('文件保存成功!');
        }
      } catch (error) {
          alert('保存文件失败: ' + error.message);
        }
    },
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
        // 打开文件选择对话框
        const dialogResult = await window.electronAPI.exportFileDialog('word');
        if (!dialogResult || !dialogResult.success) {
          return; // 用户取消选择
        }
        
        const result = await window.electronAPI.exportWord(
          { content: this.texContent },
          dialogResult.filePath
        );
        if (result.success) {
          alert('Word文档导出成功!');
        } else {
            alert('导出失败: ' + result.error);
          }
      } catch (error) {
        alert('导出失败: ' + error.message);
      }
    },
    async exportTex() {
      try {
        // 打开文件选择对话框
        const dialogResult = await window.electronAPI.exportFileDialog('tex');
        if (!dialogResult || !dialogResult.success) {
          return; // 用户取消选择
        }
        
        const result = await window.electronAPI.exportTex(
          { content: this.texContent },
          dialogResult.filePath
        );
        if (result.success) {
          alert('LaTeX文件导出成功!');
        } else {
            alert('导出失败: ' + result.error);
          }
      } catch (error) {
        alert('导出失败: ' + error.message);
      }
    },
    async exportPdf() {
      try {
        // 打开文件选择对话框
        const dialogResult = await window.electronAPI.exportFileDialog('pdf');
        if (!dialogResult || !dialogResult.success) {
          return; // 用户取消选择
        }
        
        const result = await window.electronAPI.exportPdf(
          { content: this.texContent },
          dialogResult.filePath
        );
        if (result.success) {
          alert('PDF文件导出成功!');
        } else {
            alert('导出失败: ' + result.error);
          }
      } catch (error) {
        alert('导出失败: ' + error.message);
      }
    },
    showAdvancedMode() {
      alert('高级模式功能开发中...');
    },
    
    showDocumentWizard() {
      this.showWizard = true;
    },
    
    handleDocumentCreated(template) {
      this.texContent = template;
      this.showWizard = false;
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

.btn-new,
.btn-word,
.btn-tex,
.btn-advanced {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.btn-new {
  background: #28a745;
  color: white;
}

.btn-new:hover {
  background: #218838;
  transform: translateY(-1px);
}

.btn-word {
  background: #007bff;
  color: white;
}

.btn-word:hover {
  background: #0069d9;
  transform: translateY(-1px);
}

.btn-tex {
  background: #6c757d;
  color: white;
}

.btn-tex:hover {
  background: #5a6268;
  transform: translateY(-1px);
}

.btn-pdf {
  background: #dc3545;
  color: white;
}

.btn-pdf:hover {
  background: #c82333;
  transform: translateY(-1px);
}

.btn-advanced {
  background: #17a2b8;
  color: white;
}

.btn-advanced:hover {
  background: #138496;
  transform: translateY(-1px);
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
