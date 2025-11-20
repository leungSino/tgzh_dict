<template>
  <Modal :title="form.id ? '编辑用户' : '新增用户'" @close="$emit('close')">
    <form @submit.prevent="saveUser" class="space-y-4">
      <!-- 用户名 -->
      <div class="flex flex-col mb-4">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">
          用户名 <span class="text-xs text-red-500 ml-1">*</span>
        </label>
        <input
          type="text"
          v-model.trim="form.username"
          @blur="validateField('username')"
          placeholder="请输入用户名"
          :class="[
            'w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white',
            usernameError ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'
          ]"
        />
        <p v-if="usernameError" class="text-red-500 text-xs mt-1">{{ usernameError }}</p>
      </div>

      <!-- 密码 -->
      <div class="flex flex-col mb-4">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">
          密码
          <span class="text-xs text-red-500 ml-1">
            {{ form.id ? '(留空表示不修改密码)' : '*' }}
          </span>
        </label>
        <input
          type="password"
          v-model.trim="form.password"
          @blur="validateField('password')"
          placeholder="请输入密码"
          :class="[
            'w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white',
            passwordError ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'
          ]"
        />
        <p v-if="passwordError" class="text-red-500 text-xs mt-1">{{ passwordError }}</p>
      </div>

      <!-- 角色 -->
      <div class="flex flex-col mb-4">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">角色</label>
        <select
          v-model="form.role"
          class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"
        >
          <option value="admin">管理员</option>
          <option value="editor">编辑者</option>
          <option value="viewer">查看者</option>
        </select>
      </div>

      <!-- 状态 -->
      <div class="flex flex-col mb-4">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">状态</label>
        <select
          v-model="form.status"
          class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"
        >
          <option value="enabled">启用</option>
          <option value="disabled">停用</option>
        </select>
      </div>

      <!-- 创建信息 -->
      <div
        v-if="form.id"
        class="text-xs text-gray-600 dark:text-gray-400 border-t border-gray-200 dark:border-gray-700 pt-3 space-y-1"
      >
        <p>创建人：{{ form.created_by || '未知' }}</p>
        <p>创建时间：{{ formatDate(form.created_at) }}</p>
        <p>更新人：{{ form.updated_by || '未知' }}</p>
        <p>更新时间：{{ formatDate(form.updated_at) }}</p>
      </div>
    </form>

    <template #footer>
      <button
        type="button"
        @click="saveUser"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        保存
      </button>
      <button
        type="button"
        @click="$emit('close')"
        class="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500 ml-2"
      >
        取消
      </button>
    </template>
  </Modal>
</template>

<script setup>
import { ref, watch } from 'vue'
import Modal from '@/components/Modal.vue'
import api from '@/api/api.js'
import { useUserStore } from '@/store/userStore.js'

const props = defineProps({ editingUser: Object })
const emit = defineEmits(['close', 'saved'])
const userStore = useUserStore()

const form = ref({
  id: null,
  username: '',
  password: '',
  role: 'viewer',
  status: 'enabled',
  created_by: '',
  created_at: '',
  updated_by: '',
  updated_at: ''
})

// 校验状态
const usernameError = ref('')
const passwordError = ref('')

// 监听编辑对象
watch(
  () => props.editingUser,
  (u) => {
    if (u) {
      Object.assign(form.value, {
        id: u.id,
        username: u.username,
        password: '',
        role: u.role || 'viewer',
        status: u.status || 'enabled',
        created_by: u.created_by || '',
        created_at: u.created_at || '',
        updated_by: u.updated_by || '',
        updated_at: u.updated_at || ''
      })
    } else {
      Object.assign(form.value, {
        id: null,
        username: '',
        password: '',
        role: 'viewer',
        status: 'enabled',
        created_by: '',
        created_at: '',
        updated_by: '',
        updated_at: ''
      })
    }
    usernameError.value = ''
    passwordError.value = ''
  },
  { immediate: true }
)

/** 校验字段 **/
async function validateField(field) {
  if (field === 'username') {
    const username = form.value.username.trim()
    if (!username) {
      usernameError.value = '用户名不能为空'
      return false
    }
    if (username.length < 4) {
      usernameError.value = '用户名长度至少4个字符'
      return false
    }

    try {
      const res = await api.checkUsername(username)
      // 如果存在且不是当前编辑的用户
      if (res?.data?.exists && res.data.user_id !== form.value.id) {
        usernameError.value = '该用户名已存在'
        return false
      }
    } catch (e) {
      console.warn('用户名检查失败', e)
    }

    usernameError.value = ''
    return true
  }

  if (field === 'password') {
    if (!form.value.password && !form.value.id) {
      passwordError.value = '密码不能为空'
      return false
    } else if (form.value.password && form.value.password.length < 4) {
      passwordError.value = '密码长度至少4个字符'
      return false
    } else {
      passwordError.value = ''
      return true
    }
  }
  return true
}

/** 保存 **/
async function saveUser() {
  const validUsername = await validateField('username')
  const validPassword = await validateField('password')
  if (!validUsername || !validPassword) return

  const payload = {
    username: form.value.username.trim(),
    role: form.value.role,
    status: form.value.status,
    ...(form.value.password ? { password: form.value.password } : {}),
    updated_by: userStore.username || 'system'
  }

  if (!form.value.id) {
    payload.created_by = userStore.username || 'system'
    await api.addUser(payload)
  } else {
    await api.updateUser(form.value.id, payload)
  }

  emit('saved')
  emit('close')
}

function formatDate(d) {
  if (!d) return ''
  const date = new Date(d)
  return date.toLocaleString('zh-CN', { hour12: false })
}
</script>
