<template>
  <div class="preview-panel">
    <div class="preview-header">
      <h3>预览</h3>
      <div class="preview-actions">
        <label class="auto-toggle">
          <input type="checkbox" v-model="autoCompile" @change="onAutoToggle" />
          自动编译
        </label>
        <button class="btn-compile" @click="compile" :disabled="compiling">
          {{ compiling ? '编译中…' : '编译预览' }}
        </button>
      </div>
    </div>

    <div class="preview-body">
      <!-- 空状态 -->
      <div v-if="status === 'empty'" class="preview-hint">
        <p>输入 LaTeX 代码或使用左侧工具栏插入内容以查看预览</p>
      </div>

      <!-- 未安装 LaTeX 引擎：给出可操作指引，而不是假装在编译 -->
      <div v-else-if="status === 'no-engine'" class="preview-hint error">
        <p class="hint-title">⚠️ 未检测到 LaTeX 引擎</p>
        <p class="hint-detail">{{ envError }}</p>
        <p class="hint-detail">
          请运行 <code>src/scripts/install.bat</code> 安装内置 TinyTeX，<br />
          或自行安装 TeX Live / MiKTeX 并加入系统 PATH。
        </p>
      </div>

      <!-- 编译失败 -->
      <div v-else-if="status === 'error'" class="preview-hint error">
        <p class="hint-title">编译失败</p>
        <pre class="error-pre">{{ errorMessage }}</pre>
        <div v-for="(w, i) in warnings" :key="'w' + i" class="warn-line">
          ⚠ {{ w }}
        </div>
      </div>

      <!-- 编译中 -->
      <div v-else-if="status === 'loading'" class="preview-hint">
        <p>正在编译并生成预览…</p>
      </div>

      <!-- 渲染结果 -->
      <div v-else class="pdf-canvas-list">
        <div v-for="(page, i) in pages" :key="i" class="pdf-page">
          <canvas :ref="el => setCanvasRef(el, i)" :data-page="i + 1"></canvas>
        </div>
        <p v-if="pages.length && warnings.length" class="preview-warns">
          <span v-for="(w, i) in warnings" :key="'ww' + i">⚠ {{ w }}</span>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
// PDF 渲染：pdf.js（项目此前宣称"实时预览"，但本组件原本是永远显示
// "正在编译预览…"的死组件，从不调用编译，也从不渲染任何东西）
import * as pdfjsLib from 'pdfjs-dist';
import PdfWorker from 'pdfjs-dist/build/pdf.worker.min.mjs?url';

pdfjsLib.GlobalWorkerOptions.workerSrc = PdfWorker;

