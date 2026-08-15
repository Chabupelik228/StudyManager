<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useUiStore } from '../../stores/ui';
import { X, Trash2 } from 'lucide-vue-next';

const uiStore = useUiStore();
const logs = ref<Array<{ time: string; text: string; type: string }>>([]);

onMounted(() => {
  const origLog = console.log;
  const origError = console.error;
  const origWarn = console.warn;

  function pushLog(type: string, args: any[]) {
    const time = new Date().toLocaleTimeString();
    const text = args
      .map((a) => (typeof a === 'object' ? JSON.stringify(a, null, 2) : String(a)))
      .join(' ');
    logs.value.unshift({ time, text, type });
    if (logs.value.length > 200) logs.value.pop();
  }

  console.log = (...args) => {
    origLog(...args);
    pushLog('info', args);
  };
  console.error = (...args) => {
    origError(...args);
    pushLog('error', args);
  };
  console.warn = (...args) => {
    origWarn(...args);
    pushLog('warn', args);
  };
});
</script>

<template>
  <div
    v-if="uiStore.showConsole"
    class="fixed inset-0 z-50 bg-black/95 text-green-400 font-mono text-xs flex flex-col p-4 pt-10"
  >
    <div class="flex items-center justify-between pb-3 border-b border-gray-800 text-white font-bold">
      <span>DEBUG CONSOLE</span>
      <div class="flex items-center gap-2">
        <button
          class="p-1.5 bg-gray-800 rounded hover:bg-gray-700 text-gray-300"
          @click="logs = []"
        >
          <Trash2 class="w-4 h-4" />
        </button>
        <button
          class="p-1.5 bg-gray-800 rounded hover:bg-gray-700 text-gray-300"
          @click="uiStore.showConsole = false"
        >
          <X class="w-4 h-4" />
        </button>
      </div>
    </div>

    <div class="flex-1 overflow-y-auto pt-3 space-y-2 select-text">
      <div
        v-for="(l, idx) in logs"
        :key="idx"
        class="border-b border-gray-900 pb-1"
        :class="{
          'text-red-400': l.type === 'error',
          'text-yellow-400': l.type === 'warn',
          'text-blue-400': l.type === 'info',
        }"
      >
        <span class="text-gray-600 font-bold">[{{ l.time }}]</span> {{ l.text }}
      </div>
    </div>
  </div>
</template>
