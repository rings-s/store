import { getContext, setContext } from 'svelte';
import { reviewsAPI } from '$lib/api/reviews';
import { toastStore } from './toast.svelte.js';

class WishlistStore {
  items = $state([]);
  isLoading = $state(false);

  constructor() {
    $effect(() => {
      this.init();
    });
  }

  async init() {
    if (typeof window === 'undefined') return;
    
    this.isLoading = true;
    try {
      const items = await reviewsAPI.getWishlist();
      this.items = items || [];
    } catch (error) {
      console.error('Failed to load wishlist:', error);
      this.items = [];
    } finally {
      this.isLoading = false;
    }
  }

  async addItem(productId) {
    try {
      await reviewsAPI.addToWishlist(productId);
      await this.init();
      toastStore.success('Added to wishlist!');
    } catch (error) {
      toastStore.error('Failed to add to wishlist');
      throw error;
    }
  }

  async removeItem(productId) {
    try {
      await reviewsAPI.removeFromWishlist(productId);
      await this.init();
      toastStore.success('Removed from wishlist');
    } catch (error) {
      toastStore.error('Failed to remove from wishlist');
      throw error;
    }
  }

  // Method to check if product is in wishlist
  isInWishlist(productId) {
    return this.items.some(item => item.product?.id === productId);
  }

  // Derived values using Svelte 5 runes
  itemCount = $derived(() => this.items.length);
  isEmpty = $derived(() => this.items.length === 0);
}

const WISHLIST_KEY = Symbol('WISHLIST');

export function setWishlistStore() {
  return setContext(WISHLIST_KEY, new WishlistStore());
}

export function getWishlistStore() {
  return getContext(WISHLIST_KEY);
}