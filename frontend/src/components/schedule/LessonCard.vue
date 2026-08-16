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
    class="premium-card rounded-2xl p-4 flex items-center gap-3.5 cursor-pointer active:scale-[0.98] transition-all duration-150 relative overflow-hidden group"
    :class="{
      'opacity-50 grayscale': lesson.canceled,
      'ring-2 ring-app-accent bg-blue-50/30 dark:bg-blue-950/20 shadow-glow-blue': lesson.is_current,
    }"
    @click="emit('click')"
  >
    <!-- CURRENT indicator -->
    <div
      v-if="lesson.is_current"
      class="absolute top-2.5 right-3 flex items-center gap-1 bg-app-accent text-white text-[9.5px] font-extrabold tracking-wider px-2 py-0.5 rounded-full shadow-sm uppercase"
    >
      <span class="w-1.5 h-1.5 rounded-full bg-white animate-pulse"></span>
      СЕЙЧАС
    </div>

    <!-- Time Badge Column -->
    <div
      class="flex flex-col items-center justify-center px-2.5 py-2 rounded-xl bg-blue-50 text-blue-700 dark:bg-blue-950/60 dark:text-blue-300 font-bold text-sm min-w-[54px] border border-blue-200/80 dark:border-blue-800/60"
    >
      <Clock class="w-3.5 h-3.5 mb-0.5 opacity-70" />
      <span>{{ lesson.time }}</span>
    </div>

    <!-- Lesson Info -->
    <div class="flex-1 min-w-0 pr-2">
      <div class="flex items-center gap-1.5">
        <h3
          class="text-[15.5px] font-bold tracking-tight text-app-text truncate"
          :class="{ 'line-through opacity-70': lesson.canceled }"
        >
          {{ lesson.name }}
        </h3>
        <span
          v-if="lesson.canceled"
          class="text-[10px] font-bold bg-rose-100 text-rose-700 dark:bg-rose-950 dark:text-rose-300 px-1.5 py-0.5 rounded border border-rose-200 dark:border-rose-800"
        >
          ОТМЕНЕНА
        </span>
      </div>

      <div class="text-xs text-app-muted flex items-center gap-1.5 mt-0.5 mb-2 font-medium">
        <User class="w-3.5 h-3.5 opacity-60 flex-shrink-0" />
        <span class="truncate">{{ lesson.teacher || 'Преподаватель не назначен' }}</span>
      </div>

      <div class="flex items-center gap-2">
        <span
          v-if="lesson.absent_count > 0"
          class="inline-flex items-center gap-1 bg-rose-50 text-rose-700 dark:bg-rose-950/60 dark:text-rose-300 border border-rose-200 dark:border-rose-800 text-[11px] font-bold px-2 py-0.5 rounded-md"
        >
          <AlertCircle class="w-3 h-3" />
          Отсутствуют: {{ lesson.absent_count }} чел.
        </span>
        <span
          v-else-if="!lesson.canceled"
          class="inline-flex items-center gap-1 bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 text-[11px] font-semibold px-2 py-0.5 rounded-md"
        >
          <CheckCircle2 class="w-3 h-3" />
          Все присутствуют
        </span>
      </div>
    </div>

    <!-- Arrow -->
    <div class="text-app-muted group-hover:text-app-text transition-colors">
      <ChevronRight class="w-4 h-4 opacity-50 group-hover:opacity-100" />
    </div>
  </div>
</template>
