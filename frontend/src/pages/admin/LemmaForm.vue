<template>
  <!-- 添加modal类名用于样式控制 -->
  <Modal
    :title="form._id ? '编辑原型词' : '新增原型词'"
    @close="$emit('close')"
    class="translation-form-modal"
  >
    <!-- 添加滚动容器 -->
    <form @submit.prevent="saveLemma" class="space-y-6 max-h-[70vh] overflow-y-auto px-1">

      <!-- 语言种类 -->
      <div class="flex flex-col mb-4">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">
          源语言
        </label>
        <LangSelector v-model="form.language" class="w-full" />
      </div>

      <!-- 将原型词和词根改为网格布局 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- 原型词 -->
        <div class="relative">
          <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">
            原型词
          </label>
          <input
            type="text"
            v-model="form.lemma"
            @blur="checkLemmaExists"
            placeholder="输入原型词（如 навиштан）"
            class="w-full border rounded-md px-3 py-2 bg-white dark:bg-gray-700
                   text-gray-800 dark:text-white border-gray-300 dark:border-gray-600
                   focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <span v-if="checkingLemma" class="ml-2 text-sm text-gray-500">检查中…</span>
          <span v-else-if="lemmaExists" class="ml-2 text-sm text-red-600 dark:text-red-400">
            已存在该原型词
          </span>
        </div>

        <!-- 词根 -->
        <div>
          <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">
            词根
          </label>
          <input
            v-model="form.root"
            type="text"
            placeholder="词根（如 навис）"
            class="w-full border rounded-md px-3 py-2 bg-white dark:bg-gray-700
                   text-gray-800 dark:text-white border-gray-300 dark:border-gray-600
                   focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      <!-- 将是否根词和词性改为网格布局 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- 是否根词 -->
        <div class="flex items-center space-x-2">
          <input
            type="checkbox"
            v-model="form.isRoot"
            class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
          />
          <span class="text-gray-800 dark:text-white">是否根词</span>
        </div>

        <!-- 词性 -->
        <div>
          <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">
            词性
          </label>
          <PosSelector v-model="form.posArray" class="w-full" />
        </div>
      </div>

      <!-- 释义 -->
      <div class="space-y-3">
        <label class="block mb-1 text-sm font-semibold text-gray-800 dark:text-gray-300">
          释义
        </label>
        <!-- 将释义改为网格布局 -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div v-for="lang in otherLangs" :key="lang">
            <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">
              {{ langLabel[lang] }} 释义
            </label>
            <input
              v-model="form.definitions[lang]"
              :placeholder="'输入' + langLabel[lang] + '释义'"
              class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700
                     text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"
            />
          </div>
        </div>
      </div>

      <!-- 动词变位 -->
      <div>
        <label class="block mb-2 font-semibold text-gray-800 dark:text-white">
          动词变位
        </label>
        <div class="space-y-3">
          <!-- 将动词变位改为网格布局 -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div v-for="tense in Object.keys(form.conjugations)" :key="tense">
              <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">
                {{ tenseLabels[tense] }}
              </label>
              <textarea
                v-model="form.conjugations[tense]"
                placeholder="以逗号分隔多个变位，如 навиштам, навиштӣ ..."
                class="w-full border rounded-md px-3 py-2 h-16 resize-none bg-white dark:bg-gray-700
                       text-gray-800 dark:text-white border-gray-300 dark:border-gray-600
                       focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- 示例句 -->
      <div>
        <label class="block mb-2 font-semibold text-gray-800 dark:text-white">
          示例句
        </label>
        <div
          v-for="(ex, index) in form.examples"
          :key="ex.key"
          :class="[
            'border rounded p-3 space-y-4 transition-all cursor-pointer mb-4',
            selectedExample === ex.key
              ? 'bg-blue-50 dark:bg-blue-900 border-blue-500'
              : 'bg-gray-50 dark:bg-gray-800 border-gray-300 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700'
          ]"
          @click="selectedExample = ex.key"
        >
          <div class="flex justify-between items-center">
            <span class="font-semibold text-gray-800 dark:text-gray-100">
              示例 {{ index + 1 }}
            </span>
            <button
              type="button"
              @click.stop="removeExample(index)"
              class="text-red-500 hover:text-red-700 text-lg"
            >
              ×
            </button>
          </div>

          <!-- 将四种语言例句改为网格布局 -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-for="lng in ALL_LANGS" :key="lng">
              <label class="block mb-1 text-sm text-gray-700 dark:text-gray-300">
                {{ langLabel[lng] }}例句
              </label>
              <textarea
                v-model="ex[lng]"
                :placeholder="langLabel[lng] + '例句'"
                class="w-full border rounded px-3 py-2 bg-white dark:bg-gray-700
                       text-gray-800 dark:text-white border-gray-300 dark:border-gray-600 min-h-[60px]"
              />
            </div>
          </div>

          <!-- 示例词性 -->
          <div>
            <label class="block mb-1 text-sm text-gray-700 dark:text-gray-300">
              词性
            </label>
            <PosSelector v-model="ex.pos" class="w-full" />
          </div>
        </div>

        <button
          type="button"
          @click="addExample"
          class="mt-3 bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700"
        >
          ➕ 添加示例句
        </button>
      </div>

      <!-- 将派生词和相关词改为网格布局 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- 派生词 -->
        <div>
          <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">
            派生词
          </label>
          <input
            v-model="form.derivedStr"
            type="text"
            placeholder="派生词（用逗号分隔）"
            class="w-full border rounded-md px-3 py-2 bg-white dark:bg-gray-700
                   text-gray-800 dark:text-white border-gray-300 dark:border-gray-600
                   focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <!-- 相关词 -->
        <div>
          <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">
            相关或反义词
          </label>
          <input
            v-model="form.relatedStr"
            type="text"
            placeholder="如 хондан, фаҳмидан ..."
            class="w-full border rounded-md px-3 py-2 bg-white dark:bg-gray-700
                   text-gray-800 dark:text-white border-gray-300 dark:border-gray-600
                   focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      <!-- 状态 -->
      <div>
        <label class="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">
          状态
        </label>
        <select
          v-model="form.status"
          class="w-full border rounded-md px-3 py-2 bg-white dark:bg-gray-700
                 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600
                 focus:ring-2 focus:ring-blue-500"
        >
          <option value="draft">草稿</option>
          <option value="published">已发布</option>
          <option value="archived">存档</option>
        </select>
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
import { ref, watch, computed } from 'vue'
import Modal from '@/components/Modal.vue'
import PosSelector from '@/components/PosSelector.vue'
import LangSelector from '@/components/LangSelector.vue'
import { useUserStore } from '@/store/userStore.js'
import api from '@/api/api.js'

