<template>
  <div class="ap-overlay" @click.self="close">
    <div class="ap-panel">
      <div class="ap-header">
        <span class="ap-title">高级模式 · LaTeX 源码编辑器</span>
        <div class="ap-actions">
          <button class="ap-btn ap-compile" @click="compile" :disabled="compiling">
            {{ compiling ? '编译中…' : '编译并检查错误' }}
          </button>
          <button class="ap-btn ap-close" @click="close">关闭</button>
        </div>
      </div>

      <div class="ap-body">
        <div class="ap-gutter" ref="gutter">
          <div v-for="n in lineCount" :key="n" class="ap-line-no"
               :class="{ 'ap-line-err': errorLines.has(n) }"
               @click="jumpToLine(n)">{{ n }}</div>
        </div>

        <div class="ap-editor-wrap" ref="wrap">
          <pre class="ap-highlight" ref="highlight" v-html="highlighted"></pre>
          <textarea
            ref="editor"
            class="ap-editor"
            v-model="code"
            spellcheck="false"
            autocomplete="off"
            autocapitalize="off"
            @input="onInput"
            @scroll="syncScroll"
          ></textarea>
        </div>
      </div>

      <div class="ap-status" :class="statusClass">
        <template v-if="status === 'idle'">
          <span class="ap-muted">尚未编译。点击「编译并检查错误」查看日志与定位。</span>
        </template>
        <template v-else-if="status === 'compiling'">
          <span>正在调用 LaTeX 引擎…</span>
        </template>
        <template v-else-if="status === 'success'">
          <span class="ap-ok">✓ 编译成功{{ warnings.length ? '，但有 ' + warnings.length + ' 条警告' : '' }}。</span>
        </template>
        <template v-else-if="status === 'error'">
          <span class="ap-bad">✗ 编译失败，定位到 {{ errors.length }} 处问题：</span>
        </template>
      </div>

      <div v-if="status === 'error' && errors.length" class="ap-errors">
        <div
          v-for="(e, i) in errors"
          :key="i"
          class="ap-error-row"
          :class="{ 'ap-error-active': e.line && e.line === activeLine }"
          @click="e.line ? jumpToLine(e.line) : null"
        >
          <span class="ap-error-line" v-if="e.line">行 {{ e.line }}</span>
          <span class="ap-error-line ap-error-noline" v-else>—</span>
          <span class="ap-error-text">{{ e.text }}</span>
        </div>
      </div>

      <div v-if="warnings.length" class="ap-warns">
        <div v-for="(w, i) in warnings" :key="'w' + i" class="ap-warn-row">
          <span class="ap-warn-tag">警告</span>{{ w }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// 项目 README 的 FAQ 宣称存在「高级模式」（语法高亮的源码编辑器 + 错误定位），
// 但此前 src/frontend 下根本没有这个组件，MainPage 的 import 会直接 404。
// 这里补齐一个零依赖的实现：透明 textarea + 背后的高亮层 + 行号槽 + 编译错误定位。
export default {
  name: 'AdvancedPanel',
  props: {
    texContent: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      code: this.texContent || '',
      status: 'idle',          // idle | compiling | success | error
      compiling: false,
      errors: [],              // { line: number|null, text: string }
      warnings: [],
      activeLine: null,
    };
  },
  computed: {
    lineCount() {
      return Math.max(1, (this.code || '').split('\n').length);
    },
    errorLines() {
      const s = new Set();
      this.errors.forEach((e) => { if (e.line) s.add(e.line); });
      return s;
    },
    highlighted() {
      return this.highlight(this.code);
    },
    statusClass() {
      return 'ap-status-' + this.status;
    },
  },
  watch: {
    texContent(val) {
      // 父组件（如侧栏插入公式）改动了内容时同步进来；
      // 用户自己输入会经 onInput 触发 update:texContent，回到这里 val 与 code 相等，不会抖动光标。
      if (val !== this.code) {
        this.code = val || '';
      }
    },
  },
  methods: {
    close() {
      this.$emit('close');
    },
    onInput() {
      this.$emit('update:texContent', this.code);
    },
    syncScroll() {
      const ta = this.$refs.editor;
      const hl = this.$refs.highlight;
      const gut = this.$refs.gutter;
      if (hl) { hl.scrollTop = ta.scrollTop; hl.scrollLeft = ta.scrollLeft; }
      if (gut) { gut.scrollTop = ta.scrollTop; }
    },
    jumpToLine(line) {
      const ta = this.$refs.editor;
      if (!ta || !line) return;
      const lines = this.code.split('\n');
      let pos = 0;
      for (let i = 0; i < line - 1 && i < lines.length; i++) pos += lines[i].length + 1;
      const len = lines[line - 1] ? lines[line - 1].length : 0;
      ta.focus();
      try { ta.setSelectionRange(pos, pos + len); } catch (e) { /* ignore */ }
      const lh = parseFloat(getComputedStyle(ta).lineHeight) || 22;
      ta.scrollTop = Math.max(0, (line - 1) * lh - ta.clientHeight / 2);
      this.activeLine = line;
      this.syncScroll();
    },
    async compile() {
      if (!this.code || !this.code.trim()) {
        this.status = 'error';
        this.errors = [{ line: null, text: '没有可编译的内容。' }];
        return;
      }
      this.compiling = true;
      this.status = 'compiling';
      try {
        const result = await window.electronAPI.compileLatex(this.code, {
          outputDir: undefined,
        });
        if (!result || result.success === false) {
          this.status = 'error';
          const log = (result && result.log) || '';
          this.errors = this.parseErrors((result && result.error) || '编译失败', log);
          this.warnings = (result && result.warnings) || [];
          return;
        }
        this.status = 'success';
        this.errors = [];
        this.warnings = result.warnings || [];
        this.activeLine = null;
      } catch (e) {
        this.status = 'error';
        this.errors = [{ line: null, text: (e && e.message) || String(e) }];
      } finally {
        this.compiling = false;
      }
    },
    parseErrors(message, log) {
      const errs = [];
      if (message && message !== '编译失败') {
        errs.push({ line: this.lineFromText(message), text: message });
      }
      if (log) {
        const lines = log.split('\n');
        for (let i = 0; i < lines.length; i++) {
          const l = lines[i];
          const isErr = /^!\s/.test(l) ||
            (/undefined control sequence|misplaced|emergency stop|runaway argument|missing \$|\binvalid\b/i.test(l));
          if (isErr) {
            const ln = this.lineFromText(l);
            errs.push({ line: ln, text: l.trim() });
          }
        }
      }
      if (!errs.length) {
        errs.push({ line: null, text: message || '编译失败（未见详细日志）。' });
      }
      return errs;
    },
    lineFromText(text) {
      // pdflatex/xelatex 常用 "l.42" 标记错误行；也兼容 "42:" 与 "line 42"
      const m = text.match(/l\.(\d+)/i) || text.match(/(\d+):/) || text.match(/line\s+(\d+)/i);
      return m ? parseInt(m[1], 10) : null;
    },
    escapeHtml(s) {
      return String(s).replace(/[&<>]/g, (c) => (
        { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]
      ));
    },
    highlight(code) {
      const escaped = this.escapeHtml(code || '');
      try {
        const RE = /(%(?=[^\n]*)[^\n]*)|(\\(?:begin|end)\{[^}]*\})|(\\(?:usepackage|documentclass|includegraphics|frac|sqrt|textbf|textit|texttt|emph|section|subsection|subsubsection|paragraph|title|author|date|maketitle|caption|label|ref|cite|item|item|centering|noindent)\b)|(\\[a-zA-Z]+)|(\\[^a-zA-Z\s])|(\$\$?)/g;
        return escaped.replace(RE, (m, comment, env, known, cmd, sym, math) => {
          if (comment !== undefined) return '<span class="tk-comment">' + m + '</span>';
          if (env !== undefined) return '<span class="tk-env">' + m + '</span>';
          if (known !== undefined) return '<span class="tk-known">' + m + '</span>';
          if (cmd !== undefined) return '<span class="tk-cmd">' + m + '</span>';
          if (sym !== undefined) return '<span class="tk-cmd">' + m + '</span>';
          if (math !== undefined) return '<span class="tk-math">' + m + '</span>';
          return m;
        });
      } catch (e) {
        return escaped;
      }
    },
  },
};
</script>