export default {
  name: 'PreviewPanel',
  props: {
    texContent: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      status: 'empty',          // empty | no-engine | error | loading | ready
      compiling: false,
      errorMessage: '',
      warnings: [],
      envError: '',
      pages: [],                // 每页一个占位对象，用于 v-for 生成 canvas
      canvasRefs: [],
      autoCompile: false,
      lastPdfPath: '',
      debounceTimer: null,
      pdfDoc: null,
    };
  },
  watch: {
    texContent() {
      if (!this.texContent || !this.texContent.trim()) {
        this.status = 'empty';
        this.pages = [];
        return;
      }
      if (this.autoCompile) {
        this.scheduleCompile();
      }
    },
  },
  beforeUnmount() {
    if (this.debounceTimer) clearTimeout(this.debounceTimer);
    if (this.pdfDoc) {
      try { this.pdfDoc.destroy(); } catch (e) { /* ignore */ }
    }
  },
  methods: {
    setCanvasRef(el, i) {
      if (el) this.canvasRefs[i] = el;
    },
    onAutoToggle() {
      if (this.autoCompile && this.texContent && this.texContent.trim()) {
        this.compile();
      }
    },
    scheduleCompile() {
      if (this.debounceTimer) clearTimeout(this.debounceTimer);
      this.debounceTimer = setTimeout(() => this.compile(), 800);
    },
    async compile() {
      if (!this.texContent || !this.texContent.trim()) {
        this.status = 'empty';
        return;
      }
      this.compiling = true;
      this.status = 'loading';
      try {
        const result = await window.electronAPI.compileLatex(this.texContent, {
          outputDir: undefined,
        });
        if (!result || result.success === false) {
          const needSetup = result && result.needSetup;
          this.errorMessage = (result && result.error) || '编译失败';
          this.warnings = (result && result.warnings) || [];
          this.status = needSetup ? 'no-engine' : 'error';
          if (needSetup) this.envError = this.errorMessage;
          return;
        }
        this.warnings = result.warnings || [];
        this.lastPdfPath = result.pdfPath;
        await this.renderPdf(result.pdfPath);
        this.status = 'ready';
      } catch (e) {
        this.errorMessage = (e && e.message) || String(e);
        this.status = 'error';
      } finally {
        this.compiling = false;
      }
    },
    async renderPdf(pdfPath) {
      // 通过 IPC 读取 PDF 二进制（base64），避免 dev 模式 http 源读取 file:// 的跨源限制
      const res = await window.electronAPI.readPdfData(pdfPath);
      if (!res || !res.success) {
        throw new Error((res && res.error) || '读取 PDF 失败');
      }
      const binary = atob(res.data);
      const len = binary.length;
      const bytes = new Uint8Array(len);
      for (let i = 0; i < len; i++) bytes[i] = binary.charCodeAt(i);

      if (this.pdfDoc) {
        try { this.pdfDoc.destroy(); } catch (e) { /* ignore */ }
      }
      this.pdfDoc = await pdfjsLib.getDocument({ data: bytes }).promise;
      const total = this.pdfDoc.numPages;
      this.pages = new Array(total).fill(0);

      // 等待 canvas 渲染出来
      await this.$nextTick();

      for (let i = 0; i < total; i++) {
        const canvas = this.canvasRefs[i];
        if (!canvas) continue;
        const page = await this.pdfDoc.getPage(i + 1);
        const desiredWidth = Math.min(canvas.parentElement.clientWidth || 600, 900);
        const baseViewport = page.getViewport({ scale: 1 });
        const scale = desiredWidth / baseViewport.width;
        const viewport = page.getViewport({ scale });
        const ctx = canvas.getContext('2d');
        const dpr = window.devicePixelRatio || 1;
        canvas.width = Math.floor(viewport.width * dpr);
        canvas.height = Math.floor(viewport.height * dpr);
        canvas.style.width = viewport.width + 'px';
        canvas.style.height = viewport.height + 'px';
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        await page.render({ canvasContext: ctx, viewport }).promise;
      }
    },
  },
};
</script>

<style scoped>
.preview-panel {
  margin-top: 20px;
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  overflow: hidden;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  border-bottom: 1px solid #dee2e6;
  background: #fafbfc;
}

.preview-header h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.preview-actions {
  display: flex;
  align-items: center;
  gap: 14px;
}

.auto-toggle {
  font-size: 13px;
  color: #666;
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
}

.btn-compile {
  padding: 6px 16px;
  border: none;
  border-radius: 4px;
  background: #007bff;
  color: white;
  cursor: pointer;
  font-size: 13px;
}

.btn-compile:hover:not(:disabled) {
  background: #0069d9;
}

.btn-compile:disabled {
  background: #adb5bd;
  cursor: not-allowed;
}

.preview-body {
  min-height: 240px;
  max-height: calc(100vh - 320px);
  overflow-y: auto;
  padding: 20px;
  background: #525659;
}

.preview-hint {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  color: #cfd4da;
  text-align: center;
  gap: 8px;
}

.preview-hint.error {
  color: #ffd7d7;
}

.hint-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
}

.hint-detail {
  font-size: 13px;
  line-height: 1.6;
  margin: 0;
  color: #e8e8e8;
}

.hint-detail code {
  background: rgba(255, 255, 255, 0.12);
  padding: 1px 6px;
  border-radius: 3px;
}

.error-pre {
  background: rgba(0, 0, 0, 0.35);
  color: #ffb3b3;
  padding: 12px 16px;
  border-radius: 6px;
  font-size: 13px;
  white-space: pre-wrap;
  text-align: left;
  max-width: 100%;
  max-height: 200px;
  overflow: auto;
  margin: 8px 0;
}

.pdf-canvas-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.pdf-page canvas {
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  border-radius: 2px;
}

.preview-warns {
  display: flex;
  flex-direction: column;
  gap: 4px;
  color: #ffe08a;
  font-size: 12px;
  width: 100%;
}
</style>
