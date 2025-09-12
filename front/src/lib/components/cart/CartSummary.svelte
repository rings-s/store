<!--
  @component CartSummary
  Premium cart summary with totals, discounts, and checkout actions.
  Features tax calculations, shipping estimates, and promo code handling.
  
  @prop items - Array of cart items
  @prop shipping - Shipping cost information (optional)
  @prop tax - Tax information (optional) 
  @prop promoCode - Applied promo code (optional)
  @prop onPromoCodeApply - Promo code apply handler (optional)
  @prop onCheckout - Checkout handler (optional)
  @prop className - Additional CSS classes
-->
<script>
  import { formatPrice } from '$lib/utils/format';
  import { toastStore } from '$lib/stores/toast.svelte.js';
  
  let { 
    items = [], 
    shipping = null,
    tax = null,
    promoCode = null,
    onPromoCodeApply = () => {},
    onCheckout = () => {},
    className = '' 
  } = $props();
  
  // State management with Svelte 5 runes
  let promoCodeInput = $state('');
  let isApplyingPromo = $state(false);
  let isCheckingOut = $state(false);
  let showPromoInput = $state(false);
  
  // Computed values
  const subtotal = $derived(() =>
    items.reduce((sum, item) => sum + (item.price * item.quantity), 0)
  );
  
  const totalItems = $derived(() =>
    items.reduce((sum, item) => sum + item.quantity, 0)
  );
  
  const discount = $derived(() => {
    if (!promoCode?.discount) return 0;
    
    if (promoCode.type === 'percentage') {
      return subtotal() * (promoCode.discount / 100);
    } else if (promoCode.type === 'fixed') {
      return Math.min(promoCode.discount, subtotal());
    }
    return 0;
  });
  
  const shippingCost = $derived(() => {
    if (!shipping) return 0;
    if (shipping.free_threshold && subtotal() >= shipping.free_threshold) return 0;
    return shipping.cost || 0;
  });
  
  const taxAmount = $derived(() => {
    if (!tax?.rate) return 0;
    const taxableAmount = subtotal() - discount() + shippingCost();
    return taxableAmount * (tax.rate / 100);
  });
  
  const total = $derived(() => 
    subtotal() - discount() + shippingCost() + taxAmount()
  );
  
  const savings = $derived(() => {
    const itemSavings = items.reduce((sum, item) => {
      if (item.original_price && item.price < item.original_price) {
        return sum + ((item.original_price - item.price) * item.quantity);
      }
      return sum;
    }, 0);
    return itemSavings + discount();
  });
  
  const freeShippingProgress = $derived(() => {
    if (!shipping?.free_threshold) return null;
    const remaining = shipping.free_threshold - subtotal();
    if (remaining <= 0) return { qualified: true, remaining: 0 };
    return { qualified: false, remaining, progress: (subtotal() / shipping.free_threshold) * 100 };
  });
  
  // Functions
  async function applyPromoCode() {
    if (!promoCodeInput.trim() || isApplyingPromo) return;
    
    isApplyingPromo = true;
    
    try {
      await onPromoCodeApply(promoCodeInput.trim());
      promoCodeInput = '';
      showPromoInput = false;
      toastStore.add({
        type: 'success',
        message: 'Promo code applied successfully!'
      });
    } catch (error) {
      toastStore.add({
        type: 'error',
        message: error.message || 'Invalid promo code. Please try again.'
      });
    } finally {
      isApplyingPromo = false;
    }
  }
  
  async function handleCheckout() {
    if (isCheckingOut || items.length === 0) return;
    
    isCheckingOut = true;
    
    try {
      await onCheckout();
    } catch (error) {
      toastStore.add({
        type: 'error',
        message: error.message || 'Failed to proceed to checkout. Please try again.'
      });
    } finally {
      isCheckingOut = false;
    }
  }
  
  function removePromoCode() {
    onPromoCodeApply('');
    toastStore.add({
      type: 'info',
      message: 'Promo code removed'
    });
  }
</script>

