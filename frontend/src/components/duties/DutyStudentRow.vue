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
    class="flex items-center justify-between p-3.5 bg-white/70 dark:bg-zinc-900/60 border-b border-black/[0.04] dark:border-white/[0.06] first:rounded-t-2xl last:rounded-b-2xl last:border-b-0 transition-all duration-150 select-none"
    :class="{
      'cursor-pointer active:scale-[0.99]': canSelect,
      'opacity-50 grayscale': student.is_absent_now,
      'bg-[#007aff]/[0.08] dark:bg-[#007aff]/15 border-l-4 !border-l-[#007aff] pl-2.5': selected,
    }"
    @click="canSelect ? emit('toggle') : null"
  >
    <div class="flex items-center gap-3 min-w-0 flex-1 mr-2">
      <Avatar :tg-id="student.tg_id" :name="student.name" size="md" />

      <div class="min-w-0 flex-1">
        <div class="font-semibold text-[15px] text-tg-text truncate flex items-center gap-1.5">
          <span class="truncate">{{ student.name }}</span>
          <span
            v-if="!student.date"
            class="inline-flex items-center gap-1 text-[10px] font-bold text-emerald-500 bg-emerald-500/10 px-1.5 py-0.5 rounded-full border border-emerald-500/20"
          >
            <Sparkles class="w-2.5 h-2.5" />
            Впервые
          </span>
        </div>

        <div class="text-xs text-tg-hint mt-0.5 flex items-center gap-1.5 truncate">
          <span v-if="student.date" class="inline-flex items-center gap-1">
            <Calendar class="w-3 h-3 opacity-60" />
            {{ student.date }}
          </span>
          <span v-else class="text-emerald-500 font-medium">Еще не дежурил</span>

          <span
            v-if="student.is_absent_now"
            class="inline-flex items-center gap-1 text-rose-500 font-semibold bg-rose-500/10 px-1.5 py-0.5 rounded text-[10px]"
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
        class="w-7 h-7 rounded-xl border flex items-center justify-center transition-all duration-200"
        :class="
          selected
            ? 'bg-[#007aff] border-[#007aff] text-white glow-blue scale-105 shadow-sm'
            : 'border-black/15 dark:border-white/15 bg-black/[0.02] dark:bg-white/[0.04]'
        "
      >
        <Check v-if="selected" class="w-4 h-4 stroke-[3]" />
      </div>
    </div>
  </div>
</template>
