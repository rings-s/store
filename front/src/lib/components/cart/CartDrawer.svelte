<!--
  @component CartDrawer
  Premium sliding cart drawer with full cart management capabilities.
  Features smooth animations, accessibility, and comprehensive cart operations.
  
  @prop isOpen - Whether drawer is open
  @prop items - Array of cart items
  @prop loading - Loading state (optional)
  @prop onClose - Close handler function
  @prop onQuantityChange - Quantity change handler (optional)
  @prop onRemoveItem - Remove item handler (optional)
  @prop onCheckout - Checkout handler (optional)
  @prop className - Additional CSS classes
-->
<script>
  import CartItem from './CartItem.svelte';
  import CartSummary from './CartSummary.svelte';
  import Drawer from '../ui/Drawer.svelte';
  import { formatPrice } from '$lib/utils/format';
  import { toastStore } from '$lib/stores/toast.svelte.js';
  
  let { 
    isOpen = false,
    items = [],
    loading = false,
    onClose = () => {},
    onQuantityChange = () => {},
    onRemoveItem = () => {},
    onCheckout = () => {},
    className = ''
  } = $props();
  
  // State management with Svelte 5 runes
  let isScrolled = $state(false);
  let drawerElement = $state(null);
  
  // Computed values
  const totalItems = $derived(() =>
    items.reduce((sum, item) => sum + item.quantity, 0)
  );
  
  const subtotal = $derived(() =>
    items.reduce((sum, item) => sum + (item.price * item.quantity), 0)
  );
  
  // Shipping config (would typically come from props or store)
  const shippingConfig = {
    free_threshold: 50,
    cost: 5.99
  };
  
  const taxConfig = {
    rate: 8.25
  };
  
  // Functions
  function handleScroll(e) {
    isScrolled = e.target.scrollTop > 20;
  }
  
  async function handleQuantityChange(itemId, newQuantity) {
    try {
      await onQuantityChange(itemId, newQuantity);
    } catch (error) {
      console.error('Failed to update quantity:', error);
      throw error;
    }
  }
  
  async function handleRemoveItem(itemId) {
    try {
      await onRemoveItem(itemId);
    } catch (error) {
      console.error('Failed to remove item:', error);
      throw error;
    }
  }
  
  async function handleCheckout() {
    try {
      await onCheckout();
      onClose(); // Close drawer after successful checkout
    } catch (error) {
      console.error('Failed to checkout:', error);
      throw error;
    }
  }
  
  function continueShopping() {
    onClose();
    toastStore.add({
      type: 'info',
      message: 'Continue shopping to find more great products!'
    });
  }
</script>

<Drawer 
  {isOpen} 
  position="right" 
  size="lg" 
  {onClose}
  className="cart-drawer {className}"
