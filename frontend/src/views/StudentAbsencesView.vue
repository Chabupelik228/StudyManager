<script setup lang="ts">
import { useStatsStore } from '../stores/stats';
import { useUiStore } from '../stores/ui';
import SubjectStatsList from '../components/stats/SubjectStatsList.vue';
import SkeletonLoader from '../components/common/SkeletonLoader.vue';
import { ChevronLeft, Calendar, BookOpen, Sparkles } from 'lucide-vue-next';

const statsStore = useStatsStore();
const uiStore = useUiStore();
</script>

<template>
  <div class="h-full flex flex-col overflow-hidden">
    <!-- Header -->
    <header class="p-3 glass-header flex items-center gap-2 sticky top-0 z-10 flex-shrink-0">
      <button
        class="text-[#007aff] flex items-center font-semibold text-sm py-1.5 px-2 -ml-1 rounded-xl hover:bg-[#007aff]/10 active:scale-95 transition-all"
        @click="uiStore.switchTab('stats')"
      >
        <ChevronLeft class="w-5 h-5 -ml-1" />
        <span>Назад</span>
      </button>

      <div class="flex-1 text-center pr-8 font-bold text-base text-tg-text truncate">
        {{ statsStore.selectedStudent?.name || 'Студент' }}
      </div>
    </header>

    <!-- Subtab Switcher -->
    <div class="p-3 glass-header border-t-0 flex-shrink-0">
      <div class="bg-black/5 dark:bg-white/10 p-1 rounded-2xl flex">
        <button
          class="flex-1 py-1.5 rounded-xl text-xs font-bold transition-all select-none flex items-center justify-center gap-1.5"
          :class="
            statsStore.subTab === 'history'
              ? 'bg-white dark:bg-zinc-800 text-[#007aff] shadow-sm'
              : 'text-tg-hint hover:text-tg-text'
          "
          @click="statsStore.subTab = 'history'"
        >
          <Calendar class="w-3.5 h-3.5" />
          <span>История пропусков</span>
        </button>
        <button
          class="flex-1 py-1.5 rounded-xl text-xs font-bold transition-all select-none flex items-center justify-center gap-1.5"
          :class="
            statsStore.subTab === 'subjects'
              ? 'bg-white dark:bg-zinc-800 text-[#007aff] shadow-sm'
              : 'text-tg-hint hover:text-tg-text'
          "
          @click="statsStore.subTab = 'subjects'"
        >
          <BookOpen class="w-3.5 h-3.5" />
          <span>По предметам</span>
        </button>
      </div>
    </div>

    <!-- Scrollable Content -->
    <div class="flex-1 overflow-y-auto p-4 space-y-3 pb-28">
      <SkeletonLoader v-if="statsStore.drilldownLoading" type="row" :count="5" />

      <!-- Tab 1: History of absences -->
      <template v-else-if="statsStore.subTab === 'history'">
        <div
          v-if="statsStore.absences.length === 0"
          class="glass-card rounded-3xl p-8 my-8 text-center flex flex-col items-center justify-center space-y-2"
        >
          <div class="w-12 h-12 rounded-2xl bg-emerald-500/10 text-emerald-500 flex items-center justify-center mb-1">
            <Sparkles class="w-6 h-6" />
          </div>
          <h3 class="text-base font-bold text-tg-text">Идеальная посещаемость!</h3>
          <p class="text-xs text-tg-hint">У студента нет пропусков в этом месяце 👏</p>
        </div>

        <div
          v-for="(a, idx) in statsStore.absences"
          :key="idx"
          class="glass-card rounded-2xl p-3.5 flex items-center justify-between gap-3"
        >
          <!-- Left: time + name + reason -->
          <div class="min-w-0 flex-1">
            <div class="flex items-center gap-2">
              <span class="text-xs font-extrabold text-[#007aff]">{{ a.date }}</span>
              <span class="text-xs font-semibold text-tg-hint">{{ a.time }}</span>
            </div>
            <div class="text-[14.5px] font-semibold text-tg-text truncate mt-0.5">
              {{ a.name }}
            </div>
            <div v-if="a.reason" class="text-xs text-amber-500 font-medium truncate mt-0.5">
              {{ a.reason }}
            </div>
          </div>

          <!-- Right: badge Н / У -->
          <div class="flex-shrink-0">
            <span
              class="w-8 h-8 rounded-xl flex items-center justify-center font-black text-xs text-white shadow-sm"
              :class="a.status === 1 ? 'bg-rose-500 glow-rose' : 'bg-amber-500 glow-amber'"
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
