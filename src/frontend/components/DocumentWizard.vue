<template>
  <div class="document-wizard">
    <div class="wizard-header">
      <h2>新建文档向导</h2>
      <button @click="closeWizard" class="close-btn">×</button>
    </div>
    
    <div class="wizard-content">
      <!-- 步骤指示器 -->
      <div class="step-indicator">
        <div 
          v-for="(step, index) in steps" 
          :key="index"
          class="step"
          :class="{ active: currentStep === index, completed: currentStep > index }"
        >
          {{ index + 1 }}
        </div>
        <div class="step-line" v-for="(step, index) in steps.length - 1" :key="'line-' + index"></div>
      </div>
      
      <!-- 步骤内容 -->
      <div class="step-content">
        <!-- 步骤1：选择文档类型 -->
        <div v-if="currentStep === 0" class="step-panel">
          <h3>选择文档类型</h3>
          <p>请选择您要创建的文档类型：</p>
          <div class="option-grid">
            <div 
              v-for="type in documentTypes" 
              :key="type.value"
              class="option-card"
              :class="{ selected: selectedOptions.type === type.value }"
              @click="selectDocumentType(type.value)"
            >
              <div class="option-icon">{{ type.icon }}</div>
              <div class="option-label">{{ type.label }}</div>
              <div class="option-desc">{{ type.description }}</div>
            </div>
          </div>
        </div>
        
        <!-- 步骤2：选择专业 -->
        <div v-else-if="currentStep === 1" class="step-panel">
          <h3>选择专业</h3>
          <p>请选择您的专业，以便我们为您配置相应的模板：</p>
          <div class="option-grid">
            <div 
              v-for="major in majors" 
              :key="major.value"
              class="option-card"
              :class="{ selected: selectedOptions.major === major.value }"
              @click="selectMajor(major.value)"
            >
              <div class="option-icon">{{ major.icon }}</div>
              <div class="option-label">{{ major.label }}</div>
              <div class="option-desc">{{ major.description }}</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 导航按钮 -->
      <div class="wizard-nav">
        <button 
          v-if="currentStep > 0"
          @click="previousStep"
          class="btn-secondary"
        >
          上一步
        </button>
        
        <button 
          v-if="currentStep < steps.length - 1"
          @click="nextStep"
          :disabled="!canProceed"
          class="btn-primary"
        >
          下一步
        </button>
        
        <button 
          v-else
          @click="createDocument"
          class="btn-primary"
        >
          创建文档
        </button>
      </div>
    </div>
  </div>
</template>

