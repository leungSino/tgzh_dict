<template>
  <Modal :title="title" @close="$emit('cancel')">
    <div class="text-gray-700 mb-4">
      <slot>
        确定要删除此项吗？此操作不可恢复。
      </slot>
    </div>

    <template #footer>
      <button
        @click="$emit('confirm')"
        class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
      >
        确认删除
      </button>
      <button
        @click="$emit('cancel')"
        class="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500"
      >
        取消
      </button>
    </template>
  </Modal>
</template>

<script setup>
import Modal from '@/components/Modal.vue'

defineProps({
  title: {
    type: String,
    default: '确认删除'
  }
})
defineEmits(['confirm', 'cancel'])
</script>
