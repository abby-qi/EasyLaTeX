<template>
  <div class="formula-panel">
    <h3>公式符号</h3>
    <div class="search-box">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="搜索符号..."
        @input="filterSymbols"
      />
    </div>
    <div class="symbol-categories">
      <div class="category" v-for="category in filteredCategories" :key="category.name">
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
      searchQuery: '',
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
  computed: {
    filteredCategories() {
      if (!this.searchQuery) {
        return this.categories;
      }

      return this.categories.map(category => ({
        name: category.name,
        symbols: category.symbols.filter(symbol =>
          symbol.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          symbol.display.includes(this.searchQuery)
        )
      }));
    }
  },
  methods: {
    async insertSymbol(symbol) {
      try {
        const result = await window.electronAPI.generateFormula({
          symbol: symbol.id,
          name: symbol.name
        });
        this.$emit('formula-inserted', result.latexCode);
      } catch (error) {
        console.error('Failed to insert formula:', error);
      }
    },
    filterSymbols() {
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

.search-box {
  margin-bottom: 15px;
}

.search-box input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
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

.symbol-btn:active {
  transform: scale(0.95);
}
</style>