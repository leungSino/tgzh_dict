<template>
  <div ref="tableWrapper" class="relative">
    <DataTableServer
      ref="tableRef"
      :columns="columns"
      :fetchData="fetchTranslations"
      :pageSize="10"
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
              class="absolute right-0 mt-1 bg-white dark:bg-gray-800 border dark:border-gray-700 rounded-xl shadow-lg z-10 flex flex-col py-1"
              style="min-width: 120px;"
            >
              <button
                @click="openForm(row); closeMenu()"
                class="px-3 py-2 text-sm text-left hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200"
              >
                ✏️ 编辑
              </button>
              <button
                @click="deleteTranslation(row.id); closeMenu()"
                class="px-3 py-2 text-sm text-left hover:bg-red-100 dark:hover:bg-red-700 text-red-600 dark:text-red-400"
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
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import DataTableServer from '@/components/DataTableServer.vue'
import TranslationForm from '@/pages/admin/TranslationForm.vue'
import api from '@/api/api.js'

const columns = [
  { key: 'sourceText', label: '原文' },
  { key: 'targetText', label: '译文' },
  { key: 'lemma', label: '原型词' },
  { key: 'pos', label: '词性' },
  { key: 'tags', label: '标签' }
]

const tableRef = ref(null)
const tableWrapper = ref(null)
const showForm = ref(false)
const editingTranslation = ref(null)
const expandedRowId = ref(null) // 当前展开的菜单行 ID

/** 获取翻译数据 **/
async function fetchTranslations(query, page, pageSize) {
  const res = await api.getTranslations(query, page, pageSize)
  if (res?.data) {
    const items = res.data.map(item => ({
      ...item,
      id: item._id || item.id,
      sourceText: item.sourceText || '-',
      targetText: Object.values(item.translations || {}).map(t => t.translation).join('; '),
      lemma: item.lemma || '-',
      pos: item.pos || '-',
      tags: (item.tags || []).join(', ')
    }))
    return { items, total: res.data.length }
  }
  return { items: [], total: 0 }
}


/** 刷新表格 **/
function reloadTable() {
  tableRef.value?.reload()
}

/** 表单操作 **/
function openForm(row = null) {
  editingTranslation.value = row
  showForm.value = true
}
function closeForm() {
  showForm.value = false
  editingTranslation.value = null
}

/** 删除 **/
async function deleteTranslation(id) {
  if (!confirm('确认删除该翻译对？')) return
  await api.deleteTranslation(id)
  reloadTable()
}

/** 移动端菜单控制 **/
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
@media (max-width: 640px) {
  .flex-wrap {
    flex-direction: column;
    align-items: stretch;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
