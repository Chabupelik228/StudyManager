<script setup lang="ts">
import { computed } from 'vue';
import { useScheduleStore } from '../../stores/schedule';
import { formatHeaderDate } from '../../utils/date';
import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from 'lucide-vue-next';

const scheduleStore = useScheduleStore();
const formattedDate = computed(() => formatHeaderDate(scheduleStore.currentDate));
</script>

<template>
  <div class="bg-app-card-subtle border border-app-border rounded-2xl p-1 flex items-center justify-between shadow-sm">
    <div class="flex items-center gap-1">
      <button
        class="w-8 h-8 rounded-xl bg-app-card border border-app-border text-app-muted hover:text-app-text flex items-center justify-center font-bold shadow-sm active:scale-95 transition-all"
        title="Предыдущий месяц"
        @click="scheduleStore.changeMonth(-1)"
      >
        <ChevronsLeft class="w-4 h-4" />
      </button>
      <button
        class="w-8 h-8 rounded-xl bg-app-card border border-app-border text-app-text flex items-center justify-center font-bold shadow-sm active:scale-95 transition-all"
        title="Предыдущий день"
        @click="scheduleStore.changeDay(-1)"
      >
        <ChevronLeft class="w-4 h-4" />
      </button>
    </div>

    <div class="text-sm font-bold capitalize px-2 text-center select-none text-app-text">
      {{ formattedDate }}
    </div>

    <div class="flex items-center gap-1">
      <button
        class="w-8 h-8 rounded-xl bg-app-card border border-app-border text-app-text flex items-center justify-center font-bold shadow-sm active:scale-95 transition-all"
        title="Следующий день"
        @click="scheduleStore.changeDay(1)"
      >
        <ChevronRight class="w-4 h-4" />
      </button>
      <button
        class="w-8 h-8 rounded-xl bg-app-card border border-app-border text-app-muted hover:text-app-text flex items-center justify-center font-bold shadow-sm active:scale-95 transition-all"
        title="Следующий месяц"
        @click="scheduleStore.changeMonth(1)"
      >
        <ChevronsRight class="w-4 h-4" />
      </button>
    </div>
  </div>
</template>
