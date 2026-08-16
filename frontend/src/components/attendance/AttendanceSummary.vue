<script setup lang="ts">
import { useAttendanceStore } from '../../stores/attendance';
import { Users, Filter } from 'lucide-vue-next';

const attendanceStore = useAttendanceStore();
</script>

<template>
  <div class="premium-card rounded-2xl p-4 space-y-3">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2.5">
        <div class="w-8 h-8 rounded-xl bg-blue-50 text-app-accent dark:bg-blue-950 dark:text-blue-400 flex items-center justify-center border border-blue-200 dark:border-blue-800">
          <Users class="w-4 h-4" />
        </div>
        <div>
          <div class="text-[11px] font-bold text-app-muted uppercase tracking-wider">Отсутствуют</div>
          <div class="text-lg font-extrabold text-app-text leading-tight">
            {{ attendanceStore.totalAbsent }} <span class="text-xs font-semibold text-app-muted">из {{ attendanceStore.students.length }} чел.</span>
          </div>
        </div>
      </div>

      <button
        class="inline-flex items-center gap-1.5 text-xs font-bold px-3 py-1.5 rounded-xl transition-all duration-150 active:scale-95 shadow-sm"
        :class="
          attendanceStore.showOnlyAbsent
            ? 'bg-app-accent text-white shadow-glow-blue'
            : 'bg-app-card-subtle text-app-text border border-app-border hover:bg-slate-200/50 dark:hover:bg-slate-800'
        "
        @click="attendanceStore.showOnlyAbsent = !attendanceStore.showOnlyAbsent"
      >
        <Filter class="w-3 h-3" />
        <span>{{ attendanceStore.showOnlyAbsent ? 'Все студенты' : 'Только отсутствующие' }}</span>
      </button>
    </div>

    <!-- Counters row -->
    <div class="grid grid-cols-2 gap-2 pt-1">
      <div class="flex items-center justify-between px-3 py-2 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800/80">
        <span class="text-xs font-bold text-rose-700 dark:text-rose-300">Неуважительная (Н)</span>
        <span class="text-sm font-extrabold text-rose-700 dark:text-rose-300">{{ attendanceStore.countNb }}</span>
      </div>
      <div class="flex items-center justify-between px-3 py-2 rounded-xl bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800/80">
        <span class="text-xs font-bold text-amber-700 dark:text-amber-300">Уважительная (У)</span>
        <span class="text-sm font-extrabold text-amber-700 dark:text-amber-300">{{ attendanceStore.countUv }}</span>
      </div>
    </div>
  </div>
</template>
