<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useStatsStore } from '../stores/stats';
import { useAuthStore } from '../stores/auth';
import { useUiStore } from '../stores/ui';
import { formatMonthYear } from '../utils/date';
import { tg } from '../utils/telegram';
import SortBar from '../components/stats/SortBar.vue';
import StatCard from '../components/stats/StatCard.vue';
import { ChevronLeft, ChevronRight, FileSpreadsheet } from 'lucide-vue-next';

const statsStore = useStatsStore();
const authStore = useAuthStore();
const uiStore = useUiStore();

const formattedMonth = computed(() => formatMonthYear(statsStore.currentMonth));

onMounted(() => {
  statsStore.loadStats();
});

function handleOpenDrilldown(st: { id: number; name: string }) {
  statsStore.openStudentDrilldown(st);
  uiStore.switchTab('student-absences');
}

function handleExportExcel() {
  const y = statsStore.currentMonth.getFullYear();
  const m = String(statsStore.currentMonth.getMonth() + 1).padStart(2, '0');
  const botUsername = 'manager_ems_bot';
  const deepLink = `https://t.me/${botUsername}?start=report_${y}_${m}`;

  tg.openTelegramLink(deepLink);
  tg.showPopup({
    title: 'Отчет формируется',
    message: 'Бот отправит вам Excel-файл прямо в чат Telegram через несколько секунд.',
  });
}
</script>

<template>
  <div class="h-full flex flex-col overflow-hidden">
    <!-- Header with Month Switcher & Excel Export -->
    <div class="p-3 bg-tg-bg/90 backdrop-blur-md border-b border-black/10 dark:border-white/10 space-y-2.5 sticky top-0 z-10 flex-shrink-0">
      <!-- Month Pill -->
      <div class="bg-tg-secondaryBg rounded-2xl p-1 flex items-center justify-between shadow-inner">
        <button
          class="w-8 h-8 rounded-xl bg-tg-bg text-tg-text flex items-center justify-center font-bold shadow-sm active:scale-95 transition-all"
          @click="statsStore.changeMonth(-1)"
        >
          <ChevronLeft class="w-4 h-4" />
        </button>

        <div class="text-sm font-semibold capitalize px-2 text-center select-none">
          {{ formattedMonth }}
        </div>

        <button
          class="w-8 h-8 rounded-xl bg-tg-bg text-tg-text flex items-center justify-center font-bold shadow-sm active:scale-95 transition-all"
          @click="statsStore.changeMonth(1)"
        >
          <ChevronRight class="w-4 h-4" />
        </button>
      </div>

      <!-- Excel Export Button for Admins -->
      <button
        v-if="authStore.isAdmin"
        class="w-full py-2.5 px-3 rounded-xl bg-tg-bg border border-black/10 dark:border-white/10 text-[#007aff] font-semibold text-xs flex items-center justify-center gap-2 active:scale-98 transition-all shadow-sm"
        @click="handleExportExcel"
      >
        <FileSpreadsheet class="w-4 h-4" />
        <span>Скачать отчет (Excel)</span>
      </button>

      <!-- Sort Bar -->
      <SortBar />
    </div>

    <!-- Stats Cards List -->
    <div class="flex-1 overflow-y-auto p-4 space-y-3 pb-24">
      <div v-if="statsStore.loading" class="text-center py-12 text-tg-hint text-sm">
        Загрузка статистики...
      </div>

      <template v-else>
        <StatCard
          v-for="s in statsStore.sortedStats"
          :key="s.id"
          :student="s"
          @click="handleOpenDrilldown(s)"
        />
      </template>
    </div>
  </div>
</template>
