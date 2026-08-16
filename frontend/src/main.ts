import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import { tg } from './utils/telegram';
import './style.css';

// Sync Telegram theme with HTML root class
function applyTelegramTheme() {
  const isDark =
    tg?.colorScheme === 'dark' ||
    (!tg?.colorScheme && window.matchMedia('(prefers-color-scheme: dark)').matches);

  if (isDark) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
}

applyTelegramTheme();
try {
  tg?.onEvent?.('themeChanged', applyTelegramTheme);
} catch {}

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.mount('#app');
