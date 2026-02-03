<template>
  <div class="preview-panel">
    <h3>预览</h3>
    <div class="preview-content">
      <div v-if="!texContent" class="empty-preview">
        <p>输入LaTeX代码或使用左侧工具栏插入内容以查看预览</p>
      </div>
      <div v-else class="preview-loading">
        <p>正在编译预览...</p>
      </div>
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
  }
};
</script>

<style scoped>
.preview-panel {
  margin-top: 20px;
}

.preview-panel h3 {
  font-size: 16px;
  margin-bottom: 15px;
  color: #333;
}

.preview-content {
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 40px;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-preview {
  text-align: center;
  color: #666;
}

.preview-loading {
  text-align: center;
  color: #666;
}
</style>
