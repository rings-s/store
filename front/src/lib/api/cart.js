import apiClient from './client';

export const cartAPI = {
  async getCart() {
    const response = await apiClient.get('/base/cart/');
    return response.data;
  },

  async addToCart(productId, quantity = 1) {
    const response = await apiClient.post('/base/cart/', {
      product_id: productId,
      quantity
    });
    return response.data;
  },

  async updateCartItem(itemId, quantity) {
    const response = await apiClient.patch(`/base/cart/items/${itemId}/`, {
      quantity
    });
    return response.data;
  },

  async removeFromCart(itemId) {
    await apiClient.delete(`/base/cart/items/${itemId}/`);
  },

  async checkout(checkoutData) {
    const response = await apiClient.post('/base/checkout/', checkoutData);
    return response.data;
  }
};