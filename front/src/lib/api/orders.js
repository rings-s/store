import apiClient from './client';

export const ordersAPI = {
  async getOrders() {
    const response = await apiClient.get('/base/orders/');
    return response.data;
  },

  async getOrder(orderNumber) {
    const response = await apiClient.get(`/base/orders/${orderNumber}/`);
    return response.data;
  }
};