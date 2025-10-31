<template>
  <DataTable
    title="词汇管理"
    :columns="columns"
    :data="words"
  >
    <template #actions>
      <button class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
              @click="addWord">新增</button>
    </template>

    <template #row-actions="{ row }">
      <button class="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600"
              @click="deleteWord(row.id)">删除</button>
    </template>
  </DataTable>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DataTable from './DataTable.vue'
import api from '../api/api.js'

const columns = [
  { key: 'word', label: '单词' },
  { key: 'translation', label: '翻译' },
  { key: 'language', label: '语言' }
]

const words = ref([])

async function loadWords() {
  const res = await api.searchWords('')
  words.value = res.data || []
}

async function addWord() {
  alert('新增词汇弹窗 / 表单逻辑')
}

async function deleteWord(id) {
  await api.deleteWord(id)
  loadWords()
}

onMounted(loadWords)
</script>
