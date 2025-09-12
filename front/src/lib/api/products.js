import apiClient from './client';

export const productsAPI = {
  async getProducts(params = {}) {
    const response = await apiClient.get('/base/products/', { params });
    return response.data;
  },

  async getProduct(slug) {
    const response = await apiClient.get(`/base/products/${slug}/`);
    return response.data;
  },

  async getFeaturedProducts() {
    const response = await apiClient.get('/base/products/featured/');
    return response.data;
  },

  async searchProducts(query) {
    const response = await apiClient.get('/base/products/search/', {
      params: { q: query }
    });
    return response.data;
  },

  async getCategories() {
    const response = await apiClient.get('/base/categories/');
    return response.data;
  },

  async getProductReviews(productId) {
    const response = await apiClient.get(`/base/products/${productId}/reviews/`);
    return response.data;
  },

  async createReview(productId, data) {
    const response = await apiClient.post(`/base/products/${productId}/reviews/`, data);
    return response.data;
  }
};