<template>
  <div class="table-editor">
    <h3>表格编辑器</h3>
    <div class="table-controls">
      <div class="control-group">
        <label>行数:</label>
        <input type="number" v-model="rows" min="1" max="20" />
      </div>
      <div class="control-group">
        <label>列数:</label>
        <input type="number" v-model="cols" min="1" max="10" />
      </div>
      <button @click="createTable" class="btn-primary">创建表格</button>
    </div>

    <div v-if="tableData.length > 0" class="table-preview">
      <table>
        <thead>
          <tr>
            <th v-for="col in cols" :key="col">列 {{ col }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, rowIndex) in tableData" :key="rowIndex">
            <td v-for="(cell, colIndex) in row" :key="colIndex">
              <input
                v-model="tableData[rowIndex][colIndex]"
                @input="updateCell(rowIndex, colIndex, $event.target.value)"
              />
            </td>
          </tr>
        </tbody>
      </table>
      <button @click="generateLatex" class="btn-success">生成LaTeX</button>
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
      this.tableData = Array(this.rows).fill(null).map(() =>
        Array(this.cols).fill('')
      );
    },
    updateCell(row, col, value) {
      this.tableData[row][col] = value;
    },
    async generateLatex() {
      try {
        const result = await window.electronAPI.generateTable({
          rows: this.rows,
          cols: this.cols,
          data: this.tableData
        });
        this.$emit('table-generated', result);
      } catch (error) {
        console.error('Failed to generate table:', error);
      }
    }
  }
};
</script>

<style scoped>
.table-editor {
  padding: 20px;
  background: #f5f5f5;
  border-radius: 8px;
}

.table-controls {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  align-items: center;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.control-group label {
  font-weight: 500;
}

.control-group input[type="number"] {
  width: 60px;
  padding: 5px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.btn-primary,
.btn-success {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-success {
  background: #28a745;
  color: white;
}

.table-preview {
  margin-top: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  margin-bottom: 15px;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

th {
  background: #007bff;
  color: white;
}

td input {
  width: 100%;
  padding: 5px;
  border: none;
  text-align: center;
}

td input:focus {
  outline: 2px solid #007bff;
}
</style>