<div class="glass-panel rounded-3xl p-6 space-y-6 {className}">
  <!-- Header -->
  <div class="flex items-center justify-between">
    <h2 class="text-xl font-display font-semibold text-gray-900 dark:text-white">
      Order Summary
    </h2>
    <div class="text-sm text-gray-600 dark:text-gray-400">
      {totalItems} item{totalItems !== 1 ? 's' : ''}
    </div>
  </div>
  
  <!-- Free Shipping Progress -->
  {#if freeShippingProgress && !freeShippingProgress.qualified}
    <div class="bg-gradient-to-r from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 
                rounded-xl p-4 border border-green-200 dark:border-green-800">
      <div class="flex items-center justify-between mb-2">
        <span class="text-sm font-medium text-green-800 dark:text-green-300">
          Free shipping progress
        </span>
        <span class="text-xs text-green-600 dark:text-green-400">
          {formatPrice(freeShippingProgress.remaining)} to go
        </span>
      </div>
      <div class="w-full bg-green-200 dark:bg-green-800 rounded-full h-2 overflow-hidden">
        <div 
          class="h-full bg-gradient-to-r from-green-500 to-green-600 transition-all duration-500 ease-out"
          style="width: {Math.min(freeShippingProgress.progress, 100)}%"
        ></div>
      </div>
      <p class="text-xs text-green-700 dark:text-green-400 mt-2">
        Add {formatPrice(freeShippingProgress.remaining)} more to qualify for free shipping!
      </p>
    </div>
  {:else if freeShippingProgress?.qualified}
    <div class="bg-gradient-to-r from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 
                rounded-xl p-4 border border-green-200 dark:border-green-800">
      <div class="flex items-center gap-2 text-green-800 dark:text-green-300">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
        </svg>
        <span class="font-medium text-sm">You qualify for free shipping!</span>
      </div>
    </div>
  {/if}
  
  <!-- Promo Code Section -->
  <div class="space-y-3">
    {#if promoCode}
      <!-- Applied Promo Code -->
      <div class="flex items-center justify-between p-3 bg-green-50 dark:bg-green-900/20 
                  rounded-xl border border-green-200 dark:border-green-800">
        <div class="flex items-center gap-2">
          <svg class="w-4 h-4 text-green-600 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
          </svg>
          <span class="text-sm font-medium text-green-800 dark:text-green-300">
            {promoCode.code}
          </span>
          <span class="text-xs text-green-600 dark:text-green-400">
            -{formatPrice(discount())}
          </span>
        </div>
        <button
          onclick={removePromoCode}
          class="text-green-600 hover:text-green-700 dark:text-green-400 dark:hover:text-green-300"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    {:else}
      <!-- Promo Code Input -->
      {#if showPromoInput}
        <div class="flex gap-2">
          <input
            type="text"
            bind:value={promoCodeInput}
            placeholder="Enter promo code"
            class="input-primary flex-1 text-sm"
            onkeydown={(e) => e.key === 'Enter' && applyPromoCode()}
          />
          <button
            onclick={applyPromoCode}
            disabled={!promoCodeInput.trim() || isApplyingPromo}
            class="btn-secondary px-4 py-2 text-sm disabled:opacity-50"
          >
            {#if isApplyingPromo}
              <svg class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            {:else}
              Apply
            {/if}
          </button>
          <button
            onclick={() => { showPromoInput = false; promoCodeInput = ''; }}
            class="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      {:else}
        <button
          onclick={() => showPromoInput = true}
          class="flex items-center gap-2 text-primary-600 hover:text-primary-700 dark:text-primary-400 
                 dark:hover:text-primary-300 text-sm font-medium"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a1.994 1.994 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
          </svg>
          Add promo code
        </button>
      {/if}
    {/if}
  </div>
  
  <!-- Order Breakdown -->
  <div class="space-y-3 border-t border-gray-200 dark:border-gray-700 pt-6">
    <!-- Subtotal -->
    <div class="flex justify-between text-sm">
      <span class="text-gray-600 dark:text-gray-400">
        Subtotal ({totalItems} item{totalItems !== 1 ? 's' : ''})
      </span>
      <span class="font-medium text-gray-900 dark:text-white">
        {formatPrice(subtotal())}
      </span>
    </div>
    
    <!-- Discount -->
    {#if discount() > 0}
      <div class="flex justify-between text-sm">
        <span class="text-green-600 dark:text-green-400">
          Discount ({promoCode?.code})
        </span>
        <span class="font-medium text-green-600 dark:text-green-400">
          -{formatPrice(discount())}
        </span>
      </div>
    {/if}
    
    <!-- Shipping -->
    <div class="flex justify-between text-sm">
      <span class="text-gray-600 dark:text-gray-400">
        Shipping
        {#if shipping?.free_threshold && subtotal() >= shipping.free_threshold}
          <span class="text-green-600 dark:text-green-400 ml-1">(Free)</span>
        {/if}
      </span>
      <span class="font-medium text-gray-900 dark:text-white">
        {shippingCost() === 0 ? 'Free' : formatPrice(shippingCost())}
      </span>
    </div>
    
    <!-- Tax -->
    {#if tax?.rate}
      <div class="flex justify-between text-sm">
        <span class="text-gray-600 dark:text-gray-400">
          Tax ({tax.rate}%)
        </span>
        <span class="font-medium text-gray-900 dark:text-white">
          {formatPrice(taxAmount())}
        </span>
      </div>
    {/if}
    
    <!-- Total Savings -->
    {#if savings() > 0}
      <div class="flex justify-between text-sm bg-green-50 dark:bg-green-900/20 
                  rounded-lg p-2 border border-green-200 dark:border-green-800">
        <span class="text-green-800 dark:text-green-300 font-medium">
          Total Savings
        </span>
        <span class="font-bold text-green-600 dark:text-green-400">
          -{formatPrice(savings())}
        </span>
      </div>
    {/if}
  </div>
  
  <!-- Final Total -->
  <div class="border-t border-gray-200 dark:border-gray-700 pt-4">
    <div class="flex justify-between items-center">
      <span class="text-lg font-display font-semibold text-gray-900 dark:text-white">
        Total
      </span>
      <div class="text-right">
        <div class="text-2xl font-display font-bold text-gray-900 dark:text-white">
          {formatPrice(total())}
        </div>
        {#if tax?.rate}
          <div class="text-xs text-gray-500 dark:text-gray-400">
            Includes {formatPrice(taxAmount())} tax
          </div>
        {/if}
      </div>
    </div>
  </div>
  
  <!-- Checkout Button -->
  <button
    onclick={handleCheckout}
    disabled={items.length === 0 || isCheckingOut}
    class="btn-primary w-full py-4 text-lg font-semibold group relative overflow-hidden 
           disabled:opacity-50 disabled:cursor-not-allowed"
  >
    <span class="relative z-10 flex items-center justify-center gap-2">
      {#if isCheckingOut}
        <svg class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Processing...
      {:else}
        <svg class="w-5 h-5 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
        </svg>
        Proceed to Checkout
      {/if}
    </span>
    <div class="absolute inset-0 bg-gradient-to-r from-primary-600 to-primary-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
  </button>
  
  <!-- Security Notice -->
  <div class="flex items-center justify-center gap-2 text-xs text-gray-500 dark:text-gray-400">
    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
      <path fill-rule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
    </svg>
    <span>Secure SSL encrypted checkout</span>
  </div>
</div>