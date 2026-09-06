<template>
  <div class="document-wizard">
    <div class="wizard-header">
      <h2>新建文档向导</h2>
      <button @click="closeWizard" class="close-btn">×</button>
    </div>

    <div class="wizard-content">
      <!-- 步骤指示器 -->
      <div class="step-indicator">
        <template v-for="(step, i) in steps" :key="'step' + i">
          <div
            class="step"
            :class="{ active: currentStep === i, completed: currentStep > i }"
          >
            {{ i + 1 }}
            <span class="step-name">{{ step }}</span>
          </div>
          <div
            v-if="i < steps.length - 1"
            class="step-line"
            :class="{ completed: currentStep > i }"
          ></div>
        </template>
      </div>

      <!-- 步骤内容 -->
      <div class="step-content">
        <!-- 步骤1：学科方向 -->
        <div v-if="currentStep === 0" class="step-panel">
          <h3>第一步 · 你的学科方向是？</h3>
          <p>先选个大方向，我们会据此为你配上合适的宏包与排版习惯。</p>
          <div class="option-grid">
            <div
              v-for="d in disciplines"
              :key="d.value"
              class="option-card"
              :class="{ selected: selectedOptions.discipline === d.value }"
              @click="selectOption('discipline', d.value)"
            >
              <div class="option-icon">{{ d.icon }}</div>
              <div class="option-label">{{ d.label }}</div>
              <div class="option-desc">{{ d.desc }}</div>
            </div>
          </div>
        </div>

        <!-- 步骤2：文档用途 -->
        <div v-else-if="currentStep === 1" class="step-panel">
          <h3>第二步 · 这份文档用来做什么？</h3>
          <p>笔记、作业、实验、论文、出卷还是开会？用途决定结构。</p>
          <div class="option-grid">
            <div
              v-for="p in purposes"
              :key="p.value"
              class="option-card"
              :class="{ selected: selectedOptions.purpose === p.value }"
              @click="selectOption('purpose', p.value)"
            >
              <div class="option-icon">{{ p.icon }}</div>
              <div class="option-label">{{ p.label }}</div>
              <div class="option-desc">{{ p.desc }}</div>
            </div>
          </div>
        </div>

        <!-- 步骤3：推荐模板 -->
        <div v-else-if="currentStep === 2" class="step-panel">
          <template v-if="recommendation">
            <h3>第三步 · 为你推荐的模板</h3>
            <p>基于「{{ disciplineLabel }} · {{ purposeLabel }}」自动生成，可一键采用。</p>

            <div class="reco-card">
              <div class="reco-row">
                <span class="reco-key">文档类</span>
                <code class="reco-val">{{ recommendation.documentClass }}</code>
              </div>
              <div class="reco-row">
                <span class="reco-key">推荐理由</span>
                <span class="reco-val">{{ recommendation.reason }}</span>
              </div>
            </div>

            <div class="reco-grid">
              <div class="reco-block">
                <h4>推荐宏包</h4>
                <ul class="pkg-list">
                  <li v-for="pkg in recommendation.packages" :key="pkg.name">
                    <code>{{ pkg.name }}</code>
                    <span class="pkg-reason">{{ pkg.reason }}</span>
                  </li>
                </ul>
              </div>
              <div class="reco-block">
                <h4>文档结构</h4>
                <ol class="struct-list">
                  <li v-for="(sec, idx) in recommendation.sections" :key="idx">{{ sec }}</li>
                </ol>
              </div>
            </div>
          </template>
        </div>

        <!-- 步骤4：完善与微调 -->
        <div v-else-if="currentStep === 3" class="step-panel">
          <h3>第四步 · 完善信息，再细细地改</h3>
          <p>填好元信息会自动写进模板；想从源码层面调整，直接在右侧代码框里改。</p>

          <div class="refine-layout">
            <div class="meta-form">
              <div class="form-row">
                <label>标题</label>
                <input
                  class="form-input"
                  v-model="meta.title"
                  placeholder="例如：基于深度学习的图像分类"
                  @input="onMetaInput"
                />
              </div>
              <div class="form-row">
                <label>作者</label>
                <input
                  class="form-input"
                  v-model="meta.author"
                  placeholder="你的名字"
                  @input="onMetaInput"
                />
              </div>
              <div class="form-row">
                <label>日期</label>
                <input
                  class="form-input"
                  v-model="meta.date"
                  placeholder="留空则使用 \\today"
                  @input="onMetaInput"
                />
              </div>
              <div class="form-row" v-if="recommendation && recommendation.abstract">
                <label>摘要</label>
                <textarea
                  class="form-input"
                  v-model="meta.abstract"
                  placeholder="一句话概括你的工作…"
                  @input="onMetaInput"
                ></textarea>
              </div>
              <div class="form-row" v-if="recommendation && recommendation.abstract">
                <label>关键词</label>
                <input
                  class="form-input"
                  v-model="meta.keywords"
                  placeholder="关键词1；关键词2"
                  @input="onMetaInput"
                />
              </div>
              <p class="hint">提示：一旦你手动编辑右侧代码框，元信息改动将不再自动覆盖源码。</p>
            </div>

            <div class="source-box">
              <div class="source-title">LaTeX 源码（可直接编辑）</div>
              <textarea
                class="code-box"
                v-model="customLatex"
                @input="sourceDirty = true"
                spellcheck="false"
              ></textarea>
            </div>
          </div>
        </div>
      </div>

      <!-- 导航按钮 -->
      <div class="wizard-nav">
        <button v-if="currentStep > 0" @click="previousStep" class="btn-secondary">
          上一步
        </button>
        <span v-else></span>

        <button
          v-if="currentStep < steps.length - 1"
          @click="nextStep"
          :disabled="!canProceed"
          class="btn-primary"
        >
          下一步
        </button>

        <button v-else @click="createDocument" class="btn-primary">
          创建文档
        </button>
      </div>
    </div>
  </div>
