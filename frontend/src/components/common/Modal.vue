<script setup lang="ts">
import { X } from 'lucide-vue-next';

defineProps<{
  show: boolean;
  title?: string;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
}>();
</script>

<template>
  <div
    v-if="show"
    class="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm flex items-center justify-center p-4 animate-fade-in"
    @click="emit('close')"
  >
    <div
      class="bg-tg-bg text-tg-text rounded-2xl w-full max-w-sm p-5 shadow-2xl relative border border-black/10 dark:border-white/10"
      @click.stop
    >
      <div v-if="title" class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-bold">{{ title }}</h3>
        <button
          class="p-1 rounded-full text-tg-hint hover:text-tg-text transition-colors"
          @click="emit('close')"
        >
          <X class="w-5 h-5" />
        </button>
      </div>

      <div>
        <slot />
      </div>
    </div>
  </div>
</template>
