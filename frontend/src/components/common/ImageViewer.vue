<script setup lang="ts">
import { useUiStore } from '../../stores/ui';
import { X } from 'lucide-vue-next';

const uiStore = useUiStore();
</script>

<template>
  <div
    v-if="uiStore.previewImage"
    class="fixed inset-0 z-50 bg-black/90 backdrop-blur-md flex items-center justify-center p-4 animate-fade-in"
    @click="uiStore.closeImageViewer()"
  >
    <button
      class="absolute top-6 right-6 w-10 h-10 rounded-full bg-white/20 hover:bg-white/30 text-white flex items-center justify-center transition-all"
      @click="uiStore.closeImageViewer()"
    >
      <X class="w-6 h-6" />
    </button>
    <img
      :src="uiStore.previewImage"
      alt="Preview"
      class="max-w-full max-h-full object-contain rounded-lg select-none"
      @click.stop
    />
  </div>
</template>