</template>

<script>
// 学科方向
const DISCIPLINES = [
  { value: 'scieng', label: '理工', icon: '🔬', desc: '数理化、计算机、工程等' },
  { value: 'agri', label: '农科', icon: '🌱', desc: '农学、植保、畜牧等' },
  { value: 'med', label: '医科', icon: '🩺', desc: '临床、基础医学、药学等' },
  { value: 'hum', label: '文科', icon: '📜', desc: '文学、历史、哲学等' },
  { value: 'econ', label: '经管', icon: '📊', desc: '经济、金融、管理类等' },
  { value: 'art', label: '艺术', icon: '🎨', desc: '设计、美术、音乐等' }
];

// 文档用途
const PURPOSES = [
  { value: 'notes', label: '课堂笔记', icon: '📓', desc: '随堂记录与复习' },
  { value: 'assignment', label: '课程作业', icon: '📝', desc: '平时作业与习题' },
  { value: 'lab', label: '实验报告', icon: '🔬', desc: '实验记录与分析' },
  { value: 'thesis', label: '毕业论文', icon: '🎓', desc: '学位论文与长篇写作' },
  { value: 'exam', label: '试卷测验', icon: '📋', desc: '出卷与测验' },
  { value: 'meeting', label: '会议汇报', icon: '📊', desc: '会议纪要 / 汇报提纲' }
];

