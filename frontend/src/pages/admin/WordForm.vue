<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="bg-white dark:bg-gray-900 w-[800px] rounded-xl shadow-lg p-6 relative">
      <button @click="$emit('close')" class="absolute top-3 right-3 text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 text-2xl font-bold">×</button>

      <h3 class="text-xl font-semibold mb-4 text-blue-600">{{ editingWord ? '编辑词汇' : '新增词汇' }}</h3>

      <div class="space-y-6 max-h-[70vh] overflow-y-auto pr-1">
        <div v-for="lang in langs" :key="lang.key" class="border rounded-lg p-4 dark:border-gray-700">
          <h4 class="font-semibold mb-2">{{ lang.label }}</h4>
          <input v-model="form.lang_entries[lang.key].word" :placeholder="`${lang.label} 单词`" class="border rounded px-3 py-2 w-full mb-2 dark:bg-gray-800" />
          <textarea v-model="form.lang_entries[lang.key].definition" :placeholder="`${lang.label} 含义`" class="border rounded px-3 py-2 w-full mb-2 dark:bg-gray-800" />
          <input v-model="examplesInput[lang.key]" placeholder="示例句（逗号分隔）" class="border rounded px-3 py-2 w-full dark:bg-gray-800" />
        </div>

        <div>
          <label class="font-semibold">标签：</label>
          <input v-model="tagsInput" placeholder="如 verb,common" class="border rounded px-3 py-2 w-full dark:bg-gray-800" />
        </div>

        <div class="flex justify-end gap-3 mt-4">
          <button class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400" @click="$emit('close')">取消</button>
          <button class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700" @click="save">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, watch } from 'vue'
import api from '@/api/api.js'

const props = defineProps({ editingWord: Object })
const emit = defineEmits(['close', 'saved'])

const langs = [
  { key: 'zh', label: '中文' },
  { key: 'tg', label: '塔吉克语' },
  { key: 'ru', label: '俄语' },
  { key: 'en', label: '英语' }
]

const form = reactive({
  lang_entries: {
    zh: { word: '', definition: '', examples: [] },
    tg: { word: '', definition: '', examples: [] },
    ru: { word: '', definition: '', examples: [] },
    en: { word: '', definition: '', examples: [] }
  },
  tags: []
})

const examplesInput = reactive({ zh: '', tg: '', ru: '', en: '' })
const tagsInput = ref('')

watch(
  () => props.editingWord,
  (newVal) => {
    if (newVal) {
      langs.forEach(lang => {
        form.lang_entries[lang.key].word = newVal.lang_entries[lang.key]?.word || ''
        form.lang_entries[lang.key].definition = newVal.lang_entries[lang.key]?.definition || ''
        examplesInput[lang.key] = (newVal.lang_entries[lang.key]?.examples || []).map(e => e.sentence).join(', ')
      })
      tagsInput.value = Array.isArray(newVal.tags) ? newVal.tags.join(',') : newVal.tags || ''
    } else {
      langs.forEach(lang => {
        form.lang_entries[lang.key].word = ''
        form.lang_entries[lang.key].definition = ''
        examplesInput[lang.key] = ''
      })
      tagsInput.value = ''
    }
  },
  { immediate: true }
)

async function save() {
  langs.forEach(lang => {
    form.lang_entries[lang.key].examples = examplesInput[lang.key]
      .split(',')
      .map(s => ({ sentence: s.trim(), translation: '' }))
      .filter(Boolean)
  })
  form.tags = tagsInput.value.split(',').map(s => s.trim()).filter(Boolean)

  if (props.editingWord?.id) {
    await api.updateWord(props.editingWord.id, form)
  } else {
    await api.addWord(form)
  }

  emit('saved')
  emit('close')
}
</script>
