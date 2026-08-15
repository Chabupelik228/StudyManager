<script setup lang="ts">
import { useStatsStore } from '../../stores/stats';

const statsStore = useStatsStore();
</script>

<template>
  <div class="space-y-3">
    <!-- Sub Sort Bar -->
    <div class="flex items-center gap-2 px-1">
      <button
        class="text-[11px] font-bold uppercase px-2.5 py-1 rounded-md transition-all"
        :class="
          statsStore.subSort === 'hours'
            ? 'bg-[#007aff]/10 text-[#007aff]'
            : 'text-tg-hint hover:text-tg-text'
        "
        @click="statsStore.subSort = 'hours'"
      >
        По часам
      </button>
      <button
        class="text-[11px] font-bold uppercase px-2.5 py-1 rounded-md transition-all"
        :class="
          statsStore.subSort === 'name'
            ? 'bg-[#007aff]/10 text-[#007aff]'
            : 'text-tg-hint hover:text-tg-text'
        "
        @click="statsStore.subSort = 'name'"
      >
        По названию
      </button>
    </div>

    <!-- Cards List -->
    <div v-if="statsStore.sortedSubjectStats.length === 0" class="text-center py-8 text-tg-hint text-sm">
      Нет данных по предметам
    </div>

    <div
      v-for="sub in statsStore.sortedSubjectStats"
      :key="sub.subject"
      class="bg-tg-bg rounded-2xl p-4 shadow-sm border border-black/5 dark:border-white/5 flex items-center gap-3.5"
    >
      <!-- Icon badge -->
      <div
        class="w-10 h-10 rounded-xl bg-gradient-to-br from-gray-500 to-gray-700 text-white font-extrabold text-base flex items-center justify-center flex-shrink-0"
      >
        {{ sub.subject.slice(0, 2).toUpperCase() }}
      </div>

      <!-- Subject info -->
      <div class="flex-1 min-w-0">
        <div class="text-[15px] font-semibold leading-snug text-tg-text mb-1">
          {{ sub.subject }}
        </div>
        <div class="text-xs text-tg-hint truncate">
          👨‍🏫 {{ sub.teacher || '—' }}
        </div>
      </div>

      <!-- Hours -->
      <div class="text-right flex-shrink-0">
        <div class="text-base font-bold text-tg-text">
          {{ sub.missed_all }} / {{ sub.total_all }} ч.
        </div>
        <div v-if="sub.missed_month > 0" class="text-[11px] font-bold text-[#ff3b30] mt-0.5">
          +{{ sub.missed_month }} в этом мес.
        </div>
      </div>
    </div>
  </div>
</template>
