<template>
  <Modal
    :title="form._id ? '编辑翻译词条' : '新增翻译词条'"
    @close="$emit('close')"
    class="translation-form-modal"
  >
    <!-- 只保留外部滚动容器 -->
    <form @submit.prevent="saveWord" class="space-y-4 max-h-[70vh] overflow-y-auto px-1">

      <!-- 将语言选择器改为网格布局 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- 源语言 -->
        <div class="flex flex-col mb-4">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">源语言</label>
          <LangSelector v-model="form.sourceLang" class="w-full" />
        </div>

        <!-- 目标语言 -->
        <div class="flex flex-col mb-4">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">目标语言</label>
          <LangSelector v-model="form.targetLang" class="w-full" />
        </div>
      </div>

      <!-- 原文 -->
      <div class="flex flex-col mb-4 relative">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">原文</label>
        <div class="flex items-center relative w-full">
          <input
            type="text"
            v-model="form.sourceText"
            @blur="checkSourceExists"
            :class="[
              'w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white',
              sourceTextExists === true
                ? 'border-red-500 dark:border-red-400'
                : sourceTextExists === false && form.sourceText.trim() && !checkingSourceText
                  ? 'border-green-500 dark:border-green-400'
                  : 'border-gray-300 dark:border-gray-600'
            ]"
            placeholder="输入原文"
          />

          <!-- 右侧绿色对勾 -->
          <span
            v-if="!sourceTextExists && form.sourceText.trim() && !checkingSourceText"
            class="absolute right-2 top-1/2 -translate-y-1/2 text-green-600 dark:text-green-400 font-bold"
          >✔</span>

          <!-- 检查中 -->
          <span v-if="checkingSourceText" class="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-gray-500">检查中…</span>
        </div>

        <!-- 红色提示 -->
        <p v-if="sourceTextExists" class="text-red-600 dark:text-red-400 text-sm mt-1">
          已有该条目
        </p>
      </div>

      <!-- 是否原型词 -->
      <div class="flex items-center space-x-2">
        <input
          type="checkbox"
          v-model="form.isLemma"
          class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
        />
        <span class="text-gray-800 dark:text-white">是否原型词</span>
      </div>

      <!-- 将原型词和词根改为网格布局 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- 原型词 lemma -->
        <div class="flex flex-col mb-4 relative">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">原型词（lemma）</label>
          <div class="relative">
            <input
              ref="lemmaInputRef"
              type="text"
              v-model="form.lemma"
              @input="onInputLemma(form.lemma)"
              @focus="onLemmaFocus"
              @blur="onLemmaBlur"
              @keydown="onLemmaKeydown"
              placeholder="输入原型词以搜索联想"
              class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
            />

            <!-- 加载指示器 -->
            <div
              v-if="lemmaLoading"
              class="absolute right-2 top-1/2 -translate-y-1/2"
            >
              <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500"></div>
            </div>

            <!-- 清空按钮 -->
            <button
              v-if="form.lemma && !lemmaLoading"
              @click="clearLemma"
              class="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
            >
              ×
            </button>
          </div>

          <!-- 下拉框 -->
          <div
            v-if="showLemmaDropdown && lemmaSuggestions.length"
            ref="lemmaDropdownRef"
            class="absolute z-50 w-full mt-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md shadow-lg max-h-60 overflow-auto"
            style="top: 100%;"
          >
            <div
              v-for="(s, index) in lemmaSuggestions"
              :key="s._id"
              @mousedown="selectLemma(s)"
              :class="[
                'px-3 py-2 cursor-pointer border-b border-gray-100 dark:border-gray-700 last:border-b-0 transition-colors',
                index === highlightedLemmaIndex
                  ? 'bg-blue-100 dark:bg-blue-700 text-blue-800 dark:text-blue-200'
                  : 'hover:bg-gray-50 dark:hover:bg-gray-700'
              ]"
            >
              <div class="font-medium text-gray-900 dark:text-white">{{ s.lemma }}</div>
              <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                ID: {{ s._id }}
              </div>
            </div>
          </div>

          <!-- 无结果提示 -->
          <div
            v-if="showLemmaDropdown && !lemmaLoading && lemmaSuggestions.length === 0 && form.lemma.trim()"
            class="absolute z-50 w-full mt-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md shadow-lg"
            style="top: 100%;"
          >
            <div class="px-3 py-4 text-gray-500 dark:text-gray-400 text-sm text-center">
              未找到匹配的原型词
            </div>
          </div>
        </div>

        <!-- 词根 -->
        <div class="flex flex-col mb-4">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">词根</label>
          <input
            v-model="form.root"
            type="text"
            placeholder="词根"
            class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"
          />
        </div>
      </div>

      <!-- 将描述和状态改为网格布局 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- 描述 -->
        <div class="flex flex-col mb-4">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">描述（释义、语法、说明）</label>
          <textarea
            v-model="form.description"
            placeholder="描述（释义、语法、说明）"
            class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"
          />
        </div>

        <!-- 状态 -->
        <div class="flex flex-col mb-4">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">状态</label>
          <select
            v-model="form.status"
            class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"
          >
            <option value="draft">草稿</option>
            <option value="published">发布</option>
            <option value="archarchived">存档</option>
          </select>
        </div>
      </div>

      <!-- 多条翻译 -->
      <!-- 移除翻译区域内部的滚动条，只保留外部滚动 -->
      <div>
        <div
          v-for="(t, index) in form.translations"
          :key="t.key"
          :class="[
            'border rounded p-3 space-y-3 transition-colors cursor-pointer mb-4',
            selectedTranslationIndex === t.key
              ? 'bg-blue-100 dark:bg-blue-800 border-blue-500'
              : 'bg-gray-50 dark:bg-gray-800 border-gray-300 dark:border-gray-600'
          ]"
          @click="selectedTranslationIndex = t.key"
        >
          <div class="flex justify-between items-center">
            <span class="font-semibold">翻译 {{ index + 1 }}</span>
            <button type="button" @click.stop="removeTranslationEx(index)" class="text-red-500 hover:text-red-700">&times;</button>
          </div>

          <!-- 翻译文本 -->
          <div class="flex flex-col">
            <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">翻译文本</label>
            <input
              v-model="t.translation"
              placeholder="翻译文本"
              class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"
            />
          </div>

          <!-- 搜索文本 -->
          <div class="flex flex-col">
            <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">搜索匹配词</label>
            <input
              v-model="t.searchTextsText"
              placeholder="多个词用逗号分隔"
              class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"
            />
          </div>

          <!-- 词性 -->
          <div class="flex flex-col">
            <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">词性</label>
            <PosSelector v-model="t.posArray" class="w-full" placeholder="请选择词性" />
          </div>

          <!-- 源语言释义 & 例句 -->
          <div v-for="lang of [form.sourceLang, form.targetLang]" :key="lang">
            <div class="mb-2">
              <label class="mb-1 text-sm">{{ getLangLabel(lang) }}释义</label>
              <input
                v-model="t.definition[lang === form.sourceLang ? 'source' : 'target']"
                :placeholder="getLangLabel(lang) + '释义'"
                class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white"
              />
            </div>
            <div>
              <label class="mb">
                {{ getLangLabel(lang) }}例句
              </label>
              <textarea
                v-model="t.context[lang === form.sourceLang ? 'source' : 'target']"
                :placeholder="getLangLabel(lang) + '例句'"
                class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- 添加翻译 -->
      <button type="button" @click="addTranslationEx" class="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700">
        ➕ 添加翻译
      </button>
    </form>

    <template #footer>
      <button type="submit" @click="saveWord" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700" :disabled="sourceTextExists || checkingSourceText">
        保存
      </button>
      <button type="button" @click="$emit('close')" class="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500">取消</button>
    </template>
  </Modal>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