>
  <!-- Drawer Header -->
  <div 
    class="sticky top-0 z-10 bg-white/95 dark:bg-gray-900/95 backdrop-blur-md 
           border-b border-gray-200 dark:border-gray-700 transition-all duration-300
           {isScrolled ? 'shadow-md' : ''}"
  >
    <div class="flex items-center justify-between p-6">
      <div class="flex items-center gap-3">
        <h2 class="text-2xl font-display font-bold text-gray-900 dark:text-white">
          Shopping Cart
        </h2>
        {#if totalItems > 0}
          <div class="bg-primary-100 dark:bg-primary-900/30 text-primary-800 dark:text-primary-300 
                      px-3 py-1 rounded-full text-sm font-medium">
            {totalItems} item{totalItems !== 1 ? 's' : ''}
          </div>
        {/if}
      </div>
      
      <button
        onclick={onClose}
        class="p-2 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-800 
               text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300 
               transition-colors"
        aria-label="Close cart"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
    
    <!-- Quick Summary in Header -->
    {#if items.length > 0}
      <div class="px-6 pb-4">
        <div class="flex items-center justify-between text-sm">
          <span class="text-gray-600 dark:text-gray-400">
            Subtotal
          </span>
          <span class="font-semibold text-gray-900 dark:text-white">
            {formatPrice(subtotal)}
          </span>
        </div>
      </div>
    {/if}
  </div>
  
  <!-- Drawer Content -->
  <div 
    class="flex-1 overflow-y-auto p-6"
    onscroll={handleScroll}
    bind:this={drawerElement}
  >
    {#if loading}
      <!-- Loading State -->
      <div class="space-y-4">
        {#each Array(3) as _}
          <div class="animate-pulse">
            <div class="flex gap-4">
              <div class="w-16 h-16 bg-gray-200 dark:bg-gray-700 rounded-xl"></div>
              <div class="flex-1 space-y-2">
                <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4"></div>
                <div class="h-3 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
                <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/4"></div>
              </div>
            </div>
          </div>
        {/each}
      </div>
    {:else if items.length === 0}
      <!-- Empty Cart State -->
      <div class="flex flex-col items-center justify-center h-full min-h-96 text-center">
        <div class="w-24 h-24 mx-auto mb-6 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center">
          <svg class="w-12 h-12 text-gray-400 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13h10M17 13v6a2 2 0 01-2 2H9a2 2 0 01-2-2v-6.01M17 13l-5-5-5 5" />
          </svg>
        </div>
        
        <h3 class="text-xl font-display font-semibold text-gray-900 dark:text-white mb-3">
          Your cart is empty
        </h3>
        
        <p class="text-gray-600 dark:text-gray-400 mb-8 max-w-sm">
          Looks like you haven't added anything to your cart yet. Start shopping to fill it up!
        </p>
        
        <button
          onclick={continueShopping}
          class="btn-primary group relative overflow-hidden"
        >
          <span class="relative z-10 flex items-center gap-2">
            <svg class="w-5 h-5 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l-1 12H6L5 9z" />
            </svg>
            Start Shopping
          </span>
          <div class="absolute inset-0 bg-gradient-to-r from-primary-600 to-primary-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </button>
        
        <!-- Featured Categories or Suggestions -->
        <div class="mt-8 w-full">
          <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">Popular categories</p>
          <div class="grid grid-cols-2 gap-3">
            <button 
              onclick={continueShopping}
              class="p-3 rounded-xl border border-gray-200 dark:border-gray-700 
                     hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors text-left"
            >
              <div class="text-sm font-medium text-gray-900 dark:text-white">Electronics</div>
              <div class="text-xs text-gray-500 dark:text-gray-400">Latest gadgets</div>
            </button>
            <button 
              onclick={continueShopping}
              class="p-3 rounded-xl border border-gray-200 dark:border-gray-700 
                     hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors text-left"
            >
              <div class="text-sm font-medium text-gray-900 dark:text-white">Fashion</div>
              <div class="text-xs text-gray-500 dark:text-gray-400">Trending styles</div>
            </button>
          </div>
        </div>
      </div>
    {:else}
      <!-- Cart Items -->
      <div class="space-y-4 mb-8">
        <div class="flex items-center justify-between">
          <h3 class="font-semibold text-gray-900 dark:text-white">
            Items in your cart
          </h3>
          <button
            onclick={continueShopping}
            class="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 
                   text-sm font-medium transition-colors"
          >
            Continue Shopping
          </button>
        </div>
        
        {#each items as item (item.id)}
          <div class="animate-fade-in">
            <CartItem 
              {item}
              compact={true}
              onQuantityChange={handleQuantityChange}
              onRemove={handleRemoveItem}
            />
          </div>
        {/each}
      </div>
      
      <!-- Cart Summary -->
      <div class="sticky bottom-0 bg-white/95 dark:bg-gray-900/95 backdrop-blur-md 
                  -mx-6 px-6 py-4 border-t border-gray-200 dark:border-gray-700">
        <CartSummary 
          {items}
          shipping={shippingConfig}
          tax={taxConfig}
          onCheckout={handleCheckout}
        />
      </div>
    {/if}
  </div>
  
  <!-- Trust Indicators Footer -->
  {#if items.length > 0}
    <div class="border-t border-gray-200 dark:border-gray-700 p-6">
      <div class="grid grid-cols-2 gap-4 text-center">
        <div class="flex flex-col items-center gap-2">
          <div class="w-10 h-10 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center">
            <svg class="w-5 h-5 text-green-600 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="text-xs text-gray-600 dark:text-gray-400">
            <div class="font-medium">Secure Checkout</div>
            <div>256-bit SSL encryption</div>
          </div>
        </div>
        
        <div class="flex flex-col items-center gap-2">
          <div class="w-10 h-10 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center">
            <svg class="w-5 h-5 text-blue-600 dark:text-blue-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 2L3 7v11c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V7l-7-5zM10 4.5L15 8v10H5V8l5-3.5z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="text-xs text-gray-600 dark:text-gray-400">
            <div class="font-medium">Free Returns</div>
            <div>30-day return policy</div>
          </div>
        </div>
      </div>
    </div>
  {/if}
</Drawer>
  
  <style>
    @keyframes fade-in {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    
    @keyframes slide-in {
      from { transform: translateX(100%); }
      to { transform: translateX(0); }
    }
    
    .animate-fade-in {
      animation: fade-in 0.3s ease-out;
    }
    
    .animate-slide-in {
      animation: slide-in 0.3s ease-out;
    }
  </style>