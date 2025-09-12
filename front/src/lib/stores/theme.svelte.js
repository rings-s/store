// src/lib/stores/theme.stores.svelte.js
import { getContext, setContext } from 'svelte';

class ThemeStore {
  isDark = $state(false);
  
  constructor() {
    $effect(() => {
      if (typeof window === 'undefined') return;
      
      const saved = localStorage.getItem('theme');
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      
      this.isDark = saved === 'dark' || (!saved && prefersDark);
      this.applyTheme();
    });
  }

  toggle() {
    this.isDark = !this.isDark;
    this.applyTheme();
    if (typeof window !== 'undefined') {
      localStorage.setItem('theme', this.isDark ? 'dark' : 'light');
    }
  }

  applyTheme() {
    if (typeof document === 'undefined') return;
    
    if (this.isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }
}

const THEME_KEY = Symbol('THEME');

export function setThemeStore() {
  return setContext(THEME_KEY, new ThemeStore());
}

export function getThemeStore() {
  return getContext(THEME_KEY);
}