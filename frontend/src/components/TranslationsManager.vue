<template>
  <div ref="tableWrapper" class="relative">
    <DataTableServer
      ref="tableRef"
      :columns="columns"
      :fetchData="fetchTranslations"
      :pageSize="10"
      class="overflow-x-auto"
    >
      <!-- 顶部操作 -->
      <template #actions>
        <button
          @click="openForm()"
          class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 transition-all"
        >
          ➕ 新增
        </button>
      </template>

      <!-- 每行操作按钮 -->
      <template #row-actions="{ row }">
        <!-- 桌面端 -->
        <div class="hidden sm:flex flex-wrap gap-2">
          <button
            @click="viewForm(row)"
            class="px-2 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-700 transition-all"
          >
            查看
          </button>
          <button
            @click="openForm(row)"
            class="px-2 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-600 dark:bg-yellow-600 dark:hover:bg-yellow-700 transition-all"
          >
            编辑
          </button>
          <button
            @click="deleteTranslation(row.id)"
            class="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600 dark:bg-red-600 dark:hover:bg-red-700 transition-all"
          >
            删除
          </button>
        </div>

        <!-- 移动端 -->
        <div class="sm:hidden relative">
          <button
            @click.stop="toggleMenu(row.id)"
            class="px-2 py-1 bg-gray-400 text-white rounded hover:bg-gray-500 dark:bg-gray-600 dark:hover:bg-gray-500 transition-all"
          >
            ⋮
          </button>
          <transition name="fade">
            <div
              v-if="expandedRowId === row.id"
              class="absolute right-0 mt-1 bg-white dark:bg-gray-800 border dark:border-gray-700 rounded-xl shadow-lg z-10 flex flex-col py-1 max-h-60 overflow-y-auto w-28"
            >
              <button
                @click="viewForm(row); closeMenu()"
                class="px-3 py-2 text-xs text-left hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200 transition-all"
              >
                🔍 查看
              </button>
              <button
                @click="openForm(row); closeMenu()"
                class="px-3 py-2 text-xs text-left hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200 transition-all"
              >
                ✏️ 编辑
              </button>
              <button
                @click="deleteTranslation(row.id); closeMenu()"
                class="px-3 py-2 text-xs text-left hover:bg-red-100 dark:hover:bg-red-700 text-red-600 dark:text-red-400 transition-all"
              >
                🗑 删除
              </button>
            </div>
          </transition>
        </div>
      </template>
    </DataTableServer>

    <!-- 编辑/新增弹窗 -->
    <TranslationForm
      v-if="showForm"
      :editingTranslation="editingTranslation"
      @close="closeForm"
      @saved="reloadTable"
    />
    <!-- 查看弹窗 -->
    <TranslationView
      v-if="showView"
      :viewingWord="viewingTranslation"
      @close="closeView"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import DataTableServer from '@/components/DataTableServer.vue'
import TranslationForm from '@/pages/admin/TranslationForm.vue'
import TranslationView from '@/pages/admin/TranslationView.vue'
import api from '@/api/api.js'

/* 表头 */
const columns = [
  { key: 'sourceText', label: '原文' },
  { key: 'targetText', label: '译文' },
  { key: 'lemma', label: '原型词' }
]

/* refs */
const tableRef = ref(null)
const tableWrapper = ref(null)
const showForm = ref(false)
const editingTranslation = ref(null)
const expandedRowId = ref(null)

const showView = ref(false)
const viewingTranslation = ref(null)

/* 拉取数据 */
async function fetchTranslations(query, page, pageSize) {
  try {
    const res = await api.getTranslations(query, page, pageSize)
    if (res?.items) {
      const items = res.items.map(item => {
        const translationsArray = Array.isArray(item.translations)
          ? item.translations
          : Object.values(item.translations || {})

        const posArray = Array.isArray(item.pos)
          ? item.pos
          : (typeof item.pos === 'string'
              ? item.pos.split(',').map(s => s.trim()).filter(Boolean)
              : [])

        return {
          ...item,
          id: item._id || item.id,
          targetText: translationsArray.map(t => t.translation).join('; ') || '-',
          pos: posArray,
          translations: translationsArray
        }
      })
      return { items, total: res.total || items.length }
    }
    return { items: [], total: 0 }
  } catch (err) {
    console.error('[fetchTranslations] 拉取失败：', err)
    return { items: [], total: 0 }
  }
}

/* 刷新 */
function reloadTable() {
  tableRef.value?.reload()
}

/* 查看 */
function viewForm(row) {
  viewingTranslation.value = row
  showView.value = true
}
function closeView() {
  showView.value = false
  viewingTranslation.value = null
}

/* 编辑/新增 */
function openForm(row = null) {
  editingTranslation.value = row
  showForm.value = true
}
function closeForm() {
  showForm.value = false
  editingTranslation.value = null
}

/* 删除 */
async function deleteTranslation(id) {
  if (!confirm('确认删除？')) return
  await api.deleteTranslation(id)
  reloadTable()
}

/* 移动端菜单 */
function toggleMenu(id) {
  expandedRowId.value = expandedRowId.value === id ? null : id
}
function closeMenu() {
  expandedRowId.value = null
}
function handleClickOutside(e) {
  if (!tableWrapper.value.contains(e.target)) closeMenu()
}

onMounted(() => document.addEventListener('click', handleClickOutside))
onBeforeUnmount(() => document.removeEventListener('click', handleClickOutside))
</script>

<style scoped>
/* 添加表格容器样式，确保在小屏幕时可以水平滚动 */
:deep(.data-table-container) {
  overflow-x: auto;
  width: 100%;
}

/* 确保表格有最小宽度，避免在小屏幕时过度压缩 */
:deep(table) {
  min-width: 600px; /* 根据列数调整这个值 */
  width: 100%;
}

/* 表格列宽设置，确保重要列有足够空间 */
:deep(th),
:deep(td) {
  min-width: 120px; /* 每列最小宽度 */
  white-space: nowrap; /* 防止文本换行 */
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 原文和译文列可以更宽一些 */
:deep(th:nth-child(1)),
:deep(td:nth-child(1)) { /* 原文列 */
  min-width: 150px;
  max-width: 200px;
}

:deep(th:nth-child(2)),
:deep(td:nth-child(2)) { /* 译文列 */
  min-width: 200px;
  max-width: 300px;
}

:deep(th:nth-child(3)),
:deep(td:nth-child(3)) { /* 原型词列 */
  min-width: 120px;
  max-width: 150px;
}

/* 操作列固定宽度 */
:deep(th:last-child),
:deep(td:last-child) {
  min-width: 140px;
  max-width: 140px;
}

/* 滚动条样式统一 */
:deep(.data-table-container)::-webkit-scrollbar {
  height: 8px;
}

:deep(.data-table-container)::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

:deep(.data-table-container)::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

:deep(.data-table-container)::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 暗黑模式滚动条 */
@media (prefers-color-scheme: dark) {
  :deep(.data-table-container)::-webkit-scrollbar-track {
    background: #374151;
  }

  :deep(.data-table-container)::-webkit-scrollbar-thumb {
    background: #6b7280;
  }

  :deep(.data-table-container)::-webkit-scrollbar-thumb:hover {
    background: #9ca3af;
  }
}

@media (max-width: 640px) {
  .flex-wrap {
    flex-direction: column;
    align-items: stretch;
  }

  /* 移动端表格最小宽度调整 */
  :deep(table) {
    min-width: 500px;
  }

  :deep(th),
  :deep(td) {
    min-width: 100px;
  }
}
</style>