<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useScheduleStore } from '../stores/schedule';
import { useAttendanceStore } from '../stores/attendance';
import { useAuthStore } from '../stores/auth';
import { useUiStore } from '../stores/ui';
import DatePill from '../components/schedule/DatePill.vue';
import LessonCard from '../components/schedule/LessonCard.vue';
import AddLessonModal from '../components/schedule/AddLessonModal.vue';
import SkeletonLoader from '../components/common/SkeletonLoader.vue';
import { Plus, Sparkles } from 'lucide-vue-next';

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
    <header class="p-3 glass-header sticky top-0 z-10 flex-shrink-0">
      <DatePill />
    </header>

    <!-- Lessons List with inner scrolling -->
    <div class="flex-1 overflow-y-auto p-4 space-y-3 pb-28">
      <!-- Loading Skeleton with Shimmer -->
      <SkeletonLoader v-if="scheduleStore.loading" type="card" :count="3" />

      <!-- Empty State -->
      <div
        v-else-if="scheduleStore.lessons.length === 0"
        class="glass-card rounded-3xl p-8 my-8 text-center flex flex-col items-center justify-center space-y-3"
      >
        <div class="w-14 h-14 rounded-2xl bg-[#007aff]/10 text-[#007aff] flex items-center justify-center mb-1">
          <Sparkles class="w-7 h-7" />
        </div>
        <h3 class="text-base font-bold text-tg-text">Выходной день!</h3>
        <p class="text-xs text-tg-hint max-w-[220px]">
          На выбранную дату пары не запланированы. Можно отдохнуть 🎉
        </p>
      </div>

      <!-- Actual Lessons -->
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
      class="fixed bottom-20 right-5 w-14 h-14 rounded-2xl bg-gradient-to-tr from-[#0062cc] to-[#007aff] text-white flex items-center justify-center shadow-lg active:scale-95 transition-all z-20 glow-blue"
      @click="showAddModal = true"
    >
      <Plus class="w-7 h-7" />
    </button>

    <!-- Add Lesson Modal -->
    <AddLessonModal :show="showAddModal" @close="showAddModal = false" />
  </div>
</template>