import Modal from '@/components/Modal.vue'
import LangSelector from '@/components/LangSelector.vue'
import PosSelector from '@/components/PosSelector.vue'
import api from '@/api/api.js'
import { useUserStore } from '@/store/userStore.js'

const props = defineProps({ editingTranslation: Object })
const emit = defineEmits(['close', 'saved'])

const userStore = useUserStore()

const selectedTranslationIndex = ref(null)

function generateUniqueId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2, 9)
}

const form = ref({
  _id: props.editingTranslation?._id || null,
  sourceLang: props.editingTranslation?.sourceLang || '',
  targetLang: props.editingTranslation?.targetLang || '',
  sourceText: props.editingTranslation?.sourceText || '',
  isLemma: props.editingTranslation?.isLemma || false,
  lemma: props.editingTranslation?.lemma || '',
  lemma_id: props.editingTranslation?.lemma_id || null,
  root: props.editingTranslation?.root || '',
  description: props.editingTranslation?.description || '',
  status: props.editingTranslation?.status || 'draft',
  created_by: props.editingTranslation?.created_by || '',
  updated_by: props.editingTranslation?.updated_by || '',
  translations: props.editingTranslation?.translations
    ? props.editingTranslation.translations.map(t => ({
        key: t.key || generateUniqueId(),
        translation: t.translation || '',
        searchTexts: t.searchTexts || [],
        searchTextsText: (t.searchTexts || []).join(', '),
        posArray: t.posArray || [],
        definition: t.definition || { source: '', target: '' },
        context: t.context || { source: '', target: '' }
      }))
    : []
})

