<template>
  <div>
    <DataTable :columns="columns" :data="translations" :pageSize="10">
      <template #actions>
        <button @click="openForm()" class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700">➕ 新增</button>
      </template>

      <template #row-actions="{ row }">
        <button @click="openForm(row)" class="px-2 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-600 mr-2">编辑</button>
        <button @click="deleteTranslation(row.id)" class="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600">删除</button>
      </template>
    </DataTable>

    <TranslationForm v-if="showForm" :editingTranslation="editingTranslation" @close="closeForm" @saved="fetchTranslations" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DataTable from '@/components/DataTable.vue'
import TranslationForm from '@/pages/admin/TranslationForm.vue'
import api from '@/api/api.js'

const columns = [
  { key: 'sourceText', label: '原文' },
  { key: 'targetText', label: '译文' },
  { key: 'lemma', label: '原型词' },
  { key: 'pos', label: '词性' },
  { key: 'tags', label: '标签' }
]

const translations = ref([])
const showForm = ref(false)
const editingTranslation = ref(null)

async function fetchTranslations() {
  const res = await api.getTranslations()
  translations.value = res.data.map(item => ({
    ...item,
    id: item._id || item.id,
    sourceText: item.sourceText || '-',
    targetText: Object.values(item.translations || {}).map(t => t.translation).join('; '),
    lemma: item.lemma || '-',
    pos: item.pos || '-',
    tags: (item.tags || []).join(', ')
  }))
}

function openForm(translation = null) {
  editingTranslation.value = translation
  showForm.value = true
}
function closeForm() {
  showForm.value = false
  editingTranslation.value = null
}
async function deleteTranslation(id) {
  if (!confirm('确认删除该翻译对？')) return
  await api.deleteTranslation(id)
  await fetchTranslations()
}

onMounted(fetchTranslations)
</script>
