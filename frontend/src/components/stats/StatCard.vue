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
    class="glass-card rounded-2xl p-4 cursor-pointer active:scale-[0.98] transition-all duration-200 hover:border-[#007aff]/30 group"
    @click="emit('click')"
  >
    <!-- Header: Avatar + Name + Arrow -->
    <div class="flex items-center justify-between mb-3">
      <div class="flex items-center gap-3 min-w-0 flex-1 mr-2">
        <Avatar :tg-id="student.tg_id" :name="student.name" size="md" />
        <span class="font-bold text-[15px] text-tg-text truncate">{{ student.name }}</span>
      </div>
      <ChevronRight class="w-4 h-4 text-tg-hint opacity-40 group-hover:opacity-80 group-hover:translate-x-0.5 transition-all flex-shrink-0" />
    </div>

    <!-- Stats Blocks: Month vs Total -->
    <div class="grid grid-cols-2 gap-2.5">
      <!-- Month -->
      <div class="bg-black/[0.03] dark:bg-white/[0.04] p-2.5 rounded-xl border border-black/[0.04] dark:border-white/[0.06]">
        <div class="text-[10px] font-bold text-tg-hint uppercase tracking-wider mb-1">
          Этот месяц
        </div>
        <div class="text-base font-black text-tg-text mb-1.5 leading-tight">
          {{ student.month_nb + student.month_uv }} <span class="text-xs font-semibold text-tg-hint">ч.</span>
        </div>
        <div class="flex items-center gap-1.5 text-[11px] font-bold">
          <span class="px-2 py-0.5 rounded-md bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/20">
            Н: {{ student.month_nb }}
          </span>
          <span class="px-2 py-0.5 rounded-md bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20">
            У: {{ student.month_uv }}
          </span>
        </div>
      </div>

      <!-- Total -->
      <div class="bg-black/[0.03] dark:bg-white/[0.04] p-2.5 rounded-xl border border-black/[0.04] dark:border-white/[0.06]">
        <div class="text-[10px] font-bold text-tg-hint uppercase tracking-wider mb-1">
          За семестр
        </div>
        <div class="text-base font-black text-tg-text mb-1.5 leading-tight">
          {{ student.total_nb + student.total_uv }} <span class="text-xs font-semibold text-tg-hint">ч.</span>
        </div>
        <div class="flex items-center gap-1.5 text-[11px] font-bold">
          <span class="px-2 py-0.5 rounded-md bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/20">
            Н: {{ student.total_nb }}
          </span>
          <span class="px-2 py-0.5 rounded-md bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20">
            У: {{ student.total_uv }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>
