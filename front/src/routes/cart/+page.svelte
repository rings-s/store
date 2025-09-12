<!--
  @component CartPage
  Premium cart page with comprehensive cart management and checkout flow.
  Features responsive design, empty states, and seamless checkout integration.
-->
<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { getCartStore } from '$lib/stores/cart.svelte.js';
  import { getAuthStore } from '$lib/stores/auth.svelte.js';
  import CartItem from '$lib/components/cart/CartItem.svelte';
  import CartSummary from '$lib/components/cart/CartSummary.svelte';
  import Button from '$lib/components/ui/Button.svelte';
  import Card from '$lib/components/ui/Card.svelte';
  import Spinner from '$lib/components/ui/Spinner.svelte';
  
  // Store access
  const cartStore = getCartStore();
  const authStore = getAuthStore();
  
  // Reactive state using Svelte 5 runes
  let mounted = $state(false);
  let isUpdating = $state(false);
  
  // Derived values from stores
  const cartItems = $derived(cartStore?.items || []);
  const isLoading = $derived(cartStore?.isLoading || false);
  const cartTotal = $derived(cartStore?.total || 0);
  const cartCount = $derived(cartStore?.itemsCount || 0);
  const isAuthenticated = $derived(authStore?.isAuthenticated || false);
  
  // Computed values
  const isEmpty = $derived(cartItems.length === 0);
  const subtotal = $derived(() => 
    cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0)
  );
  
  // Shipping and tax calculation
  const shippingConfig = {
    free_threshold: 50,
    cost: 5.99
  };
  
  const taxConfig = {
    rate: 8.25
  };
  
  const shipping = $derived(() => 
    subtotal >= shippingConfig.free_threshold ? 0 : shippingConfig.cost
  );
  
  const tax = $derived(() => subtotal * (taxConfig.rate / 100));
  const finalTotal = $derived(() => subtotal + shipping + tax);
  
  // Cart operations
  async function handleQuantityChange(itemId, newQuantity) {
    if (isUpdating) return;
    
    isUpdating = true;
    try {
      await cartStore.updateItem(itemId, newQuantity);
    } catch (error) {
      console.error('Failed to update item:', error);
    } finally {
      isUpdating = false;
    }
  }
  
  async function handleRemoveItem(itemId) {
    if (isUpdating) return;
    
    isUpdating = true;
    try {
      await cartStore.removeItem(itemId);
    } catch (error) {
      console.error('Failed to remove item:', error);
    } finally {
      isUpdating = false;
    }
  }
  
  function handleContinueShopping() {
    goto('/products');
  }
  
  async function handleCheckout() {
    if (!isAuthenticated) {
      goto('/auth/login?redirect=' + encodeURIComponent($page.url.pathname));
      return;
    }
    
    goto('/checkout');
  }
  
  function clearCart() {
    // Implement clear cart functionality
    console.log('Clear cart requested');
  }
  
  // Lifecycle
  onMount(() => {
    mounted = true;
    
    // Initialize cart if not already loaded
    if (cartStore && !cartStore.items?.length) {
      cartStore.init();
    }
  });
</script>

<svelte:head>
  <title>Shopping Cart - Premium Store</title>
  <meta name="description" content="Review and manage items in your shopping cart before checkout" />
</svelte:head>

