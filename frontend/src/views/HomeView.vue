<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <!-- 顶部导航栏 -->
    <!-- <Navbar /> -->

    <!-- 主体内容 -->
    <div class="flex-grow flex flex-col items-center px-4 py-8 md:px-8 lg:px-16">
      <div
        class="w-full max-w-4xl bg-white rounded-2xl shadow-lg p-6 md:p-8 transition-all"
      >
        <!-- 语言选择 -->
        <div
          class="flex flex-col md:flex-row justify-between items-center gap-4 mb-6"
        >
          <div class="flex items-center gap-2">
            <select
              v-model="sourceLang"
              class="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="zh">中文</option>
              <option value="tg">塔吉克语</option>
              <option value="ru">俄语</option>
              <option value="en">英语</option>
            </select>
            <button
              @click="swapLanguages"
              class="p-2 hover:bg-gray-100 rounded-full transition"
              title="切换语言"
            >
              🔄
            </button>
            <select
              v-model="targetLang"
              class="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="zh">中文</option>
              <option value="tg">塔吉克语</option>
              <option value="ru">俄语</option>
              <option value="en">英语</option>
            </select>
          </div>
        </div>

        <!-- 输入框 -->
        <textarea
          v-model="inputText"
          rows="4"
          placeholder="输入要翻译的内容..."
          class="w-full border border-gray-300 rounded-xl px-4 py-3 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
        ></textarea>

        <!-- 翻译按钮 -->
        <div class="flex justify-end mt-4">
          <button
            @click="translateText"
            class="btn flex items-center gap-2"
          >
            🔍 翻译
          </button>
        </div>

        <!-- 翻译结果 -->
        <div
          v-if="translatedText"
          class="mt-6 border-t border-gray-200 pt-4 text-lg leading-relaxed"
        >
          <p class="text-gray-700 whitespace-pre-line">{{ translatedText }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Navbar from "@/components/Navbar.vue";

const sourceLang = ref("zh");
const targetLang = ref("tg");
const inputText = ref("");
const translatedText = ref("");

const swapLanguages = () => {
  const temp = sourceLang.value;
  sourceLang.value = targetLang.value;
  targetLang.value = temp;
};

const translateText = async () => {
  if (!inputText.value.trim()) return;
  // 模拟 API 请求
  translatedText.value = `（${sourceLang.value} → ${targetLang.value}）翻译结果：${inputText.value}`;
};
</script>

<style scoped>
.btn {
  @apply bg-blue-600 text-white px-5 py-2 rounded-lg hover:bg-blue-700 transition;
}
</style>
