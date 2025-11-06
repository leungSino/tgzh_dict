<template>
  <Modal
    :title="form._id ? '编辑翻译词条' : '新增翻译词条'"
    @close="$emit('close')"
  >
    <form @submit.prevent="saveWord" class="space-y-4">

      <!-- 源语言 -->
      <div class="flex flex-col mb-4">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">源语言</label>
        <LangSelector
          v-model="form.sourceLang"
          class="w-full"
        />
      </div>

      <!-- 目标语言 -->
      <div class="flex flex-col mb-4">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">目标语言</label>
        <LangSelector
          v-model="form.targetLang"
          class="w-full"
        />
      </div>

      <!-- 原文 -->
      <div class="flex flex-col mb-4 relative">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">原文</label>
        <input
          type="text"
          v-model="form.sourceText"
          @input="onInputLemma(form.sourceText)"
          placeholder="输入原文"
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
          class="w-full border rounded px-3 py-2 h-24 resize-none bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"
        />
      </div>

      <!-- 多条翻译 -->
      <div v-for="(t, index) in form.translations" :key="t.key" class="border rounded p-3 space-y-3 bg-gray-50 dark:bg-gray-800 transition-colors">

        <div class="flex justify-between items-center">
          <span class="font-semibold">翻译 {{ index + 1 }}</span>
          <button type="button" @click="removeTranslation(index)" class="text-red-500 hover:text-red-700">&times;</button>
        </div>

        <!-- 翻译文本 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">翻译文本</label>
          <input v-model="t.translation" placeholder="翻译文本" class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600" />
        </div>

        <!-- 词性选择 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">词性</label>
          <PosSelector
            v-model="t.posArray"
            class="w-full"
            placeholder="请选择词性"
          />
        </div>

        <!-- 中文释义 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">中文释义</label>
          <input v-model="t.definition.zh" placeholder="中文释义" class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600" />
        </div>

        <!-- 英文释义 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">英文释义</label>
          <input v-model="t.definition.en" placeholder="英文释义" class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600" />
        </div>

        <!-- 塔吉克语例句 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">塔吉克语例句</label>
          <textarea v-model="t.context.tg" placeholder="塔吉克语例句" class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"></textarea>
        </div>

        <!-- 中文例句 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">中文例句</label>
          <textarea v-model="t.context.zh" placeholder="中文例句" class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"></textarea>
        </div>

      </div>

      <button type="button" @click="addTranslation" class="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700">
        ➕ 添加翻译
      </button>

    </form>

    <template #footer>
      <button type="submit" @click="saveWord" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
        保存
      </button>
      <button
        type="button"
        @click="$emit('close')"
        class="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500"
      >
        取消
      </button>
    </template>
  </Modal>
</template>

<script setup>
import { ref } from 'vue'
import Modal from '@/components/Modal.vue'
import LangSelector from '@/components/LangSelector.vue'
import PosSelector from '@/components/PosSelector.vue'
import api from '@/api/api.js'

const props = defineProps({ editingWord: Object })
const emit = defineEmits(['close', 'saved'])

// 表单结构初始化
const form = ref({
  _id: props.editingWord?._id || null,
  sourceLang: props.editingWord?.sourceLang || '',
  targetLang: props.editingWord?.targetLang || '',
  sourceText: props.editingWord?.sourceText || '',
  lemma: props.editingWord?.lemma || '',
  lemma_id: props.editingWord?.lemma_id || null,
  root: props.editingWord?.root || '',
  description: props.editingWord?.description || '',
  translations: props.editingWord?.translations
    ? Object.entries(props.editingWord.translations).map(([key, val]) => ({
        key: key || crypto.randomUUID(),
        translation: val.translation || '',
        posArray: val.pos || [],
        definition: val.definition || { zh: '', en: '' },
        context: val.context || { tg: '', zh: '' }
      }))
    : []
})

// ✅ 词性选择：自动补全、输入提示
const lemmaSuggestions = ref([])
let debounceTimer = null

function onInputLemma(query) {
  clearTimeout(debounceTimer)
  if (!query.trim()) {
    lemmaSuggestions.value = []
    return
  }
  debounceTimer = setTimeout(async () => {
    const res = await api.searchLemmas(query)
    lemmaSuggestions.value = res.data
  }, 300)
}

function selectLemma(lemma) {
  form.value.lemma = lemma.lemma
  form.value.lemma_id = lemma._id
  form.value.root = lemma.root || ''
  form.value.description = lemma.description || ''
  lemmaSuggestions.value = []
}

// ✅ 动态增删翻译
function addTranslation() {
  form.value.translations = [
    ...form.value.translations,
    {
      key: crypto.randomUUID(),
      translation: '',
      posArray: [],
      definition: { zh: '', en: '' },
      context: { tg: '', zh: '' }
    }
  ]
}

function removeTranslation(index) {
  form.value.translations = form.value.translations.filter((_, i) => i !== index)
}

// ✅ 保存逻辑
async function saveWord() {
  const payload = {
    _id: form.value._id,
    sourceLang: form.value.sourceLang,
    targetLang: form.value.targetLang,
    sourceText: form.value.sourceText,
    lemma: form.value.lemma,
    lemma_id: form.value.lemma_id,
    root: form.value.root,
    description: form.value.description,
    translations: form.value.translations.reduce((acc, t) => {
      acc[t.key] = {
        translation: t.translation,
        pos: t.posArray,
        definition: t.definition,
        context: t.context
      }
      return acc
    }, {})
  }

  if (form.value._id) await api.updateWord(form.value._id, payload)
  else await api.addWord(payload)

  emit('saved')
  emit('close')
}
</script>
