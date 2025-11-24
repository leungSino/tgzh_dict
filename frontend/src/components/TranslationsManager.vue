<template>
  <div ref="tableWrapper" class="relative">
    <DataTableServer
      ref="tableRef"
      :columns="columns"
      :fetchData="fetchUsers"
      :pageSize="10"
    >
      <!-- 顶部操作 -->
      <template #actions>
        <button
          @click="openAdd"
          class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 transition-all"
        >
          ➕ 新增用户
        </button>
      </template>

      <!-- 每行操作按钮 -->
      <template #row-actions="{ row }">
        <!-- 桌面端 -->
        <div class="hidden sm:flex flex-wrap gap-2 justify-start">
          <button
            @click="toggleStatus(row)"
            :class="[
              'flex-1 min-w-[60px] px-2 py-1 rounded text-white text-center transition-all',
              row.status === 'enabled'
                ? 'bg-yellow-500 hover:bg-yellow-600 dark:bg-yellow-600 dark:hover:bg-yellow-700'
                : 'bg-green-500 hover:bg-green-600 dark:bg-green-600 dark:hover:bg-green-700'
            ]"
          >
            {{ row.status === 'enabled' ? '停用' : '启用' }}
          </button>

          <button
            @click="editUser(row)"
            class="flex-1 min-w-[60px] px-2 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-700 text-center transition-all"
          >
            编辑
          </button>

          <button
            @click="deleteUser(row.id)"
            class="flex-1 min-w-[60px] px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600 dark:bg-red-600 dark:hover:bg-red-700 text-center transition-all"
          >
            删除
          </button>
        </div>

        <!-- 移动端 -->
        <div class="sm:hidden relative">
          <button
            @click.stop="toggleMenu(row)"
            class="px-2 py-1 bg-gray-400 text-white rounded hover:bg-gray-500 dark:bg-gray-600 dark:hover:bg-gray-500 transition-all"
          >
            ⋮
          </button>

          <transition name="fade">
            <div
              v-if="row.id === expandedRowId"
              class="absolute right-0 mt-1 bg-white dark:bg-gray-800 border dark:border-gray-700 rounded-xl shadow-lg z-10 flex flex-col py-1 transition-all"
              style="min-width: 120px;"
            >
              <button
                @click="toggleStatus(row); closeMenu()"
                class="px-3 py-2 text-sm text-left hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200 transition-all"
              >
                {{ row.status === 'enabled' ? '停用' : '启用' }}
              </button>

              <button
                @click="editUser(row); closeMenu()"
                class="px-3 py-2 text-sm text-left hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200 transition-all"
              >
                编辑
              </button>

              <button
                @click="deleteUser(row.id); closeMenu()"
                class="px-3 py-2 text-sm text-left hover:bg-red-100 dark:hover:bg-red-700 text-red-600 dark:text-red-400 transition-all"
              >
                删除
              </button>
            </div>
          </transition>
        </div>
      </template>
    </DataTableServer>

    <!-- 编辑/新增用户弹窗 -->
    <UserForm
      v-if="showForm"
      :editingUser="editingUser"
      @close="showForm = false"
      @saved="reloadTable"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import DataTableServer from './DataTableServer.vue'
import UserForm from '@/pages/admin/UserForm.vue'
import api from '@/api/api.js'

const columns = [
  { key: 'username', label: '用户名' },
  { key: 'role', label: '角色' },
  { key: 'status', label: '状态' },
  { key: 'created_by', label: '创建人' },
  { key: 'created_at', label: '创建时间' },
  { key: 'updated_by', label: '更新人' },
  { key: 'updated_at', label: '更新时间' }
]

const showForm = ref(false)
const editingUser = ref(null)
const tableWrapper = ref(null)
const tableRef = ref(null)

// 控制移动端展开行
const expandedRowId = ref(null)

/** 异步拉取用户（DataTableServer 调用） **/
async function fetchUsers(query, page, pageSize) {
  try {
    const res = await api.searchUsers(query, page, pageSize)
    return res
  } catch (e) {
    console.error('加载用户失败：', e)
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
  if (!tableWrapper.value.contains(e.target)) {
    expandedRowId.value = null
  }
}

/** 切换启用/停用 **/
async function toggleStatus(row) {
  const newStatus = row.status === 'enabled' ? 'disabled' : 'enabled'
  await api.updateUser?.(row.id, { status: newStatus })
  reloadTable()
}

/** 新增 **/
function openAdd() {
  editingUser.value = null
  showForm.value = true
}

/** 编辑 **/
function editUser(user) {
  editingUser.value = { ...user }
  showForm.value = true
}

/** 删除 **/
async function deleteUser(id) {
  if (!confirm('确认删除该用户？')) return
  await api.deleteUser?.(id)
  reloadTable()
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

/* 移动端菜单淡入淡出 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 所有按钮统一过渡 */
button {
  transition: all 0.2s ease;
}
</style>
