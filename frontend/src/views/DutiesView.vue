<script setup lang="ts">
import { onMounted } from 'vue';
import { useDutyStore } from '../stores/duties';
import { useAuthStore } from '../stores/auth';
import { useUiStore } from '../stores/ui';
import DutyStudentRow from '../components/duties/DutyStudentRow.vue';
import { Save } from 'lucide-vue-next';

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
    <div class="p-3.5 bg-tg-bg/90 backdrop-blur-md border-b border-black/10 dark:border-white/10 flex items-center justify-between sticky top-0 z-10 flex-shrink-0">
      <div class="font-bold text-base text-tg-text">Назначение дежурных</div>
      <input
        v-model="dutyStore.dutyDate"
        type="date"
        class="bg-tg-secondaryBg text-[#007aff] font-bold text-xs p-2 rounded-xl border-none outline-none focus:ring-2 focus:ring-[#007aff]"
      />
    </div>

    <!-- Students List -->
    <div class="flex-1 overflow-y-auto p-4 pb-24">
      <div v-if="dutyStore.loading" class="text-center py-12 text-tg-hint text-sm">
        Загрузка списка дежурных...
      </div>

      <div
        v-else
        class="rounded-2xl overflow-hidden shadow-sm border border-black/5 dark:border-white/5 bg-tg-bg"
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
      class="fixed bottom-20 right-5 w-14 h-14 rounded-full bg-[#007aff] text-white flex items-center justify-center shadow-xl active:scale-95 transition-all z-20"
      :disabled="dutyStore.saving"
      @click="handleSaveDuties"
    >
      <Save class="w-6 h-6" />
    </button>
  </div>
</template>
