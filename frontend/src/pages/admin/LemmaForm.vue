<template>
  <Modal
    :title="form._id ? '编辑原型词' : '新增原型词'"
    @close="$emit('close')"
  >
    <form @submit.prevent="saveLemma" class="space-y-6">

      <!-- 原型词 -->
      <div class="relative">
        <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">原型词</label>
        <input
          type="text"
          v-model="form.lemma"
          @input="onInput(form.lemma)"
          placeholder="输入原型词（如 навиштан）"
          class="w-full border rounded-md px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <ul
          v-if="suggestions.length"
          class="absolute z-20 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 w-full rounded-md shadow-lg mt-1 max-h-44 overflow-auto"
        >
          <li
            v-for="s in suggestions"
            :key="s"
            @click="selectSuggestion(s)"
            class="px-3 py-2 hover:bg-blue-100 dark:hover:bg-blue-700 cursor-pointer"
          >
            {{ s }}
          </li>
        </ul>
      </div>

      <!-- 词根 -->
      <div>
        <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">词根</label>
        <input
          v-model="form.root"
          type="text"
          placeholder="词根"
          class="w-full border rounded-md px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <!-- 是否根词 -->
      <div class="flex items-center space-x-2">
        <input type="checkbox" v-model="form.isRoot" class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500"/>
        <span class="text-gray-800 dark:text-white">是否根词</span>
      </div>

      <!-- 词性 -->
      <div>
        <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">词性</label>
        <PosSelector v-model="form.posArray" class="w-full"/>
      </div>

      <!-- 释义 -->
      <div class="space-y-2">
        <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">中文释义</label>
        <textarea
          v-model="form.definition.zh"
          placeholder="中文释义"
          class="w-full border rounded-md px-3 py-2 h-20 resize-none bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">英文释义</label>
        <textarea
          v-model="form.definition.en"
          placeholder="英文释义"
          class="w-full border rounded-md px-3 py-2 h-20 resize-none bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <!-- 示例句 -->
      <div>
        <label class="block mb-2 font-semibold text-gray-800 dark:text-white">示例句</label>
        <div v-for="(ex, index) in form.examples" :key="ex.key" class="flex gap-2 mb-2">
          <input
            v-model="ex.tg"
            placeholder="塔语句"
            class="flex-1 border rounded-md px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <input
            v-model="ex.zh"
            placeholder="中文翻译"
            class="flex-1 border rounded-md px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="button"
            @click="removeExample(index)"
            class="bg-red-500 text-white px-3 rounded-md hover:bg-red-600"
          >
            删除
          </button>
        </div>
        <button
          type="button"
          @click="addExample"
          class="bg-green-600 text-white px-3 py-1 rounded-md hover:bg-green-700"
        >
          ➕ 添加示例句
        </button>
      </div>

      <!-- 派生词 -->
      <div>
        <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">派生词</label>
        <input
          v-model="form.derivedStr"
          type="text"
          placeholder="派生词（用逗号分隔）"
          class="w-full border rounded-md px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <!-- 反义词 -->
      <div>
        <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">反义词</label>
        <input
          v-model="form.relatedStr"
          type="text"
          placeholder="反义词（用逗号分隔）"
          class="w-full border rounded-md px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

    </form>

    <template #footer>
      <div class="flex justify-end gap-3">
        <button
          type="button"
          @click="saveLemma"
          class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
        >
          保存
        </button>
        <button
          type="button"
          @click="$emit('close')"
          class="bg-gray-400 text-white px-4 py-2 rounded-md hover:bg-gray-500"
        >
          取消
        </button>
      </div>
    </template>
  </Modal>
</template>

<script setup>
import { ref } from 'vue'
import Modal from '@/components/Modal.vue'
import PosSelector from '@/components/PosSelector.vue'
import api from '@/api/api.js'

const props = defineProps({ editingLemma: Object })
const emit = defineEmits(['close', 'saved'])

const form = ref({
  _id: props.editingLemma?._id || null,
  lemma: props.editingLemma?.lemma || '',
  root: props.editingLemma?.root || '',
  isRoot: props.editingLemma?.isRoot || false,
  posArray: props.editingLemma?.pos || [],
  definition: {
    zh: props.editingLemma?.definition?.zh || '',
    en: props.editingLemma?.definition?.en || ''
  },
  examples: props.editingLemma?.examples?.map(e => ({ ...e, key: crypto.randomUUID() })) || [],
  derivedStr: (props.editingLemma?.derived || []).join(', '),
  relatedStr: (props.editingLemma?.related || []).join(', ')
})

const suggestions = ref([])
let debounceTimer = null

function onInput(query) {
  clearTimeout(debounceTimer)
  if (!query.trim()) {
    suggestions.value = []
    return
  }
  debounceTimer = setTimeout(async () => {
    const res = await api.searchLemmas(query)
    suggestions.value = res.data.map(i => i.lemma)
  }, 300)
}

function selectSuggestion(word) {
  form.value.lemma = word
  suggestions.value = []
}

function addExample() {
  form.value.examples.push({ tg: '', zh: '', key: crypto.randomUUID() })
}
function removeExample(index) {
  form.value.examples.splice(index, 1)
}

async function saveLemma() {
  const payload = {
    _id: form.value._id,
    lemma: form.value.lemma,
    root: form.value.root,
    isRoot: form.value.isRoot,
    pos: form.value.posArray,
    definition: { ...form.value.definition },
    examples: form.value.examples.filter(e => e.tg && e.zh).map(({tg, zh}) => ({tg, zh})),
    derived: form.value.derivedStr.split(',').map(s => s.trim()).filter(Boolean),
    related: form.value.relatedStr.split(',').map(s => s.trim()).filter(Boolean)
  }

  if (form.value._id) await api.updateLemma(form.value._id, payload)
  else await api.addLemma(payload)

  emit('saved')
  emit('close')
}
</script>