<style scoped>
.ap-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.ap-panel {
  width: min(960px, 92vw);
  height: min(720px, 88vh);
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  font-family: -apple-system, 'Segoe UI', 'Microsoft YaHei', sans-serif;
}

.ap-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 18px;
  background: #2b3038;
  color: #fff;
}

.ap-title {
  font-size: 15px;
  font-weight: 600;
}

.ap-actions {
  display: flex;
  gap: 10px;
}

.ap-btn {
  border: none;
  border-radius: 5px;
  padding: 6px 14px;
  font-size: 13px;
  cursor: pointer;
  font-weight: 500;
}

.ap-compile {
  background: #17a2b8;
  color: #fff;
}

.ap-compile:hover:not(:disabled) {
  background: #138496;
}

.ap-compile:disabled {
  background: #6c868c;
  cursor: not-allowed;
}

.ap-close {
  background: #6c757d;
  color: #fff;
}

.ap-close:hover {
  background: #5a6268;
}

.ap-body {
  flex: 1;
  display: flex;
  min-height: 0;
  background: #fafbfc;
}

.ap-gutter {
  width: 52px;
  flex: 0 0 52px;
  overflow: hidden;
  padding: 12px 0;
  background: #eef1f4;
  border-right: 1px solid #dee2e6;
  text-align: right;
  user-select: none;
  font-family: 'Courier New', Consolas, monospace;
  font-size: 14px;
  line-height: 1.6;
  color: #98a2ad;
}

