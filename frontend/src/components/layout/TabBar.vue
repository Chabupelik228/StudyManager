<script setup lang="ts">
import { useUiStore, type ScreenTab } from '../../stores/ui';
import { useAuthStore } from '../../stores/auth';
import { Calendar, BarChart3, Users, Shield } from 'lucide-vue-next';

const uiStore = useUiStore();
const authStore = useAuthStore();

const tabs: Array<{ id: ScreenTab; label: string; icon: any; adminOnly?: boolean }> = [
  { id: 'schedule', label: 'Расписание', icon: Calendar },
  { id: 'stats', label: 'Статистика', icon: BarChart3 },
  { id: 'duties', label: 'Дежурства', icon: Users },
  { id: 'admin', label: 'Админка', icon: Shield, adminOnly: true },
];

function isTabActive(tabId: ScreenTab): boolean {
  if (uiStore.activeScreen === tabId) return true;
  if (tabId === 'schedule' && uiStore.activeScreen === 'details') return true;
  if (tabId === 'stats' && uiStore.activeScreen === 'student-absences') return true;
  return false;
}
</script>

<template>
  <nav
    class="fixed bottom-0 left-0 right-0 z-30 glass-nav flex items-center justify-around px-2 pt-1 pb-[calc(var(--safe-bottom)+4px)]"
  >
    <template v-for="t in tabs" :key="t.id">
      <button
        v-if="!t.adminOnly || authStore.isAdmin"
        class="flex-1 flex flex-col items-center justify-center py-1.5 px-1 rounded-2xl transition-all duration-200 relative group active:scale-95"
        @click="uiStore.switchTab(t.id)"
      >
        <!-- Active Background Pill -->
        <div
          v-if="isTabActive(t.id)"
          class="absolute inset-0 rounded-2xl bg-[#007aff]/10 dark:bg-[#007aff]/15 -z-10 transition-all duration-300 scale-95"
        ></div>

        <!-- Icon with smooth scale and glow on active -->
        <div class="relative flex items-center justify-center mb-0.5">
          <component
            :is="t.icon"
            class="w-5 h-5 transition-transform duration-200"
            :class="
              isTabActive(t.id)
                ? 'text-[#007aff] scale-110'
                : 'text-tg-hint group-hover:text-tg-text'
            "
            :stroke-width="isTabActive(t.id) ? 2.3 : 1.8"
          />
          <!-- Active Dot -->
          <span
            v-if="isTabActive(t.id)"
            class="absolute -bottom-1 w-1 h-1 rounded-full bg-[#007aff] glow-blue"
          ></span>
        </div>

        <span
          class="text-[10.5px] tracking-tight font-medium transition-colors duration-200 mt-0.5"
          :class="
            isTabActive(t.id)
              ? 'text-[#007aff] font-semibold'
              : 'text-tg-hint group-hover:text-tg-text'
          "
        >
          {{ t.label }}
        </span>
      </button>
    </template>
  </nav>
</template>
