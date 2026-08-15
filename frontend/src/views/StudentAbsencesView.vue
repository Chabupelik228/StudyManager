<script setup lang="ts">
import { useStatsStore } from '../stores/stats';
import { useUiStore } from '../stores/ui';
import SubjectStatsList from '../components/stats/SubjectStatsList.vue';
import { ChevronLeft } from 'lucide-vue-next';

const statsStore = useStatsStore();
const uiStore = useUiStore();
</script>

<template>
  <div class="h-full flex flex-col overflow-hidden">
    <!-- Header -->
    <div class="p-3 bg-tg-bg/90 backdrop-blur-md border-b border-black/10 dark:border-white/10 flex items-center gap-2 sticky top-0 z-10 flex-shrink-0">
      <button
        class="text-[#007aff] flex items-center font-medium text-sm p-1 -ml-1 active:opacity-70"
        @click="uiStore.switchTab('stats')"
      >
        <ChevronLeft class="w-5 h-5" />
        <span>Назад</span>
      </button>

      <div class="flex-1 text-center pr-12 font-bold text-base text-tg-text truncate">
        {{ statsStore.selectedStudent?.name || 'Студент' }}
      </div>
    </div>

    <!-- Subtab Switcher -->
    <div class="p-3 bg-tg-bg border-b border-black/5 dark:border-white/5 flex-shrink-0">
      <div class="bg-tg-secondaryBg p-1 rounded-xl flex">
        <button
          class="flex-1 py-1.5 rounded-lg text-xs font-semibold transition-all select-none"
          :class="
            statsStore.subTab === 'history'
              ? 'bg-tg-bg text-[#007aff] shadow-sm'
              : 'text-tg-hint hover:text-tg-text'
          "
          @click="statsStore.subTab = 'history'"
        >
          История
        </button>
        <button
          class="flex-1 py-1.5 rounded-lg text-xs font-semibold transition-all select-none"
          :class="
            statsStore.subTab === 'subjects'
              ? 'bg-tg-bg text-[#007aff] shadow-sm'
              : 'text-tg-hint hover:text-tg-text'
          "
          @click="statsStore.subTab = 'subjects'"
        >
          По предметам
        </button>
      </div>
    </div>

    <!-- Scrollable Content -->
    <div class="flex-1 overflow-y-auto p-4 space-y-3 pb-24">
      <div v-if="statsStore.drilldownLoading" class="text-center py-12 text-tg-hint text-sm">
        Загрузка данных...
      </div>

      <!-- Tab 1: History of absences -->
      <template v-else-if="statsStore.subTab === 'history'">
        <div v-if="statsStore.absences.length === 0" class="text-center py-16 text-tg-hint text-sm">
          Пропусков нет 👏
        </div>

        <div
          v-for="(a, idx) in statsStore.absences"
          :key="idx"
          class="bg-tg-bg rounded-2xl p-3.5 shadow-sm border border-black/5 dark:border-white/5 flex items-center justify-between gap-3"
        >
          <!-- Left: time + name + reason -->
          <div class="min-w-0">
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold text-[#007aff]">{{ a.date }}</span>
              <span class="text-xs font-semibold text-tg-hint">{{ a.time }}</span>
            </div>
            <div class="text-sm font-medium text-tg-text truncate mt-0.5">
              {{ a.name }}
            </div>
            <div v-if="a.reason" class="text-xs text-[#ff9500] font-medium truncate mt-0.5">
              {{ a.reason }}
            </div>
          </div>

          <!-- Right: badge Н / У -->
          <div class="flex-shrink-0">
            <span
              class="w-7 h-7 rounded-full flex items-center justify-center font-bold text-xs text-white"
              :class="a.status === 1 ? 'bg-[#ff3b30]' : 'bg-[#ff9500]'"
            >
              {{ a.status === 1 ? 'Н' : 'У' }}
            </span>
          </div>
        </div>
      </template>

      <!-- Tab 2: By Subjects -->
      <template v-else-if="statsStore.subTab === 'subjects'">
        <SubjectStatsList />
      </template>
    </div>
  </div>
</template>
