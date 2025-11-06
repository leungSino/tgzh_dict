<template>
  <div>
    <DataTable :columns="columns" :data="lemmas" :pageSize="10">
      <template #actions>
        <button @click="openForm()" class="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700">➕ 新增</button>
      </template>

      <template #row-actions="{ row }">
        <button @click="openForm(row)" class="px-2 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-600 mr-2">编辑</button>
        <button @click="deleteLemma(row.id)" class="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600">删除</button>
      </template>
    </DataTable>

    <LemmaForm v-if="showForm" :editingLemma="editingLemma" @close="closeForm" @saved="fetchLemmas" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DataTable from '@/components/DataTable.vue'
import LemmaForm from '@/pages/admin/LemmaForm.vue'
import api from '@/api/api.js'

const columns = [
  { key: 'lemma', label: '原型词' },
  { key: 'root', label: '词根' },
  { key: 'pos', label: '词性' },
  { key: 'definition', label: '释义' },
  { key: 'derived', label: '派生词' }
]

const lemmas = ref([])
const showForm = ref(false)
const editingLemma = ref(null)

async function fetchLemmas() {
  const res = await api.getLemmas()
  lemmas.value = res.data.map(item => ({
    ...item,
    id: item._id || item.id,
    definition: item.definition?.zh || item.definition?.en || '-',
    derived: (item.derived || []).join(', ')
  }))
}

function openForm(lemma = null) {
  editingLemma.value = lemma
  showForm.value = true
}
function closeForm() {
  showForm.value = false
  editingLemma.value = null
}
async function deleteLemma(id) {
  if (!confirm('确认删除该原型词？')) return
  await api.deleteLemma(id)
  await fetchLemmas()
}

onMounted(fetchLemmas)
</script>
