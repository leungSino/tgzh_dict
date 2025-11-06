<template>
  <DataTable title="操作日志" :columns="columns" :data="logs">
    <template #actions>
      <button
        @click="openClearModal"
        class="px-3 py-1 bg-gray-600 text-white rounded hover:bg-gray-700"
      >
        清空日志
      </button>
    </template>

    <template #row-actions="{ row }">
      <button
        @click="openDeleteModal(row)"
        class="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600"
      >
        删除
      </button>
    </template>
  </DataTable>

  <!-- 删除确认弹窗 -->
  <DeleteConfirm
    v-if="showDeleteModal"
    title="确认删除日志"
    @confirm="confirmDelete"
    @cancel="showDeleteModal = false"
  >
    <p class="text-red-500" >确定要删除该日志吗？此操作不可恢复。</p>
  </DeleteConfirm>

  <!-- 清空日志弹窗 -->
  <DeleteConfirm
    v-if="showClearModal"
    title="清空所有日志"
    @confirm="confirmClear"
    @cancel="showClearModal = false"
  >
    <p class="text-red-600">⚠️ 确认要清空所有日志吗？此操作不可恢复！</p>
  </DeleteConfirm>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DataTable from './DataTable.vue'
import Modal from '@/components/Modal.vue'
import DeleteConfirm from '@/components/DeleteConfirm.vue'
import api from '@/api/api.js'

const columns = [
  { key: 'user', label: '操作用户' },
  { key: 'action', label: '操作内容' },
  { key: 'time', label: '时间' }
]

const logs = ref([])
const showDeleteModal = ref(false)
const showClearModal = ref(false)
const pendingDeleteId = ref(null)

async function loadLogs() {
  try {
    const res = await api.getLogs?.()
    logs.value = (res && res.data) ? res.data : (res || [])
  } catch (e) {
    logs.value = []
  }
}

function openDeleteModal(row) {
  pendingDeleteId.value = row._id
  showDeleteModal.value = true
}

async function confirmDelete() {
  await api.deleteLog?.(pendingDeleteId.value)
  showDeleteModal.value = false
  await loadLogs()
}

function openClearModal() {
  showClearModal.value = true
}

async function confirmClear() {
  await api.clearLogs?.()
  showClearModal.value = false
  await loadLogs()
}

onMounted(loadLogs)
</script>
