<template>
  <DataTable
    title="用户管理"
    :columns="columns"
    :data="users"
  >
    <template #actions>
      <button class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
              @click="addUser">新增</button>
    </template>

    <template #row-actions="{ row }">
      <button class="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600"
              @click="deleteUser(row.id)">删除</button>
    </template>
  </DataTable>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DataTable from './DataTable.vue'
import api from '../api/api.js'

const columns = [
  { key: 'username', label: '用户名' },
  { key: 'role', label: '角色' },
  { key: 'email', label: '邮箱' }
]

const users = ref([])

async function loadUsers() {
  const res = await api.searchUsers('')
  users.value = res.data || []
}

async function addUser() {
  alert('新增用户弹窗 / 表单逻辑')
}

async function deleteUser(id) {
  await api.deleteUser(id)
  loadUsers()
}

onMounted(loadUsers)
</script>
