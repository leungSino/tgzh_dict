<template>
  <div class="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900 text-gray-700 dark:text-white">
    <div class="flex-grow flex flex-col items-center px-4 py-8 md:px-8 lg:px-16 mt-16">
      <div class="w-full max-w-4xl rounded-2xl shadow-lg p-6 md:p-8 bg-white dark:bg-gray-800 transition-all">

        <!-- 语言选择 -->
        <div class="flex flex-col md:flex-row justify-between items-center gap-4 mb-6">
          <div class="flex items-center gap-3">
            <div class="w-40">
              <LangSelector v-model="sourceLang" />
            </div>

            <button
              @click="swapLanguages"
              class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full transition"
              title="切换语言"
            >
              🔄
            </button>

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
        <div v-if="translatedResults.length" class="mt-6 border-t border-gray-200 dark:border-gray-700 pt-4 text-lg leading-relaxed text-gray-700 dark:text-gray-200">
          <div v-for="(res, index) in translatedResults" :key="index" class="mb-4 p-2 border border-gray-300 dark:border-gray-700 rounded-lg">
            <p><strong>翻译:</strong> {{ res.translation }}</p>
            <p><strong>描述:</strong> {{ res.description }}</p>
            <p><strong>词性:</strong> {{ res.pos }}</p>
            <p>
              <strong>原型词:</strong>

              <!-- 可点击原型词 -->
              <button
                class="text-blue-600 dark:text-blue-400 hover:underline"
                @click="openLemma(res.lemma)"
              >
                {{ res.lemma }}
              </button>

              <!-- 只有 lemma 存在时才显示提示文字 -->
              <span
                v-if="res.lemma"
                class="text-sm text-gray-500 dark:text-gray-400 ml-1 italic"
              >
                (可点击查看)
              </span>
            </p>
            <p><strong>词根:</strong> {{ res.root }}</p>
            <p><strong>例句:</strong> {{ res.originalSentence }} → {{ res.translatedSentence }}</p>
          </div>
        </div>

        <!-- 只读查看弹窗 -->
        <LemmaView
          v-if="showView"
          :viewingLemma="viewingLemma"
          @close="closeView"
        />

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import LangSelector from '@/components/LangSelector.vue'
import LemmaView from '@/pages/admin/LemmaView.vue'
import api from '@/api/api.js'

const sourceLang = ref('tg')
const targetLang = ref('zh')
const inputText = ref('')
const translatedResults = ref([])

const showView = ref(false)
const viewingLemma = ref(null)

/** 查看操作 **/
async function openLemma(lemmaText) {
  try {
    const res = await api.getLemmaByLemma(lemmaText)

    if (res.data.success && res.data.data) {
      viewingLemma.value = res.data.data   // 赋值 lemma 对象
      showView.value = true                // 展示弹窗
    } else {
      alert("未找到该原型词的详细信息")
    }
  } catch (error) {
    console.error(error)
    alert("查询原型词信息失败")
  }
}


function closeView() {
  showView.value = false
  viewingLemma.value = null
}

const swapLanguages = () => {
  const temp = sourceLang.value
  sourceLang.value = targetLang.value
  targetLang.value = temp
}

const translateText = async () => {
  if (!inputText.value.trim()) return
  translatedResults.value = [] // 清空上一次结果

  try {
    const res = await api.translateText({
      sourceText: inputText.value,
      sourceLang: sourceLang.value,
      targetLang: targetLang.value
    })

    if (res.success) {
      translatedResults.value = res.results
    } else {
      translatedResults.value = [{ translation: '翻译失败', description: '', pos: '', lemma: '', root: '', originalSentence: '', translatedSentence: '' }]
    }
  } catch (err) {
    console.error(err)
    translatedResults.value = [{ translation: '请求错误，请检查后端', description: '', pos: '', lemma: '', root: '', originalSentence: '', translatedSentence: '' }]
  }
}
</script>
