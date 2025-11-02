<template>
  <div class="bg-white dark:bg-gray-800 shadow-md rounded-lg overflow-hidden">
    <table class="w-full text-left border-collapse">
      <thead class="bg-gray-100 dark:bg-gray-700">
        <tr>
          <th class="px-4 py-2">中文</th>
          <th class="px-4 py-2">塔吉克语</th>
          <th class="px-4 py-2">俄语</th>
          <th class="px-4 py-2">英语</th>
          <th class="px-4 py-2">标签</th>
          <th class="px-4 py-2 text-center">操作</th>
        </tr>
      </thead>

      <tbody v-if="!loading && words.length">
        <tr
          v-for="word in words"
          :key="word.id || word._id"
          class="border-b hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
        >
          <td class="px-4 py-2">{{ word.lang_entries?.zh?.word || '-' }}</td>
          <td class="px-4 py-2">{{ word.lang_entries?.tg?.word || '-' }}</td>
          <td class="px-4 py-2">{{ word.lang_entries?.ru?.word || '-' }}</td>
          <td class="px-4 py-2">{{ word.lang_entries?.en?.word || '-' }}</td>

          <td class="px-4 py-2">
            <template v-if="word.tags?.length">
              <span
                v-for="tag in word.tags"
                :key="`${word.id || word._id}-${tag}`"
                class="inline-block bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 text-xs font-medium px-2 py-1 rounded mr-1"
              >
                {{ tag }}
              </span>
            </template>
            <span v-else class="text-gray-400 text-sm">无标签</span>
          </td>

          <td class="px-4 py-2 text-center space-x-3">
            <button
              class="text-blue-500 hover:underline"
              @click="$emit('edit', word.id || word._id)"
            >
              编辑
            </button>
            <button
              class="text-red-500 hover:underline"
              @click="$emit('delete', word.id || word._id)"
            >
              删除
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-4 text-gray-500">
      加载中...
    </div>

    <!-- 空数据状态 -->
    <div v-else-if="!loading && !words.length" class="text-center py-4 text-gray-500">
      暂无数据
    </div>
  </div>
</template>

<script setup lang="ts">
interface LangEntry {
  word: string
}

interface WordItem {
  id?: string
  _id?: string
  lang_entries: {
    zh?: LangEntry
    tg?: LangEntry
    ru?: LangEntry
    en?: LangEntry
  }
  tags?: string[]
}

defineProps<{
  words: WordItem[]
  loading: boolean
}>()

defineEmits<{
  (e: 'edit', id: string): void
  (e: 'delete', id: string): void
}>()
</script>

<style scoped>
table {
  border-spacing: 0;
}
th {
  font-weight: 600;
  color: #374151;
}
.dark th {
  color: #d1d5db;
}
</style>
