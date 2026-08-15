<script setup lang="ts">
import { computed } from 'vue';
import { useScheduleStore } from '../../stores/schedule';
import { formatHeaderDate } from '../../utils/date';
import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from 'lucide-vue-next';

const scheduleStore = useScheduleStore();
const formattedDate = computed(() => formatHeaderDate(scheduleStore.currentDate));
</script>

<template>
  <div class="bg-tg-secondaryBg rounded-2xl p-1 flex items-center justify-between shadow-inner">
    <div class="flex items-center gap-1">
      <button
        class="w-8 h-8 rounded-xl bg-tg-bg text-tg-hint hover:text-tg-text flex items-center justify-center font-bold shadow-sm active:scale-95 transition-all"
        @click="scheduleStore.changeMonth(-1)"
      >
        <ChevronsLeft class="w-4 h-4" />
      </button>
      <button
        class="w-8 h-8 rounded-xl bg-tg-bg text-tg-text flex items-center justify-center font-bold shadow-sm active:scale-95 transition-all"
        @click="scheduleStore.changeDay(-1)"
      >
        <ChevronLeft class="w-4 h-4" />
      </button>
    </div>

    <div class="text-sm font-semibold capitalize px-2 text-center select-none">
      {{ formattedDate }}
    </div>

    <div class="flex items-center gap-1">
      <button
        class="w-8 h-8 rounded-xl bg-tg-bg text-tg-text flex items-center justify-center font-bold shadow-sm active:scale-95 transition-all"
        @click="scheduleStore.changeDay(1)"
      >
        <ChevronRight class="w-4 h-4" />
      </button>
      <button
        class="w-8 h-8 rounded-xl bg-tg-bg text-tg-hint hover:text-tg-text flex items-center justify-center font-bold shadow-sm active:scale-95 transition-all"
        @click="scheduleStore.changeMonth(1)"
      >
        <ChevronsRight class="w-4 h-4" />
      </button>
    </div>
  </div>
</template>
