<template>
  <Modal
    title="查看原型词"
    @close="$emit('close')"
  >
    <form class="space-y-6">
      <!-- 语言种类 -->
      <div class="flex flex-col mb-4">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">源语言</label>
        <LangSelector v-model="form.language" class="w-full" :disabled="true" />
      </div>

      <!-- 原型词 -->
      <div class="relative">
        <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">原型词</label>
        <input
          type="text"
          v-model="form.lemma"
          readonly
          class="w-full border rounded-md px-3 py-2 bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600"
        />
      </div>

      <!-- 词根 -->
      <div>
        <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">词根</label>
        <input
          v-model="form.root"
          type="text"
          readonly
          class="w-full border rounded-md px-3 py-2 bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600"
        />
      </div>

      <!-- 是否根词 -->
      <div class="flex items-center space-x-2">
        <input type="checkbox" v-model="form.isRoot" disabled class="w-4 h-4" />
        <span class="text-gray-800 dark:text-white">是否根词</span>
      </div>

      <!-- 词性 -->
      <div>
        <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">词性</label>
        <PosSelector v-model="form.posArray" class="w-full" :disabled="true"/>
      </div>

      <!-- 释义（多语言） -->
      <div class="space-y-3">
        <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">释义（多语言）</label>
        <div v-for="lang in otherLangs" :key="lang">
          <input
            v-model="form.definitions[lang]"
            readonly
            :placeholder="langLabel[lang] + '释义'"
            class="w-full border rounded px-3 py-2 bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600"
          />
        </div>
      </div>

      <!-- 动词变位 -->
      <div>
        <label class="block mb-2 font-semibold text-gray-800 dark:text-white">动词变位</label>
        <div class="space-y-3">
          <div v-for="(forms, tense) in form.conjugations" :key="tense">
            <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">
              {{ tenseLabels[tense] }}
            </label>
            <textarea
              v-model="form.conjugations[tenseStr(tense)]"
              readonly
              class="w-full border rounded-md px-3 py-2 h-16 resize-none bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600"
            />
          </div>
        </div>
      </div>

      <!-- 示例句 -->
      <div>
        <label class="block mb-2 font-semibold text-gray-800 dark:text-white">示例句</label>
        <div
          v-for="(ex, index) in form.examples"
          :key="ex.key"
          class="border rounded p-3 space-y-3 bg-gray-50 dark:bg-gray-800 border-gray-300 dark:border-gray-600"
        >
          <div class="flex justify-between items-center">
            <span class="font-semibold text-gray-800 dark:text-gray-100">示例 {{ index + 1 }}</span>
          </div>

          <textarea v-model="ex.tg" placeholder="塔吉克语例句" readonly class="w-full border rounded px-3 py-2 bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600"/>
          <textarea v-model="ex.zh" placeholder="中文例句" readonly class="w-full border rounded px-3 py-2 bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600"/>
          <textarea v-model="ex.ru" placeholder="俄语例句" readonly class="w-full border rounded px-3 py-2 bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600"/>
          <textarea v-model="ex.en" placeholder="英文例句" readonly class="w-full border rounded px-3 py-2 bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600"/>
          <div>
            <label class="block mb-1 text-sm text-gray-700 dark:text-gray-300">词性</label>
            <PosSelector v-model="ex.pos" class="w-full" :disabled="true"/>
          </div>
        </div>
      </div>

      <!-- 派生词 -->
      <div>
        <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">派生词</label>
        <input v-model="form.derivedStr" type="text" readonly class="w-full border rounded-md px-3 py-2 bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600"/>
      </div>

      <!-- 相关/反义词 -->
      <div>
        <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">相关或反义词</label>
        <input v-model="form.relatedStr" type="text" readonly class="w-full border rounded-md px-3 py-2 bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600"/>
      </div>

      <!-- 状态 -->
      <div>
        <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">状态</label>
        <input v-model="form.status" type="text" readonly class="w-full border rounded-md px-3 py-2 bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600"/>
      </div>
    </form>

    <template #footer>
      <div class="flex justify-end">
        <button type="button" @click="$emit('close')" class="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500">
          关闭
        </button>
      </div>
    </template>
  </Modal>
</template>

<script setup>
import { ref, computed } from 'vue'
import Modal from '@/components/Modal.vue'
import PosSelector from '@/components/PosSelector.vue'
import LangSelector from '@/components/LangSelector.vue'

const props = defineProps({ viewingLemma: Object })
const emit = defineEmits(['close'])

const langLabel = { tg: "塔吉克语", zh: "中文", ru: "俄语", en: "英文" }

const form = ref({
  _id: props.viewingLemma?._id || null,
  language: props.viewingLemma?.language || 'tg',
  lemma: props.viewingLemma?.lemma || '',
  root: props.viewingLemma?.root || '',
  isRoot: props.viewingLemma?.isRoot || false,
  posArray: props.viewingLemma?.pos || [],
  definitions: props.viewingLemma?.definitions || { tg:'', zh:'', ru:'', en:'' },
  conjugations: props.viewingLemma?.conjugations || { past: [], present: [], future: [] },
  examples: props.viewingLemma?.examples?.map(e => ({ ...e, key: crypto.randomUUID(), pos: e.pos || [] })) || [],
  derivedStr: (props.viewingLemma?.derived || []).join(', '),
  relatedStr: (props.viewingLemma?.related || []).join(', '),
  status: props.viewingLemma?.status || 'draft'
})

const otherLangs = computed(() =>
  ["tg", "zh", "ru", "en"].filter(l => l !== form.value.language)
)

const tenseLabels = { past: '过去式', present: '现在式', future: '将来式' }
function tenseStr(t) { return t }
</script>
