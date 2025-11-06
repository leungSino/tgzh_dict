<template>
  <Modal
    :title="form._id ? '编辑翻译词条' : '新增翻译词条'"
    @close="$emit('close')"
  >
    <form @submit.prevent="saveWord" class="space-y-4">
      <!-- 塔吉克语 -->
      <div class="relative">
        <input
          type="text"
          v-model="form.tg"
          @input="onInput('tg', form.tg)"
          placeholder="输入塔吉克语单词"
          class="w-full border rounded px-3 py-2"
        />
        <ul
          v-if="suggestions.tg.length"
          class="absolute z-10 bg-white border w-full rounded shadow mt-1 max-h-40 overflow-auto"
        >
          <li
            v-for="s in suggestions.tg"
            :key="s"
            @click="selectSuggestion('tg', s)"
            class="px-3 py-2 hover:bg-blue-100 cursor-pointer"
          >
            {{ s }}
          </li>
        </ul>
      </div>

      <!-- 中文 -->
      <div class="relative">
        <input
          type="text"
          v-model="form.zh"
          @input="onInput('zh', form.zh)"
          placeholder="输入中文翻译"
          class="w-full border rounded px-3 py-2"
        />
        <ul
          v-if="suggestions.zh.length"
          class="absolute z-10 bg-white border w-full rounded shadow mt-1 max-h-40 overflow-auto"
        >
          <li
            v-for="s in suggestions.zh"
            :key="s"
            @click="selectSuggestion('zh', s)"
            class="px-3 py-2 hover:bg-blue-100 cursor-pointer"
          >
            {{ s }}
          </li>
        </ul>
      </div>

      <input v-model="form.en" type="text" placeholder="输入英文翻译" class="w-full border rounded px-3 py-2" />
      <input v-model="form.ru" type="text" placeholder="输入俄语翻译" class="w-full border rounded px-3 py-2" />
      <input v-model="form.tags" type="text" placeholder="标签（用逗号分隔）" class="w-full border rounded px-3 py-2" />
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
import api from '@/api/api.js'
import Modal from '@/components/Modal.vue'

const props = defineProps({ editingWord: Object })
const emit = defineEmits(['close', 'saved'])

const form = ref({
  _id: props.editingWord?._id || null,
  tg: props.editingWord?.tg || '',
  zh: props.editingWord?.zh || '',
  en: props.editingWord?.en || '',
  ru: props.editingWord?.ru || '',
  tags: props.editingWord?.tags?.join(', ') || ''
})

const suggestions = ref({ tg: [], zh: [] })
let debounceTimer = null

function onInput(lang, query) {
  clearTimeout(debounceTimer)
  if (!query.trim()) {
    suggestions.value[lang] = []
    return
  }
  debounceTimer = setTimeout(async () => {
    const res = await api.searchWords(query, lang)
    suggestions.value[lang] = res.data.map(i => i.word)
  }, 300)
}

function selectSuggestion(lang, word) {
  form.value[lang] = word
  suggestions.value[lang] = []
}

async function saveWord() {
  if (form.value._id) await api.updateWord(form.value._id, form.value)
  else await api.addWord(form.value)
  emit('saved')
  emit('close')
}
</script>
