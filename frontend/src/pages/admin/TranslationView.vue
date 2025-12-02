<template>
  <Modal
    title="查看翻译词条"
    @close="$emit('close')"
  >
    <div class="space-y-4">
      <!-- 基本信息网格布局 -->
      <div class="grid grid-cols-2 gap-4 mb-4">
        <!-- 源语言 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">源语言</label>
          <div class="border rounded px-3 py-2 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600">
            {{ getLangLabel(form.sourceLang) }}
          </div>
        </div>

        <!-- 目标语言 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">目标语言</label>
          <div class="border rounded px-3 py-2 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600">
            {{ getLangLabel(form.targetLang) }}
          </div>
        </div>
      </div>

      <!-- 原文 -->
      <div class="flex flex-col mb-4">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">原文</label>
        <div class="border rounded px-3 py-2 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600">
          {{ form.sourceText }}
        </div>
      </div>

      <!-- 是否原型词 -->
      <div class="flex flex-col">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">词类</label>
        <div class="py-2 px-3 border rounded bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white">
          {{ form.isLemma ? '原型词' : '非原型词' }}
        </div>
      </div>

      <!-- 原型词和词根 -->
      <div class="grid grid-cols-2 gap-4 mb-4">
        <!-- lemma -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">原型词（lemma）</label>
          <div class="border rounded px-3 py-2 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600">
            {{ form.lemma || '-' }}
          </div>
        </div>

        <!-- 词根 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">词根</label>
          <div class="border rounded px-3 py-2 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600">
            {{ form.root || '-' }}
          </div>
        </div>
      </div>

      <!-- 描述 -->
      <div class="flex flex-col mb-4">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">描述（释义、语法、说明）</label>
        <div class="border rounded px-3 py-2 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600 min-h-[80px]">
          {{ form.description || '-' }}
        </div>
      </div>

      <!-- 状态和创建信息 -->
      <div class="grid grid-cols-2 gap-4 mb-4">
        <!-- 状态 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">状态</label>
          <div class="border rounded px-3 py-2 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600">
            {{ getStatusLabel(form.status) }}
          </div>
        </div>

        <!-- 创建者 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">创建者</label>
          <div class="border rounded px-3 py-2 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600">
            {{ form.created_by || '-' }}
          </div>
        </div>
      </div>

      <!-- 多条翻译 -->
      <div class="space-y-4">
        <h3 class="text-lg font-medium text-gray-900 dark:text-white">翻译内容</h3>

        <div
          v-for="(t, index) in form.translations"
          :key="t.key"
          class="border rounded p-4 space-y-4 bg-gray-50 dark:bg-gray-800 border-gray-300 dark:border-gray-600"
        >
          <div class="flex justify-between items-center pb-2 border-b border-gray-200 dark:border-gray-700">
            <span class="font-semibold text-gray-900 dark:text-white">翻译 {{ index + 1 }}</span>
          </div>

          <!-- 翻译文本 -->
          <div class="flex flex-col">
            <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">翻译文本</label>
            <div class="border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600">
              {{ t.translation || '-' }}
            </div>
          </div>

          <!-- 搜索文本 -->
          <div class="flex flex-col">
            <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">搜索匹配词</label>
            <div class="border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600">
              {{ t.searchTexts?.join(', ') || '-' }}
            </div>
          </div>

          <!-- 词性 -->
          <div class="flex flex-col">
            <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">词性</label>
            <div class="flex flex-wrap gap-2 p-2 border rounded bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600">
              <span v-if="!t.posArray?.length" class="text-gray-400 text-sm">-</span>
              <span
                v-for="pos in t.posArray"
                :key="pos"
                class="px-2 py-1 bg-blue-100 dark:bg-blue-800 text-blue-800 dark:text-blue-200 rounded text-sm"
              >
                {{ pos }}
              </span>
            </div>
          </div>

          <!-- 释义和例句 -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- 源语言 -->
            <div class="space-y-3">
              <h4 class="font-medium text-gray-900 dark:text-white">{{ getLangLabel(form.sourceLang) }}</h4>

              <div class="flex flex-col">
                <label class="mb-1 text-sm text-gray-600 dark:text-gray-400">释义</label>
                <div class="border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600">
                  {{ t.definition?.source || '-' }}
                </div>
              </div>

              <div class="flex flex-col">
                <label class="mb-1 text-sm text-gray-600 dark:text-gray-400">例句</label>
                <div class="border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600 min-h-[60px]">
                  {{ t.context?.source || '-' }}
                </div>
              </div>
            </div>

            <!-- 目标语言 -->
            <div class="space-y-3">
              <h4 class="font-medium text-gray-900 dark:text-white">{{ getLangLabel(form.targetLang) }}</h4>

              <div class="flex flex-col">
                <label class="mb-1 text-sm text-gray-600 dark:text-gray-400">释义</label>
                <div class="border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600">
                  {{ t.definition?.target || '-' }}
                </div>
              </div>

              <div class="flex flex-col">
                <label class="mb-1 text-sm text-gray-600 dark:text-gray-400">例句</label>
                <div class="border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600 min-h-[60px]">
                  {{ t.context?.target || '-' }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <button
        type="button"
        @click="$emit('close')"
        class="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500 transition-colors"
      >
        关闭
      </button>
    </template>
  </Modal>
</template>

<script setup>
import { ref, watch } from 'vue'
import Modal from '@/components/Modal.vue'

const props = defineProps({ viewingWord: Object })
const emit = defineEmits(['close'])

// 表单数据
const form = ref({
  _id: null,
  sourceLang: '',
  targetLang: '',
  sourceText: '',
  isLemma: false,
  lemma: '',
  lemma_id: null,
  root: '',
  description: '',
  status: 'draft',
  created_by: '',
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
      isLemma: newWord.isLemma || false,
      lemma: newWord.lemma || '',
      lemma_id: newWord.lemma_id || null,
      root: newWord.root || '',
      description: newWord.description || '',
      status: newWord.status || 'draft',
      created_by: newWord.created_by || '',
      translations: Array.isArray(newWord.translations)
        ? newWord.translations.map((t, index) => ({
            key: t.key || `translation-${index}`,
            translation: t.translation || '',
            searchTexts: Array.isArray(t.searchTexts) ? t.searchTexts : [],
            posArray: Array.isArray(t.posArray) ? t.posArray : [],
            definition: t.definition || { source: '', target: '' },
            context: t.context || { source: '', target: '' }
          }))
        : []
    }
  },
  { immediate: true }
)

// 工具函数
function getLangLabel(code) {
  const map = { zh: '中文', en: '英文', tg: '塔吉克语', ru: '俄语' }
  return map[code] || code || '未知语言'
}

function getStatusLabel(status) {
  const map = {
    draft: '草稿',
    published: '发布',
    archived: '存档'
  }
  return map[status] || status
}
</script>