/*
|--------------------------------------------------------------------------
|    ★ 核心逻辑：检查 sourceText 是否被占用
|--------------------------------------------------------------------------
| 后端返回: { exists: true/false, source_text_id: "xxx" }
| 逻辑：
|   1. 编辑模式下，如果返回 source_text_id === 当前 _id → 不算冲突
|   2. 新增模式 或 返回 source_text_id ≠ 当前 _id → 视为冲突
*/
const sourceTextExists = ref(false)
const checkingSourceText = ref(false)

async function checkSourceExists() {
  const txt = form.value.sourceText.trim()
  if (!txt) {
    sourceTextExists.value = false
    return
  }

  checkingSourceText.value = true
  try {
    const res = await api.checkSourceTextExists(txt)
    const exists = !!res.data.exists
    const foundId = res.data.source_text_id || null

    if (!exists) {
      // 未被占用
      sourceTextExists.value = false
    } else {
      // 已存在
      if (form.value._id && foundId === form.value._id) {
        // 编辑模式：自己就是自己 → 不算重复
        sourceTextExists.value = false
      } else {
        // 新增模式 或 编辑时撞到别的词条
        sourceTextExists.value = true
      }
    }
  } catch (err) {
    console.error('检查 sourceText 出错:', err)
    sourceTextExists.value = false
  } finally {
    checkingSourceText.value = false
  }
}

/*
|--------------------------------------------------------------------------
| 保存逻辑：若冲突（sourceTextExists=true），则禁止提交
|--------------------------------------------------------------------------
*/
async function saveWord() {
  if (sourceTextExists.value || checkingSourceText.value) {
    alert('原文已存在，无法保存')
    return
  }

  // 处理 searchTexts
  form.value.translations.forEach(t => {
    t.searchTexts = Array.from(
      new Set(
        (t.searchTextsText || '')
          .split(/[,，;；、/\s]+/)
          .map(s => s.trim())
          .filter(Boolean)
      )
    )
  })

  const payload = {
    ...form.value,
    updated_by: userStore.username || 'system',
    translations: form.value.translations.map(t => ({
      key: t.key,
      translation: t.translation,
      searchTexts: t.searchTexts,
      posArray: t.posArray,
      definition: t.definition,
      context: t.context
    }))
  }

  try {
    if (!form.value._id) {
      payload.created_by = userStore.username || 'system'
      await api.addTranslation(payload)
    } else {
      await api.updateTranslation(form.value._id, payload)
    }

    emit('saved')
    emit('close')
  } catch (err) {
    console.error('保存失败:', err)
    alert('保存失败: ' + (err?.response?.data?.detail || err?.message))
  }
}