<div class="min-h-screen bg-gray-50 dark:bg-dark-50 py-8">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    
    <!-- Page Header -->
    <div class="mb-8">
      <nav class="flex mb-4" aria-label="Breadcrumb">
        <ol class="flex items-center space-x-2 text-sm">
          <li>
            <a href="/" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300">
              Home
            </a>
          </li>
          <li class="text-gray-400">/</li>
          <li>
            <a href="/products" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300">
              Products
            </a>
          </li>
          <li class="text-gray-400">/</li>
          <li class="text-gray-900 dark:text-white font-medium">Cart</li>
        </ol>
      </nav>
      
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-display font-bold text-gray-900 dark:text-white">
            Shopping Cart
          </h1>
          {#if !isEmpty}
            <p class="mt-2 text-gray-600 dark:text-gray-400">
              {cartCount} item{cartCount !== 1 ? 's' : ''} in your cart
            </p>
          {/if}
        </div>
        
        {#if !isEmpty && !isLoading}
          <Button
            variant="ghost" 
            size="sm"
            onclick={clearCart}
            class="text-gray-500 hover:text-red-600"
          >
            Clear Cart
          </Button>
        {/if}
      </div>
    </div>

    {#if isLoading}
      <!-- Loading State -->
      <div class="flex justify-center items-center py-16">
        <div class="text-center">
          <Spinner size="lg" />
          <p class="mt-4 text-gray-600 dark:text-gray-400">Loading your cart...</p>
        </div>
      </div>
      
    {:else if isEmpty}
      <!-- Empty Cart State -->
      <div class="text-center py-16">
        <Card class="max-w-md mx-auto glass">
          <div class="w-24 h-24 mx-auto mb-6 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center">
            <svg class="w-12 h-12 text-gray-400 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13h10" />
            </svg>
          </div>
          
          <h2 class="text-2xl font-display font-semibold text-gray-900 dark:text-white mb-3">
            Your cart is empty
          </h2>
          
          <p class="text-gray-600 dark:text-gray-400 mb-8">
            Looks like you haven't added anything to your cart yet. Start shopping to fill it up!
          </p>
          
          <Button
            variant="primary"
            size="lg"
            onclick={handleContinueShopping}
            class="hover-lift"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l-1 12H6L5 9z" />
            </svg>
            Start Shopping
          </Button>
          
          <!-- Featured Categories -->
          <div class="mt-12 grid grid-cols-2 gap-4">
            <a 
              href="/products?category=electronics"
              class="p-4 rounded-xl border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors group"
            >
              <div class="text-sm font-medium text-gray-900 dark:text-white group-hover:text-primary-600">
                Electronics
              </div>
              <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">Latest gadgets</div>
            </a>
            <a 
              href="/products?category=fashion"
              class="p-4 rounded-xl border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors group"
            >
              <div class="text-sm font-medium text-gray-900 dark:text-white group-hover:text-primary-600">
                Fashion
              </div>
              <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">Trending styles</div>
            </a>
          </div>
        </Card>
      </div>
      
    {:else}
      <!-- Cart Content -->
      <div class="lg:grid lg:grid-cols-12 lg:gap-8">
        
        <!-- Cart Items -->
        <div class="lg:col-span-8">
          <Card class="glass">
            <div class="p-6">
              <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-6">
                Items in your cart ({cartCount})
              </h2>
              
              <div class="space-y-4">
                {#each cartItems as item (item.id)}
                  <div class="animate-fade-in">
                    <CartItem 
                      {item}
                      onQuantityChange={handleQuantityChange}
                      onRemove={handleRemoveItem}
                      disabled={isUpdating}
                    />
                  </div>
                {/each}
              </div>
              
              <!-- Continue Shopping -->
              <div class="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
                <Button
                  variant="ghost"
                  onclick={handleContinueShopping}
                  class="hover-lift"
                >
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                  </svg>
                  Continue Shopping
                </Button>
              </div>
            </div>
          </Card>
        </div>
        
        <!-- Order Summary -->
        <div class="lg:col-span-4 mt-8 lg:mt-0">
          <div class="sticky top-8">
            <Card class="glass">
              <div class="p-6">
                <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-6">
                  Order Summary
                </h2>
                
                <CartSummary 
                  items={cartItems}
                  shipping={shippingConfig}
                  tax={taxConfig}
                  onCheckout={handleCheckout}
                />
                
                <!-- Security Badges -->
                <div class="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
                  <div class="grid grid-cols-2 gap-4 text-center">
                    <div class="flex flex-col items-center">
                      <div class="w-8 h-8 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center mb-2">
                        <svg class="w-4 h-4 text-green-600 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
                        </svg>
                      </div>
                      <span class="text-xs text-gray-600 dark:text-gray-400">
                        Secure Checkout
                      </span>
                    </div>
                    
                    <div class="flex flex-col items-center">
                      <div class="w-8 h-8 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center mb-2">
                        <svg class="w-4 h-4 text-blue-600 dark:text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M10 2L3 7v11c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V7l-7-5z" clip-rule="evenodd" />
                        </svg>
                      </div>
                      <span class="text-xs text-gray-600 dark:text-gray-400">
                        Free Returns
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </Card>
            
            <!-- Shipping Info -->
            <Card class="glass mt-4">
              <div class="p-4">
                <div class="flex items-center">
                  <svg class="w-5 h-5 text-green-600 dark:text-green-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <div>
                    <p class="text-sm font-medium text-gray-900 dark:text-white">
                      {#if subtotal >= shippingConfig.free_threshold}
                        Free shipping included
                      {:else}
                        Add ${(shippingConfig.free_threshold - subtotal).toFixed(2)} for free shipping
                      {/if}
                    </p>
                    {#if subtotal < shippingConfig.free_threshold}
                      <div class="mt-2">
                        <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                          <div 
                            class="bg-gradient-to-r from-primary-500 to-primary-600 h-2 rounded-full transition-all duration-500"
                            style="width: {Math.min((subtotal / shippingConfig.free_threshold) * 100, 100)}%"
                          ></div>
                        </div>
                      </div>
                    {/if}
                  </div>
                </div>
              </div>
            </Card>
          </div>
        </div>
        
      </div>
    {/if}
  </div>
</div>

<style>
  @keyframes fade-in {
    from { 
      opacity: 0; 
      transform: translateY(10px); 
    }
    to { 
      opacity: 1; 
      transform: translateY(0); 
    }
  }
  
  .animate-fade-in {
    animation: fade-in 0.3s ease-out;
  }
</style>