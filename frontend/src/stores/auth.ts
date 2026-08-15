import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { ApiClient } from '../api/client';
import { tg } from '../utils/telegram';

export type UserRole = 'viewer' | 'admin' | 'super';

export const useAuthStore = defineStore('auth', () => {
  const role = ref<UserRole>('viewer');
  const user = ref<{ id: number; first_name: string } | null>(null);
  const isForbidden = ref(false);
  const showPcLoginModal = ref(false);
  const debugRoleOverride = ref<UserRole | null>(null);

  const effectiveRole = computed(() => debugRoleOverride.value || role.value);
  const isAdmin = computed(() => effectiveRole.value === 'admin' || effectiveRole.value === 'super');
  const isSuperAdmin = computed(() => effectiveRole.value === 'super' || (user.value?.id === 620159705));
  const myTgId = computed(() => user.value?.id || tg.initDataUnsafe?.user?.id || 0);

  async function init() {
    // If running in regular browser without TG WebApp and no JWT token, show PC login modal
    if (!tg.initData && !ApiClient.getToken()) {
      showPcLoginModal.value = true;
      return;
    }

    try {
      const data = await ApiClient.get('/api/init');
      if (data) {
        role.value = data.role === 'admin' ? 'admin' : 'viewer';
        user.value = data.user;
        isForbidden.value = false;
        showPcLoginModal.value = false;

        // Superadmin check
        if (user.value?.id === 620159705) {
          role.value = 'super';
        }

        if (isAdmin.value) {
          ApiClient.get('/api/admin/ping').catch(() => {});
        }
      }
    } catch (e: any) {
      if (e.message === 'FORBIDDEN_NOT_IN_GROUP') {
        isForbidden.value = true;
      } else if (e.message === 'UNAUTHORIZED') {
        showPcLoginModal.value = true;
      }
    }
  }

  function setDebugRole(newRole: UserRole) {
    debugRoleOverride.value = newRole;
  }



  return {
    role,
    user,
    isForbidden,
    showPcLoginModal,
    effectiveRole,
    isAdmin,
    isSuperAdmin,
    myTgId,
    init,
    setDebugRole,
  };
});