// 各用途的基础骨架
const PURPOSE_BASE = {
  notes: {
    label: '课堂笔记',
    documentClass: '\\documentclass[12pt,a4paper]{article}',
    basePackages: ['ctex', 'geometry', 'amsmath', 'amssymb', 'graphicx', 'booktabs', 'hyperref'],
    setup: '\\geometry{a4paper,left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}\n\\linespread{1.5}',
    abstract: false,
    toc: false,
    sections: ['课程信息', '本次笔记要点', '例题与练习', '课后思考'],
    reason: '课堂笔记推荐 article 文档类，搭配「课程信息—要点—例题—思考」四段结构，方便快速记录与复习。'
  },
  assignment: {
    label: '课程作业',
    documentClass: '\\documentclass[12pt,a4paper]{article}',
    basePackages: ['ctex', 'geometry', 'amsmath', 'amssymb', 'graphicx', 'booktabs', 'enumitem', 'hyperref'],
    setup: '\\geometry{a4paper,left=3cm,right=3cm,top=2.5cm,bottom=2.5cm}',
    abstract: false,
    toc: false,
    sections: ['题目要求', '分析与思路', '解答过程', '总结'],
    reason: '课程作业采用标准 article 结构，含标题/作者与「要求—思路—过程—总结」分节。'
  },
  lab: {
    label: '实验报告',
    documentClass: '\\documentclass[12pt,a4paper]{article}',
    basePackages: ['ctex', 'geometry', 'amsmath', 'amssymb', 'graphicx', 'booktabs', 'siunitx', 'float', 'hyperref'],
    setup: '\\geometry{a4paper,left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}',
    abstract: false,
    toc: false,
    sections: ['实验目的', '实验原理', '实验器材', '实验步骤', '数据记录与处理', '结果与讨论', '实验结论'],
    reason: '实验报告采用标准七段式：目的、原理、器材、步骤、数据处理、讨论、结论，并预留图表位置。'
  },
  thesis: {
    label: '毕业论文',
    documentClass: '\\documentclass[12pt,a4paper]{article}',
    basePackages: ['ctex', 'geometry', 'amsmath', 'amssymb', 'graphicx', 'booktabs', 'siunitx', 'natbib', 'hyperref'],
    setup: '\\geometry{a4paper,left=3cm,right=3cm,top=3cm,bottom=3cm}\n\\linespread{1.5}',
    abstract: true,
    toc: true,
    sections: ['引言', '相关工作', '研究方法', '实验与结果', '结论与展望'],
    reason: '毕业论文结构含摘要、目录与「引言—方法—结果—结论」标准学术框架。'
  },
  exam: {
    label: '试卷测验',
    documentClass: '\\documentclass[12pt,a4paper]{article}',
    basePackages: ['ctex', 'geometry', 'amsmath', 'amssymb', 'enumitem', 'fancyhdr', 'lastpage', 'hyperref'],
    setup: '\\geometry{a4paper,left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}',
    abstract: false,
    toc: false,
    sections: ['一、选择题', '二、填空题', '三、计算题', '四、证明题'],
    reason: '试卷模板含页眉页脚与「选择—填空—计算—证明」标准题型分区。'
  },
  meeting: {
    label: '会议汇报',
    documentClass: '\\documentclass[12pt,a4paper]{article}',
    basePackages: ['ctex', 'geometry', 'amsmath', 'graphicx', 'booktabs', 'hyperref'],
    setup: '\\geometry{a4paper,left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}',
    abstract: false,
    toc: false,
    sections: ['会议信息', '议程', '讨论要点', '决议事项', '行动项与责任人'],
    reason: '会议纪要结构含会议信息、议程、讨论、决议与行动项，便于追踪落实。'
  }
};

// 各学科的附加宏包（带推荐理由）
const DISCIPLINE_PKGS = {
  scieng: [
    { name: 'listings', reason: '源代码与算法排版' },
    { name: 'siunitx', reason: '单位与数值规范' },
    { name: 'tikz', reason: '矢量绘图' }
  ],
  agri: [
    { name: 'siunitx', reason: '单位与数值' },
    { name: 'chemformula', reason: '化学式排版' },
    { name: 'tikz', reason: '示意图绘制' }
  ],
  med: [
    { name: 'siunitx', reason: '医学测量单位' },
    { name: 'multirow', reason: '病例/数据跨行表格' }
  ],
  hum: [
    { name: 'setspace', reason: '行距控制（段落舒展）' },
    { name: 'csquotes', reason: '智能引号与引文' }
  ],
  econ: [
    { name: 'pgfplots', reason: '数据图表' },
    { name: 'siunitx', reason: '财务数值与单位' },
    { name: 'tikz', reason: '框架图绘制' }
  ],
  art: [
    { name: 'xcolor', reason: '色彩支持' },
    { name: 'tikz', reason: '矢量图形' }
  ]
};

// 宏包理由（基础包用）
const PACKAGE_REASONS = {
  ctex: '中文排版（必选）',
  geometry: '页面边距设置',
  amsmath: '数学公式环境',
  amssymb: '数学符号',
  graphicx: '插入图片',
  booktabs: '三线表（专业表格）',
  hyperref: '超链接与书签',
  siunitx: '单位与数值规范',
  listings: '源代码/算法排版',
  tikz: '矢量绘图',
  pgfplots: '数据图表',
  xcolor: '色彩支持',
  setspace: '行距控制',
  csquotes: '智能引号',
  multirow: '表格跨行',
  chemformula: '化学式',
  enumitem: '自定义列表',
  fancyhdr: '页眉页脚',
  lastpage: '页码引用',
  float: '图表浮动控制',
  natbib: '参考文献引用'
};

// 学科补充理由（拼接进推荐理由）
const DISCIPLINE_REASON = {
  scieng: '已加入公式、代码与绘图支持。',
  agri: '已加入化学式与数据单位支持。',
  med: '已加强医学表格与单位规范。',
  hum: '已优化中文行距与引文格式。',
  econ: '已加入财务图表与数据分析支持。',
  art: '已加入色彩与矢量图形支持。'
};

