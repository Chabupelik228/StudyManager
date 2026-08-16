<script setup lang="ts">
import type { DutyStudent } from '../../types/duty';
import Avatar from '../common/Avatar.vue';
import { Check, Calendar, Sparkles, AlertCircle } from 'lucide-vue-next';

defineProps<{
  student: DutyStudent;
  selected: boolean;
  canSelect: boolean;
}>();

const emit = defineEmits<{
  (e: 'toggle'): void;
}>();
</script>

<template>
  <div
    class="flex items-center justify-between p-3.5 bg-app-card border-b border-app-border first:rounded-t-2xl last:rounded-b-2xl last:border-b-0 transition-all duration-150 select-none"
    :class="{
      'cursor-pointer active:scale-[0.99]': canSelect,
      'opacity-50 grayscale': student.is_absent_now,
      'bg-blue-50/50 dark:bg-blue-950/30 border-l-4 !border-l-app-accent pl-2.5': selected,
    }"
    @click="canSelect ? emit('toggle') : null"
  >
    <div class="flex items-center gap-3 min-w-0 flex-1 mr-2">
      <Avatar :tg-id="student.tg_id" :name="student.name" size="md" />

      <div class="min-w-0 flex-1">
        <div class="font-bold text-[15px] text-app-text truncate flex items-center gap-1.5">
          <span class="truncate">{{ student.name }}</span>
          <span
            v-if="!student.date"
            class="inline-flex items-center gap-1 text-[10px] font-extrabold text-emerald-700 dark:text-emerald-300 bg-emerald-50 dark:bg-emerald-950 px-1.5 py-0.5 rounded border border-emerald-200 dark:border-emerald-800"
          >
            <Sparkles class="w-2.5 h-2.5" />
            Впервые
          </span>
        </div>

        <div class="text-xs text-app-muted mt-0.5 flex items-center gap-1.5 truncate font-medium">
          <span v-if="student.date" class="inline-flex items-center gap-1">
            <Calendar class="w-3 h-3 opacity-60" />
            {{ student.date }}
          </span>
          <span v-else class="text-emerald-600 dark:text-emerald-400 font-semibold">Еще не дежурил</span>

          <span
            v-if="student.is_absent_now"
            class="inline-flex items-center gap-1 text-rose-700 dark:text-rose-300 font-bold bg-rose-50 dark:bg-rose-950 px-1.5 py-0.5 rounded border border-rose-200 dark:border-rose-800 text-[10px]"
          >
            <AlertCircle class="w-2.5 h-2.5" />
            Отсутствует
          </span>
        </div>
      </div>
    </div>

    <!-- Selection indicator -->
    <div v-if="canSelect" class="flex-shrink-0">
      <div
        class="w-7 h-7 rounded-xl border flex items-center justify-center transition-all duration-150"
        :class="
          selected
            ? 'bg-app-accent border-app-accent text-white shadow-glow-blue scale-105'
            : 'border-app-border bg-app-card-subtle'
        "
      >
        <Check v-if="selected" class="w-4 h-4 stroke-[3]" />
      </div>
    </div>
  </div>
</template>
