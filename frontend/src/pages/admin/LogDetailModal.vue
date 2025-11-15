<template>
  <Modal :title="'日志详情'" @close="$emit('close')">
    <div class="space-y-4">
      <!-- 基本信息 -->
      <div class="flex flex-col">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">操作用户</label>
        <input
          type="text"
          :value="log.user"
          readonly
          class="w-full border rounded px-3 py-2 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"
        />
      </div>

      <div class="flex flex-col">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">角色</label>
        <input
          type="text"
          :value="log.role"
          readonly
          class="w-full border rounded px-3 py-2 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"
        />
      </div>

      <div class="flex flex-col">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">操作</label>
        <input
          type="text"
          :value="log.action"
          readonly
          class="w-full border rounded px-3 py-2 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"
        />
      </div>

      <div class="flex flex-col">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">目标集合</label>
        <input
          type="text"
          :value="log.target_collection"
          readonly
          class="w-full border rounded px-3 py-2 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"
        />
      </div>

      <div class="flex flex-col">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">目标ID</label>
        <input
          type="text"
          :value="log.target_id"
          readonly
          class="w-full border rounded px-3 py-2 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"
        />
      </div>

      <div class="flex flex-col">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">摘要</label>
        <textarea
          :value="log.target_summary"
          readonly
          rows="2"
          class="w-full border rounded px-3 py-2 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600 resize-none"
        ></textarea>
      </div>

      <div class="flex flex-col">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">备注</label>
        <textarea
          :value="log.note || '-'"
          readonly
          rows="2"
          class="w-full border rounded px-3 py-2 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600 resize-none"
        ></textarea>
      </div>

      <div class="flex flex-col">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">时间</label>
        <input
          type="text"
          :value="log.time"
          readonly
          class="w-full border rounded px-3 py-2 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600"
        />
      </div>

      <!-- diff 对比 -->
      <div class="flex flex-col">
        <label class="mb-1 text-sm font-medium text-gray-700 dark:text-gray-300">Diff</label>
        <div class="w-full border rounded bg-gray-50 dark:bg-gray-800 text-gray-800 dark:text-white p-2 overflow-x-auto text-xs">
          <div v-if="log.diff && Object.keys(log.diff).length">
            <div v-for="(change, key) in log.diff" :key="key" class="mb-1">
              <p class="font-medium">{{ key }}</p>
              <div class="flex gap-2 text-sm">
                <span class="text-red-600">旧: {{ change.old }}</span>
                <span class="text-green-600">新: {{ change.new }}</span>
              </div>
            </div>
          </div>
          <div v-else>-</div>
        </div>
      </div>
    </div>

    <template #footer>
      <button
        type="button"
        @click="$emit('close')"
        class="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500"
      >
        关闭
      </button>
    </template>
  </Modal>
</template>

<script setup>
import Modal from '@/components/Modal.vue'

const props = defineProps({
  log: { type: Object, required: true }
})
</script>