<script>
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
      steps: ['选择文档类型', '选择专业'],
      selectedOptions: {
        type: '',
        major: ''
      },
      documentTypes: [
        {
          value: 'thesis',
          label: '毕业论文',
          description: '适用于本科生、研究生的学位论文',
          icon: '📄'
        },
        {
          value: 'exam',
          label: '试卷',
          description: '适用于各类考试的试卷模板',
          icon: '📝'
        }
      ],
      majors: [
        {
          value: 'math',
          label: '数学专业',
          description: '包含数学公式和符号支持',
          icon: '🔢'
        },
        {
          value: 'physics',
          label: '物理专业',
          description: '包含物理公式和单位支持',
          icon: '⚛️'
        },
        {
          value: 'computer',
          label: '计算机专业',
          description: '包含代码和算法支持',
          icon: '💻'
        },
        {
          value: 'other',
          label: '其他专业',
          description: '通用模板，适用于其他专业',
          icon: '📚'
        }
      ]
    };
  },
  computed: {
    canProceed() {
      if (this.currentStep === 0) {
        return this.selectedOptions.type !== '';
      } else if (this.currentStep === 1) {
        return this.selectedOptions.major !== '';
      }
      return false;
    }
  },
  methods: {
    selectDocumentType(type) {
      this.selectedOptions.type = type;
    },
    
    selectMajor(major) {
      this.selectedOptions.major = major;
    },
    
    nextStep() {
      if (this.canProceed) {
        this.currentStep++;
      }
    },
    
    previousStep() {
      if (this.currentStep > 0) {
        this.currentStep--;
      }
    },
    
    createDocument() {
      // 生成文档模板
      const template = this.generateTemplate();
      this.$emit('document-created', template);
      this.closeWizard();
    },
    
    closeWizard() {
      // 重置状态
      this.currentStep = 0;
      this.selectedOptions = {
        type: '',
        major: ''
      };
      this.$emit('close');
    },
    
    generateTemplate() {
      const { type, major } = this.selectedOptions;
      
      // 根据文档类型和专业生成模板
      if (type === 'thesis') {
        return this.generateThesisTemplate(major);
      } else if (type === 'exam') {
        return this.generateExamTemplate(major);
      }
      
      return '';
    },
    
    generateThesisTemplate(major) {
      let template = '\\documentclass[12pt,a4paper]{article}\n\n\\usepackage{ctex}\n\\usepackage{amsmath,amssymb,amsfonts}\n\\usepackage{graphicx}\n\\usepackage{booktabs}\n\\usepackage{geometry}\n\\usepackage{setspace}\n';
      
      // 根据专业添加特定包
      if (major === 'math') {
        template += '\\usepackage{mathtools}\n\\usepackage{mathrsfs}\n\\usepackage{wasysym}\n';
      } else if (major === 'physics') {
        template += '\\usepackage{physics}\n\\usepackage{siunitx}\n';
      } else if (major === 'computer') {
        template += '\\usepackage{listings}\n\\usepackage{xcolor}\n\\lstset{language=Python, basicstyle=\\ttfamily\\small, keywordstyle=\\color{blue}, stringstyle=\\color{red}, commentstyle=\\color{green}}\n';
      }
      
      template += '\n\\geometry{a4paper,left=3.17cm,right=3.17cm,top=2.54cm,bottom=2.54cm}\n\\onehalfspacing\n\n\\title{毕业论文}\n\\author{作者姓名}\n\\date{\\today}\n\n\\begin{document}\n\n\\maketitle\n\n\\section{引言}\n\n在这里写引言内容...\n\n\\section{正文}\n\n在这里写正文内容...\n\n\\subsection{子章节}\n\n在这里写子章节内容...\n\n\\section{结论}\n\n在这里写结论内容...\n\n\\begin{thebibliography}{99}\n\n\\bibitem{ref1} 参考文献1\n\\bibitem{ref2} 参考文献2\n\n\\end{thebibliography}\n\n\\end{document}';
      
      return template;
    },
    
    generateExamTemplate(major) {
      let template = '\\documentclass[12pt,a4paper]{article}\n\n\\usepackage{ctex}\n\\usepackage{amsmath,amssymb,amsfonts}\n\\usepackage{graphicx}\n\\usepackage{booktabs}\n\\usepackage{geometry}\n\\usepackage{fancyhdr}\n\\usepackage{lastpage}\n';
      
      // 根据专业添加特定包
      if (major === 'math') {
        template += '\\usepackage{mathtools}\n\\usepackage{mathrsfs}\n';
      } else if (major === 'physics') {
        template += '\\usepackage{physics}\n\\usepackage{siunitx}\n';
      } else if (major === 'computer') {
        template += '\\usepackage{listings}\n\\usepackage{xcolor}\n\\lstset{language=Python, basicstyle=\\ttfamily\\small}\n';
      }
      
      template += '\n\\geometry{a4paper,left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}\n\n\\pagestyle{fancy}\n\\fancyhf{}\n\\fancyhead[L]{试卷标题}\n\\fancyhead[R]{第\\thepage\\页 共\\pageref{LastPage}页}\n\\fancyfoot[C]{}\n\n\\begin{document}\n\n\\begin{center}\n\\Large\\textbf{试卷标题}\n\n\\vspace{0.5cm}\n\\normalsize\n考试时间：120分钟 \\quad 满分：100分\n\\end{center}\n\n\\section*{一、选择题（每题5分，共20分）}\n\n1. 题目内容...\n\n\\begin{enumerate}\n    \\item A. 选项A \\quad B. 选项B \\quad C. 选项C \\quad D. 选项D\n    \\item A. 选项A \\quad B. 选项B \\quad C. 选项C \\quad D. 选项D\n\\end{enumerate}\n\n\\section*{二、填空题（每题5分，共20分）}\n\n1. \\underline{\\hspace{5cm}}\n\n2. \\underline{\\hspace{5cm}}\n\n\\section*{三、计算题（每题15分，共30分）}\n\n1. 题目内容...\n\n\\vspace{3cm}\n\n2. 题目内容...\n\n\\vspace{3cm}\n\n\\section*{四、证明题（每题15分，共30分）}\n\n1. 题目内容...\n\n\\vspace{5cm}\n\n2. 题目内容...\n\n\\vspace{5cm}\n\n\\end{document}';
      
      return template;
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
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.step-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 30px 0;
  gap: 10px;
}

.step {
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

.step.active {
  background: #007bff;
  color: white;
}

.step.completed {
  background: #28a745;
  color: white;
}

.step-line {
  width: 40px;
  height: 2px;
  background: #e9ecef;
  transition: background 0.3s;
}

.step-indicator.completed .step-line {
  background: #28a745;
}

.step-content {
  padding: 0 40px 40px;
}

.step-panel {
  animation: fadeIn 0.3s ease;
}

.step-panel h3 {
  font-size: 18px;
  margin-bottom: 10px;
  color: #333;
}

.step-panel p {
  color: #6c757d;
  margin-bottom: 30px;
}

.option-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.option-card {
  border: 2px solid #dee2e6;
  border-radius: 8px;
  padding: 20px;
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
  background: rgba(0, 123, 255, 0.05);
}

.option-icon {
  font-size: 48px;
  margin-bottom: 15px;
}

.option-label {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 8px;
  color: #333;
}

.option-desc {
  font-size: 14px;
  color: #6c757d;
  line-height: 1.4;
}

.wizard-nav {
  display: flex;
  justify-content: space-between;
  padding: 20px 40px;
  border-top: 1px solid #dee2e6;
  background: #f8f9fa;
  border-radius: 0 0 8px 8px;
}

.btn-primary, .btn-secondary {
  padding: 10px 24px;
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
    margin: 20px;
  }
  
  .step-content {
    padding: 0 20px 30px;
  }
  
  .wizard-nav {
    padding: 15px 20px;
  }
  
  .option-grid {
    grid-template-columns: 1fr;
  }
}
</style>