export default {
  name: 'DocumentWizard',
  props: {
    visible: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      currentStep: 0,
      steps: ['学科方向', '文档用途', '推荐模板', '完善微调'],
      disciplines: DISCIPLINES,
      purposes: PURPOSES,
      selectedOptions: {
        discipline: '',
        purpose: ''
      },
      meta: {
        title: '',
        author: '',
        date: '',
        abstract: '',
        keywords: ''
      },
      customLatex: '',
      sourceDirty: false
    };
  },
  computed: {
    disciplineLabel() {
      const d = this.disciplines.find((x) => x.value === this.selectedOptions.discipline);
      return d ? d.label : '';
    },
    purposeLabel() {
      const p = this.purposes.find((x) => x.value === this.selectedOptions.purpose);
      return p ? p.label : '';
    },
    canProceed() {
      if (this.currentStep === 0) return this.selectedOptions.discipline !== '';
      if (this.currentStep === 1) return this.selectedOptions.purpose !== '';
      return true;
    },
    recommendation() {
      if (!this.selectedOptions.discipline || !this.selectedOptions.purpose) return null;
      return this.buildRecommendation(this.selectedOptions.discipline, this.selectedOptions.purpose);
    }
  },
  methods: {
    selectOption(field, value) {
      this.selectedOptions[field] = value;
    },
    buildRecommendation(disc, purp) {
      const base = PURPOSE_BASE[purp];
      const discPkgs = DISCIPLINE_PKGS[disc] || [];
      const names = base.basePackages.slice();
      for (const p of discPkgs) {
        if (!names.includes(p.name)) names.push(p.name);
      }
      const packages = names.map((n) => ({
        name: n,
        reason: PACKAGE_REASONS[n] || '基础排版支持'
      }));
      const reason =
        (DISCIPLINE_REASON[disc] ? base.reason + ' ' + DISCIPLINE_REASON[disc] : base.reason);
      return {
        documentClass: base.documentClass,
        packages,
        setup: base.setup,
        abstract: base.abstract,
        toc: base.toc,
        sections: base.sections,
        reason
      };
    },
    generateLatex() {
      const rec = this.recommendation;
      if (!rec) return '';
      const meta = this.meta;

      // 把 hyperref 放到最后加载，避免与其他宏包冲突
      const pkgs = rec.packages.slice();
      const hi = pkgs.findIndex((p) => p.name === 'hyperref');
      if (hi > -1) {
        const h = pkgs.splice(hi, 1)[0];
        pkgs.push(h);
      }

      let s = rec.documentClass + '\n\n';
      for (const p of pkgs) {
        s += '\\usepackage{' + p.name + '}\n';
      }
      s += '\n' + rec.setup + '\n\n';
      s += '\\title{' + (meta.title || '未命名文档') + '}\n';
      s += '\\author{' + (meta.author || '作者') + '}\n';
      s += '\\date{' + (meta.date || '\\today') + '}\n\n';
      s += '\\begin{document}\n\n';
      s += '\\maketitle\n\n';

      if (rec.abstract && (meta.abstract || meta.keywords)) {
        s += '\\begin{abstract}\n';
        s += (meta.abstract || '在此撰写摘要…') + '\n';
        if (meta.keywords) {
          s += '\\par\\textbf{关键词：}' + meta.keywords + '\n';
        }
        s += '\\end{abstract}\n\n';
      }

      if (rec.toc) {
        s += '\\tableofcontents\n\n';
      }

      for (const sec of rec.sections) {
        s += '\\section{' + sec + '}\n\n';
        s += '在此撰写' + sec + '的内容…\n\n';
      }

      s += '\\end{document}\n';
      return s;
    },
    onMetaInput() {
      if (!this.sourceDirty) {
        this.customLatex = this.generateLatex();
      }
    },
    nextStep() {
      if (!this.canProceed) return;
      // 进入第4步时，根据前3步生成初始源码
      if (this.currentStep === 2) {
        this.customLatex = this.generateLatex();
        this.sourceDirty = false;
      }
      this.currentStep++;
    },
    previousStep() {
      if (this.currentStep > 0) this.currentStep--;
    },
    createDocument() {
      this.$emit('document-created', this.customLatex || this.generateLatex());
      this.closeWizard();
    },
    closeWizard() {
      this.currentStep = 0;
      this.selectedOptions = { discipline: '', purpose: '' };
      this.meta = { title: '', author: '', date: '', abstract: '', keywords: '' };
      this.customLatex = '';
      this.sourceDirty = false;
      this.$emit('close');
    }
  }
};
</script>

<style scoped>
.document-wizard {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.wizard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: #007bff;
  color: white;
  border-radius: 8px 8px 0 0;
}

