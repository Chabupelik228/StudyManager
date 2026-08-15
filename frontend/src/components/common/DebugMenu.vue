<script setup lang="ts">
import { useAuthStore } from '../../stores/auth';
import { useUiStore } from '../../stores/ui';
import { useAdminStore } from '../../stores/admin';
import { Wrench } from 'lucide-vue-next';

const authStore = useAuthStore();
const uiStore = useUiStore();
const adminStore = useAdminStore();

async function handleResetLimits() {
  await adminStore.resetMyAiLimits();
  uiStore.showToast('Дневной лимит AI сброшен!', 'success');
}
</script>

<template>
  <div v-if="authStore.isAdmin" class="relative z-40">
    <!-- Floating FAB Button on right edge -->
    <button
      class="fixed top-1/2 right-0 -translate-y-1/2 w-8 h-12 rounded-l-xl bg-black/40 hover:bg-black/80 text-white flex items-center justify-center backdrop-blur-sm transition-all shadow-md active:scale-95"
      @click="uiStore.showDebugMenu = !uiStore.showDebugMenu"
    >
      <Wrench class="w-4 h-4" />
    </button>

    <!-- Menu Popup -->
    <div
      v-if="uiStore.showDebugMenu"
      class="fixed top-1/2 right-12 -translate-y-1/2 bg-black/90 text-white rounded-xl p-3 shadow-2xl flex flex-col gap-2 w-44 backdrop-blur-md border border-white/10 text-xs animate-fade-in"
    >
      <div class="text-[10px] uppercase font-bold text-gray-400 text-center mb-1">Смена роли</div>
      <button
        class="py-1.5 px-2 rounded-lg text-left transition-colors"
        :class="authStore.effectiveRole === 'super' ? 'bg-[#007aff] font-bold' : 'hover:bg-white/10'"
        @click="authStore.setDebugRole('super')"
      >
        👨‍💻 Супер-Админ
      </button>
      <button
        class="py-1.5 px-2 rounded-lg text-left transition-colors"
        :class="authStore.effectiveRole === 'admin' ? 'bg-[#007aff] font-bold' : 'hover:bg-white/10'"
        @click="authStore.setDebugRole('admin')"
      >
        👮‍♂️ Админ
      </button>
      <button
        class="py-1.5 px-2 rounded-lg text-left transition-colors"
        :class="authStore.effectiveRole === 'viewer' ? 'bg-[#007aff] font-bold' : 'hover:bg-white/10'"
        @click="authStore.setDebugRole('viewer')"
      >
        👤 Юзер
      </button>

      <div class="h-px bg-white/10 my-1"></div>

      <button
        class="py-1.5 px-2 rounded-lg text-left text-[#ff3b30] hover:bg-white/10 transition-colors"
        @click="handleResetLimits"
      >
        🔄 Сброс лимита AI
      </button>
      <button
        class="py-1.5 px-2 rounded-lg text-left text-gray-300 hover:bg-white/10 transition-colors"
        @click="uiStore.showConsole = true; uiStore.showDebugMenu = false"
      >
        🖥 Консоль
      </button>
    </div>
  </div>
</template>
