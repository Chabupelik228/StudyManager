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
import { ChevronLeft } from 'lucide-vue-next';
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
  // Cycle: 0 -> 1 -> 2 -> 0
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
    <div class="p-3 bg-tg-bg/90 backdrop-blur-md border-b border-black/10 dark:border-white/10 flex items-center gap-2 sticky top-0 z-10 flex-shrink-0">
      <button
        class="text-[#007aff] flex items-center font-medium text-sm p-1 -ml-1 active:opacity-70"
        @click="uiStore.switchTab('schedule')"
      >
        <ChevronLeft class="w-5 h-5" />
        <span>Назад</span>
      </button>

      <div class="flex-1 text-center pr-12 min-w-0">
        <div class="font-semibold text-base text-tg-text truncate">
          {{ attendanceStore.lessonName }}
        </div>
        <div class="text-xs text-tg-hint truncate">
          👨‍🏫 {{ attendanceStore.lessonTeacher || 'Не назначен' }}
        </div>
      </div>
    </div>

    <!-- Content List -->
    <div class="flex-1 overflow-y-auto p-4 space-y-4 pb-24">
      <!-- Admin Tools Box -->
      <div v-if="authStore.isAdmin" class="flex gap-2">
        <button
          class="flex-1 py-2.5 rounded-xl bg-tg-bg text-tg-text font-semibold text-sm shadow-sm border border-black/5 dark:border-white/5 active:scale-95 transition-all"
          @click="openRename"
        >
          Изменить
        </button>
        <button
          class="flex-1 py-2.5 rounded-xl font-semibold text-sm shadow-sm active:scale-95 transition-all"
          :class="
            attendanceStore.isCanceled
              ? 'bg-tg-bg text-tg-text border border-black/5 dark:border-white/5'
              : 'bg-[#ff3b30]/15 text-[#ff3b30] border border-[#ff3b30]/20'
          "
          @click="toggleCancelLesson"
        >
          {{ attendanceStore.isCanceled ? 'Восстановить' : 'Отменить пару' }}
        </button>
      </div>

      <!-- Attendance Summary -->
      <AttendanceSummary />

      <!-- Student Rows Card Container -->
      <div class="rounded-2xl overflow-hidden shadow-sm border border-black/5 dark:border-white/5">
        <div v-if="attendanceStore.loading" class="text-center py-12 bg-tg-bg text-tg-hint text-sm">
          Загрузка студентов...
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
            class="w-full p-3 rounded-xl bg-tg-secondaryBg border-none text-tg-text text-sm focus:ring-2 focus:ring-[#007aff] outline-none"
          />
        </div>

        <div>
          <label class="text-xs text-tg-hint font-medium mb-1 block">Преподаватель</label>
          <input
            v-model="renameTeacher"
            type="text"
            class="w-full p-3 rounded-xl bg-tg-secondaryBg border-none text-tg-text text-sm focus:ring-2 focus:ring-[#007aff] outline-none"
          />
        </div>

        <div class="flex gap-2 pt-2">
          <button
            class="flex-1 py-3 rounded-xl bg-tg-secondaryBg text-tg-text font-semibold active:scale-95 transition-all"
            @click="showRenameModal = false"
          >
            Отмена
          </button>
          <button
            class="flex-1 py-3 rounded-xl bg-[#007aff] text-white font-semibold shadow-md active:scale-95 transition-all"
            @click="handleSaveRename"
          >
            Сохранить
          </button>
        </div>
      </div>
    </Modal>
  </div>
</template>
