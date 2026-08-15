<script setup lang="ts">
import type { ActionLogItem } from '../../types/admin';
import { useAuthStore } from '../../stores/auth';
import { formatDateTime } from '../../utils/date';
import { Trash2 } from 'lucide-vue-next';

defineProps<{
  log: ActionLogItem;
}>();

const emit = defineEmits<{
  (e: 'delete', id: number): void;
}>();

const authStore = useAuthStore();
</script>

<template>
  <div class="bg-tg-secondaryBg rounded-xl p-3 border-l-4 border-l-[#007aff] shadow-sm animate-fade-in">
    <!-- Header -->
    <div class="flex items-center justify-between text-[11px] text-tg-hint mb-1">
      <span class="font-semibold text-tg-text">👤 {{ log.admin_name }}</span>
      <span>{{ formatDateTime(log.created_at) }}</span>
    </div>

    <!-- Body -->
    <div class="flex items-start justify-between gap-2">
      <div class="text-sm font-semibold text-tg-text leading-tight">
        {{ log.action_type }}
      </div>

      <!-- Delete Button (Superadmin only) -->
      <button
        v-if="authStore.isSuperAdmin"
        class="text-tg-hint hover:text-[#ff3b30] p-1 -mr-1 -mt-1 active:scale-90 transition-all flex-shrink-0"
        title="Удалить запись"
        @click="emit('delete', log.id)"
      >
        <Trash2 class="w-4 h-4" />
      </button>
    </div>

    <!-- Details -->
    <div class="text-xs text-tg-hint mt-1.5 whitespace-pre-line leading-relaxed font-mono">
      {{ log.details }}
    </div>
  </div>
</template>
