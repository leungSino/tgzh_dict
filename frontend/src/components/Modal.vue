<template>
  <!-- ✅ 遮罩层 -->
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <!-- ✅ 弹窗主体 -->
    <div class="bg-white rounded-lg shadow-xl w-full max-w-xl mx-4 p-6 relative animate-fadeIn">
      <!-- 关闭按钮 -->
      <button
        @click="$emit('close')"
        class="absolute top-2 right-3 text-gray-500 hover:text-gray-700 text-2xl font-bold"
      >
        &times;
      </button>

      <!-- ✅ 标题 -->
      <h2 v-if="title" class="text-xl font-semibold mb-4 text-center">{{ title }}</h2>

      <!-- ✅ 主体内容 -->
      <div class="overflow-y-auto max-h-[70vh]">
        <slot />
      </div>

      <!-- ✅ 底部操作区（可选插槽） -->
      <div v-if="$slots.footer" class="mt-6 pt-4 border-t flex justify-end space-x-3">
        <slot name="footer" />
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, default: '' }
})
defineEmits(['close'])
</script>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fadeIn {
  animation: fadeIn 0.2s ease-out;
}
</style>
