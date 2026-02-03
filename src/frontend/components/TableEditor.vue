<template>
  <div class="table-editor">
    <h3>表格编辑器</h3>
    <div class="table-controls">
      <div class="control-group">
        <label>行数:</label>
        <input type="number" v-model.number="rows" min="1" max="50">
      </div>
      <div class="control-group">
        <label>列数:</label>
        <input type="number" v-model.number="cols" min="1" max="20">
      </div>
      <button @click="createTable" class="btn-primary">创建表格</button>
    </div>
    
    <div v-if="tableData.length > 0" class="table-preview">
      <table>
        <tbody>
          <tr v-for="(row, rowIndex) in tableData" :key="rowIndex">
            <td v-for="(cell, colIndex) in row" :key="colIndex">
              <input 
                v-model="tableData[rowIndex][colIndex]" 
                type="text" 
                placeholder="内容"
              >
            </td>
          </tr>
        </tbody>
      </table>
      <button @click="generateLatex" class="btn-primary">生成LaTeX</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TableEditor',
  data() {
    return {
      rows: 3,
      cols: 3,
      tableData: []
    };
  },
  methods: {
    createTable() {
      // 初始化表格数据
      this.tableData = [];
      for (let i = 0; i < this.rows; i++) {
        const row = [];
        for (let j = 0; j < this.cols; j++) {
          row.push('');
        }
        this.tableData.push(row);
      }
    },
    
    generateLatex() {
      if (this.tableData.length === 0) {
        alert('请先创建表格');
        return;
      }
      
      let latexCode = '\\begin{table}[htbp]\n';
      latexCode += '\\centering\n';
      latexCode += '\\begin{tabular}{';
      
      // 生成列格式
      for (let i = 0; i < this.cols; i++) {
        latexCode += 'c';
      }
      latexCode += '}\n';
      latexCode += '\\toprule\\\n';
      
      // 生成表格内容
      this.tableData.forEach((row, rowIndex) => {
        row.forEach((cell, colIndex) => {
          latexCode += cell || ' ';
          if (colIndex < this.cols - 1) {
            latexCode += ' & ';
          }
        });
        latexCode += ' \\\\';
        if (rowIndex === 0) {
          latexCode += '\\midrule';
        }
        latexCode += '\n';
      });
      
      latexCode += '\\bottomrule\n';
      latexCode += '\\end{tabular}\n';
      latexCode += '\\caption{表格标题}\\label{tab:example}\n';
      latexCode += '\\end{table}';
      
      this.$emit('table-generated', latexCode);
    }
  }
};
</script>

<style scoped>
.table-editor {
  margin-bottom: 30px;
}

.table-editor h3 {
  font-size: 16px;
  margin-bottom: 15px;
  color: #333;
}

.table-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 5px;
}

.control-group label {
  font-size: 14px;
  color: #666;
}

.control-group input {
  width: 60px;
  padding: 4px 8px;
  border: 1px solid #dee2e6;
  border-radius: 4px;
}

.table-preview {
  margin-top: 20px;
}

.table-preview table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 15px;
}

.table-preview td {
  border: 1px solid #dee2e6;
  padding: 5px;
}

.table-preview input {
  width: 100%;
  border: none;
  padding: 4px;
  font-size: 14px;
}

.table-preview input:focus {
  outline: none;
  background: #f8f9fa;
}
</style>
