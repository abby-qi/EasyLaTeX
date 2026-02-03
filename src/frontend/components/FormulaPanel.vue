<template>
  <div class="formula-panel">
    <h3>公式符号</h3>
    <div class="formula-categories">
      <div class="category">
        <h4>基本符号</h4>
        <div class="symbol-grid">
          <button @click="insertSymbol('+')" class="symbol-btn">+</button>
          <button @click="insertSymbol('-')" class="symbol-btn">-</button>
          <button @click="insertSymbol('×')" class="symbol-btn">×</button>
          <button @click="insertSymbol('÷')" class="symbol-btn">÷</button>
          <button @click="insertSymbol('=')" class="symbol-btn">=</button>
          <button @click="insertSymbol('≠')" class="symbol-btn">≠</button>
          <button @click="insertSymbol('<')" class="symbol-btn"><</button>
          <button @click="insertSymbol('>')" class="symbol-btn">></button>
        </div>
      </div>
      
      <div class="category">
        <h4>数学符号</h4>
        <div class="symbol-grid">
          <button @click="insertSymbol('\\alpha')" class="symbol-btn">α</button>
          <button @click="insertSymbol('\\beta')" class="symbol-btn">β</button>
          <button @click="insertSymbol('\\gamma')" class="symbol-btn">γ</button>
          <button @click="insertSymbol('\\delta')" class="symbol-btn">δ</button>
          <button @click="insertSymbol('\\pi')" class="symbol-btn">π</button>
          <button @click="insertSymbol('\\sum')" class="symbol-btn">∑</button>
          <button @click="insertSymbol('\\int')" class="symbol-btn">∫</button>
          <button @click="insertSymbol('\\infty')" class="symbol-btn">∞</button>
        </div>
      </div>
      
      <div class="category">
        <h4>公式结构</h4>
        <div class="symbol-grid">
          <button @click="insertFormula('fraction')" class="symbol-btn">分数</button>
          <button @click="insertFormula('sqrt')" class="symbol-btn">根号</button>
          <button @click="insertFormula('subscript')" class="symbol-btn">下标</button>
          <button @click="insertFormula('superscript')" class="symbol-btn">上标</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FormulaPanel',
  methods: {
      insertSymbol(symbol) {
        this.$emit('formula-inserted', symbol);
      },
    
    insertFormula(type) {
      let latexCode = '';
      switch (type) {
        case 'fraction':
          latexCode = '\\frac{}{}';
          break;
        case 'sqrt':
          latexCode = '\\sqrt{}';
          break;
        case 'subscript':
          latexCode = '_{}';
          break;
        case 'superscript':
          latexCode = '^{}';
          break;
      }
      this.$emit('formula-inserted', latexCode);
    }
  }
};
</script>

<style scoped>
.formula-panel {
  margin-bottom: 30px;
}

.formula-panel h3 {
  font-size: 16px;
  margin-bottom: 15px;
  color: #333;
}

.category {
  margin-bottom: 20px;
}

.category h4 {
  font-size: 14px;
  margin-bottom: 10px;
  color: #666;
}

.symbol-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}

.symbol-btn {
  padding: 8px;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.symbol-btn:hover {
  background: #f8f9fa;
  border-color: #007bff;
  transform: translateY(-1px);
}
</style>
