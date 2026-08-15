<script setup lang="ts">
import { tg } from '../../utils/telegram';
</script>

<template>
  <div class="h-screen w-screen flex flex-col items-center justify-center p-6 text-center bg-tg-secondaryBg">
    <div class="text-6xl mb-4">🚫</div>
    <h2 class="text-xl font-bold mb-2">Доступ закрыт</h2>
    <p class="text-sm text-tg-hint max-w-xs mb-8">
      Это приложение доступно только для участников учебной группы.
    </p>
    <button
      class="px-8 py-3 bg-[#007aff] text-white font-semibold rounded-xl shadow-md active:scale-95 transition-all"
      @click="tg.close()"
    >
      Закрыть
    </button>
  </div>
</template>
