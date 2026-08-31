<script setup lang="ts">
import { onMounted, watch } from 'vue';
import { useAuthStore } from './stores/auth';
import { useUiStore } from './stores/ui';
import { useWsStore } from './stores/ws';
import { tg } from './utils/telegram';

import TabBar from './components/layout/TabBar.vue';
import Toast from './components/common/Toast.vue';
import ImageViewer from './components/common/ImageViewer.vue';
import ForbiddenScreen from './components/common/ForbiddenScreen.vue';
import DebugMenu from './components/common/DebugMenu.vue';
import InAppConsole from './components/common/InAppConsole.vue';

import ScheduleView from './views/ScheduleView.vue';
import LessonDetailsView from './views/LessonDetailsView.vue';
import StatsView from './views/StatsView.vue';
import StudentAbsencesView from './views/StudentAbsencesView.vue';
import DutiesView from './views/DutiesView.vue';
import AdminView from './views/AdminView.vue';

const authStore = useAuthStore();
const uiStore = useUiStore();
const wsStore = useWsStore();

onMounted(async () => {
  await authStore.init();
  wsStore.connect();

  // Telegram BackButton handler
  if (tg?.isVersionAtLeast?.('6.1')) {
    tg.BackButton.onClick(() => {
      uiStore.goBack();
    });
  }
});

// Update Telegram BackButton visibility on active screen change
watch(
  () => uiStore.activeScreen,
  (screen) => {
    if (tg?.isVersionAtLeast?.('6.1')) {
      if (screen === 'details' || screen === 'student-absences') {
        tg.BackButton.show();
      } else {
        tg.BackButton.hide();
      }
    }
  }
);

let touchStartX = 0;
let touchStartY = 0;
let touchStartTime = 0;

function handleTouchStart(e: TouchEvent) {
  if (e.touches.length !== 1) return;
  touchStartX = e.touches[0].clientX;
  touchStartY = e.touches[0].clientY;
  touchStartTime = Date.now();
}

function handleTouchEnd(e: TouchEvent) {
  if (e.changedTouches.length !== 1) return;
  const deltaX = e.changedTouches[0].clientX - touchStartX;
  const deltaY = e.changedTouches[0].clientY - touchStartY;
  const elapsed = Date.now() - touchStartTime;

  // Horizontal right swipe detected -> Go Back
  if (elapsed < 600 && deltaX > 60 && Math.abs(deltaX) > Math.abs(deltaY) * 1.5) {
    if (uiStore.activeScreen === 'details' || uiStore.activeScreen === 'student-absences') {
      uiStore.goBack();
    }
  }
}
</script>

<template>
  <div 
    class="h-full w-full relative overflow-hidden bg-tg-secondaryBg text-tg-text"
    @touchstart="handleTouchStart"
    @touchend="handleTouchEnd"
  >
    <!-- Forbidden Screen if not in group -->
    <ForbiddenScreen v-if="authStore.isForbidden" />

    <!-- Main App Screens -->
    <template v-else>
      <main class="h-full w-full relative">
        <KeepAlive>
          <component
            :is="
              uiStore.activeScreen === 'schedule'
                ? ScheduleView
                : uiStore.activeScreen === 'details'
                ? LessonDetailsView
                : uiStore.activeScreen === 'stats'
                ? StatsView
                : uiStore.activeScreen === 'student-absences'
                ? StudentAbsencesView
                : uiStore.activeScreen === 'duties'
                ? DutiesView
                : AdminView
            "
          />
        </KeepAlive>
      </main>

      <!-- Bottom TabBar -->
      <TabBar />

      <!-- Global Overlay Components -->
      <Toast />
      <ImageViewer />
      <DebugMenu />
      <InAppConsole />
    </template>
  </div>
</template>
