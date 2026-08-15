<script setup lang="ts">
import { ref } from 'vue';
import { useScheduleStore } from '../../stores/schedule';
import Modal from '../common/Modal.vue';

const props = defineProps<{
  show: boolean;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
}>();

const scheduleStore = useScheduleStore();
const time = ref('');
const name = ref('');
const teacher = ref('');
const saving = ref(false);

async function handleSave() {
  if (!time.value || !name.value) return;
  saving.value = true;
  try {
    await scheduleStore.updateOverride(time.value, name.value, teacher.value || null, 0);
    time.value = '';
    name.value = '';
    teacher.value = '';
    emit('close');
  } catch (e) {
    console.error('Failed to add lesson', e);
  } finally {
    saving.value = false;
  }
}
</script>

<template>
  <Modal :show="props.show" title="Добавить пару" @close="emit('close')">
    <div class="space-y-3">
      <div>
        <label class="text-xs text-tg-hint font-medium mb-1 block">Время начала</label>
        <input
          v-model="time"
          type="time"
          class="w-full p-3 rounded-xl bg-tg-secondaryBg border-none text-tg-text text-sm focus:ring-2 focus:ring-[#007aff] outline-none"
        />
      </div>

      <div>
        <label class="text-xs text-tg-hint font-medium mb-1 block">Название предмета</label>
        <input
          v-model="name"
          type="text"
          placeholder="Например, Математика"
          class="w-full p-3 rounded-xl bg-tg-secondaryBg border-none text-tg-text text-sm focus:ring-2 focus:ring-[#007aff] outline-none"
        />
      </div>

      <div>
        <label class="text-xs text-tg-hint font-medium mb-1 block">Преподаватель</label>
        <input
          v-model="teacher"
          type="text"
          placeholder="Иванов И.И."
          class="w-full p-3 rounded-xl bg-tg-secondaryBg border-none text-tg-text text-sm focus:ring-2 focus:ring-[#007aff] outline-none"
        />
      </div>

      <div class="flex gap-2 pt-2">
        <button
          class="flex-1 py-3 rounded-xl bg-tg-secondaryBg text-tg-text font-semibold active:scale-95 transition-all"
          @click="emit('close')"
        >
          Отмена
        </button>
        <button
          class="flex-1 py-3 rounded-xl bg-[#007aff] text-white font-semibold shadow-md active:scale-95 transition-all disabled:opacity-50"
          :disabled="!time || !name || saving"
          @click="handleSave"
        >
          {{ saving ? 'Сохранение...' : 'Готово' }}
        </button>
      </div>
    </div>
  </Modal>
</template>
