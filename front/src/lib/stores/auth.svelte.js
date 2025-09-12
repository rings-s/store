// src/lib/stores/auth.stores.svelte.js
import { getContext, setContext } from 'svelte';
import { authAPI } from '$lib/api/auth';

class AuthStore {
  user = $state(null);
  isLoading = $state(true);
  isAuthenticated = $state(false);

  constructor() {
    $effect(() => {
      this.init();
    });
  }

  async init() {
    if (typeof window === 'undefined') return;
    
    const token = localStorage.getItem('access_token');
    if (token) {
      try {
        const user = await authAPI.getProfile();
        this.user = user;
        this.isAuthenticated = true;
      } catch {
        this.clearAuth();
      }
    }
    this.isLoading = false;
  }

  async login(email, password) {
    const data = await authAPI.login(email, password);
    this.user = data.user;
    this.isAuthenticated = true;
    return data;
  }

  async register(userData) {
    const data = await authAPI.register(userData);
    this.user = data.user;
    this.isAuthenticated = true;
    return data;
  }

  async logout() {
    await authAPI.logout();
    this.clearAuth();
  }

  clearAuth() {
    this.user = null;
    this.isAuthenticated = false;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    }
  }

  async updateProfile(data) {
    const updatedUser = await authAPI.updateProfile(data);
    this.user = updatedUser;
    return updatedUser;
  }
}

const AUTH_KEY = Symbol('AUTH');

export function setAuthStore() {
  return setContext(AUTH_KEY, new AuthStore());
}

export function getAuthStore() {
  return getContext(AUTH_KEY);
}