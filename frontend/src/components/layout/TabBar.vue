<script setup lang="ts">
import { useUiStore, type ScreenTab } from '../../stores/ui';
import { useAuthStore } from '../../stores/auth';
import { Calendar, BarChart3, Users, Settings } from 'lucide-vue-next';

const uiStore = useUiStore();
const authStore = useAuthStore();

const tabs: Array<{ id: ScreenTab; label: string; icon: any; adminOnly?: boolean }> = [
  { id: 'schedule', label: 'Расписание', icon: Calendar },
  { id: 'stats', label: 'Статистика', icon: BarChart3 },
  { id: 'duties', label: 'Дежурства', icon: Users },
  { id: 'admin', label: 'Админка', icon: Settings, adminOnly: true },
];
</script>

<template>
  <div
    class="fixed bottom-0 left-0 right-0 z-30 bg-tg-bg/90 backdrop-blur-xl border-t border-black/10 dark:border-white/10 flex items-center justify-around pb-[var(--safe-bottom)]"
  >
    <template v-for="t in tabs" :key="t.id">
      <button
        v-if="!t.adminOnly || authStore.isAdmin"
        class="flex-1 flex flex-col items-center py-2 text-[11px] font-medium transition-all"
        :class="
          uiStore.activeScreen === t.id ||
          (t.id === 'schedule' && uiStore.activeScreen === 'details') ||
          (t.id === 'stats' && uiStore.activeScreen === 'student-absences')
            ? 'text-[#007aff]'
            : 'text-tg-hint hover:text-tg-text'
        "
        @click="uiStore.switchTab(t.id)"
      >
        <component :is="t.icon" class="w-6 h-6 mb-0.5" />
        <span>{{ t.label }}</span>
      </button>
    </template>
  </div>
</template>
