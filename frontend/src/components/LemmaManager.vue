<template>
  <div ref="tableWrapper" class="relative">
    <DataTableServer
      ref="tableRef"
      :columns="columns"
      :fetchData="fetchLemmas"
      :pageSize="10"
    >
      <!-- 顶部操作 -->
      <template #actions>
        <button
          @click="openForm()"
          class="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700 dark:bg-green-500 dark:hover:bg-green-600 transition-all"
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
            @click="deleteLemma(row.id)"
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
                @click="viewForm(row); closeMenu()"
                class="px-3 py-2 text-sm text-left hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200"
              >
                🔍 查看
              </button>
              <button
                @click="openForm(row); closeMenu()"
                class="px-3 py-2 text-sm text-left hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200"
              >
                ✏️ 编辑
              </button>
              <button
                @click="deleteLemma(row.id); closeMenu()"
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
    <LemmaForm
      v-if="showForm"
      :editingLemma="editingLemma"
      @close="closeForm"
      @saved="reloadTable"
    />

    <!-- 只读查看弹窗 -->
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

const tableRef = ref(null)
const tableWrapper = ref(null)
const showForm = ref(false)
const editingLemma = ref(null)
const expandedRowId = ref(null)

const showView = ref(false)
const viewingLemma = ref(null)

/** 拉取数据 **/
async function fetchLemmas(query, page, pageSize) {
  try {
    const res = await api.getLemmas(query, page, pageSize)
    if (res?.items) {
      const items = res.items.map(item => {
        // 保证 pos 仍然是数组（编辑/查看必须用数组）
        const posArray = Array.isArray(item.pos)
          ? item.pos
          : (typeof item.pos === 'string'
            ? item.pos.split(',').map(s => s.trim()).filter(Boolean)
            : [])

        return {
          ...item,

          /** id 统一处理 **/
          id: item._id || item.id,

          /** 用于表格显示的字段：仅用于 DataTable，不影响编辑 **/
          posDisplay: posArray.join(', ') || '-',

          /** 原始 pos 必须保留为数组 **/
          pos: posArray,

          /** 释义取中文，否则英文，否则 '-' **/
          definition: item.definitions?.zh || item.definitions?.en || '-',

          /** 保证 derived, related 为数组 **/
          derived: Array.isArray(item.derived) ? item.derived : [],
          related: Array.isArray(item.related) ? item.related : []
        }
      })
      return { items, total: res.total || items.length }
    }

    return { items: [], total: 0 }
  } catch (err) {
    console.error('[fetchLemmas] 拉取失败：', err)
    return { items: [], total: 0 }
  }
}


/** 刷新表格 **/
function reloadTable() {
  tableRef.value?.reload()
}

/** 查看操作 **/
function viewForm(row) {
  viewingLemma.value = row
  showView.value = true
}

function closeView() {
  showView.value = false
  viewingLemma.value = null
}

/** 打开/关闭表单 **/
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
