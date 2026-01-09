<template>
  <div class="formula-panel">
    <h3>公式符号</h3>
    <div class="symbol-categories">
      <div class="category" v-for="category in categories" :key="category.name">
        <h4>{{ category.name }}</h4>
        <div class="symbols">
          <button
            v-for="symbol in category.symbols"
            :key="symbol.id"
            class="symbol-btn"
            @click="insertSymbol(symbol)"
            :title="symbol.name"
          >
            {{ symbol.display }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FormulaPanel',
  data() {
    return {
      categories: [
        {
          name: '希腊字母',
          symbols: [
            { id: 'alpha', name: 'Alpha', display: 'α' },
            { id: 'beta', name: 'Beta', display: 'β' },
            { id: 'gamma', name: 'Gamma', display: 'γ' },
            { id: 'delta', name: 'Delta', display: 'δ' },
            { id: 'epsilon', name: 'Epsilon', display: 'ε' },
            { id: 'pi', name: 'Pi', display: 'π' },
            { id: 'theta', name: 'Theta', display: 'θ' },
            { id: 'lambda', name: 'Lambda', display: 'λ' },
            { id: 'mu', name: 'Mu', display: 'μ' },
            { id: 'sigma', name: 'Sigma', display: 'σ' },
            { id: 'phi', name: 'Phi', display: 'φ' },
            { id: 'omega', name: 'Omega', display: 'ω' },
          ]
        },
        {
          name: '运算符',
          symbols: [
            { id: 'integral', name: 'Integral', display: '∫' },
            { id: 'summation', name: 'Summation', display: '∑' },
            { id: 'product', name: 'Product', display: '∏' },
            { id: 'infinity', name: 'Infinity', display: '∞' },
            { id: 'partial', name: 'Partial', display: '∂' },
            { id: 'nabla', name: 'Nabla', display: '∇' },
          ]
        },
        {
          name: '结构',
          symbols: [
            { id: 'sqrt', name: 'Square Root', display: '√' },
            { id: 'fraction', name: 'Fraction', display: 'a/b' },
            { id: 'matrix', name: 'Matrix', display: '[ ]' },
          ]
        }
      ]
    };
  },
  methods: {
    async insertSymbol(symbol) {
      try {
        const result = await window.electronAPI.generateFormula({
          symbol: symbol.id,
          name: symbol.name
        });
        this.$emit('formula-inserted', result);
      } catch (error) {
        console.error('Failed to insert formula:', error);
      }
    }
  }
};
</script>

<style scoped>
.formula-panel {
  padding: 20px;
  background: #f5f5f5;
  border-radius: 8px;
}

.symbol-categories {
  margin-top: 15px;
}

.category {
  margin-bottom: 20px;
}

.category h4 {
  margin-bottom: 10px;
  font-size: 14px;
  color: #333;
}

.symbols {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.symbol-btn {
  min-width: 40px;
  height: 40px;
  padding: 8px;
  font-size: 18px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.symbol-btn:hover {
  background: #007bff;
  color: white;
  border-color: #007bff;
}
</style>