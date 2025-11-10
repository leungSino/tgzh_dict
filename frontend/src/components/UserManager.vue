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
          class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          新增用户
        </button>
      </template>

      <!-- 每行操作按钮 -->
      <template #row-actions="{ row }">
        <!-- 桌面端 -->
        <div class="hidden sm:flex flex-wrap gap-2 justify-start">
          <button
            @click="toggleStatus(row)"
            :class="[
              'flex-1 min-w-[60px] px-2 py-1 rounded text-white text-center',
              row.status === 'enabled'
                ? 'bg-yellow-500 hover:bg-yellow-600'
                : 'bg-green-500 hover:bg-green-600'
            ]"
          >
            {{ row.status === 'enabled' ? '停用' : '启用' }}
          </button>

          <button
            @click="editUser(row)"
            class="flex-1 min-w-[60px] px-2 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 text-center"
          >
            编辑
          </button>

          <button
            @click="deleteUser(row.id)"
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
              @click="toggleStatus(row); closeMenu()"
              class="flex-1 min-w-[60px] px-2 py-1 text-white bg-yellow-500 hover:bg-yellow-600 rounded text-center"
            >
              {{ row.status === 'enabled' ? '停用' : '启用' }}
            </button>
            <button
              @click="editUser(row); closeMenu()"
              class="flex-1 min-w-[60px] px-2 py-1 text-white bg-blue-500 hover:bg-blue-600 rounded text-center"
            >
              编辑
            </button>
            <button
              @click="deleteUser(row.id); closeMenu()"
              class="flex-1 min-w-[60px] px-2 py-1 text-white bg-red-500 hover:bg-red-600 rounded text-center"
            >
              删除
            </button>
          </div>
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
    // res 已经是 { items, total }
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
