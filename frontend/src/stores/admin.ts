import { defineStore } from 'pinia';
import { ref } from 'vue';
import { ApiClient } from '../api/client';
import type { AdminUser, AdminUsersResponse, ActionLogItem, AdminLogsResponse } from '../types/admin';

export const useAdminStore = defineStore('admin', () => {
  const admins = ref<AdminUser[]>([]);
  const logs = ref<ActionLogItem[]>([]);
  const filterUsers = ref<string[]>([]);
  const filterActions = ref<string[]>([]);
  const selectedUserFilter = ref<string>('all');
  const selectedActionFilter = ref<string>('all');
  const offset = ref<number>(0);
  const hasMoreLogs = ref<boolean>(true);
  const loading = ref<boolean>(false);
  const loadingLogs = ref<boolean>(false);

  async function loadAdmins() {
    loading.value = true;
    try {
      const res = await ApiClient.get<AdminUsersResponse>('/api/admin/users');
      admins.value = res.admins || [];
    } catch (e) {
      console.error('Failed to load admins', e);
    } finally {
      loading.value = false;
    }
  }

  async function loadLogs(reset = false) {
    if (reset) {
      offset.value = 0;
      logs.value = [];
      hasMoreLogs.value = true;
    }

    loadingLogs.value = true;
    try {
      const url = `/api/admin/logs?offset=${offset.value}&limit=20&user_filter=${encodeURIComponent(
        selectedUserFilter.value
      )}&action_filter=${encodeURIComponent(selectedActionFilter.value)}`;

      const res = await ApiClient.get<AdminLogsResponse>(url);
      const newLogs = res.logs || [];

      if (reset) {
        logs.value = newLogs;
        filterUsers.value = res.filter_users || [];
        filterActions.value = res.filter_actions || [];
      } else {
        logs.value.push(...newLogs);
      }

      hasMoreLogs.value = newLogs.length === 20;
      offset.value += newLogs.length;
    } catch (e) {
      console.error('Failed to load logs', e);
    } finally {
      loadingLogs.value = false;
    }
  }

  async function deleteLog(logId: number) {
    try {
      await ApiClient.delete(`/api/admin/logs/${logId}`);
      logs.value = logs.value.filter((l) => l.id !== logId);
    } catch (e) {
      console.error('Failed to delete log', e);
    }
  }

  async function resetMyAiLimits() {
    try {
      await ApiClient.post('/api/admin/reset_my_limits');
    } catch (e) {
      console.error('Failed to reset AI limits', e);
    }
  }

  return {
    admins,
    logs,
    filterUsers,
    filterActions,
    selectedUserFilter,
    selectedActionFilter,
    hasMoreLogs,
    loading,
    loadingLogs,
    loadAdmins,
    loadLogs,
    deleteLog,
    resetMyAiLimits,
  };
});
