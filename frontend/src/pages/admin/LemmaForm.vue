<template>
  <Modal
    :title="form._id ? '编辑原型词' : '新增原型词'"
    @close="$emit('close')"
  >
    <form @submit.prevent="saveLemma" class="space-y-6">
      <!-- 语言种类 -->
      <div class="flex flex-col mb-4">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">源语言</label>
        <LangSelector v-model="form.language" class="w-full" />
      </div>
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
          placeholder="词根（如 навис）"
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

      <!-- 释义（多语言） - 自动根据源语言隐藏对应项 -->
      <div class="space-y-3">
        <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">释义（多语言）</label>

        <div v-for="lang in otherLangs" :key="lang">
          <input
            v-model="form.definitions[lang]"
            :placeholder="langLabel[lang] + '释义'"
            class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"
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
              placeholder="以逗号分隔多个变位，如 навиштам, навиштӣ, навишт ..."
              class="w-full border rounded-md px-3 py-2 h-16 resize-none bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-blue-500"
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
          :class="[
            'border rounded p-3 space-y-3 transition-all cursor-pointer',
            selectedExample === ex.key
              ? 'bg-blue-50 dark:bg-blue-900 border-blue-500'
              : 'bg-gray-50 dark:bg-gray-800 border-gray-300 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700'
          ]"
          @click="selectedExample = ex.key"
        >
          <div class="flex justify-between items-center">
            <span class="font-semibold text-gray-800 dark:text-gray-100">示例 {{ index + 1 }}</span>
            <button
              type="button"
              @click.stop="removeExample(index)"
              class="text-red-500 hover:text-red-700 text-lg"
            >
              ×
            </button>
          </div>

          <!-- 塔吉克语 -->
          <textarea v-model="ex.tg" placeholder="塔吉克语例句" class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"/>
          <!-- 中文 -->
          <textarea v-model="ex.zh" placeholder="中文例句" class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"/>
          <!-- 俄语 -->
          <textarea v-model="ex.ru" placeholder="俄语例句" class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"/>
          <!-- 英语 -->
          <textarea v-model="ex.en" placeholder="英文例句" class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"/>
          <!-- 词性 -->
          <div>
            <label class="block mb-1 text-sm text-gray-700 dark:text-gray-300">词性</label>
            <PosSelector v-model="ex.pos" class="w-full"/>
          </div>
        </div>

        <button type="button" @click="addExample" class="mt-3 bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700">
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
          class="w-full border rounded-md px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <!-- 相关/反义词 -->
      <div>
        <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">相关或反义词</label>
        <input
          v-model="form.relatedStr"
          type="text"
          placeholder="如 хондан, фаҳмидан ..."
          class="w-full border rounded-md px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <!-- 状态 -->
      <div>
        <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">状态</label>
        <select
          v-model="form.status"
          class="w-full border rounded-md px-3 py-2 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-blue-500"
        >
          <option value="draft">草稿</option>
          <option value="published">已发布</option>
          <option value="archived">存档</option>
        </select>
      </div>

    </form>

    <template #footer>
      <div class="flex justify-end gap-3">
        <button type="button" @click="saveLemma" class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">保存</button>
        <button type="button" @click="$emit('close')" class="bg-gray-400 text-white px-4 py-2 rounded-md hover:bg-gray-500">取消</button>
      </div>
    </template>
  </Modal>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import Modal from '@/components/Modal.vue'
import PosSelector from '@/components/PosSelector.vue'
import LangSelector from '@/components/LangSelector.vue'
import api from '@/api/api.js'

const props = defineProps({ editingLemma: Object })
const emit = defineEmits(['close', 'saved'])

// 语言标签
const langLabel = { tg: "塔吉克语", zh: "中文", ru: "俄语", en: "英文" }

// 自动计算除当前语言以外的三种
const otherLangs = computed(() =>
  ["tg", "zh", "ru", "en"].filter(l => l !== form.value.language)
)

const form = ref({
  _id: props.editingLemma?._id || null,
  language: props.editingLemma?.language || 'tg',
  lemma: props.editingLemma?.lemma || '',
  root: props.editingLemma?.root || '',
  isRoot: props.editingLemma?.isRoot || false,
  posArray: props.editingLemma?.pos || [],
  definitions: props.editingLemma?.definitions || { tg:'', zh:'', ru:'', en:'' },
  conjugations: props.editingLemma?.conjugations || { past: [], present: [], future: [] },
  examples: props.editingLemma?.examples?.map(e => ({ ...e, key: crypto.randomUUID(), pos: e.pos || [] })) || [],
  derivedStr: (props.editingLemma?.derived || []).join(', '),
  relatedStr: (props.editingLemma?.related || []).join(', '),
  status: props.editingLemma?.status || 'draft'
})

/* ------------------------------------
   自动根据语言调整 definitions（核心逻辑）
------------------------------------ */
watch(
  () => form.value.language,
  (newLang) => {
    const others = ["tg", "zh", "ru", "en"].filter(l => l !== newLang)

    // 语言修改时清空 definitions，只保留其他三种语言
    form.value.definitions = Object.fromEntries(
      others.map(l => [l, ""])
    )
  },
  { immediate: true }
)

const tenseLabels = { past: '过去式', present: '现在式', future: '将来式' }
function tenseStr(t) { return t }

const suggestions = ref([])
let debounceTimer = null
function onInput(query){
  clearTimeout(debounceTimer)
  if(!query.trim()){ suggestions.value=[]; return }
  debounceTimer = setTimeout(async ()=>{
    const res = await api.searchLemmas(query)
    suggestions.value = res.data.map(i=>i.lemma)
  },300)
}
function selectSuggestion(word){ form.value.lemma=word; suggestions.value=[] }

const selectedExample = ref(null)
function addExample(){
  const newEx = { tg:'', zh:'', ru:'', en:'', pos:[], key: crypto.randomUUID() }
  form.value.examples.push(newEx)
  selectedExample.value = newEx.key
}
function removeExample(index){
  const removed = form.value.examples.splice(index,1)
  if(selectedExample.value===removed[0]?.key) selectedExample.value=null
}

async function saveLemma(){
  const payload = {
    _id: form.value._id,
    language: form.value.language,
    lemma: form.value.lemma,
    root: form.value.root,
    isRoot: form.value.isRoot,
    pos: form.value.posArray,
    definitions: form.value.definitions,
    conjugations: Object.fromEntries(
      Object.entries(form.value.conjugations).map(([t,v])=>[t,v.toString().split(',').map(s=>s.trim()).filter(Boolean)])
    ),
    examples: form.value.examples.filter(e=>e.tg && e.zh).map(({tg, zh, ru, en, pos})=>({tg, zh, ru, en, pos})),
    derived: form.value.derivedStr.split(',').map(s=>s.trim()).filter(Boolean),
    related: form.value.relatedStr.split(',').map(s=>s.trim()).filter(Boolean),
    status: form.value.status
  }

  if(form.value._id) await api.updateLemma(form.value._id, payload)
  else await api.addLemma(payload)

  emit('saved')
  emit('close')
}
</script>

