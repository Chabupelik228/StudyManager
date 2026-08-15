/**
 * Safe Telegram WebApp SDK Wrapper
 */

declare global {
  interface Window {
    Telegram?: {
      WebApp: any;
    };
  }
}

export const tg = typeof window !== 'undefined' && window.Telegram?.WebApp
  ? window.Telegram.WebApp
  : {
      initData: '',
      initDataUnsafe: { user: { id: 0, first_name: 'Guest' } },
      expand: () => {},
      ready: () => {},
      close: () => {},
      BackButton: {
        show: () => {},
        hide: () => {},
        onClick: (_cb: () => void) => {},
        offClick: (_cb: () => void) => {},
      },
      HapticFeedback: {
        impactOccurred: (_style: 'light' | 'medium' | 'heavy' | 'rigid' | 'soft') => {},
        notificationOccurred: (_type: 'error' | 'success' | 'warning') => {},
        selectionChanged: () => {},
      },
      showAlert: (msg: string) => alert(msg),
      showConfirm: (msg: string, cb: (ok: boolean) => void) => cb(confirm(msg)),
      showPopup: (params: any, _cb?: (id: string) => void) => alert(params.message || params.title),
      openTelegramLink: (url: string) => window.open(url, '_blank'),
    };

// Auto-expand & set ready on load
try {
  tg.expand();
  tg.ready();
} catch {}

export function triggerHaptic(type: 'light' | 'medium' | 'heavy' | 'select' | 'success' | 'error') {
  try {
    if (!tg?.isVersionAtLeast?.('6.1')) return;
    if (type === 'select') {
      tg.HapticFeedback?.selectionChanged?.();
    } else if (type === 'success' || type === 'error') {
      tg.HapticFeedback?.notificationOccurred?.(type);
    } else {
      tg.HapticFeedback?.impactOccurred?.(type);
    }
  } catch {}
}
