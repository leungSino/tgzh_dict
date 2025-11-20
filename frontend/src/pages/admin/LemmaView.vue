<template>
  <Modal
    :title="viewingLemma.lemma + '（查看）'"
    @close="$emit('close')"
  >
    <div class="space-y-6">
      <!-- 基本信息网格 -->
      <div class="grid grid-cols-2 gap-4 mb-4">
        <!-- 语言 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">源语言</label>
          <div class="py-2 px-3 border rounded bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white">
            {{ langLabel[form.language] }}
          </div>
        </div>

        <!-- 是否根词 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">词类</label>
          <div class="py-2 px-3 border rounded bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white">
            {{ form.isRoot ? '词根' : '非词根' }}
          </div>
        </div>
      </div>

      <!-- 原型词和词根 -->
      <div class="grid grid-cols-2 gap-4">
        <!-- 原型词 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">原型词</label>
          <div class="py-2 px-3 border rounded bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white">
            {{ form.lemma || '-' }}
          </div>
        </div>

        <!-- 词根 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">词根</label>
          <div class="py-2 px-3 border rounded bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white">
            {{ form.root || '-' }}
          </div>
        </div>
      </div>

      <!-- 词性 -->
      <div class="flex flex-col">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">词性</label>
        <div class="flex flex-wrap gap-2 p-3 border rounded bg-gray-100 dark:bg-gray-700 border-gray-300 dark:border-gray-600">
          <span v-if="!form.posArray.length" class="text-gray-400">-</span>
          <span
            v-for="pos in form.posArray"
            :key="pos"
            class="px-2 py-1 bg-blue-100 dark:bg-blue-800 text-blue-800 dark:text-blue-200 rounded text-sm"
          >
            {{ pos }}
          </span>
        </div>
      </div>

      <!-- 释义（多语言） -->
      <div class="space-y-3">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">释义（多语言）</label>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div
            v-for="lang in otherLangs"
            :key="lang"
            class="border rounded p-3 bg-gray-50 dark:bg-gray-800"
          >
            <label class="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
              {{ getDefinitionLabel(lang) }}
            </label>
            <div class="text-gray-900 dark:text-white">
              {{ form.definitions?.[lang] || '-' }}
            </div>
          </div>
        </div>
      </div>

      <!-- 动词变位 -->
      <div class="border rounded p-4 bg-gray-50 dark:bg-gray-800">
        <label class="block mb-3 text-sm font-medium text-gray-700 dark:text-gray-300">动词变位</label>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div
            v-for="tense in Object.keys(form.conjugations)"
            :key="tense"
            class="border rounded p-3 bg-white dark:bg-gray-700"
          >
            <label class="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
              {{ tenseLabels[tense] }}
            </label>
            <div class="text-gray-900 dark:text-white text-sm">
              {{ Array.isArray(form.conjugations[tense]) ? form.conjugations[tense].join(', ') : '-' }}
            </div>
          </div>
        </div>
      </div>

      <!-- 示例句 -->
      <div class="border rounded p-4 bg-gray-50 dark:bg-gray-800">
        <label class="block mb-3 text-sm font-medium text-gray-700 dark:text-gray-300">示例句</label>
        <div class="space-y-4">
          <div
            v-for="(ex, index) in form.examples"
            :key="ex._id || index"
            class="border rounded p-4 space-y-3 bg-white dark:bg-gray-700"
          >
            <div class="font-semibold text-gray-800 dark:text-gray-100 border-b pb-2">
              示例 {{ index + 1 }}
            </div>

            <!-- 多语言示例 -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div
                v-for="lng in ALL_LANGS"
                :key="lng"
                class="space-y-1"
              >
                <label class="block text-sm text-gray-600 dark:text-gray-400">
                  {{ langLabel[lng] }}示例
                </label>
                <div class="text-gray-900 dark:text-white text-sm p-2 bg-gray-100 dark:bg-gray-600 rounded">
                  {{ ex[lng] || '-' }}
                </div>
              </div>
            </div>

            <!-- 示例词性 -->
            <div class="pt-2">
              <label class="block mb-2 text-sm text-gray-600 dark:text-gray-400">词性</label>
              <div class="flex flex-wrap gap-2">
                <span v-if="!ex.pos?.length" class="text-gray-400 text-sm">-</span>
                <span
                  v-for="pos in ex.pos"
                  :key="pos"
                  class="px-2 py-1 bg-green-100 dark:bg-green-800 text-green-800 dark:text-green-200 rounded text-sm"
                >
                  {{ pos }}
                </span>
              </div>
            </div>
          </div>

          <div v-if="!form.examples.length" class="text-center text-gray-400 py-4">
            暂无示例句
          </div>
        </div>
      </div>

      <!-- 派生词和相关词 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- 派生词 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">派生词</label>
          <div class="py-2 px-3 border rounded bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white">
            {{ form.derivedStr || '-' }}
          </div>
        </div>

        <!-- 相关或反义词 -->
        <div class="flex flex-col">
          <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">相关或反义词</label>
          <div class="py-2 px-3 border rounded bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white">
            {{ form.relatedStr || '-' }}
          </div>
        </div>
      </div>

      <!-- 状态 -->
      <div class="flex flex-col">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">状态</label>
        <div class="py-2 px-3 border rounded bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white">
          {{ getStatusLabel(form.status) }}
        </div>
      </div>
    </div>

    <template #footer>
      <div class="flex justify-end">
        <button
          type="button"
          @click="$emit('close')"
          class="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500 transition-colors"
        >
          关闭
        </button>
      </div>
    </template>
  </Modal>
</template>

<script setup>
import { computed } from 'vue'
import Modal from '@/components/Modal.vue'

const props = defineProps({ viewingLemma: Object })
const emit = defineEmits(['close'])

const ALL_LANGS = ['tg', 'zh', 'ru', 'en']
const langLabel = { tg: "塔吉克语", zh: "中文", ru: "俄语", en: "英文" }
const tenseLabels = { past: '过去式', present: '现在式', future: '将来式' }

const form = computed(() => ({
  _id: props.viewingLemma?._id || null,
  language: props.viewingLemma?.language || 'tg',
  lemma: props.viewingLemma?.lemma || '',
  root: props.viewingLemma?.root || '',
  isRoot: props.viewingLemma?.isRoot || false,
  posArray: props.viewingLemma?.pos || [],
  definitions: props.viewingLemma?.definitions || { tg: '', zh: '', ru: '', en: '' },
  conjugations: props.viewingLemma?.conjugations || { past: [], present: [], future: [] },
  examples: props.viewingLemma?.examples?.map(e => ({ ...e, pos: e.pos || [] })) || [],
  derivedStr: (props.viewingLemma?.derived || []).join(', ') || '-',
  relatedStr: (props.viewingLemma?.related || []).join(', ') || '-',
  status: props.viewingLemma?.status || 'draft'
}))

const otherLangs = computed(() => ALL_LANGS.filter(l => l !== form.value.language))

function getDefinitionLabel(lang) {
  return {
    tg: "塔语释义",
    zh: "中文释义",
    ru: "俄语释义",
    en: "英文释义"
  }[lang] || (lang + " 释义")
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