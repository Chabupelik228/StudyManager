import { defineStore } from 'pinia';
import { ref } from 'vue';
import { ApiClient } from '../api/client';
import { toApiDate } from '../utils/date';
import type { DutyStudent, DutiesResponse } from '../types/duty';

export const useDutyStore = defineStore('duties', () => {
  const dutyDate = ref<string>('');
  const duties = ref<DutyStudent[]>([]);
  const selectedStudentIds = ref<number[]>([]);
  const loading = ref(false);
  const saving = ref(false);

  // Initialize duty date as tomorrow by default
  function initDefaultDate() {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    dutyDate.value = toApiDate(tomorrow);
  }

  async function loadDuties() {
    if (!dutyDate.value) {
      initDefaultDate();
    }
    loading.value = true;
    try {
      const res = await ApiClient.get<DutiesResponse>('/api/duties');
      duties.value = res.duties || [];
    } catch (e) {
      console.error('Failed to load duties', e);
    } finally {
      loading.value = false;
    }
  }

  function toggleStudentSelection(id: number) {
    const idx = selectedStudentIds.value.indexOf(id);
    if (idx >= 0) {
      selectedStudentIds.value.splice(idx, 1);
    } else {
      selectedStudentIds.value.push(id);
    }
  }

  async function saveDuties(): Promise<boolean> {
    if (!selectedStudentIds.value.length || !dutyDate.value) return false;
    saving.value = true;
    try {
      await ApiClient.post('/api/duties/assign', {
        date: dutyDate.value,
        student_ids: selectedStudentIds.value,
      });
      selectedStudentIds.value = [];
      await loadDuties();
      return true;
    } catch (e) {
      console.error('Failed to assign duties', e);
      return false;
    } finally {
      saving.value = false;
    }
  }

  return {
    dutyDate,
    duties,
    selectedStudentIds,
    loading,
    saving,
    initDefaultDate,
    loadDuties,
    toggleStudentSelection,
    saveDuties,
  };
});
