<template>
  <div ref="tableWrapper" class="relative">
    <DataTableServer
      ref="tableRef"
      title="操作日志"
      :columns="columns"
      :fetchData="fetchLogs"
      :pageSize="10"
    >
      <!-- 顶部操作 -->
      <template #actions>
        <button
          @click="openClearModal"
          class="px-3 py-1 bg-gray-600 text-white rounded hover:bg-gray-700"
        >
          清空日志
        </button>
      </template>

      <!-- 每行操作按钮 -->
      <template #row-actions="{ row }">
        <!-- 桌面端 -->
        <div class="hidden sm:flex flex-wrap gap-2 justify-start">
          <button
            @click="openDeleteModal(row)"
            class="flex-1 min-w-[60px] px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600 text-center"
          >
            删除
          </button>
        </div>

        <!-- 移动端 -->
        <div class="sm:hidden relative">
          <button
            @click="toggleMenu(row)"
            class="px-2 py-1 bg-gray-400 text-white rounded hover:bg-gray-500"
          >
            ⋮
          </button>
          <div
            v-if="row.id === expandedRowId"
            class="absolute right-0 mt-1 bg-white border rounded shadow-lg z-10 flex flex-wrap gap-1 p-1"
            style="min-width: 120px;"
          >
            <button
              @click="openDeleteModal(row); closeMenu()"
              class="flex-1 min-w-[60px] px-2 py-1 text-white bg-red-500 hover:bg-red-600 rounded text-center"
            >
              删除
            </button>
          </div>
        </div>
      </template>
    </DataTableServer>

    <!-- 删除确认弹窗 -->
    <DeleteConfirm
      v-if="showDeleteModal"
      title="确认删除日志"
      @confirm="confirmDelete"
      @cancel="showDeleteModal = false"
    >
      <p class="text-red-500">确定要删除该日志吗？此操作不可恢复。</p>
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
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import DataTableServer from './DataTableServer.vue'
import DeleteConfirm from '@/components/DeleteConfirm.vue'
import api from '@/api/api.js'

const columns = [
  { key: 'user', label: '操作用户' },
  { key: 'action', label: '操作内容' },
  { key: 'time', label: '时间' }
]

const tableRef = ref(null)
const tableWrapper = ref(null)
const showDeleteModal = ref(false)
const showClearModal = ref(false)
const pendingDeleteId = ref(null)

// 控制移动端展开行
const expandedRowId = ref(null)

/** 异步拉取日志 **/
async function fetchLogs(query, page, pageSize) {
  try {
    const { items, total } = await api.getLogs(query, page, pageSize)
    const normalizedItems = items.map(item => ({
      id: item._id || item.id,
      user: item.user || '未知用户',
      action: item.action || '未知操作',
      time: item.timestamp ? new Date(item.timestamp).toLocaleString() : '-',
      ...item
    }))
    return { items: normalizedItems, total }
  } catch (e) {
    console.error('加载日志失败', e)
    return { items: [], total: 0 }
  }
}


/** 刷新表格 **/
function reloadTable() {
  tableRef.value?.reload()
}

/** 删除日志 **/
function openDeleteModal(row) {
  pendingDeleteId.value = row.id
  showDeleteModal.value = true
}

/** 清空日志 **/
function openClearModal() {
  showClearModal.value = true
}

async function confirmDelete() {
  await api.deleteLog?.(pendingDeleteId.value)
  showDeleteModal.value = false
  reloadTable()
}

async function confirmClear() {
  await api.clearLogs?.()
  showClearModal.value = false
  reloadTable()
}

/** 移动端菜单操作 **/
function toggleMenu(row) {
  expandedRowId.value = expandedRowId.value === row.id ? null : row.id
}
function closeMenu() {
  expandedRowId.value = null
}
function handleClickOutside(e) {
  if (!tableWrapper.value.contains(e.target)) {
    closeMenu()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})
onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
@media (max-width: 640px) {
  .flex-wrap {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