.wizard-header h2 {
  margin: 0;
  font-size: 20px;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.2s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.wizard-content {
  background: white;
  border-radius: 8px;
  width: 92%;
  max-width: 860px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.step-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 28px 20px 10px;
  gap: 6px;
  flex-wrap: wrap;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  width: 34px;
}

.step > :first-child {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #e9ecef;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: #6c757d;
  transition: all 0.3s;
  z-index: 1;
}

.step.active > :first-child {
  background: #007bff;
  color: white;
}

.step.completed > :first-child {
  background: #28a745;
  color: white;
}

.step-name {
  font-size: 12px;
  color: #6c757d;
  white-space: nowrap;
}

.step.active .step-name,
.step.completed .step-name {
  color: #333;
  font-weight: 600;
}

.step-line {
  width: 46px;
  height: 2px;
  background: #e9ecef;
  transition: background 0.3s;
  margin-bottom: 22px;
}

.step-line.completed {
  background: #28a745;
}

.step-content {
  padding: 10px 40px 30px;
}

.step-panel {
  animation: fadeIn 0.3s ease;
}

.step-panel h3 {
  font-size: 18px;
  margin-bottom: 8px;
  color: #333;
}

.step-panel > p {
  color: #6c757d;
  margin-bottom: 26px;
}

.option-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 18px;
}

.option-card {
  border: 2px solid #dee2e6;
  border-radius: 8px;
  padding: 18px;
  cursor: pointer;
  transition: all 0.3s;
  text-align: center;
}

.option-card:hover {
  border-color: #007bff;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.15);
  transform: translateY(-2px);
}

.option-card.selected {
  border-color: #007bff;
  background: rgba(0, 123, 255, 0.06);
}

.option-icon {
  font-size: 42px;
  margin-bottom: 12px;
}

.option-label {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 6px;
  color: #333;
}

.option-desc {
  font-size: 13px;
  color: #6c757d;
  line-height: 1.4;
}

/* 步骤3：推荐卡片 */
.reco-card {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 16px 18px;
  background: #f8f9fa;
  margin-bottom: 22px;
}

.reco-row {
  display: flex;
  gap: 12px;
  padding: 6px 0;
  align-items: flex-start;
}

.reco-key {
  flex: 0 0 70px;
  font-weight: 600;
  color: #495057;
}

.reco-val {
  color: #333;
  line-height: 1.5;
}

.reco-val code {
  background: #e9ecef;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
}

.reco-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 22px;
}

.reco-block h4 {
  margin: 0 0 10px;
  font-size: 15px;
  color: #007bff;
}

.pkg-list,
.struct-list {
  margin: 0;
  padding-left: 18px;
  color: #495057;
  line-height: 1.9;
}

.pkg-list li code {
  background: #e9ecef;
  padding: 1px 6px;
  border-radius: 4px;
  font-size: 13px;
  margin-right: 8px;
}

.pkg-reason {
  color: #6c757d;
  font-size: 13px;
}

/* 步骤4：完善与微调 */
.refine-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.meta-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.form-row {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-row label {
  font-size: 13px;
  font-weight: 600;
  color: #495057;
}

.form-input {
  padding: 9px 11px;
  border: 1px solid #ced4da;
  border-radius: 5px;
  font-size: 14px;
  font-family: inherit;
  transition: border-color 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #007bff;
}

textarea.form-input {
  resize: vertical;
  min-height: 64px;
}

.hint {
  font-size: 12px;
  color: #adb5bd;
  margin: 4px 0 0;
}

.source-box {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.source-title {
  font-size: 13px;
  font-weight: 600;
  color: #495057;
}

.code-box {
  width: 100%;
  height: 360px;
  padding: 12px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  font-family: 'Courier New', Consolas, monospace;
  font-size: 12.5px;
  line-height: 1.5;
  resize: vertical;
  background: #fbfbfd;
}

.code-box:focus {
  outline: 2px solid #007bff;
  border-color: transparent;
}

.wizard-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 40px;
  border-top: 1px solid #dee2e6;
  background: #f8f9fa;
  border-radius: 0 0 8px 8px;
}

.btn-primary,
.btn-secondary {
  padding: 10px 26px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #0069d9;
  transform: translateY(-1px);
}

.btn-primary:disabled {
  background: #6c757d;
  cursor: not-allowed;
  transform: none;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
  transform: translateY(-1px);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .wizard-content {
    width: 95%;
    margin: 12px;
  }

  .step-content {
    padding: 10px 20px 24px;
  }

  .wizard-nav {
    padding: 14px 20px;
  }

  .reco-grid,
  .refine-layout {
    grid-template-columns: 1fr;
  }

  .code-box {
    height: 240px;
  }

  .option-grid {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
