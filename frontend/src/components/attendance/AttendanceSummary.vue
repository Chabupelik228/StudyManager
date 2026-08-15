<script setup lang="ts">
import { useAttendanceStore } from '../../stores/attendance';
import { Users, Filter } from 'lucide-vue-next';

const attendanceStore = useAttendanceStore();
</script>

<template>
  <div class="glass-card rounded-2xl p-4 space-y-3">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <div class="w-8 h-8 rounded-xl bg-[#007aff]/10 text-[#007aff] flex items-center justify-center">
          <Users class="w-4 h-4" />
        </div>
        <div>
          <div class="text-[11px] font-medium text-tg-hint uppercase tracking-wider">Отсутствуют</div>
          <div class="text-lg font-black text-tg-text leading-tight">
            {{ attendanceStore.totalAbsent }} <span class="text-xs font-medium text-tg-hint">из {{ attendanceStore.students.length }}</span>
          </div>
        </div>
      </div>

      <button
        class="inline-flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-xl transition-all duration-200 active:scale-95 shadow-sm"
        :class="
          attendanceStore.showOnlyAbsent
            ? 'bg-[#007aff] text-white glow-blue'
            : 'bg-black/5 dark:bg-white/10 text-tg-text hover:bg-black/10 dark:hover:bg-white/15'
        "
        @click="attendanceStore.showOnlyAbsent = !attendanceStore.showOnlyAbsent"
      >
        <Filter class="w-3 h-3" />
        <span>{{ attendanceStore.showOnlyAbsent ? 'Показать всех' : 'Только отсутствующие' }}</span>
      </button>
    </div>

    <!-- Counters row -->
    <div class="grid grid-cols-2 gap-2 pt-1">
      <div class="flex items-center justify-between px-3 py-2 rounded-xl bg-rose-500/10 border border-rose-500/20">
        <span class="text-xs font-bold text-rose-600 dark:text-rose-400">Неуважительная (Н)</span>
        <span class="text-sm font-black text-rose-600 dark:text-rose-400">{{ attendanceStore.countNb }}</span>
      </div>
      <div class="flex items-center justify-between px-3 py-2 rounded-xl bg-amber-500/10 border border-amber-500/20">
        <span class="text-xs font-bold text-amber-600 dark:text-amber-400">Уважительная (У)</span>
        <span class="text-sm font-black text-amber-600 dark:text-amber-400">{{ attendanceStore.countUv }}</span>
      </div>
    </div>
  </div>
</template>
