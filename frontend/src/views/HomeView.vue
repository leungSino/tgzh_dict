<template>
  <div class="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900 text-gray-700 dark:text-white">
    <div class="flex-grow flex flex-col items-center px-4 py-8 md:px-8 lg:px-16 mt-16">
      <div class="w-full max-w-4xl rounded-2xl shadow-lg p-6 md:p-8 bg-white dark:bg-gray-800 transition-all">

        <!-- 语言选择 -->
        <div class="flex flex-col md:flex-row justify-between items-center gap-4 mb-6">
          <div class="flex items-center gap-3">
            <!-- 源语言选择框 -->
            <div class="w-40">
              <LangSelector v-model="sourceLang" />
            </div>

            <!-- 切换按钮 -->
            <button
              @click="swapLanguages"
              class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full transition"
              title="切换语言"
            >
              🔄
            </button>

            <!-- 目标语言选择框 -->
            <div class="w-40">
              <LangSelector v-model="targetLang" />
            </div>
          </div>
        </div>

        <!-- 输入框 -->
        <textarea
          v-model="inputText"
          rows="4"
          placeholder="输入要翻译的内容..."
          class="w-full border border-gray-300 dark:border-gray-600 rounded-xl px-4 py-3 text-lg bg-white dark:bg-gray-700 text-gray-700 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
        ></textarea>

        <!-- 翻译按钮 -->
        <div class="flex justify-end mt-4">
          <button
            @click="translateText"
            class="bg-blue-600 text-white px-5 py-2 rounded-lg hover:bg-blue-700 transition"
          >
            🔍 翻译
          </button>
        </div>

        <!-- 翻译结果 -->
        <div
          v-if="translatedText"
          class="mt-6 border-t border-gray-200 dark:border-gray-700 pt-4 text-lg leading-relaxed text-gray-700 dark:text-gray-200"
        >
          <p class="whitespace-pre-line">{{ translatedText }}</p>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import LangSelector from '@/components/LangSelector.vue'

const sourceLang = ref('')
const targetLang = ref('')
const inputText = ref('')
const translatedText = ref('')

const swapLanguages = () => {
  const temp = sourceLang.value
  sourceLang.value = targetLang.value
  targetLang.value = temp
}

const translateText = () => {
  if (!inputText.value.trim()) return
  translatedText.value = `（${sourceLang.value} → ${targetLang.value}）翻译结果：${inputText.value}`
}
</script>
