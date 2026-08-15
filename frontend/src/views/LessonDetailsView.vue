<script setup lang="ts">
import { ref } from 'vue';
import { useAttendanceStore } from '../stores/attendance';
import { useScheduleStore } from '../stores/schedule';
import { useAuthStore } from '../stores/auth';
import { useUiStore } from '../stores/ui';
import StudentRow from '../components/attendance/StudentRow.vue';
import AttendanceSummary from '../components/attendance/AttendanceSummary.vue';
import ReasonModal from '../components/attendance/ReasonModal.vue';
import Modal from '../components/common/Modal.vue';
import SkeletonLoader from '../components/common/SkeletonLoader.vue';
import { ChevronLeft, Edit2, Ban, RotateCcw } from 'lucide-vue-next';
import type { StudentAttendance } from '../types/attendance';

const attendanceStore = useAttendanceStore();
const scheduleStore = useScheduleStore();
const authStore = useAuthStore();
const uiStore = useUiStore();

const showRenameModal = ref(false);
const renameName = ref('');
const renameTeacher = ref('');

function openRename() {
  renameName.value = attendanceStore.lessonName;
  renameTeacher.value = attendanceStore.lessonTeacher;
  showRenameModal.value = true;
}

async function handleSaveRename() {
  await scheduleStore.updateOverride(
    attendanceStore.lessonTime,
    renameName.value,
    renameTeacher.value || null,
    attendanceStore.isCanceled ? 1 : 0
  );
  attendanceStore.lessonName = renameName.value;
  attendanceStore.lessonTeacher = renameTeacher.value;
  showRenameModal.value = false;
  uiStore.showToast('Пара изменена', 'success');
}

async function toggleCancelLesson() {
  const newCanceled = attendanceStore.isCanceled ? 0 : 1;
  await scheduleStore.updateOverride(
    attendanceStore.lessonTime,
    attendanceStore.lessonName,
    attendanceStore.lessonTeacher,
    newCanceled
  );
  attendanceStore.isCanceled = Boolean(newCanceled);
  uiStore.showToast(newCanceled ? 'Пара отменена' : 'Пара восстановлена', 'info');
}

function handleStatusToggle(s: StudentAttendance) {
  // Cycle: 0 (Present) -> 1 (Absent) -> 2 (Excused) -> 0 (Present)
  if (s.status === 0) {
    attendanceStore.updateSingleAttendance(s.id, 1, s.reason);
  } else if (s.status === 1) {
    attendanceStore.updateSingleAttendance(s.id, 2, s.reason);
  } else {
    attendanceStore.updateSingleAttendance(s.id, 0, '');
  }
}

function handleOpenReason(s: StudentAttendance) {
  attendanceStore.pendingStudent = s;
  attendanceStore.showReasonModal = true;
}
</script>

<template>
  <div class="h-full flex flex-col overflow-hidden">
    <!-- Header -->
    <header class="p-3 glass-header flex items-center gap-2 sticky top-0 z-10 flex-shrink-0">
      <button
        class="text-[#007aff] flex items-center font-semibold text-sm py-1.5 px-2 -ml-1 rounded-xl hover:bg-[#007aff]/10 active:scale-95 transition-all"
        @click="uiStore.switchTab('schedule')"
      >
        <ChevronLeft class="w-5 h-5 -ml-1" />
        <span>Назад</span>
      </button>

      <div class="flex-1 text-center pr-8 min-w-0">
        <div class="font-bold text-base text-tg-text truncate leading-tight">
          {{ attendanceStore.lessonName }}
        </div>
        <div class="text-xs text-tg-hint truncate mt-0.5">
          👨‍🏫 {{ attendanceStore.lessonTeacher || 'Преподаватель не назначен' }}
        </div>
      </div>
    </header>

    <!-- Content List -->
    <div class="flex-1 overflow-y-auto p-4 space-y-4 pb-28">
      <!-- Admin Tools Box -->
      <div v-if="authStore.isAdmin" class="flex gap-2">
        <button
          class="flex-1 py-2.5 px-3 rounded-2xl glass-card text-tg-text font-semibold text-xs flex items-center justify-center gap-1.5 active:scale-95 transition-all hover:border-[#007aff]/30"
          @click="openRename"
        >
          <Edit2 class="w-3.5 h-3.5 opacity-70" />
          <span>Изменить пару</span>
        </button>
        <button
          class="flex-1 py-2.5 px-3 rounded-2xl font-semibold text-xs flex items-center justify-center gap-1.5 active:scale-95 transition-all shadow-sm"
          :class="
            attendanceStore.isCanceled
              ? 'glass-card text-emerald-600 dark:text-emerald-400 border-emerald-500/30'
              : 'bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/20'
          "
          @click="toggleCancelLesson"
        >
          <RotateCcw v-if="attendanceStore.isCanceled" class="w-3.5 h-3.5" />
          <Ban v-else class="w-3.5 h-3.5" />
          <span>{{ attendanceStore.isCanceled ? 'Восстановить' : 'Отменить пару' }}</span>
        </button>
      </div>

      <!-- Attendance Summary -->
      <AttendanceSummary />

      <!-- Student Rows Card Container -->
      <div class="glass-card rounded-3xl overflow-hidden">
        <div v-if="attendanceStore.loading" class="p-3">
          <SkeletonLoader type="row" :count="6" />
        </div>

        <template v-else>
          <StudentRow
            v-for="s in attendanceStore.filteredStudents"
            :key="s.id"
            :student="s"
            @toggle-status="handleStatusToggle"
            @open-reason="handleOpenReason"
          />
        </template>
      </div>
    </div>

    <!-- Reason Modal -->
    <ReasonModal />

    <!-- Edit/Rename Lesson Modal -->
    <Modal :show="showRenameModal" title="Редактировать пару" @close="showRenameModal = false">
      <div class="space-y-3">
        <div>
          <label class="text-xs text-tg-hint font-medium mb-1 block">Название предмета</label>
          <input
            v-model="renameName"
            type="text"
            class="w-full p-3 rounded-xl bg-black/5 dark:bg-white/5 border border-black/10 dark:border-white/10 text-tg-text text-sm focus:ring-2 focus:ring-[#007aff] outline-none"
          />
        </div>

        <div>
          <label class="text-xs text-tg-hint font-medium mb-1 block">Преподаватель</label>
          <input
            v-model="renameTeacher"
            type="text"
            class="w-full p-3 rounded-xl bg-black/5 dark:bg-white/5 border border-black/10 dark:border-white/10 text-tg-text text-sm focus:ring-2 focus:ring-[#007aff] outline-none"
          />
        </div>

        <div class="flex gap-2 pt-2">
          <button
            class="flex-1 py-3 rounded-xl bg-black/5 dark:bg-white/10 text-tg-text font-semibold active:scale-95 transition-all"
            @click="showRenameModal = false"
          >
            Отмена
          </button>
          <button
            class="flex-1 py-3 rounded-xl bg-[#007aff] text-white font-semibold shadow-md active:scale-95 transition-all glow-blue"
            @click="handleSaveRename"
          >
            Сохранить
          </button>
        </div>
      </div>
    </Modal>
  </div>
</template>
