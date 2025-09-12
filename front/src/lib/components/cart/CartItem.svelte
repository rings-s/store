<!--
  @component CartItem
  Premium cart item with quantity controls and item management.
  Features smooth animations, accessibility, and comprehensive item display.
  
  @prop item - Cart item object with product details
  @prop readonly - Whether item is read-only (optional)
  @prop compact - Compact display mode (optional)
  @prop onQuantityChange - Quantity change handler (optional)
  @prop onRemove - Remove item handler (optional)
  @prop className - Additional CSS classes
-->
<script>
  import { formatPrice } from '$lib/utils/format';
  import { toastStore } from '$lib/stores/toast.svelte.js';
  
  let { 
    item, 
    readonly = false,
    compact = false,
    onQuantityChange = () => {},
    onRemove = () => {},
    className = '' 
  } = $props();
  
  // State management with Svelte 5 runes
  let isUpdating = $state(false);
  let isRemoving = $state(false);
  let imageError = $state(false);
  
  // Computed values
  const totalPrice = $derived(() => 
    (item.price || 0) * (item.quantity || 1)
  );
  
  const discountAmount = $derived(() => {
    if (item.original_price && item.price < item.original_price) {
      return (item.original_price - item.price) * item.quantity;
    }
    return 0;
  });
  
  const stockWarning = $derived(() => {
    if (!item.stock_quantity) return null;
    if (item.quantity > item.stock_quantity) return 'exceed';
    if (item.stock_quantity <= 5) return 'low';
    return null;
  });
  
  // Functions
  async function updateQuantity(newQuantity) {
    if (readonly || isUpdating || newQuantity < 1) return;
    
    // Check stock limits
    if (item.stock_quantity && newQuantity > item.stock_quantity) {
      toastStore.add({
        type: 'warning',
        message: `Only ${item.stock_quantity} items available`
      });
      return;
    }
    
    isUpdating = true;
    
    try {
      await onQuantityChange(item.id, newQuantity);
    } catch (error) {
      toastStore.add({
        type: 'error',
        message: 'Failed to update quantity. Please try again.'
      });
    } finally {
      isUpdating = false;
    }
  }
  
  async function removeItem() {
    if (readonly || isRemoving) return;
    
    isRemoving = true;
    
    try {
      await onRemove(item.id);
      toastStore.add({
        type: 'success',
        message: `${item.name} removed from cart`
      });
    } catch (error) {
      toastStore.add({
        type: 'error',
        message: 'Failed to remove item. Please try again.'
      });
      isRemoving = false;
    }
  }
  
  function handleImageError() {
    imageError = true;
  }
</script>

<div 
  class="group relative bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 
         transition-all duration-300 hover:shadow-lg hover:shadow-gray-500/10 dark:hover:shadow-gray-900/20 
         {isRemoving ? 'animate-slide-out opacity-50' : 'animate-slide-in'} 
         {compact ? 'p-4' : 'p-6'} {className}"
