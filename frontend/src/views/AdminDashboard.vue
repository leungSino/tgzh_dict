<template>
  <div class="min-h-screen flex bg-gray-100">
    <!-- 侧边栏 -->
    <aside class="w-64 bg-white shadow-md flex flex-col p-4 hidden md:flex">
      <h2 class="text-xl font-bold text-blue-600 mb-6">管理员控制台</h2>
      <nav class="flex flex-col space-y-2">
        <button @click="activeTab='words'" :class="tabClass('words')">单词管理</button>
        <button @click="activeTab='users'" :class="tabClass('users')">用户管理</button>
        <button @click="activeTab='logs'" :class="tabClass('logs')">操作记录</button>
      </nav>
    </aside>

    <!-- 主内容区 -->
    <div class="flex-1 p-6">
      <!-- 顶部导航 (移动端显示) -->
      <div class="md:hidden mb-4 flex justify-between items-center">
        <h2 class="text-xl font-bold text-blue-600">管理员控制台</h2>
        <select v-model="activeTab" class="border rounded px-3 py-1">
          <option value="words">单词管理</option>
          <option value="users">用户管理</option>
          <option value="logs">操作记录</option>
        </select>
      </div>

      <!-- 组件内容 -->
      <div class="bg-white shadow rounded-lg p-4 min-h-[60vh]">
        <WordManager v-if="activeTab==='words'" />
        <UserManager v-if="activeTab==='users'" />
        <LogViewer v-if="activeTab==='logs'" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
//import WordManager from '../components/WordManager.vue'
//import UserManager from '../components/UserManager.vue'
//import LogViewer from '../components/LogViewer.vue'

const activeTab = ref('words')

const tabClass = tab =>
  activeTab.value === tab
    ? 'px-4 py-2 bg-blue-600 text-white rounded'
    : 'px-4 py-2 bg-white text-blue-600 rounded border hover:bg-blue-50 transition'
</script>

<style>
/* 可选：让侧边栏固定高度并滚动 */
aside {
  min-height: 100vh;
}
</style>
