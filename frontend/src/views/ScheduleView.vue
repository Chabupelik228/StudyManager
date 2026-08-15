<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useScheduleStore } from '../stores/schedule';
import { useAttendanceStore } from '../stores/attendance';
import { useAuthStore } from '../stores/auth';
import { useUiStore } from '../stores/ui';
import DatePill from '../components/schedule/DatePill.vue';
import LessonCard from '../components/schedule/LessonCard.vue';
import AddLessonModal from '../components/schedule/AddLessonModal.vue';
import { Plus } from 'lucide-vue-next';

const scheduleStore = useScheduleStore();
const attendanceStore = useAttendanceStore();
const authStore = useAuthStore();
const uiStore = useUiStore();

const showAddModal = ref(false);

onMounted(() => {
  scheduleStore.loadSchedule();
});

function openDetails(lesson: any) {
  attendanceStore.loadDetails(lesson.time, lesson.name, lesson.teacher, lesson.canceled);
  uiStore.switchTab('details');
}
</script>

<template>
  <div class="h-full flex flex-col overflow-hidden">
    <!-- Header with Date Pill -->
    <div class="p-3 bg-tg-bg/85 backdrop-blur-md border-b border-black/10 dark:border-white/10 sticky top-0 z-10 flex-shrink-0">
      <DatePill />
    </div>

    <!-- Lessons List with inner scrolling -->
    <div class="flex-1 overflow-y-auto p-4 space-y-3 pb-24">
      <div v-if="scheduleStore.loading" class="text-center py-12 text-tg-hint text-sm">
        Загрузка расписания...
      </div>

      <div
        v-else-if="scheduleStore.lessons.length === 0"
        class="text-center py-16 text-tg-hint text-base"
      >
        На этот день пар нет 🎉
      </div>

      <template v-else>
        <LessonCard
          v-for="l in scheduleStore.lessons"
          :key="l.time"
          :lesson="l"
          @click="openDetails(l)"
        />
      </template>
    </div>

    <!-- Floating Add Button for Admins -->
    <button
      v-if="authStore.isAdmin"
      class="fixed bottom-20 right-5 w-14 h-14 rounded-full bg-[#007aff] text-white flex items-center justify-center shadow-xl active:scale-95 transition-all z-20"
      @click="showAddModal = true"
    >
      <Plus class="w-7 h-7" />
    </button>

    <!-- Add Lesson Modal -->
    <AddLessonModal :show="showAddModal" @close="showAddModal = false" />
  </div>
</template>
