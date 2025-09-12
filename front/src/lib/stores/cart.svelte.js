// src/lib/stores/cart.stores.svelte.js
import { getContext, setContext } from 'svelte';
import { cartAPI } from '$lib/api/cart';
import { toastStore } from './toast.svelte.js';

class CartStore {
  items = $state([]);
  total = $state(0);
  itemsCount = $state(0);
  isLoading = $state(false);
  isDrawerOpen = $state(false);

  constructor() {
    $effect(() => {
      this.init();
    });
  }

  async init() {
    if (typeof window === 'undefined') return;
    
    this.isLoading = true;
    try {
      const cart = await cartAPI.getCart();
      this.items = cart.items || [];
      this.total = cart.total || 0;
      this.itemsCount = cart.items_count || 0;
    } catch (error) {
      console.error('Failed to load cart:', error);
    } finally {
      this.isLoading = false;
    }
  }

  async addItem(productId, quantity = 1, options = {}) {
    try {
      const cart = await cartAPI.addToCart(productId, quantity);
      this.items = cart.items || [];
      this.total = cart.total || 0;
      this.itemsCount = cart.items_count || 0;
      
      if (!options.silent) {
        toastStore.success('Added to cart!', {
          action: {
            label: 'View Cart',
            onClick: () => this.openDrawer()
          }
        });
        this.openDrawer();
      }
      
      return cart;
    } catch (error) {
      toastStore.error('Failed to add item to cart');
      throw error;
    }
  }

  async updateItem(itemId, quantity) {
    try {
      await cartAPI.updateCartItem(itemId, quantity);
      await this.init();
    } catch (error) {
      toastStore.error('Failed to update cart');
      throw error;
    }
  }

  async removeItem(itemId) {
    try {
      await cartAPI.removeFromCart(itemId);
      await this.init();
      toastStore.success('Item removed');
    } catch (error) {
      toastStore.error('Failed to remove item');
      throw error;
    }
  }

  openDrawer() {
    this.isDrawerOpen = true;
  }

  closeDrawer() {
    this.isDrawerOpen = false;
  }

  toggleDrawer() {
    this.isDrawerOpen = !this.isDrawerOpen;
  }

  // Derived values using Svelte 5 runes
  isEmpty = $derived(() => this.items.length === 0);
  
  subtotal = $derived(() => this.items.reduce((sum, item) => sum + item.subtotal, 0));
}

const CART_KEY = Symbol('CART');

export function setCartStore() {
  return setContext(CART_KEY, new CartStore());
}

export function getCartStore() {
  return getContext(CART_KEY);
}