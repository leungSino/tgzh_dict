<template>
  <Modal
    :title="form._id ? '编辑翻译词条' : '新增翻译词条'"
    @close="$emit('close')"
  >
    <form @submit.prevent="saveWord" class="space-y-4">

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

      <!-- 原文 -->
      <div class="flex flex-col mb-4 relative">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">原文</label>
        <div class="flex items-center">
          <input
            type="text"
            v-model="form.sourceText"
            @blur="checkSourceExists"
            placeholder="输入原文（失焦时检查条目是否已存在）"
            class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"
          />
          <span v-if="checkingSource" class="ml-3 text-sm text-gray-500">检查中…</span>
          <span v-else-if="sourceExists === true" class="ml-3 text-sm text-green-600 dark:text-green-400">已有条目</span>
          <span v-else-if="sourceExists === false && form.sourceText.trim()" class="ml-3 text-sm text-orange-600 dark:text-orange-400">未找到</span>
        </div>
      </div>

      <!-- lemma -->
      <div class="flex flex-col mb-4 relative">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">原型词（lemma）</label>
        <input
          type="text"
          v-model="form.lemma"
          @input="onInputLemma(form.lemma)"
          placeholder="输入原型词以搜索联想"
          class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"
        />
        <ul
          v-if="lemmaSuggestions.length"
          class="absolute z-10 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 w-full rounded shadow mt-1 max-h-40 overflow-auto"
        >
          <li
            v-for="s in lemmaSuggestions"
            :key="s._id"
            @click="selectLemma(s)"
            class="px-3 py-2 hover:bg-blue-100 dark:hover:bg-blue-700 cursor-pointer"
          >
            {{ s.lemma }}
          </li>
        </ul>
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
          <option value="archived">存档</option>
        </select>
      </div>

      <!-- 多条翻译 -->
      <div
        v-for="(t, index) in form.translations"
        :key="t.key"
        @click="selectedTranslationIndex = index"
        :class="[
          'border rounded p-3 space-y-3 transition-colors cursor-pointer',
          selectedTranslationIndex === index
            ? 'bg-blue-100 dark:bg-blue-800 border-blue-500'
            : 'bg-gray-50 dark:bg-gray-800 border-gray-300 dark:border-gray-600'
        ]"
      >
        <div class="flex justify-between items-center">
          <span class="font-semibold">翻译 {{ index + 1 }}</span>
          <button type="button" @click.stop="removeTranslation(index)" class="text-red-500 hover:text-red-700">&times;</button>
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

        <!-- 搜索文本（searchTexts） -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">
            搜索匹配词（searchTexts）
          </label>
          <input
            v-model="t.searchTextsText"
            placeholder="多个词请用中文逗号或英文逗号分隔，例如：快, 快的, 迅速"
            class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"
          />
          <p class="text-xs text-gray-500 mt-1">
            用于中文 → 其他语言反查，例如输入“快的”“迅速”“速度快”等都能命中。
          </p>
        </div>

        <!-- 词性选择 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">词性</label>
          <PosSelector v-model="t.posArray" class="w-full" placeholder="请选择词性" />
        </div>

        <!-- 源语言释义 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">
            {{ getLangLabel(form.sourceLang) }} 释义
          </label>
          <input
            v-model="t.definition.source"
            :placeholder="getLangLabel(form.sourceLang) + '释义'"
            class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"
          />
        </div>

        <!-- 目标语言释义 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">
            {{ getLangLabel(form.targetLang) }} 释义
          </label>
          <input
            v-model="t.definition.target"
            :placeholder="getLangLabel(form.targetLang) + '释义'"
            class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"
          />
        </div>

        <!-- 源语言例句 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">
            {{ getLangLabel(form.sourceLang) }} 例句
          </label>
          <textarea
            v-model="t.context.source"
            :placeholder="getLangLabel(form.sourceLang) + '例句'"
            class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"
          ></textarea>
        </div>

        <!-- 目标语言例句 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">
            {{ getLangLabel(form.targetLang) }} 例句
          </label>
          <textarea
            v-model="t.context.target"
            :placeholder="getLangLabel(form.targetLang) + '例句'"
            class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"
          ></textarea>
        </div>
      </div>

      <!-- 添加按钮 -->
      <button
        type="button"
        @click="addTranslation"
        class="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700 mt-3"
      >
        ➕ 添加翻译
      </button>
    </form>

    <template #footer>
      <button type="submit" @click="saveWord" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
        保存
      </button>
      <button type="button" @click="$emit('close')" class="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500">
        取消
      </button>
    </template>
  </Modal>