.ap-line-no {
  padding: 0 10px 0 0;
  cursor: pointer;
}

.ap-line-no:hover {
  color: #495057;
}

.ap-line-err {
  color: #c92a2a;
  font-weight: 700;
  background: rgba(201, 42, 42, 0.08);
}

.ap-editor-wrap {
  position: relative;
  flex: 1;
  min-width: 0;
  overflow: hidden;
}

.ap-highlight,
.ap-editor {
  margin: 0;
  padding: 12px 14px;
  font-family: 'Courier New', Consolas, monospace;
  font-size: 14px;
  line-height: 1.6;
  tab-size: 2;
  white-space: pre;
  word-wrap: normal;
  border: 0;
  box-sizing: border-box;
}

.ap-highlight {
  position: absolute;
  inset: 0;
  overflow: auto;
  color: #24292e;
  background: #fafbfc;
  pointer-events: none;
  z-index: 1;
}

.ap-editor {
  position: absolute;
  inset: 0;
  overflow: auto;
  color: transparent;
  background: transparent;
  caret-color: #000;
  resize: none;
  outline: none;
  z-index: 2;
}

.tk-comment { color: #6a737d; font-style: italic; }
.tk-env { color: #6f42c1; font-weight: 600; }
.tk-known { color: #d73a49; font-weight: 600; }
.tk-cmd { color: #005cc5; }
.tk-math { color: #e36209; }

.ap-status {
  padding: 10px 18px;
  font-size: 13px;
  border-top: 1px solid #e9ecef;
  background: #f8f9fa;
}

.ap-muted { color: #868e96; }
.ap-ok { color: #2f9e44; font-weight: 600; }
.ap-bad { color: #c92a2a; font-weight: 600; }

.ap-errors {
  max-height: 190px;
  overflow-y: auto;
  border-top: 1px solid #f1cad0;
  background: #fdf3f4;
}

.ap-error-row {
  display: flex;
  gap: 10px;
  padding: 7px 18px;
  font-size: 13px;
  border-bottom: 1px solid #f6dfe3;
  cursor: pointer;
}

.ap-error-row:hover { background: #fbe3e7; }
.ap-error-active { background: #f7cdd3; }

.ap-error-line {
  flex: 0 0 52px;
  color: #c92a2a;
  font-weight: 700;
  font-family: 'Courier New', monospace;
}

.ap-error-noline { color: #adb5bd; font-weight: 400; }

.ap-error-text {
  color: #495057;
  white-space: pre-wrap;
  word-break: break-word;
}

.ap-warns {
  max-height: 130px;
  overflow-y: auto;
  border-top: 1px solid #ffe8a3;
  background: #fffaf0;
}

.ap-warn-row {
  padding: 6px 18px;
  font-size: 12px;
  color: #7a5b00;
  border-bottom: 1px solid #fcefc7;
}

.ap-warn-tag {
  display: inline-block;
  margin-right: 8px;
  padding: 0 6px;
  background: #ffd43b;
  color: #664d00;
  border-radius: 3px;
  font-weight: 600;
}
</style>
