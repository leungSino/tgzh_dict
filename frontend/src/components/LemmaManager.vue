<template>
  <div ref="tableWrapper" class="relative">
    <DataTableServer
      ref="tableRef"
      :columns="columns"
      :fetchData="fetchLemmas"
      :pageSize="10"
      class="overflow-x-auto"
    >
      <template #actions>
        <button
          @click="openForm()"
          class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          新增原型词
        </button>
      </template>

      <template #row-actions="{ row }">
        <div class="hidden sm:flex flex-wrap gap-2 justify-start">
          <button
            @click="viewForm(row)"
            class="flex-1 min-w-[60px] px-2 py-1 bg-green-500 text-white rounded hover:bg-green-600 text-center"
          >
            查看
          </button>

          <button
            @click="openForm(row)"
            class="flex-1 min-w-[60px] px-2 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 text-center"
          >
            编辑
          </button>

          <button
            @click="deleteLemma(row.id)"
            class="flex-1 min-w-[60px] px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600 text-center"
          >
            删除
          </button>
        </div>

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
              @click="viewForm(row); closeMenu()"
              class="flex-1 min-w-[60px] px-2 py-1 text-white bg-green-500 hover:bg-green-600 rounded text-center"
            >
              查看
            </button>
            <button
              @click="openForm(row); closeMenu()"
              class="flex-1 min-w-[60px] px-2 py-1 text-white bg-blue-500 hover:bg-blue-600 rounded text-center"
            >
              编辑
            </button>
            <button
              @click="deleteLemma(row.id); closeMenu()"
              class="flex-1 min-w-[60px] px-2 py-1 text-white bg-red-500 hover:bg-red-600 rounded text-center"
            >
              删除
            </button>
          </div>
        </div>
      </template>
    </DataTableServer>

    <LemmaForm
      v-if="showForm"
      :editingLemma="editingLemma"
      @close="closeForm"
      @saved="reloadTable"
    />

    <LemmaView
      v-if="showView"
      :viewingLemma="viewingLemma"
      @close="closeView"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import DataTableServer from '@/components/DataTableServer.vue'
import LemmaForm from '@/pages/admin/LemmaForm.vue'
import LemmaView from '@/pages/admin/LemmaView.vue'
import api from '@/api/api.js'

const columns = [
  { key: 'lemma', label: '原型词' },
  { key: 'definition', label: '释义' },
  { key: 'root', label: '词根' }
]

const showForm = ref(false)
const showView = ref(false)
const editingLemma = ref(null)
const viewingLemma = ref(null)

const tableWrapper = ref(null)
const tableRef = ref(null)

// 控制移动端展开行
const expandedRowId = ref(null)

/** 异步拉取数据（DataTableServer 调用） **/
async function fetchLemmas(query, page, pageSize) {
  try {
    const res = await api.getLemmas(query, page, pageSize)
    if (res?.items) {
      const items = res.items.map(item => {
        // 保证 pos 仍然是数组
        const posArray = Array.isArray(item.pos)
          ? item.pos
          : (typeof item.pos === 'string'
            ? item.pos.split(',').map(s => s.trim()).filter(Boolean)
            : [])

        return {
          ...item,
          // id 统一处理
          id: item._id || item.id,
          // 用于表格显示的字段
          posDisplay: posArray.join(', ') || '-',
          // 原始 pos 必须保留为数组
          pos: posArray,
          // 释义取中文，否则英文，否则 '-'
          definition: item.definitions?.zh || item.definitions?.en || '-',
          // 保证 derived, related 为数组
          derived: Array.isArray(item.derived) ? item.derived : [],
          related: Array.isArray(item.related) ? item.related : []
        }
      })
      return { items, total: res.total || items.length }
    }
    return { items: [], total: 0 }
  } catch (err) {
    console.error('加载原型词失败：', err)
    return { items: [], total: 0 }
  }
}

/** 刷新表格 **/
function reloadTable() {
  tableRef.value?.reload()
}

/** 切换移动端菜单显示 **/
function toggleMenu(row) {
  expandedRowId.value = expandedRowId.value === row.id ? null : row.id
}
function closeMenu() {
  expandedRowId.value = null
}
function handleClickOutside(e) {
  if (tableWrapper.value && !tableWrapper.value.contains(e.target)) {
    expandedRowId.value = null
  }
}

/** 查看 **/
function viewForm(row) {
  viewingLemma.value = row
  showView.value = true
}
function closeView() {
  showView.value = false
  viewingLemma.value = null
}

/** 新增/编辑 **/
function openForm(lemma = null) {
  editingLemma.value = lemma
  showForm.value = true
}
function closeForm() {
  showForm.value = false
  editingLemma.value = null
}

/** 删除 **/
async function deleteLemma(id) {
  if (!confirm('确认删除该原型词？')) return
  await api.deleteLemma(id)
  reloadTable()
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

/* --- 表格样式优化：处理长文本和移动端滚动 --- */

/* 强制表格容器横向滚动 */
:deep(.data-table-container) {
  overflow-x: auto;
  width: 100%;
}

/* 确保表格有最小宽度，防止在小屏幕时过度压缩 */
:deep(table) {
  min-width: 600px; /* 最小宽度确保内容不会被挤压 */
  width: 100%;
}

/* 对所有单元格应用基本宽度 */
:deep(th),
:deep(td) {
  min-width: 100px; /* 默认最小宽度 */
  max-width: 250px;
}

/* 只对非操作列应用文本截断（:not(:last-child)） */
/* 操作列必须排除，否则绝对定位的菜单会被剪裁 */
:deep(td:not(:last-child)) {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 确保操作列（:last-child）保持可见，并固定宽度 */
:deep(th:last-child),
:deep(td:last-child) {
  /* CRITICAL FIX: 确保菜单可以超出单元格边界显示 */
  overflow: visible;
  /* 允许按钮文本换行，以防按钮被挤压 */
  white-space: normal;
  min-width: 140px;
  max-width: 140px;
}

/* 针对长文本列设置特定宽度 */
/* **翻译管理页面**：针对第二列（译文）设置更宽的限制 */
/* **原型词管理页面**：针对第二列（释义）设置更宽的限制 */
:deep(th:nth-child(2)),
:deep(td:nth-child(2)) {
  min-width: 200px;
  max-width: 300px;
}
</style>