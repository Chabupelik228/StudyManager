<script setup lang="ts">
import type { DutyStudent } from '../../types/duty';
import Avatar from '../common/Avatar.vue';
import { Check } from 'lucide-vue-next';

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
    class="flex items-center justify-between p-3.5 bg-tg-bg border-b border-black/5 dark:border-white/5 first:rounded-t-2xl last:rounded-b-2xl last:border-b-0 transition-all select-none"
    :class="{
      'cursor-pointer active:scale-[0.99]': canSelect,
      'opacity-50 grayscale': student.is_absent_now,
      'bg-[#007aff]/5 border-l-4 !border-l-[#007aff] pl-2.5': selected,
    }"
    @click="canSelect ? emit('toggle') : null"
  >
    <div class="flex items-center gap-3 min-w-0">
      <Avatar :tg-id="student.tg_id" :name="student.name" size="md" />

      <div class="min-w-0">
        <div class="font-medium text-base text-tg-text truncate">
          {{ student.name }}
        </div>
        <div class="text-xs text-tg-hint mt-0.5">
          <span v-if="student.date">Последнее: {{ student.date }}</span>
          <span v-else class="text-emerald-500 font-semibold">Еще не дежурил</span>
          <span v-if="student.is_absent_now" class="text-[#ff3b30] font-bold ml-2">
            (Отсутствует сейчас)
          </span>
        </div>
      </div>
    </div>

    <!-- Selection indicator -->
    <div v-if="canSelect" class="flex-shrink-0">
      <div
        class="w-7 h-7 rounded-full border-2 flex items-center justify-center transition-all"
        :class="
          selected
            ? 'bg-[#007aff] border-[#007aff] text-white shadow-sm'
            : 'border-black/15 dark:border-white/15'
        "
      >
        <Check v-if="selected" class="w-4 h-4" />
      </div>
    </div>
  </div>
</template>
