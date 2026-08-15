<script setup lang="ts">
import { useAttendanceStore } from '../../stores/attendance';

const attendanceStore = useAttendanceStore();
</script>

<template>
  <div class="bg-tg-bg rounded-2xl p-4 shadow-sm border border-black/5 dark:border-white/5 space-y-3">
    <div class="flex items-center justify-between">
      <div class="text-sm font-semibold">
        Отсутствуют: <b class="text-[#007aff]">{{ attendanceStore.totalAbsent }}</b>
      </div>
      <button
        class="text-xs font-semibold px-3 py-1.5 rounded-lg transition-all"
        :class="
          attendanceStore.showOnlyAbsent
            ? 'bg-[#007aff] text-white shadow-sm'
            : 'bg-tg-secondaryBg text-tg-text hover:bg-black/5'
        "
        @click="attendanceStore.showOnlyAbsent = !attendanceStore.showOnlyAbsent"
      >
        {{ attendanceStore.showOnlyAbsent ? 'Все студенты' : 'Только отсутствующие' }}
      </button>
    </div>

    <div class="flex gap-2">
      <span class="text-xs font-bold px-2.5 py-1 rounded-md bg-[#ff3b30]/10 text-[#ff3b30]">
        Н: {{ attendanceStore.countNb }} чел.
      </span>
      <span class="text-xs font-bold px-2.5 py-1 rounded-md bg-[#ff9500]/10 text-[#ff9500]">
        У: {{ attendanceStore.countUv }} чел.
      </span>
    </div>
  </div>
</template>
