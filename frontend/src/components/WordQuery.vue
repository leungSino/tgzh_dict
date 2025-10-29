<template>
  <div class="space-y-4">
    <div class="flex items-center gap-2">
      <select v-model="direction" class="input w-32">
        <option value="tg-zh">塔吉克语 → 中文</option>
        <option value="zh-tg">中文 → 塔吉克语</option>
      </select>
      <input v-model="query" placeholder="输入单词..." class="input flex-1" />
      <button @click="searchWord" class="btn">查询</button>
    </div>

    <div v-if="result" class="p-4 bg-gray-50 border rounded">
      <p><strong>结果：</strong> {{ result.translation }}</p>
      <p class="text-gray-600 text-sm mt-1">示例：{{ result.example }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const direction = ref('tg-zh')
const query = ref('')
const result = ref(null)

const searchWord = async () => {
  if (!query.value) return
  // TODO: 调用后端 API
  result.value = {
    translation: "示例翻译",
    example: "他正在学习塔吉克语。",
  }
}
</script>
