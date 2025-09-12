<!--
  @component CheckoutPage
  Premium checkout page with comprehensive payment flow and order processing.
  Features multi-step checkout, address management, and secure payment integration.
-->
<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { getCartStore } from '$lib/stores/cart.svelte.js';
  import { getAuthStore } from '$lib/stores/auth.svelte.js';
  import CheckoutForm from '$lib/components/checkout/CheckoutForm.svelte';
  import OrderSummary from '$lib/components/checkout/OrderSummary.svelte';
  import Button from '$lib/components/ui/Button.svelte';
  import Card from '$lib/components/ui/Card.svelte';
  import Spinner from '$lib/components/ui/Spinner.svelte';
  import Badge from '$lib/components/ui/Badge.svelte';
  
  // Store access
  const cartStore = getCartStore();
  const authStore = getAuthStore();
  
  // Reactive state using Svelte 5 runes
  let mounted = $state(false);
  let currentStep = $state(1);
  let isProcessing = $state(false);
  let processingMessage = $state('');
  let orderData = $state({
    shipping_address: {},
    billing_address: {},
    payment_method: null,
    shipping_method: 'standard',
    special_instructions: ''
  });
  
  // Derived values from stores
  const cartItems = $derived(cartStore?.items || []);
  const isCartLoading = $derived(cartStore?.isLoading || false);
  const cartTotal = $derived(cartStore?.total || 0);
  const cartCount = $derived(cartStore?.itemsCount || 0);
  const isAuthenticated = $derived(authStore?.isAuthenticated || false);
  const user = $derived(authStore?.user || null);
  
  // Checkout steps
  const steps = [
    { id: 1, title: 'Shipping', description: 'Delivery information' },
    { id: 2, title: 'Payment', description: 'Payment method' },
    { id: 3, title: 'Review', description: 'Confirm your order' }
  ];
  
  // Computed values
  const isEmpty = $derived(cartItems.length === 0);
  const subtotal = $derived(() => 
    cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0)
  );
  
  const shippingMethods = [
    { 
      id: 'standard', 
      name: 'Standard Shipping', 
      description: '5-7 business days', 
      price: 5.99,
      estimated: '5-7 days'
    },
    { 
      id: 'express', 
      name: 'Express Shipping', 
      description: '2-3 business days', 
      price: 12.99,
      estimated: '2-3 days'
    },
    { 
      id: 'overnight', 
      name: 'Overnight Shipping', 
      description: 'Next business day', 
      price: 24.99,
      estimated: 'Next day'
    }
  ];
  
  const selectedShipping = $derived(() => 
    shippingMethods.find(method => method.id === orderData.shipping_method) || shippingMethods[0]
  );
  
  const shippingCost = $derived(() => 
    subtotal >= 50 && orderData.shipping_method === 'standard' ? 0 : selectedShipping.price
  );
  
  const tax = $derived(() => subtotal * 0.0825);
  const finalTotal = $derived(() => subtotal + shippingCost + tax);
  
  // Authentication guard
  function checkAuthentication() {
    if (!isAuthenticated) {
      goto('/auth/login?redirect=' + encodeURIComponent('/checkout'));
      return false;
    }
    return true;
  }
  
  // Cart validation
  function validateCart() {
    if (isEmpty) {
      goto('/cart');
      return false;
    }
    return true;
  }
  
  // Step navigation
  function goToStep(step) {
    if (step <= currentStep || isProcessing) return;
    currentStep = step;
  }
  
  function nextStep() {
    if (currentStep < steps.length && !isProcessing) {
      currentStep++;
    }
  }
  
  function previousStep() {
    if (currentStep > 1 && !isProcessing) {
      currentStep--;
    }
  }
  
  // Checkout form handlers
  function handleShippingUpdate(shippingData) {
    orderData.shipping_address = { ...shippingData.address };
    orderData.shipping_method = shippingData.shipping_method;
    
    // Auto-advance to payment if address is complete
    if (shippingData.address.street && shippingData.address.city) {
      nextStep();
    }
  }
  
  function handlePaymentUpdate(paymentData) {
    orderData.payment_method = paymentData.payment_method;
    orderData.billing_address = { ...paymentData.billing_address };
    
    // Auto-advance to review if payment is selected
    if (paymentData.payment_method) {
      nextStep();
    }
  }
  
  // Order processing
  async function processOrder() {
    if (isProcessing) return;
    
    isProcessing = true;
    processingMessage = 'Validating order details...';
    
    try {
      // Step 1: Validate order
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      processingMessage = 'Processing payment...';
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      processingMessage = 'Confirming order...';
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Call checkout API
      const response = await cartStore.checkout({
        ...orderData,
        items: cartItems,
        subtotal,
        shipping_cost: shippingCost,
        tax,
        total: finalTotal
      });
      
      // Redirect to order confirmation
      goto(`/account/orders/${response.order_id}?success=true`);
      
    } catch (error) {
      console.error('Checkout failed:', error);
      isProcessing = false;
      processingMessage = '';
      // Handle error (show toast, etc.)
    }
  }
  
  // Return to cart
  function returnToCart() {
    goto('/cart');
  }
  
  // Lifecycle
  onMount(() => {
    mounted = true;
    
    // Validate prerequisites
    if (!checkAuthentication() || !validateCart()) {
      return;
    }
    
    // Initialize cart if needed
    if (cartStore && !cartStore.items?.length) {
      cartStore.init();
    }
  });
