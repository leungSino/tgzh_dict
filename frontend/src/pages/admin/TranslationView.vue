<template>
  <Modal
    title="查看翻译词条"
    @close="$emit('close')"
  >
    <form class="space-y-4">
      <!-- 源语言 -->
      <div class="flex flex-col mb-4">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">源语言</label>
        <LangSelector v-model="form.sourceLang" class="w-full" :disabled="true" />
      </div>

      <!-- 目标语言 -->
      <div class="flex flex-col mb-4">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">目标语言</label>
        <LangSelector v-model="form.targetLang" class="w-full" :disabled="true" />
      </div>

      <!-- 原文 -->
      <div class="flex flex-col mb-4">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">原文</label>
        <input
          type="text"
          v-model="form.sourceText"
          class="w-full border rounded px-3 py-2 bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600"
          readonly
        />
      </div>

      <!-- lemma -->
      <div class="flex flex-col mb-4">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">原型词（lemma）</label>
        <input
          type="text"
          v-model="form.lemma"
          class="w-full border rounded px-3 py-2 bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600"
          readonly
        />
      </div>

      <!-- 词根 -->
      <div class="flex flex-col mb-4">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">词根</label>
        <input
          v-model="form.root"
          type="text"
          class="w-full border rounded px-3 py-2 bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600"
          readonly
        />
      </div>

      <!-- 描述 -->
      <div class="flex flex-col mb-4">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">描述（释义、语法、说明）</label>
        <textarea
          v-model="form.description"
          class="w-full border rounded px-3 py-2 bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600"
          readonly
        ></textarea>
      </div>

      <!-- 状态 -->
      <div class="flex flex-col mb-4">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">状态</label>
        <input
          type="text"
          v-model="form.status"
          class="w-full border rounded px-3 py-2 bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600"
          readonly
        />
      </div>

      <!-- 多条翻译 -->
      <div
        v-for="(t, index) in form.translations"
        :key="t.key || `translation-${index}`"
        class="border rounded p-3 space-y-3 bg-gray-50 dark:bg-gray-800 border-gray-300 dark:border-gray-600"
      >
        <div class="font-semibold">翻译 {{ index + 1 }}</div>

        <!-- 翻译文本 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">翻译文本</label>
          <input
            v-model="t.translation"
            class="w-full border rounded px-3 py-2 bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600"
            readonly
          />
        </div>

        <!-- 搜索文本 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">搜索匹配词（searchTexts）</label>
          <input
            v-model="t.searchTextsText"
            class="w-full border rounded px-3 py-2 bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600"
            readonly
          />
        </div>

        <!-- 词性 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">词性</label>
          <PosSelector v-model="t.posArray" class="w-full" :disabled="true" />
        </div>

        <!-- 源语言释义 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">{{ getLangLabel(form.sourceLang) }} 释义</label>
          <input
            v-model="t.definition.source"
            class="w-full border rounded px-3 py-2 bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600"
            readonly
          />
        </div>

        <!-- 目标语言释义 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">{{ getLangLabel(form.targetLang) }} 释义</label>
          <input
            v-model="t.definition.target"
            class="w-full border rounded px-3 py-2 bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600"
            readonly
          />
        </div>

        <!-- 源语言例句 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">{{ getLangLabel(form.sourceLang) }} 例句</label>
          <textarea
            v-model="t.context.source"
            class="w-full border rounded px-3 py-2 bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600"
            readonly
          ></textarea>
        </div>

        <!-- 目标语言例句 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">{{ getLangLabel(form.targetLang) }} 例句</label>
          <textarea
            v-model="t.context.target"
            class="w-full border rounded px-3 py-2 bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600"
            readonly
          ></textarea>
        </div>
      </div>
    </form>

    <template #footer>
      <button type="button" @click="$emit('close')" class="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500">
        关闭
      </button>
    </template>
  </Modal>
</template>

<script setup>
import { ref, watch } from 'vue'
import Modal from '@/components/Modal.vue'
import LangSelector from '@/components/LangSelector.vue'
import PosSelector from '@/components/PosSelector.vue'

const props = defineProps({ viewingWord: Object })
const emit = defineEmits(['close'])

const form = ref({
  _id: null,
  sourceLang: '',
  targetLang: '',
  sourceText: '',
  lemma: '',
  lemma_id: null,
  root: '',
  description: '',
  status: 'draft',
  translations: []
})

// 响应父组件变化
watch(
  () => props.viewingWord,
  (newWord) => {
    if (!newWord) return
    form.value = {
      _id: newWord._id || null,
      sourceLang: newWord.sourceLang || '',
      targetLang: newWord.targetLang || '',
      sourceText: newWord.sourceText || '',
      lemma: newWord.lemma || '',
      lemma_id: newWord.lemma_id || null,
      root: newWord.root || '',
      description: newWord.description || '',
      status: newWord.status || 'draft',
      translations: newWord.translations
        ? Object.entries(newWord.translations).map(([key, val], index) => ({
            key: key || `translation-${index}`,
            translation: val.translation || '',
            searchTexts: Array.isArray(val.searchTexts) ? val.searchTexts : [],
            searchTextsText: Array.isArray(val.searchTexts) ? val.searchTexts.join(', ') : '',
            posArray: val.posArray || [],
            definition: val.definition || { source: '', target: '' },
            context: val.context || { source: '', target: '' }
          }))
        : []
    }
  },
  { immediate: true }
)

function getLangLabel(code) {
  const map = { zh: '中文', en: '英文', tg: '塔吉克语', ru: '俄语' }
  return map[code] || code || '语言'
}
</script>
