<script setup lang="ts">
import { computed } from 'vue';
import type { StudentAttendance } from '../../types/attendance';
import { useAuthStore } from '../../stores/auth';
import Avatar from '../common/Avatar.vue';
import { triggerHaptic } from '../../utils/telegram';
import { Check, Edit3 } from 'lucide-vue-next';

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
    class="flex items-center justify-between p-3.5 bg-white/70 dark:bg-zinc-900/60 border-b border-black/[0.04] dark:border-white/[0.06] first:rounded-t-2xl last:rounded-b-2xl last:border-b-0 transition-colors duration-150"
    :class="{ 'bg-[#007aff]/[0.06] dark:bg-[#007aff]/10 border-l-4 !border-l-[#007aff] pl-2.5': isMe }"
  >
    <!-- Left: Avatar and Info -->
    <div class="flex items-center gap-3 min-w-0 flex-1 mr-2">
      <Avatar :tg-id="student.tg_id" :name="student.name" size="md" />

      <div class="min-w-0 flex-1">
        <div class="font-semibold text-[15px] text-tg-text flex items-center gap-1.5 truncate">
          <span class="truncate">{{ student.name }}</span>
          <span
            v-if="isMe"
            class="bg-gradient-to-r from-[#0062cc] to-[#007aff] text-white text-[9px] font-extrabold px-1.5 py-0.5 rounded-full tracking-wider uppercase shadow-sm"
          >
            Я
          </span>
          <span
            v-if="student.is_all_day"
            class="bg-black/5 dark:bg-white/10 text-tg-hint text-[9.5px] font-bold px-1.5 py-0.5 rounded-md uppercase"
          >
            Весь день
          </span>
        </div>

        <div
          v-if="student.status > 0"
          class="text-xs font-medium truncate mt-1 flex items-center gap-1 cursor-pointer transition-opacity hover:opacity-80"
          :class="student.reason ? 'text-amber-500 dark:text-amber-400' : 'text-tg-hint hover:text-tg-text'"
          @click="authStore.isAdmin ? emit('openReason', student) : null"
        >
          <Edit3 v-if="authStore.isAdmin" class="w-3 h-3 flex-shrink-0 opacity-60" />
          <span class="truncate">{{ student.reason || '+ Добавить причину' }}</span>
        </div>
      </div>
    </div>

    <!-- Right: Status Button -->
    <div class="flex items-center">
      <button
        class="w-10 h-10 rounded-2xl flex items-center justify-center font-bold text-sm transition-all duration-200 select-none shadow-sm"
        :class="{
          'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/25': student.status === 0,
          'bg-rose-500 text-white font-black glow-rose scale-105': student.status === 1,
          'bg-amber-500 text-white font-black glow-amber scale-105': student.status === 2,
          'cursor-pointer active:scale-90 hover:brightness-105': authStore.isAdmin,
          'cursor-default opacity-80': !authStore.isAdmin,
        }"
        :disabled="!authStore.isAdmin"
        @click="handleStatusClick"
      >
        <Check v-if="student.status === 0" class="w-4 h-4 stroke-[2.5]" />
        <span v-else-if="student.status === 1">Н</span>
        <span v-else-if="student.status === 2">У</span>
      </button>
    </div>
  </div>
</template>
