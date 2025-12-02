<template>
  <div class="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900 text-gray-700 dark:text-white">
    <div class="flex-grow flex flex-col items-center px-4 py-8 md:px-8 lg:px-16 mt-16">
      <div class="w-full max-w-4xl rounded-2xl shadow-lg p-6 md:p-8 bg-white dark:bg-gray-800 transition-all">

        <div class="flex flex-col md:flex-row justify-between items-center gap-4 mb-6 w-full">
          <div class="flex items-center gap-3 w-full md:w-auto">

            <div class="flex-1 min-w-[120px] max-w-[180px]">
              <LangSelector v-model="sourceLang" />
            </div>

            <button
              @click="swapLanguages"
              class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full transition flex-shrink-0"
              title="切换语言"
            >
              ⇄
            </button>

            <div class="flex-1 min-w-[120px] max-w-[180px]">
              <LangSelector v-model="targetLang" />
            </div>
          </div>
        </div>

        <textarea
          v-model="inputText"
          rows="4"
          placeholder="输入要翻译的内容..."
          class="w-full border border-gray-300 dark:border-gray-600 rounded-xl px-4 py-3 text-lg bg-white dark:bg-gray-700 text-gray-700 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
        ></textarea>

        <div class="flex justify-end mt-4">
          <button
            @click="translateText"
            class="bg-blue-600 text-white px-5 py-2 rounded-lg hover:bg-blue-700 transition"
          >
            🔍 翻译
          </button>
        </div>

        <div v-if="translatedResults.length" class="mt-6 border-t border-gray-200 dark:border-gray-700 pt-4 text-lg leading-relaxed text-gray-700 dark:text-gray-200">
          <div v-for="(res, index) in translatedResults" :key="index" class="mb-4 p-2 border border-gray-300 dark:border-gray-700 rounded-lg">
            <p><strong>翻译:</strong> {{ res.translation }}</p>

            <div v-if="res.meanings?.length">
              <strong>释义:</strong>
              <ul class="list-disc ml-6">
                <li v-for="(m, i) in res.meanings" :key="i">{{ m }}</li>
              </ul>
            </div>

            <p v-if="res.description">
              <strong>描述:</strong> {{ res.description }}
            </p>

            <p v-if="res.pos">
              <strong>词性:</strong> {{ res.pos }}
            </p>

            <p v-if="res.lemma">
              <strong>原型词:</strong>
              <button
                @click="openLemma(res.lemma)"
                class="text-blue-600 dark:text-blue-400 hover:underline"
              >
                {{ res.lemma }}
              </button>
              <span class="text-sm italic text-gray-500">(点击查看完整动词结构)</span>
            </p>

            <p v-if="res.root">
              <strong>词根:</strong> {{ res.root }}
            </p>


            <p v-if="res.brief">
              <strong>说明:</strong> {{ res.brief }}
            </p>

            <div v-if="res.forms">
              <h3 class="font-bold mt-4 mb-1">动词变位</h3>

              <div v-if="res.forms.present?.length">
                <strong>现在时:</strong>
                <ul class="ml-6 list-disc">
                  <li v-for="(f, i) in res.forms.present" :key="i">
                    {{ f.form }} <span v-if="f.meaning">— {{ f.meaning }}</span>
                  </li>
                </ul>
              </div>

              <div v-if="res.forms.past?.length">
                <strong>过去时:</strong>
                <ul class="ml-6 list-disc">
                  <li v-for="(f, i) in res.forms.past" :key="i">
                    {{ f.form }} <span v-if="f.meaning">— {{ f.meaning }}</span>
                  </li>
                </ul>
              </div>

              <div v-if="res.forms.future?.length">
                <strong>将来时:</strong>
                <ul class="ml-6 list-disc">
                  <li v-for="(f, i) in res.forms.future" :key="i">
                    {{ f.form }} <span v-if="f.meaning">— {{ f.meaning }}</span>
                  </li>
                </ul>
              </div>

              <div v-if="res.forms.imperative?.length">
                <strong>命令式:</strong>
                <ul class="ml-6 list-disc">
                  <li v-for="(f, i) in res.forms.imperative" :key="i">
                    {{ f.form }} <span v-if="f.meaning">— {{ f.meaning }}</span>
                  </li>
                </ul>
              </div>

              <div v-if="res.forms.derivatives?.length">
                <strong>派生词:</strong>
                <ul class="ml-6 list-disc">
                  <li v-for="(d, i) in res.forms.derivatives" :key="i">
                    {{ d.form }}
                  </li>
                </ul>
              </div>
            </div>

            <div v-if="res.examples?.length">
              <h3 class="font-bold mt-4 mb-2">例句</h3>
              <div
                v-for="(ex, i) in res.examples"
                :key="i"
                class="ml-2 mb-2"
              >
                <p>{{ ex.source }}</p>
                <p class="text-gray-500">→ {{ ex.target }}</p>
              </div>
            </div>

            <div v-else-if="res.originalSentence && res.originalSentence.trim()">
              <h3 class="font-bold mt-4 mb-2">例句</h3>
              <p>{{ res.originalSentence }}</p>
              <p class="text-gray-500">→ {{ res.translatedSentence }}</p>
            </div>

          </div>
        </div>

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
// 假设 LangSelector 和 LemmaView 的路径是正确的
import LangSelector from '@/components/LangSelector.vue'
import LemmaView from '@/pages/admin/LemmaView.vue'
// 导入 API 模块
import api from '@/api/api.js'