function addTranslationEx() {
  const newEx = {
    key: generateUniqueId(),
    translation:'',
    searchTexts:'',
    posArray:[],
    definition:{},
    context:{}
  }
  form.value.translations.push(newEx)
  selectedTranslationIndex.value = newEx.key
}

function removeTranslationEx(index) {
  const removed = form.value.translations.splice(index,1)
  if(selectedTranslationIndex.value===removed[0]?.key) selectedTranslationIndex.value=null
}


/*
|--------------------------------------------------------------------------
| Lemma 下拉选择相关逻辑 - 根据实际API响应调整
|--------------------------------------------------------------------------
*/
const lemmaSuggestions = ref([])
const lemmaLoading = ref(false)
const showLemmaDropdown = ref(false)
const highlightedLemmaIndex = ref(-1)
let debounceTimer = null
const lemmaInputRef = ref(null)
const lemmaDropdownRef = ref(null)

// 监听键盘事件
function onLemmaKeydown(event) {
  if (!showLemmaDropdown.value || !lemmaSuggestions.value.length) return

  switch (event.key) {
    case 'ArrowDown':
      event.preventDefault()
      highlightedLemmaIndex.value =
        highlightedLemmaIndex.value < lemmaSuggestions.value.length - 1
          ? highlightedLemmaIndex.value + 1
          : 0
      scrollToHighlightedItem()
      break
    case 'ArrowUp':
      event.preventDefault()
      highlightedLemmaIndex.value =
        highlightedLemmaIndex.value > 0
          ? highlightedLemmaIndex.value - 1
          : lemmaSuggestions.value.length - 1
      scrollToHighlightedItem()
      break
    case 'Enter':
      event.preventDefault()
      if (highlightedLemmaIndex.value >= 0) {
        selectLemma(lemmaSuggestions.value[highlightedLemmaIndex.value])
      } else if (lemmaSuggestions.value.length > 0) {
        // 如果没有高亮项但有结果，选择第一个
        selectLemma(lemmaSuggestions.value[0])
      }
      break
    case 'Escape':
      hideLemmaDropdown()
      break
    case 'Tab':
      // Tab 键时如果有高亮项就选择
      if (highlightedLemmaIndex.value >= 0 && !event.shiftKey) {
        event.preventDefault()
        selectLemma(lemmaSuggestions.value[highlightedLemmaIndex.value])
      }
      break
  }
}

// 滚动到高亮项
function scrollToHighlightedItem() {
  nextTick(() => {
    const dropdown = lemmaDropdownRef.value
    const items = dropdown?.querySelectorAll('div[class*="px-3"]')
    if (items && items[highlightedLemmaIndex.value]) {
      items[highlightedLemmaIndex.value].scrollIntoView({
        block: 'nearest',
        behavior: 'smooth'
      })
    }
  })
}

// 输入处理 - 简化版
function onInputLemma(query) {
  clearTimeout(debounceTimer)
  highlightedLemmaIndex.value = -1

  const trimmedQuery = query?.trim()
  if (!trimmedQuery) {
    lemmaSuggestions.value = []
    hideLemmaDropdown()
    return
  }

  if (trimmedQuery.length < 2) {
    lemmaSuggestions.value = []
    hideLemmaDropdown()
    return
  }

  lemmaLoading.value = true
  showLemmaDropdown.value = true

  debounceTimer = setTimeout(async () => {
    try {
      const res = await api.searchLemmas(trimmedQuery)

      // 直接使用返回的数组
      lemmaSuggestions.value = res || []

      if (lemmaSuggestions.value.length > 0) {
        highlightedLemmaIndex.value = 0
        await nextTick()
        scrollToHighlightedItem()
      }
    } catch (err) {
      console.error('搜索 lemma 失败:', err)
      lemmaSuggestions.value = []
    } finally {
      lemmaLoading.value = false
    }
  }, 350)
}

