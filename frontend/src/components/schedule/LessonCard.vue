<script setup lang="ts">
import type { Lesson } from '../../types/schedule';
import { ChevronRight } from 'lucide-vue-next';

defineProps<{
  lesson: Lesson;
}>();

const emit = defineEmits<{
  (e: 'click'): void;
}>();
</script>

<template>
  <div
    class="bg-tg-bg rounded-2xl p-4 shadow-sm border border-black/5 dark:border-white/5 flex items-center gap-4 cursor-pointer active:scale-[0.98] transition-all relative overflow-hidden"
    :class="{
      'opacity-60': lesson.canceled,
      'border-2 !border-[#007aff] bg-[#007aff]/5': lesson.is_current,
    }"
    @click="emit('click')"
  >
    <!-- CURRENT indicator -->
    <div
      v-if="lesson.is_current"
      class="absolute top-2 right-3 text-[10px] font-black tracking-wider text-[#007aff] uppercase"
    >
      СЕЙЧАС
    </div>

    <!-- Time Column -->
    <div class="flex flex-col items-center justify-center font-bold text-[#007aff] text-base min-w-[48px]">
      {{ lesson.time }}
    </div>

    <!-- Lesson Info -->
    <div class="flex-1 min-w-0">
      <h3
        class="text-[17px] font-semibold tracking-tight text-tg-text truncate"
        :class="{ 'line-through': lesson.canceled }"
      >
        {{ lesson.name }}
      </h3>
      <div class="text-xs text-tg-hint flex items-center gap-1 mt-0.5 mb-1.5">
        <span>👨‍🏫</span>
        <span class="truncate">{{ lesson.teacher || 'Не назначен' }}</span>
      </div>

      <div>
        <span
          v-if="lesson.absent_count > 0"
          class="inline-block bg-[#007aff]/10 text-[#007aff] text-xs font-semibold px-2 py-0.5 rounded-md"
        >
          Отсутствуют: {{ lesson.absent_count }} чел.
        </span>
        <span v-else class="text-xs text-tg-hint">
          Все присутствуют
        </span>
      </div>
    </div>

    <!-- Arrow -->
    <div class="text-tg-hint">
      <ChevronRight class="w-5 h-5 opacity-40" />
    </div>
  </div>
</template>