const props = defineProps({ editingLemma: Object })
const emit = defineEmits(['close', 'saved'])
const userStore = useUserStore()

const ALL_LANGS = ['tg', 'zh', 'ru', 'en']
const langLabel = { tg: '塔吉克语', zh: '中文', ru: '俄语', en: '英文' }
const tenseLabels = { past: '过去式', present: '现在式', future: '将来式' }

// 使用时间戳+随机数生成唯一ID
function generateUniqueId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2, 9)
}

const form = ref({
  _id: props.editingLemma?._id || null,
  language: props.editingLemma?.language || 'tg',
  lemma: props.editingLemma?.lemma || '',
  root: props.editingLemma?.root || '',
  isRoot: props.editingLemma?.isRoot || false,
  posArray: props.editingLemma?.pos || [],
  definitions: { tg: '', zh: '', ru: '', en: '', ...(props.editingLemma?.definitions || {}) },
  conjugations: props.editingLemma?.conjugations || { past: [], present: [], future: [] },
  examples: props.editingLemma?.examples?.map(e => ({ ...e, key: generateUniqueId(), pos: e.pos || [] })) || [],
  derivedStr: (props.editingLemma?.derived || []).join(', '),
  relatedStr: (props.editingLemma?.related || []).join(', '),
  status: props.editingLemma?.status || 'draft',
  created_by: '',
  updated_by: ''
})

const selectedExample = ref(null)
const otherLangs = computed(() => ALL_LANGS.filter(l => l !== form.value.language))