// 输入框获得焦点
function onLemmaFocus() {
  if (lemmaSuggestions.value.length > 0 && form.value.lemma.trim()) {
    showLemmaDropdown.value = true
  } else if (form.value.lemma.trim().length >= 2) {
    // 如果输入框有内容且长度足够，重新搜索
    onInputLemma(form.value.lemma)
  }
}

// 输入框失去焦点
function onLemmaBlur() {
  // 延迟隐藏下拉框，以便点击选项能正常触发
  setTimeout(() => {
    hideLemmaDropdown()
  }, 150)
}

// 选择 lemma
function selectLemma(lemma) {
  form.value.lemma = lemma.lemma
  form.value.lemma_id = lemma._id
  // 根据您的API，如果没有root和description字段，可以注释掉下面两行
  // form.value.root = lemma.root || ''
  // form.value.description = lemma.description || ''
  hideLemmaDropdown()

  // 让输入框保持焦点
  nextTick(() => {
    lemmaInputRef.value?.focus()
  })
}

// 清空 lemma
function clearLemma() {
  form.value.lemma = ''
  form.value.lemma_id = null
  form.value.root = ''
  form.value.description = ''
  lemmaSuggestions.value = []
  hideLemmaDropdown()
  lemmaInputRef.value?.focus()
}

// 隐藏下拉框
function hideLemmaDropdown() {
  showLemmaDropdown.value = false
  highlightedLemmaIndex.value = -1
}

// 窗口变化时重新定位下拉框
function handleWindowChange() {
  if (showLemmaDropdown.value && lemmaSuggestions.value.length) {
    nextTick(() => {
      const input = lemmaInputRef.value
      const dropdown = lemmaDropdownRef.value
      if (input && dropdown) {
        const rect = input.getBoundingClientRect()
        dropdown.style.width = rect.width + 'px'
        dropdown.style.left = '0px'
      }
    })
  }
}

// 添加键盘事件监听
onMounted(() => {
  window.addEventListener('resize', handleWindowChange)
  window.addEventListener('scroll', handleWindowChange, true)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleWindowChange)
  window.removeEventListener('scroll', handleWindowChange, true)
  clearTimeout(debounceTimer)
})

/*
|--------------------------------------------------------------------------
| 工具函数：语言名称
|--------------------------------------------------------------------------
*/
function getLangLabel(code) {
  const map = { zh: '中文', en: '英文', tg: '塔吉克语', ru: '俄语' }
  return map[code] || code || '语言'
}
</script>

<!-- 修改6：只保留外部滚动条样式 -->
<style scoped>
/* 滚动条样式统一 */
.translation-form-modal :deep(.modal-content) {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e0 #f7fafc;
}

.translation-form-modal :deep(.modal-content)::-webkit-scrollbar {
  width: 6px;
}

.translation-form-modal :deep(.modal-content)::-webkit-scrollbar-track {
  background: #f7fafc;
  border-radius: 3px;
}

.translation-form-modal :deep(.modal-content)::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 3px;
}

.translation-form-modal :deep(.modal-content)::-webkit-scrollbar-thumb:hover {
  background: #a0aec0;
}

/* 移动端优化 */
@media (max-width: 768px) {
  .translation-form-modal :deep(.modal-container) {
    margin: 1rem;
    max-height: calc(100vh - 2rem);
  }
}

/* 暗黑模式滚动条 */
@media (prefers-color-scheme: dark) {
  .translation-form-modal :deep(.modal-content) {
    scrollbar-color: #4a5568 #2d3748;
  }

  .translation-form-modal :deep(.modal-content)::-webkit-scrollbar-track {
    background: #2d3748;
  }

  .translation-form-modal :deep(.modal-content)::-webkit-scrollbar-thumb {
    background: #4a5568;
  }

  .translation-form-modal :deep(.modal-content)::-webkit-scrollbar-thumb:hover {
    background: #718096;
  }
}
</style>