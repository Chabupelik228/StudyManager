<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '../../stores/auth';
import { useUiStore } from '../../stores/ui';
import { ApiClient } from '../../api/client';
import { Monitor, KeyRound, ShieldCheck } from 'lucide-vue-next';

const authStore = useAuthStore();
const uiStore = useUiStore();

const code = ref('');
const loading = ref(false);

async function handleLogin() {
  const trimmed = code.value.trim();
  if (!trimmed) return;
  loading.value = true;
  try {
    const res = await ApiClient.post<{ token: string }>('/api/auth/login_by_code', {
      code: trimmed,
    });
    ApiClient.setToken(res.token);
    uiStore.showToast('Успешный вход!', 'success');
    await authStore.init();
    authStore.showPcLoginModal = false;
  } catch (e: any) {
    uiStore.showToast('Неверный код/пароль или срок действия истек', 'error');
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div
    v-if="authStore.showPcLoginModal"
    class="fixed inset-0 z-50 bg-black/60 backdrop-blur-md flex items-center justify-center p-4 animate-fade-in"
  >
    <div class="bg-tg-bg rounded-3xl w-full max-w-sm p-6 shadow-2xl border border-black/10 dark:border-white/10 text-center space-y-5">
      <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#007aff] to-[#5ac8fa] text-white flex items-center justify-center mx-auto shadow-lg shadow-[#007aff]/20">
        <Monitor class="w-8 h-8" />
      </div>

      <div>
        <h2 class="text-xl font-bold text-tg-text">Вход с ПК / Браузера</h2>
        <p class="text-xs text-tg-hint mt-1.5 leading-relaxed">
          Введите пароль разработчика или 6-значный код из Telegram Mini App (<i>Админка</i> → <i>Доступ с ПК</i>).
        </p>
      </div>

      <!-- Code / Password Input -->
      <div class="space-y-2.5">
        <div class="relative">
          <KeyRound class="w-5 h-5 text-tg-hint absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            v-model="code"
            type="password"
            placeholder="Код или пароль..."
            class="w-full pl-11 pr-4 py-3.5 rounded-2xl bg-tg-secondaryBg border-none text-tg-text text-center text-lg font-mono font-bold tracking-wider outline-none focus:ring-2 focus:ring-[#007aff]"
            @keyup.enter="handleLogin"
          />
        </div>

        <button
          class="w-full py-3.5 rounded-2xl bg-[#007aff] text-white font-semibold text-sm shadow-md active:scale-95 transition-all disabled:opacity-50 flex items-center justify-center gap-2"
          :disabled="!code.trim() || loading"
          @click="handleLogin"
        >
          <ShieldCheck class="w-4 h-4" />
          <span>{{ loading ? 'Проверка...' : 'Войти' }}</span>
        </button>
      </div>
    </div>
  </div>
</template>
