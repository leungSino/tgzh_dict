<template>
  <Modal
    :title="form._id ? '编辑原型词' : '新增原型词'"
    @close="$emit('close')"
  >
    <form @submit.prevent="saveLemma" class="space-y-4">
      <div class="relative">
        <input
          type="text"
          v-model="form.lemma"
          @input="onInput(form.lemma)"
          placeholder="输入原型词（如 навиштан）"
          class="w-full border rounded px-3 py-2"
        />
        <ul
          v-if="suggestions.length"
          class="absolute z-10 bg-white border w-full rounded shadow mt-1 max-h-40 overflow-auto"
        >
          <li
            v-for="s in suggestions"
            :key="s"
            @click="selectSuggestion(s)"
            class="px-3 py-2 hover:bg-blue-100 cursor-pointer"
          >
            {{ s }}
          </li>
        </ul>
      </div>

      <input v-model="form.root" type="text" placeholder="词根" class="w-full border rounded px-3 py-2" />
      <textarea
        v-model="form.description"
        placeholder="描述（释义、语法、说明）"
        class="w-full border rounded px-3 py-2 h-24 resize-none"
      />
    </form>

    <!-- footer slot 必须在 Modal 外面使用 -->
    <template #footer>
      <button type="button" @click="saveLemma" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
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
import api from '@/api/api.js'

const props = defineProps({ modelValue: Boolean, editingLemma: Object })
const emit = defineEmits(['update:modelValue', 'saved'])

const form = ref({
  _id: props.editingLemma?._id || null,
  lemma: props.editingLemma?.lemma || '',
  root: props.editingLemma?.root || '',
  description: props.editingLemma?.description || ''
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

async function saveLemma() {
  if (form.value._id) await api.updateLemma(form.value._id, form.value)
  else await api.addLemma(form.value)
  emit('saved')
  emit('close')
}
</script>
