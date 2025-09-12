import apiClient from './client';
import { browser } from '$app/environment';

export const authAPI = {
  async login(email, password) {
    const response = await apiClient.post('/accounts/login/', { email, password });
    if (browser && response.data.tokens) {
      localStorage.setItem('access_token', response.data.tokens.access);
      localStorage.setItem('refresh_token', response.data.tokens.refresh);
    }
    return response.data;
  },

  async register(userData) {
    const response = await apiClient.post('/accounts/register/', userData);
    if (browser && response.data.tokens) {
      localStorage.setItem('access_token', response.data.tokens.access);
      localStorage.setItem('refresh_token', response.data.tokens.refresh);
    }
    return response.data;
  },

  async logout() {
    try {
      const refreshToken = browser ? localStorage.getItem('refresh_token') : null;
      await apiClient.post('/accounts/logout/', { refresh_token: refreshToken });
    } finally {
      if (browser) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      }
    }
  },

  async getProfile() {
    const response = await apiClient.get('/accounts/profile/');
    return response.data;
  },

  async updateProfile(data) {
    const response = await apiClient.patch('/accounts/profile/', data);
    return response.data;
  },

  async changePassword(oldPassword, newPassword, newPasswordConfirm) {
    const response = await apiClient.post('/accounts/change-password/', {
      old_password: oldPassword,
      new_password: newPassword,
      new_password_confirm: newPasswordConfirm
    });
    return response.data;
  },

  async requestPasswordReset(email) {
    const response = await apiClient.post('/accounts/password-reset/', { email });
    return response.data;
  },

  async confirmPasswordReset(token, password, passwordConfirm) {
    const response = await apiClient.post('/accounts/password-reset-confirm/', {
      token,
      password,
      password_confirm: passwordConfirm
    });
    return response.data;
  }
};