// --- 响应式状态 ---
const sourceLang = ref('tg') // 默认源语言
const targetLang = ref('zh') // 默认目标语言
const inputText = ref('')    // 输入文本
const translatedResults = ref([]) // 翻译结果数组

const showView = ref(false)     // 控制 LemmaView 弹窗的显示
const viewingLemma = ref(null)  // 当前查看的原型词详情数据

// --- 方法 ---

/**
 * @description 查看 lemma 详情，通过 API 获取数据并打开弹窗
 * @param {string} lemmaText - 要查询的原型词文本
 */
async function openLemma(lemmaText) {
  try {
    // 假设 api.getLemmaByLemma(lemmaText) 返回 { data: { success: boolean, data: object } }
    const res = await api.getLemmaByLemma(lemmaText)

    if (res.data.success && res.data.data) {
      viewingLemma.value = res.data.data
      showView.value = true
    } else {
      alert('未找到该原型词的详细信息')
    }
  } catch (error) {
    console.error('查询原型词信息失败:', error)
    alert('查询原型词信息失败')
  }
}

/**
 * @description 关闭 LemmaView 弹窗并清空数据
 */
function closeView() {
  showView.value = false
  viewingLemma.value = null
}

/**
 * @description 切换源语言和目标语言
 */
const swapLanguages = () => {
  const temp = sourceLang.value
  sourceLang.value = targetLang.value
  targetLang.value = temp
}

/**
 * @description 执行翻译操作
 */
const translateText = async () => {
  if (!inputText.value.trim()) {
    translatedResults.value = [] // 清空结果
    return
  }
  translatedResults.value = []

  try {
    // 假设 api.translateText 返回 { success: boolean, results: Array<object> }
    const res = await api.translateText({
      sourceText: inputText.value,
      sourceLang: sourceLang.value,
      targetLang: targetLang.value,
    })

    if (res.success) {
      translatedResults.value = res.results
    } else {
      // 翻译 API 调用成功但业务失败
      translatedResults.value = [
        {
          translation: '翻译失败',
          description: '',
          pos: '',
          lemma: '',
          root: '',
          originalSentence: '',
          translatedSentence: '',
        },
      ]
    }
  } catch (err) {
    // API 请求/网络错误
    console.error('翻译请求错误:', err)
    translatedResults.value = [
      {
        translation: '请求错误，请检查网络或后端服务',
        description: '',
        pos: '',
        lemma: '',
        root: '',
        originalSentence: '',
        translatedSentence: '',
      },
    ]
  }
}
</script>

<style>
/* 修复 iOS/安卓下 select 被放大变形的问题 */
select {
  -webkit-appearance: none;
  appearance: none;
}
</style>