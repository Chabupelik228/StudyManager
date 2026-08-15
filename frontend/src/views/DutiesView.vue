<script setup lang="ts">
import { onMounted } from 'vue';
import { useDutyStore } from '../stores/duties';
import { useAuthStore } from '../stores/auth';
import { useUiStore } from '../stores/ui';
import DutyStudentRow from '../components/duties/DutyStudentRow.vue';
import SkeletonLoader from '../components/common/SkeletonLoader.vue';
import { Save, Calendar } from 'lucide-vue-next';

const dutyStore = useDutyStore();
const authStore = useAuthStore();
const uiStore = useUiStore();

onMounted(() => {
  dutyStore.loadDuties();
});

async function handleSaveDuties() {
  const ok = await dutyStore.saveDuties();
  if (ok) {
    uiStore.showToast('Дежурные успешно назначены!', 'success');
  } else {
    uiStore.showToast('Ошибка при назначении дежурных', 'error');
  }
}
</script>

<template>
  <div class="h-full flex flex-col overflow-hidden">
    <!-- Header with Date Picker -->
    <header class="p-3.5 glass-header flex items-center justify-between sticky top-0 z-10 flex-shrink-0">
      <div class="flex items-center gap-2">
        <div class="w-8 h-8 rounded-xl bg-[#007aff]/10 text-[#007aff] flex items-center justify-center">
          <Calendar class="w-4 h-4" />
        </div>
        <div>
          <div class="font-bold text-[15px] text-tg-text leading-tight">График дежурств</div>
          <div class="text-[11px] text-tg-hint">
            {{ authStore.isAdmin ? 'Выберите студентов для назначения' : 'Очередь дежурных' }}
          </div>
        </div>
      </div>

      <input
        v-if="authStore.isAdmin"
        v-model="dutyStore.dutyDate"
        type="date"
        class="bg-black/5 dark:bg-white/10 text-[#007aff] font-bold text-xs p-2 rounded-xl border border-black/5 dark:border-white/10 outline-none focus:ring-2 focus:ring-[#007aff]"
      />
    </header>

    <!-- Students List -->
    <div class="flex-1 overflow-y-auto p-4 pb-28 space-y-3">
      <!-- Loading Skeleton -->
      <SkeletonLoader v-if="dutyStore.loading" type="duty" :count="7" />

      <!-- Students List Container -->
      <div
        v-else
        class="glass-card rounded-3xl overflow-hidden shadow-sm"
      >
        <DutyStudentRow
          v-for="s in dutyStore.duties"
          :key="s.id"
          :student="s"
          :selected="dutyStore.selectedStudentIds.includes(s.id)"
          :can-select="authStore.isAdmin"
          @toggle="dutyStore.toggleStudentSelection(s.id)"
        />
      </div>
    </div>

    <!-- Floating Save Button -->
    <button
      v-if="authStore.isAdmin && dutyStore.selectedStudentIds.length > 0"
      class="fixed bottom-20 right-5 px-5 h-14 rounded-2xl bg-gradient-to-tr from-[#0062cc] to-[#007aff] text-white flex items-center justify-center gap-2 font-bold text-sm shadow-xl active:scale-95 transition-all z-20 glow-blue"
      :disabled="dutyStore.saving"
      @click="handleSaveDuties"
    >
      <Save class="w-5 h-5" />
      <span>Назначить ({{ dutyStore.selectedStudentIds.length }})</span>
    </button>
  </div>
</template>
