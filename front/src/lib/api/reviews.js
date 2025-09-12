import apiClient from './client';

export const reviewsAPI = {
  async getWishlist() {
    const response = await apiClient.get('/base/wishlist/');
    return response.data;
  },

  async addToWishlist(productId) {
    const response = await apiClient.post('/base/wishlist/', {
      product_id: productId
    });
    return response.data;
  },

  async removeFromWishlist(productId) {
    await apiClient.delete(`/base/wishlist/${productId}/`);
  }
};