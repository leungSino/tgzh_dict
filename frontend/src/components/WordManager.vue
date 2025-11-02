<template>
  <div>
    <DataTable :columns="columns" :data="words" :pageSize="10">
      <template #actions>
        <button @click="openForm()" class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700">➕ 新增</button>
      </template>

      <template #row-actions="{ row }">
        <button @click="openForm(row)" class="px-2 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-600 mr-2">编辑</button>
        <button @click="deleteWord(row.id || row._id)" class="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600">删除</button>
      </template>
    </DataTable>

    <WordForm v-if="showForm" :editingWord="editingWord" @close="closeForm" @saved="fetchWords" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DataTable from '@/components/DataTable.vue'
import WordForm from '@/pages/admin/WordForm.vue'
import api from '@/api/api.js'

const columns = [
  { key: 'zh', label: '中文' },
  { key: 'tg', label: '塔吉克语' },
  { key: 'ru', label: '俄语' },
  { key: 'en', label: '英语' },
  { key: 'tags', label: '标签' }
]

const words = ref([])
const loading = ref(false)
const showForm = ref(false)
const editingWord = ref(null)

async function fetchWords() {
  loading.value = true
  try {
    const res = await api.getWords()
    words.value = res.data.map(item => ({
      ...item,
      id: item.id || item._id,
      zh: item.lang_entries?.zh?.word || '-',
      tg: item.lang_entries?.tg?.word || '-',
      ru: item.lang_entries?.ru?.word || '-',
      en: item.lang_entries?.en?.word || '-',
      tags: (item.tags || []).join(', ')
    }))
  } finally {
    loading.value = false
  }
}

function openForm(word = null) {
  editingWord.value = word
  showForm.value = true
}

function closeForm() {
  showForm.value = false
  editingWord.value = null
}

async function deleteWord(id) {
  console.log('Deleting word with id:', id)
  if (!confirm('确认删除该词条？')) return
  await api.deleteWord(id)
  await fetchWords()
}

onMounted(fetchWords)
</script>
