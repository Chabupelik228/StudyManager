<script setup lang="ts">
import { useAdminStore } from '../../stores/admin';

const adminStore = useAdminStore();

function handleChange() {
  adminStore.loadLogs(true);
}
</script>

<template>
  <div class="grid grid-cols-2 gap-2 mb-3">
    <!-- User Filter -->
    <select
      v-model="adminStore.selectedUserFilter"
      class="p-2.5 rounded-xl bg-tg-secondaryBg border border-black/10 dark:border-white/10 text-xs font-medium text-tg-text outline-none focus:ring-2 focus:ring-[#007aff]"
      @change="handleChange"
    >
      <option value="all">Все пользователи</option>
      <option v-for="u in adminStore.filterUsers" :key="u" :value="u">
        {{ u }}
      </option>
    </select>

    <!-- Action Filter -->
    <select
      v-model="adminStore.selectedActionFilter"
      class="p-2.5 rounded-xl bg-tg-secondaryBg border border-black/10 dark:border-white/10 text-xs font-medium text-tg-text outline-none focus:ring-2 focus:ring-[#007aff]"
      @change="handleChange"
    >
      <option value="all">Все действия</option>
      <option v-for="a in adminStore.filterActions" :key="a" :value="a">
        {{ a }}
      </option>
    </select>
  </div>
</template>
