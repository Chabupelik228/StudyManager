<script setup lang="ts">
import { useAuthStore } from '../../stores/auth';
import { useUiStore } from '../../stores/ui';
import { Wrench } from 'lucide-vue-next';

const authStore = useAuthStore();
const uiStore = useUiStore();
</script>

<template>
  <div v-if="authStore.isDeveloper" class="relative z-40">
    <!-- Floating FAB Button on right edge -->
    <button
      class="fixed top-1/2 right-0 -translate-y-1/2 w-7 h-11 rounded-l-xl bg-slate-900/80 dark:bg-white/20 text-white flex items-center justify-center backdrop-blur-md transition-all shadow-lg active:scale-95 border border-r-0 border-white/20"
      title="Панель разработчика"
      @click="uiStore.showDebugMenu = !uiStore.showDebugMenu"
    >
      <Wrench class="w-3.5 h-3.5" />
    </button>

    <!-- Menu Popup -->
    <div
      v-if="uiStore.showDebugMenu"
      class="fixed top-1/2 right-10 -translate-y-1/2 bg-slate-900/95 text-white rounded-2xl p-3 shadow-2xl flex flex-col gap-1.5 w-44 backdrop-blur-xl border border-white/10 text-xs animate-fade-in z-50"
    >
      <div class="text-[10px] uppercase font-extrabold text-slate-400 text-center mb-1 tracking-wider">
        Режим просмотра
      </div>
      <button
        class="py-2 px-2.5 rounded-xl text-left font-semibold transition-all flex items-center gap-2"
        :class="authStore.effectiveRole === 'super' ? 'bg-blue-600 text-white font-bold shadow-sm' : 'hover:bg-white/10 text-slate-300'"
        @click="authStore.setDebugRole('super')"
      >
        <span>👨‍💻</span>
        <span>Супер-Админ</span>
      </button>
      <button
        class="py-2 px-2.5 rounded-xl text-left font-semibold transition-all flex items-center gap-2"
        :class="authStore.effectiveRole === 'admin' ? 'bg-blue-600 text-white font-bold shadow-sm' : 'hover:bg-white/10 text-slate-300'"
        @click="authStore.setDebugRole('admin')"
      >
        <span>👮‍♂️</span>
        <span>Админ</span>
      </button>
      <button
        class="py-2 px-2.5 rounded-xl text-left font-semibold transition-all flex items-center gap-2"
        :class="authStore.effectiveRole === 'viewer' ? 'bg-blue-600 text-white font-bold shadow-sm' : 'hover:bg-white/10 text-slate-300'"
        @click="authStore.setDebugRole('viewer')"
      >
        <span>👤</span>
        <span>Студент</span>
      </button>

      <div class="h-px bg-white/10 my-1"></div>

      <button
        class="py-2 px-2.5 rounded-xl text-left text-slate-300 hover:bg-white/10 font-semibold transition-colors flex items-center gap-2"
        @click="uiStore.showConsole = true; uiStore.showDebugMenu = false"
      >
        <span>🖥</span>
        <span>Консоль логов</span>
      </button>
    </div>
  </div>
</template>
