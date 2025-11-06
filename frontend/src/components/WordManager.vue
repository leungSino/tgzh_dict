<template>
  <div class="min-h-screen p-6 bg-gray-50 dark:bg-gray-900 text-gray-700 dark:text-white">

    <!-- 顶部按钮切换 -->
    <div class="flex gap-4 mb-6">
      <button
        @click="activeTab='translations'"
        :class="tabClass(activeTab === 'translations')"
      >
        📘 翻译对管理
      </button>
      <button
        @click="activeTab='lemmas'"
        :class="tabClass(activeTab === 'lemmas')"
      >
        📗 原型词管理
      </button>
    </div>

    <!-- Tab 内容区域 -->
    <div>
      <TranslationsManager v-if="activeTab==='translations'" />
      <LemmaManager v-if="activeTab==='lemmas'" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import TranslationsManager from './TranslationsManager.vue'
import LemmaManager from './LemmaManager.vue'

const activeTab = ref('translations')

const tabClass = (isActive) => [
  'px-4 py-2 rounded-lg font-medium transition',
  isActive
    ? 'bg-blue-600 text-white dark:bg-blue-500'
    : 'bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
]
</script>
