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
    class="bg-tg-bg rounded-2xl p-4 shadow-sm border border-black/5 dark:border-white/5 cursor-pointer active:scale-[0.98] transition-all"
    @click="emit('click')"
  >
    <!-- Header: Avatar + Name + Arrow -->
    <div class="flex items-center justify-between mb-3">
      <div class="flex items-center gap-3 min-w-0">
        <Avatar :tg-id="student.tg_id" :name="student.name" size="sm" />
        <span class="font-semibold text-[17px] text-tg-text truncate">{{ student.name }}</span>
      </div>
      <ChevronRight class="w-5 h-5 text-tg-hint opacity-40 flex-shrink-0" />
    </div>

    <!-- Stats Blocks: Month vs Total -->
    <div class="grid grid-cols-2 gap-2.5">
      <!-- Month -->
      <div class="bg-tg-secondaryBg p-3 rounded-xl">
        <div class="text-[11px] font-bold text-tg-hint uppercase tracking-wider mb-1">
          Этот месяц
        </div>
        <div class="text-sm font-semibold mb-1.5">
          {{ student.month_nb + student.month_uv }} ч.
        </div>
        <div class="flex gap-1.5 text-xs font-bold">
          <span class="px-1.5 py-0.5 rounded bg-[#ff3b30]/10 text-[#ff3b30]">
            Н: {{ student.month_nb }}
          </span>
          <span class="px-1.5 py-0.5 rounded bg-[#ff9500]/10 text-[#ff9500]">
            У: {{ student.month_uv }}
          </span>
        </div>
      </div>

      <!-- Total -->
      <div class="bg-tg-secondaryBg p-3 rounded-xl">
        <div class="text-[11px] font-bold text-tg-hint uppercase tracking-wider mb-1">
          Всего
        </div>
        <div class="text-sm font-semibold mb-1.5">
          {{ student.total_nb + student.total_uv }} ч.
        </div>
        <div class="flex gap-1.5 text-xs font-bold">
          <span class="px-1.5 py-0.5 rounded bg-[#ff3b30]/10 text-[#ff3b30]">
            Н: {{ student.total_nb }}
          </span>
          <span class="px-1.5 py-0.5 rounded bg-[#ff9500]/10 text-[#ff9500]">
            У: {{ student.total_uv }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>