// 更新 definitions 时保留已有数据
watch(
  () => form.value.language,
  newLang => {
    for (const l of ALL_LANGS) {
      if (l === newLang) form.value.definitions[l] = ''
      else form.value.definitions[l] = form.value.definitions[l] || ''
    }
  },
  { immediate: true }
)

const lemmaExists = ref(false)
const checkingLemma = ref(false)

async function checkLemmaExists() {
  const txt = form.value.lemma.trim()
  if (!txt) { lemmaExists.value = false; return }

  checkingLemma.value = true
  try {
    const res = await api.checkLemmaExists(txt)
    lemmaExists.value = !!res.data.exists
  } catch (err) {
    console.error('检查 lemma 出错:', err)
    lemmaExists.value = false
  } finally { checkingLemma.value = false }
}

function addExample() {
  const newEx = { tg:'', zh:'', ru:'', en:'', pos:[], key: generateUniqueId() }
  form.value.examples.push(newEx)
  selectedExample.value = newEx.key
}

function removeExample(index) {
  const removed = form.value.examples.splice(index,1)
  if(selectedExample.value===removed[0]?.key) selectedExample.value=null
}

async function saveLemma() {
  if (lemmaExists.value) { alert("已存在该原型词，请修改后再提交"); return }

  const transformedExamples = form.value.examples
    .filter(e => e.tg || e.zh || e.ru || e.en)
    .map(e => ({ tg:e.tg||'', zh:e.zh||'', ru:e.ru||'', en:e.en||'', pos:e.pos||[], key:e.key||null }))

  const transformedConjugations = {}
  Object.keys(form.value.conjugations).forEach(tense => {
    const value = form.value.conjugations[tense]
    transformedConjugations[tense] = typeof value==='string' ? value.split(',').map(s=>s.trim()).filter(Boolean) : value||[]
  })

  const payload = {
    _id: form.value._id,
    language: form.value.language,
    lemma: form.value.lemma.trim(),
    root: form.value.root?.trim() || '',
    isRoot: form.value.isRoot,
    pos: form.value.posArray || [],
    definitions: form.value.definitions,
    conjugations: transformedConjugations,
    examples: transformedExamples,
    derived: form.value.derivedStr.split(',').map(s=>s.trim()).filter(Boolean),
    related: form.value.relatedStr.split(',').map(s=>s.trim()).filter(Boolean),
    status: form.value.status,
    updated_by: userStore.username || 'system'
  }

  try {
    if (!form.value._id){
      payload.created_by = userStore.username || 'system'
      await api.addLemma(payload)
    } else await api.updateLemma(form.value._id, payload)

    emit('saved'); emit('close')
  } catch (error) {
    console.error('保存失败:', error)
    alert('保存失败: ' + (error.response?.data?.detail || '请检查数据格式'))
  }
}
</script>

<!-- 添加相同的滚动条样式 -->
<style scoped>
/* 滚动条样式统一 */
.translation-form-modal :deep(.modal-content) {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e0 #f7fafc;
}

.translation-form-modal :deep(.modal-content)::-webkit-scrollbar {
  width: 6px;
}

.translation-form-modal :deep(.modal-content)::-webkit-scrollbar-track {
  background: #f7fafc;
  border-radius: 3px;
}

.translation-form-modal :deep(.modal-content)::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 3px;
}

.translation-form-modal :deep(.modal-content)::-webkit-scrollbar-thumb:hover {
  background: #a0aec0;
}

/* 移动端优化 */
@media (max-width: 768px) {
  .translation-form-modal :deep(.modal-container) {
    margin: 1rem;
    max-height: calc(100vh - 2rem);
  }

  .grid-cols-2, .grid-cols-3 {
    grid-template-columns: 1fr;
  }
}

/* 暗黑模式滚动条 */
@media (prefers-color-scheme: dark) {
  .translation-form-modal :deep(.modal-content) {
    scrollbar-color: #4a5568 #2d3748;
  }

  .translation-form-modal :deep(.modal-content)::-webkit-scrollbar-track {
    background: #2d3748;
  }

  .translation-form-modal :deep(.modal-content)::-webkit-scrollbar-thumb {
    background: #4a5568;
  }

  .translation-form-modal :deep(.modal-content)::-webkit-scrollbar-thumb:hover {
    background: #718096;
  }
}
</style>