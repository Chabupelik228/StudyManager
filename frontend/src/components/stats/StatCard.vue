<script setup lang="ts">
import type { StudentStatsRow } from '../../types/stats';
import Avatar from '../common/Avatar.vue';
import { ChevronRight } from 'lucide-vue-next';

defineProps<{
  student: StudentStatsRow;
}>();

const emit = defineEmits<{
  (e: 'click'): void;
}>();
</script>

<template>
  <div
    class="premium-card rounded-2xl p-4 cursor-pointer active:scale-[0.98] transition-all duration-150 group"
    @click="emit('click')"
  >
    <!-- Header: Avatar + Name + Arrow -->
    <div class="flex items-center justify-between mb-3">
      <div class="flex items-center gap-3 min-w-0 flex-1 mr-2">
        <Avatar :tg-id="student.tg_id" :name="student.name" size="md" />
        <span class="font-bold text-[15.5px] text-app-text truncate">{{ student.name }}</span>
      </div>
      <ChevronRight class="w-4 h-4 text-app-muted group-hover:text-app-text group-hover:translate-x-0.5 transition-all flex-shrink-0" />
    </div>

    <!-- Stats Blocks: Month vs Total -->
    <div class="grid grid-cols-2 gap-2.5">
      <!-- Month -->
      <div class="bg-app-card-subtle p-2.5 rounded-xl border border-app-border">
        <div class="text-[10px] font-bold text-app-muted uppercase tracking-wider mb-1">
          Этот месяц
        </div>
        <div class="text-base font-extrabold text-app-text mb-1.5 leading-tight">
          {{ student.month_nb + student.month_uv }} <span class="text-xs font-semibold text-app-muted">ч.</span>
        </div>
        <div class="flex items-center gap-1.5 text-[11px] font-bold">
          <span class="px-2 py-0.5 rounded-md bg-rose-50 text-rose-700 dark:bg-rose-950/70 dark:text-rose-300 border border-rose-200 dark:border-rose-800">
            Н: {{ student.month_nb }}
          </span>
          <span class="px-2 py-0.5 rounded-md bg-amber-50 text-amber-700 dark:bg-amber-950/70 dark:text-amber-300 border border-amber-200 dark:border-amber-800">
            У: {{ student.month_uv }}
          </span>
        </div>
      </div>

      <!-- Total -->
      <div class="bg-app-card-subtle p-2.5 rounded-xl border border-app-border">
        <div class="text-[10px] font-bold text-app-muted uppercase tracking-wider mb-1">
          За семестр
        </div>
        <div class="text-base font-extrabold text-app-text mb-1.5 leading-tight">
          {{ student.total_nb + student.total_uv }} <span class="text-xs font-semibold text-app-muted">ч.</span>
        </div>
        <div class="flex items-center gap-1.5 text-[11px] font-bold">
          <span class="px-2 py-0.5 rounded-md bg-rose-50 text-rose-700 dark:bg-rose-950/70 dark:text-rose-300 border border-rose-200 dark:border-rose-800">
            Н: {{ student.total_nb }}
          </span>
          <span class="px-2 py-0.5 rounded-md bg-amber-50 text-amber-700 dark:bg-amber-950/70 dark:text-amber-300 border border-amber-200 dark:border-amber-800">
            У: {{ student.total_uv }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>