</script>

<svelte:head>
  <title>Checkout - Premium Store</title>
  <meta name="description" content="Complete your purchase securely with our streamlined checkout process" />
</svelte:head>

{#if !isAuthenticated}
  <!-- Authentication Required -->
  <div class="min-h-screen bg-gray-50 dark:bg-dark-50 flex items-center justify-center">
    <Card class="glass max-w-md mx-auto text-center">
      <h2 class="text-2xl font-display font-bold text-gray-900 dark:text-white mb-4">
        Sign In Required
      </h2>
      <p class="text-gray-600 dark:text-gray-400 mb-6">
        Please sign in to continue with your checkout.
      </p>
      <Button variant="primary" href="/auth/login?redirect=/checkout">
        Sign In to Continue
      </Button>
    </Card>
  </div>
  
{:else if isEmpty && !isCartLoading}
  <!-- Empty Cart -->
  <div class="min-h-screen bg-gray-50 dark:bg-dark-50 flex items-center justify-center">
    <Card class="glass max-w-md mx-auto text-center">
      <h2 class="text-2xl font-display font-bold text-gray-900 dark:text-white mb-4">
        Your Cart is Empty
      </h2>
      <p class="text-gray-600 dark:text-gray-400 mb-6">
        Add some items to your cart before proceeding to checkout.
      </p>
      <Button variant="primary" href="/products">
        Continue Shopping
      </Button>
    </Card>
  </div>
  
{:else if isCartLoading}
  <!-- Loading State -->
  <div class="min-h-screen bg-gray-50 dark:bg-dark-50 flex items-center justify-center">
    <div class="text-center">
      <Spinner size="lg" />
      <p class="mt-4 text-gray-600 dark:text-gray-400">Loading checkout...</p>
    </div>
  </div>
  
{:else}
  <!-- Checkout Content -->
  <div class="min-h-screen bg-gray-50 dark:bg-dark-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <!-- Header -->
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
              <a href="/cart" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300">
                Cart
              </a>
            </li>
            <li class="text-gray-400">/</li>
            <li class="text-gray-900 dark:text-white font-medium">Checkout</li>
          </ol>
        </nav>
        
        <div class="flex items-center justify-between">
          <h1 class="text-3xl font-display font-bold text-gray-900 dark:text-white">
            Secure Checkout
          </h1>
          <Badge variant="success" class="flex items-center">
            <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
            </svg>
            SSL Secured
          </Badge>
        </div>
      </div>
      
      <!-- Progress Steps -->
      <div class="mb-8">
        <Card class="glass">
          <div class="p-6">
            <nav aria-label="Progress">
              <ol class="flex items-center justify-center space-x-4 sm:space-x-8">
                {#each steps as step (step.id)}
                  <li class="flex items-center">
                    <button
                      onclick={() => goToStep(step.id)}
                      disabled={step.id > currentStep || isProcessing}
                      class="group flex flex-col items-center"
                    >
                      <div class="flex items-center justify-center w-10 h-10 rounded-full border-2 transition-all
                                  {step.id < currentStep 
                                    ? 'bg-primary-600 border-primary-600 text-white' 
                                    : step.id === currentStep 
                                      ? 'border-primary-600 text-primary-600 bg-white dark:bg-dark-100' 
                                      : 'border-gray-300 text-gray-500 bg-white dark:bg-dark-100'
                                  }
                                  {step.id <= currentStep && !isProcessing ? 'cursor-pointer hover:scale-105' : 'cursor-default'}">
                        {#if step.id < currentStep}
                          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                          </svg>
                        {:else}
                          <span class="text-sm font-medium">{step.id}</span>
                        {/if}
                      </div>
                      <div class="mt-2 text-center">
                        <div class="text-sm font-medium text-gray-900 dark:text-white">
                          {step.title}
                        </div>
                        <div class="text-xs text-gray-500 dark:text-gray-400">
                          {step.description}
                        </div>
                      </div>
                    </button>
                    
                    {#if step.id < steps.length}
                      <div class="hidden sm:block w-16 h-px bg-gray-300 dark:bg-gray-600 ml-4"></div>
                    {/if}
                  </li>
                {/each}
              </ol>
            </nav>
          </div>
        </Card>
      </div>
      
      <div class="lg:grid lg:grid-cols-12 lg:gap-8">
        
        <!-- Checkout Form -->
        <div class="lg:col-span-7">
          <Card class="glass">
            <div class="p-6">
              {#if isProcessing}
                <!-- Processing State -->
                <div class="text-center py-12">
                  <Spinner size="lg" />
                  <h3 class="mt-4 text-lg font-semibold text-gray-900 dark:text-white">
                    Processing Your Order
                  </h3>
                  <p class="mt-2 text-gray-600 dark:text-gray-400">
                    {processingMessage}
                  </p>
                  <div class="mt-4 w-64 mx-auto bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div class="bg-gradient-to-r from-primary-500 to-primary-600 h-2 rounded-full transition-all duration-1000"
                         style="width: {processingMessage.includes('Validating') ? '33%' : processingMessage.includes('Processing') ? '66%' : '100%'}"></div>
                  </div>
                </div>
              {:else}
                <CheckoutForm 
                  {currentStep}
                  {orderData}
                  {shippingMethods}
                  onShippingUpdate={handleShippingUpdate}
                  onPaymentUpdate={handlePaymentUpdate}
                />
              {/if}
            </div>
            
            {#if !isProcessing}
              <!-- Navigation Buttons -->
              <div class="px-6 py-4 bg-gray-50 dark:bg-dark-100 rounded-b-2xl flex items-center justify-between">
                <div>
                  {#if currentStep > 1}
                    <Button
                      variant="ghost"
                      onclick={previousStep}
                      disabled={isProcessing}
                    >
                      <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                      </svg>
                      Previous
                    </Button>
                  {:else}
                    <Button
                      variant="ghost"
                      onclick={returnToCart}
                    >
                      <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                      </svg>
                      Back to Cart
                    </Button>
                  {/if}
                </div>
                
                <div>
                  {#if currentStep < steps.length}
                    <Button
                      variant="primary"
                      onclick={nextStep}
                      disabled={isProcessing}
                    >
                      Continue
                      <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                      </svg>
                    </Button>
                  {:else}
                    <Button
                      variant="primary"
                      onclick={processOrder}
                      disabled={isProcessing}
                      class="hover-lift"
                    >
                      <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      Complete Order
                    </Button>
                  {/if}
                </div>
              </div>
            {/if}
          </Card>
        </div>
        
        <!-- Order Summary -->
        <div class="lg:col-span-5 mt-8 lg:mt-0">
          <div class="sticky top-8">
            <OrderSummary 
              items={cartItems}
              subtotal={subtotal}
              shippingCost={shippingCost}
              tax={tax}
              total={finalTotal}
              shippingMethod={selectedShipping}
            />
            
            <!-- Security & Guarantees -->
            <Card class="glass mt-6">
              <div class="p-4">
                <h3 class="font-semibold text-gray-900 dark:text-white mb-4">
                  Your Order is Protected
                </h3>
                
                <div class="space-y-3">
                  <div class="flex items-center">
                    <svg class="w-5 h-5 text-green-600 dark:text-green-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
                    </svg>
                    <span class="text-sm text-gray-600 dark:text-gray-400">
                      256-bit SSL encryption
                    </span>
                  </div>
                  
                  <div class="flex items-center">
                    <svg class="w-5 h-5 text-blue-600 dark:text-blue-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M10 2L3 7v11c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V7l-7-5z" clip-rule="evenodd" />
                    </svg>
                    <span class="text-sm text-gray-600 dark:text-gray-400">
                      30-day money-back guarantee
                    </span>
                  </div>
                  
                  <div class="flex items-center">
                    <svg class="w-5 h-5 text-purple-600 dark:text-purple-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
                    </svg>
                    <span class="text-sm text-gray-600 dark:text-gray-400">
                      24/7 customer support
                    </span>
                  </div>
                </div>
              </div>
            </Card>
          </div>
        </div>
        
      </div>
    </div>
  </div>
{/if}