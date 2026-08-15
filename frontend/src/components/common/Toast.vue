<script setup lang="ts">
import { useUiStore } from '../../stores/ui';

const uiStore = useUiStore();
</script>

<template>
  <div class="fixed top-4 left-4 right-4 z-50 pointer-events-none flex flex-col items-center gap-2">
    <div
      v-for="t in uiStore.toasts"
      :key="t.id"
      class="animate-fade-in pointer-events-auto px-4 py-2.5 rounded-xl shadow-lg text-sm font-medium backdrop-blur-md transition-all"
      :class="{
        'bg-black/85 text-white dark:bg-white/90 dark:text-black': !t.type || t.type === 'info',
        'bg-[#34c759] text-white': t.type === 'success',
        'bg-[#ff3b30] text-white': t.type === 'error',
      }"
    >
      {{ t.text }}
    </div>
  </div>
</template>
