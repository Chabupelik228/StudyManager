<script setup lang="ts">
import { computed } from 'vue';
import type { StudentAttendance } from '../../types/attendance';
import { useAuthStore } from '../../stores/auth';
import Avatar from '../common/Avatar.vue';
import { triggerHaptic } from '../../utils/telegram';

const props = defineProps<{
  student: StudentAttendance;
}>();

const emit = defineEmits<{
  (e: 'toggleStatus', student: StudentAttendance): void;
  (e: 'openReason', student: StudentAttendance): void;
}>();

const authStore = useAuthStore();
const isMe = computed(() => props.student.tg_id === authStore.myTgId);

function handleStatusClick() {
  if (!authStore.isAdmin) return;
  triggerHaptic('select');
  emit('toggleStatus', props.student);
}
</script>

<template>
  <div
    class="flex items-center justify-between p-3.5 bg-tg-bg border-b border-black/5 dark:border-white/5 first:rounded-t-2xl last:rounded-b-2xl last:border-b-0"
    :class="{ 'bg-[#007aff]/5 border-l-4 !border-l-[#007aff] pl-2.5': isMe }"
  >
    <!-- Left: Avatar and Info -->
    <div class="flex items-center gap-3 min-w-0">
      <Avatar :tg-id="student.tg_id" :name="student.name" size="md" />

      <div class="min-w-0">
        <div class="font-medium text-base text-tg-text flex items-center gap-1.5 truncate">
          <span class="truncate">{{ student.name }}</span>
          <span
            v-if="isMe"
            class="bg-[#007aff] text-white text-[10px] font-bold px-1.5 py-0.5 rounded tracking-wide uppercase"
          >
            Я
          </span>
          <span
            v-if="student.is_all_day"
            class="bg-black/10 dark:bg-white/15 text-tg-hint text-[10px] font-bold px-1.5 py-0.5 rounded uppercase"
          >
            Весь день
          </span>
        </div>

        <div
          v-if="student.status > 0"
          class="text-xs font-medium truncate mt-0.5 cursor-pointer hover:underline"
          :class="student.reason ? 'text-[#ff9500]' : 'text-tg-hint'"
          @click="authStore.isAdmin ? emit('openReason', student) : null"
        >
          {{ student.reason || '+ Добавить причину' }}
        </div>
      </div>
    </div>

    <!-- Right: Status Button -->
    <div class="flex items-center gap-2">
      <button
        class="w-10 h-10 rounded-full flex items-center justify-center font-bold text-base transition-all select-none shadow-sm"
        :class="{
          'border-2 border-black/10 dark:border-white/10 bg-tg-bg text-tg-hint/30': student.status === 0,
          'bg-[#ff3b30] text-white border-2 border-[#ff3b30]': student.status === 1,
          'bg-[#ff9500] text-white border-2 border-[#ff9500]': student.status === 2,
          'cursor-pointer active:scale-95': authStore.isAdmin,
          'cursor-default opacity-80': !authStore.isAdmin,
        }"
        :disabled="!authStore.isAdmin"
        @click="handleStatusClick"
      >
        <span v-if="student.status === 0">✔</span>
        <span v-else-if="student.status === 1">Н</span>
        <span v-else-if="student.status === 2">У</span>
      </button>
    </div>
  </div>
</template>