</template>

<script setup>
import { ref, watch } from 'vue'
import Modal from '@/components/Modal.vue'
import LangSelector from '@/components/LangSelector.vue'
import PosSelector from '@/components/PosSelector.vue'
import { useUserStore } from '@/store/userStore.js'
import api from '@/api/api.js'

const props = defineProps({ editingWord: Object })
const emit = defineEmits(['close', 'saved'])
const user = useUserStore()
const selectedTranslationIndex = ref(null)

const form = ref({
  _id: props.editingWord?._id || null,
  sourceLang: props.editingWord?.sourceLang || '',
  targetLang: props.editingWord?.targetLang || '',
  sourceText: props.editingWord?.sourceText || '',
  lemma: props.editingWord?.lemma || '',
  lemma_id: props.editingWord?.lemma_id || null,
  root: props.editingWord?.root || '',
  description: props.editingWord?.description || '',
  status: props.editingWord?.status || 'draft',

  /* 读取 translations */
  translations: props.editingWord?.translations
    ? Object.entries(props.editingWord.translations).map(([key, val]) => ({
        key: key || crypto.randomUUID(),
        translation: val.translation || '',

        // searchTexts 解析
        searchTexts: Array.isArray(val.searchTexts) ? val.searchTexts : [],
        searchTextsText: Array.isArray(val.searchTexts)
          ? val.searchTexts.join(', ')
          : '',

        posArray: val.posArray || [],
        definition: val.definition || { source: '', target: '' },
        context: val.context || { source: '', target: '' }
      }))
    : []
})

const lemmaSuggestions = ref([])
let debounceTimer = null
const sourceExists = ref(null)
const checkingSource = ref(false)

function getLangLabel(code) {
  const map = { zh: '中文', en: '英文', tg: '塔吉克语', ru: '俄语' }
  return map[code] || code || '语言'
}

function onInputLemma(query) {
  clearTimeout(debounceTimer)
  if (!query?.trim()) return (lemmaSuggestions.value = [])
  debounceTimer = setTimeout(async () => {
    try {
      const res = await api.searchLemmas(query)
      lemmaSuggestions.value = res.data || []
    } catch {
      lemmaSuggestions.value = []
    }
  }, 250)
}

function selectLemma(lemma) {
  form.value.lemma = lemma.lemma
  form.value.lemma_id = lemma._id
  form.value.root = lemma.root || ''
  form.value.description = lemma.description || ''
  lemmaSuggestions.value = []
}

async function checkSourceExists() {
  const txt = form.value.sourceText.trim()
  if (!txt) return
  checkingSource.value = true
  try {
    const res = await api.findBySourceText(txt)
    sourceExists.value = !!res.data
  } finally {
    checkingSource.value = false
  }
}

function addTranslation() {
  form.value.translations.push({
    key: crypto.randomUUID(),
    translation: '',
    searchTexts: [],
    searchTextsText: '',
    posArray: [],
    definition: { source: '', target: '' },
    context: { source: '', target: '' }
  })
}

function removeTranslation(index) {
  form.value.translations.splice(index, 1)
}

/** 监听语言切换，清空 translations 对应字段 **/
watch(
  () => [form.value.sourceLang, form.value.targetLang],
  ([newSource, newTarget], [oldSource, oldTarget]) => {
    if (newSource !== oldSource || newTarget !== oldTarget) {
      form.value.translations.forEach(t => {
        t.definition.source = ''
        t.definition.target = ''
        t.context.source = ''
        t.context.target = ''
      })
    }
  }
)

async function saveWord() {
  // 保存前先把 searchTextsText 拆成数组去重清洗
  for (const t of form.value.translations) {
    t.searchTexts = Array.from(
      new Set(
        (t.searchTextsText || '')
          .split(/[,，;；、/\s]+/)
          .map(s => s.trim())
          .filter(Boolean)
      )
    )
  }

  const payload = {
    ...form.value,
    translations: form.value.translations.reduce((acc, t) => {
      acc[t.key] = t
      return acc
    }, {})
  }

  if (form.value._id) await api.updateWord(form.value._id, payload)
  else await api.addWord(payload)

  emit('saved')
  emit('close')
}
</script>