>
  {#if isRemoving}
    <!-- Removing Overlay -->
    <div class="absolute inset-0 bg-white/80 dark:bg-gray-800/80 rounded-2xl flex items-center justify-center z-10">
      <div class="flex items-center gap-2 text-gray-600 dark:text-gray-400">
        <svg class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span class="text-sm">Removing...</span>
      </div>
    </div>
  {/if}
  
  <div class="flex gap-4">
    <!-- Product Image -->
    <div class="flex-shrink-0">
      <div class="{compact ? 'w-16 h-16' : 'w-20 h-20'} rounded-xl overflow-hidden bg-gray-100 dark:bg-gray-700">
        {#if item.image && !imageError}
          <img
            src={item.image}
            alt={item.name}
            class="w-full h-full object-cover transition-transform group-hover:scale-105"
            onerror={handleImageError}
            loading="lazy"
          />
        {:else}
          <!-- Placeholder Image -->
          <div class="w-full h-full flex items-center justify-center text-gray-400 dark:text-gray-600">
            <svg class="{compact ? 'w-6 h-6' : 'w-8 h-8'}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
        {/if}
      </div>
    </div>
    
    <!-- Product Details -->
    <div class="flex-1 min-w-0">
      <div class="flex flex-col {compact ? 'space-y-2' : 'space-y-3'}">
        <!-- Product Name & Variant -->
        <div>
          <h3 class="font-semibold text-gray-900 dark:text-white text-sm leading-tight">
            <a 
              href="/products/{item.product_id}" 
              class="hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
            >
              {item.name}
            </a>
          </h3>
          {#if item.variant}
            <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
              {item.variant}
            </p>
          {/if}
        </div>
        
        <!-- Price Information -->
        <div class="flex items-center gap-2">
          <span class="font-bold text-gray-900 dark:text-white text-sm">
            {formatPrice(item.price)}
          </span>
          {#if item.original_price && item.price < item.original_price}
            <span class="text-xs text-gray-500 dark:text-gray-400 line-through">
              {formatPrice(item.original_price)}
            </span>
          {/if}
          {#if !compact}
            <span class="text-xs text-gray-500 dark:text-gray-400">
              each
            </span>
          {/if}
        </div>
        
        <!-- Stock Warning -->
        {#if stockWarning === 'exceed'}
          <div class="flex items-center gap-1 text-red-600 dark:text-red-400 text-xs">
            <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
            <span>Exceeds available stock ({item.stock_quantity})</span>
          </div>
        {:else if stockWarning === 'low'}
          <div class="flex items-center gap-1 text-yellow-600 dark:text-yellow-400 text-xs">
            <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
            <span>Low stock ({item.stock_quantity} left)</span>
          </div>
        {/if}
      </div>
    </div>
    
    <!-- Quantity & Actions -->
    <div class="flex flex-col items-end justify-between">
      <!-- Remove Button -->
      {#if !readonly}
        <button
          onclick={removeItem}
          disabled={isRemoving}
          class="p-1 rounded-lg text-gray-400 hover:text-red-500 dark:hover:text-red-400 
                 hover:bg-red-50 dark:hover:bg-red-900/20 transition-all duration-200 
                 opacity-0 group-hover:opacity-100 focus:opacity-100 disabled:opacity-50"
          aria-label="Remove {item.name} from cart"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      {/if}
      
      <!-- Quantity Controls -->
      {#if readonly}
        <div class="text-right">
          <div class="text-sm font-medium text-gray-900 dark:text-white">
            Qty: {item.quantity}
          </div>
          <div class="text-sm font-bold text-gray-900 dark:text-white">
            {formatPrice(totalPrice)}
          </div>
        </div>
      {:else}
        <div class="space-y-2">
          <!-- Quantity Selector -->
          <div class="flex items-center bg-gray-50 dark:bg-gray-700 rounded-lg">
            <button
              onclick={() => updateQuantity(item.quantity - 1)}
              disabled={isUpdating || item.quantity <= 1}
              class="p-1 hover:bg-gray-200 dark:hover:bg-gray-600 disabled:opacity-50 
                     disabled:cursor-not-allowed rounded-l-lg transition-colors text-sm"
              aria-label="Decrease quantity"
            >
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
              </svg>
            </button>
            
            <div class="px-2 py-1 min-w-8 text-center text-sm font-medium">
              {#if isUpdating}
                <svg class="w-3 h-3 animate-spin mx-auto" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              {:else}
                {item.quantity}
              {/if}
            </div>
            
            <button
              onclick={() => updateQuantity(item.quantity + 1)}
              disabled={isUpdating || (item.stock_quantity && item.quantity >= item.stock_quantity)}
              class="p-1 hover:bg-gray-200 dark:hover:bg-gray-600 disabled:opacity-50 
                     disabled:cursor-not-allowed rounded-r-lg transition-colors text-sm"
              aria-label="Increase quantity"
            >
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
            </button>
          </div>
          
          <!-- Total Price -->
          <div class="text-right">
            <div class="text-sm font-bold text-gray-900 dark:text-white">
              {formatPrice(totalPrice)}
            </div>
            {#if discountAmount > 0}
              <div class="text-xs text-green-600 dark:text-green-400">
                Save {formatPrice(discountAmount)}
              </div>
            {/if}
          </div>
        </div>
      {/if}
    </div>
  </div>
</div>

<style>
  @keyframes slide-out {
    0% {
      transform: translateX(0);
      opacity: 1;
    }
    100% {
      transform: translateX(-100%);
      opacity: 0;
    }
  }
  
  @keyframes slide-in {
    0% {
      transform: translateX(-20px);
      opacity: 0;
    }
    100% {
      transform: translateX(0);
      opacity: 1;
    }
  }
  
  .animate-slide-out {
    animation: slide-out 0.3s ease-in-out forwards;
  }
  
  .animate-slide-in {
    animation: slide-in 0.3s ease-out;
  }
  
  /* Reduced motion preferences */
  @media (prefers-reduced-motion: reduce) {
    .animate-slide-out,
    .animate-slide-in,
    .transition-transform,
    .group-hover\\:scale-105 {
      animation: none !important;
      transition: none !important;
      transform: none !important;
    }
  }
</style>