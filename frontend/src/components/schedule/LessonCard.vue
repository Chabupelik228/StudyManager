<script setup lang="ts">
import type { Lesson } from '../../types/schedule';
import { ChevronRight, Clock, User, CheckCircle2, AlertCircle } from 'lucide-vue-next';

defineProps<{
  lesson: Lesson;
}>();

const emit = defineEmits<{
  (e: 'click'): void;
}>();
</script>

<template>
  <div
    class="glass-card rounded-2xl p-4 flex items-center gap-3.5 cursor-pointer active:scale-[0.98] transition-all duration-200 relative overflow-hidden group hover:border-[#007aff]/30"
    :class="{
      'opacity-60 bg-black/5 dark:bg-white/5': lesson.canceled,
      'ring-2 ring-[#007aff]/60 bg-[#007aff]/[0.03] dark:bg-[#007aff]/[0.08] shadow-[0_0_20px_rgba(0,122,255,0.15)]': lesson.is_current,
    }"
    @click="emit('click')"
  >
    <!-- CURRENT glowing indicator -->
    <div
      v-if="lesson.is_current"
      class="absolute top-2.5 right-3 flex items-center gap-1 bg-[#007aff] text-white text-[9.5px] font-bold tracking-wider px-2 py-0.5 rounded-full shadow-sm glow-blue uppercase"
    >
      <span class="w-1.5 h-1.5 rounded-full bg-white animate-pulse"></span>
      СЕЙЧАС
    </div>

    <!-- Time Badge Column -->
    <div
      class="flex flex-col items-center justify-center px-2.5 py-2 rounded-xl bg-[#007aff]/10 dark:bg-[#007aff]/20 text-[#007aff] font-bold text-sm min-w-[54px] border border-[#007aff]/20"
      :class="{ 'border-emerald-500/20 text-emerald-500 bg-emerald-500/10': !lesson.is_current && lesson.absent_count === 0 }"
    >
      <Clock class="w-3.5 h-3.5 mb-0.5 opacity-75" />
      <span>{{ lesson.time }}</span>
    </div>

    <!-- Lesson Info -->
    <div class="flex-1 min-w-0 pr-2">
      <div class="flex items-center gap-1.5">
        <h3
          class="text-[16px] font-bold tracking-tight text-tg-text truncate"
          :class="{ 'line-through opacity-70': lesson.canceled }"
        >
          {{ lesson.name }}
        </h3>
        <span
          v-if="lesson.canceled"
          class="text-[10px] font-semibold bg-rose-500/15 text-rose-500 px-1.5 py-0.5 rounded-md border border-rose-500/20"
        >
          ОТМЕНЕНА
        </span>
      </div>

      <div class="text-xs text-tg-hint flex items-center gap-1.5 mt-0.5 mb-2">
        <User class="w-3.5 h-3.5 opacity-60 flex-shrink-0" />
        <span class="truncate">{{ lesson.teacher || 'Преподаватель не назначен' }}</span>
      </div>

      <div class="flex items-center gap-2">
        <span
          v-if="lesson.absent_count > 0"
          class="inline-flex items-center gap-1 bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/20 text-[11px] font-semibold px-2 py-0.5 rounded-full"
        >
          <AlertCircle class="w-3 h-3" />
          Отсутствуют: {{ lesson.absent_count }} чел.
        </span>
        <span
          v-else-if="!lesson.canceled"
          class="inline-flex items-center gap-1 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20 text-[11px] font-medium px-2 py-0.5 rounded-full"
        >
          <CheckCircle2 class="w-3 h-3" />
          Все присутствуют
        </span>
      </div>
    </div>

    <!-- Arrow -->
    <div class="text-tg-hint transition-transform duration-200 group-hover:translate-x-0.5">
      <ChevronRight class="w-4 h-4 opacity-40 group-hover:opacity-80" />
    </div>
  </div>
</template>
