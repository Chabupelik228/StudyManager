<script setup lang="ts">
import { onMounted } from 'vue';
import { useAdminStore } from '../stores/admin';

import { useUiStore } from '../stores/ui';
import AdminOnlineCard from '../components/admin/AdminOnlineCard.vue';
import LogFilters from '../components/admin/LogFilters.vue';
import LogCard from '../components/admin/LogCard.vue';
import { RefreshCw } from 'lucide-vue-next';

const adminStore = useAdminStore();
const uiStore = useUiStore();

onMounted(() => {
  adminStore.loadAdmins();
  adminStore.loadLogs(true);
});

async function handleDeleteLog(id: number) {
  await adminStore.deleteLog(id);
  uiStore.showToast('Запись удалена', 'info');
}
</script>

<template>
  <div class="h-full flex flex-col overflow-hidden">
    <!-- Header -->
    <div class="p-3.5 bg-tg-bg/90 backdrop-blur-md border-b border-black/10 dark:border-white/10 text-center font-bold text-base sticky top-0 z-10 flex-shrink-0">
      Панель управления
    </div>

    <!-- Scrollable content -->
    <div class="flex-1 overflow-y-auto p-4 space-y-4 pb-24">
      <!-- Section 1: Admins Network -->
      <div class="bg-tg-bg rounded-2xl p-4 shadow-sm border border-black/5 dark:border-white/5 space-y-3">
        <div class="text-xs font-bold text-tg-hint uppercase tracking-wider">
          Сеть администраторов
        </div>

        <div v-if="adminStore.loading" class="text-center py-4 text-tg-hint text-xs">
          Загрузка администраторов...
        </div>

        <div v-else class="space-y-1">
          <AdminOnlineCard
            v-for="a in adminStore.admins"
            :key="a.id"
            :admin="a"
          />
        </div>
      </div>

      <!-- Section 3: Action Logs -->
      <div class="bg-tg-bg rounded-2xl p-4 shadow-sm border border-black/5 dark:border-white/5 space-y-3">
        <div class="flex items-center justify-between">
          <div class="text-xs font-bold text-tg-hint uppercase tracking-wider">
            Журнал действий
          </div>
          <button
            class="text-tg-hint hover:text-tg-text p-1"
            title="Обновить журнал"
            @click="adminStore.loadLogs(true)"
          >
            <RefreshCw class="w-3.5 h-3.5" :class="{ 'animate-spin': adminStore.loadingLogs }" />
          </button>
        </div>

        <!-- Filters -->
        <LogFilters />

        <!-- Logs list -->
        <div v-if="adminStore.logs.length === 0" class="text-center py-6 text-tg-hint text-xs">
          Записей нет
        </div>

        <div v-else class="space-y-2.5">
          <LogCard
            v-for="l in adminStore.logs"
            :key="l.id"
            :log="l"
            @delete="handleDeleteLog"
          />
        </div>

        <!-- Load More Button -->
        <button
          v-if="adminStore.hasMoreLogs"
          class="w-full py-2.5 mt-2 rounded-xl bg-tg-secondaryBg text-tg-text text-xs font-semibold hover:bg-black/5 dark:hover:bg-white/5 active:scale-98 transition-all"
          :disabled="adminStore.loadingLogs"
          @click="adminStore.loadLogs(false)"
        >
          {{ adminStore.loadingLogs ? 'Загрузка...' : 'Загрузить еще' }}
        </button>
      </div>
    </div>
  </div>
</template>
