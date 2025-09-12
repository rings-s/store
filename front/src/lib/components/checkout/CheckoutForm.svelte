<!--
  @component CheckoutForm
  Premium checkout form with comprehensive validation and payment processing.
  Features multi-step flow, address validation, and secure payment handling.
  
  @prop items - Array of cart items
  @prop onSubmit - Form submission handler
  @prop loading - Loading state (optional)
  @prop className - Additional CSS classes
-->
<script>
  import { formatPrice } from '$lib/utils/format';
  import { validateEmail, validatePhone, validateRequired, validateCreditCard } from '$lib/utils/validators';
  import { toastStore } from '$lib/stores/toast.svelte.js';
  
  let { 
    items = [],
    onSubmit = () => {},
    loading = false,
    className = '' 
  } = $props();
  
  // State management with Svelte 5 runes
  let currentStep = $state(1);
  let isSubmitting = $state(false);
  let errors = $state({});
  
  // Form data
  let formData = $state({
    // Shipping Information
    shipping: {
      firstName: '',
      lastName: '',
      email: '',
      phone: '',
      address: '',
      apartment: '',
      city: '',
      state: '',
      zipCode: '',
      country: 'US'
    },
    
    // Billing Information
    billing: {
      sameAsShipping: true,
      firstName: '',
      lastName: '',
      address: '',
      apartment: '',
      city: '',
      state: '',
      zipCode: '',
      country: 'US'
    },
    
    // Payment Information
    payment: {
      method: 'card',
      cardNumber: '',
      expiryDate: '',
      cvv: '',
      nameOnCard: ''
    },
    
    // Additional Options
    options: {
      createAccount: false,
      password: '',
      newsletter: false,
      specialInstructions: ''
    }
  });
  
  // Computed values
  const totalSteps = 3;
  const progressPercentage = $derived(() => (currentStep / totalSteps) * 100);
  
  const subtotal = $derived(() =>
    items.reduce((sum, item) => sum + (item.price * item.quantity), 0)
  );
  
  const shipping = 5.99;
  const tax = $derived(() => subtotal() * 0.0825); // 8.25% tax
  const total = $derived(() => subtotal() + shipping + tax());
  
  // Functions
  function validateStep(step) {
    const newErrors = {};
    
    switch (step) {
      case 1: // Shipping Information
        if (!validateRequired(formData.shipping.firstName)) {
          newErrors['shipping.firstName'] = 'First name is required';
        }
        if (!validateRequired(formData.shipping.lastName)) {
          newErrors['shipping.lastName'] = 'Last name is required';
        }
        if (!validateEmail(formData.shipping.email)) {
          newErrors['shipping.email'] = 'Valid email is required';
        }
        if (!validatePhone(formData.shipping.phone)) {
          newErrors['shipping.phone'] = 'Valid phone number is required';
        }
        if (!validateRequired(formData.shipping.address)) {
          newErrors['shipping.address'] = 'Address is required';
        }
        if (!validateRequired(formData.shipping.city)) {
          newErrors['shipping.city'] = 'City is required';
        }
        if (!validateRequired(formData.shipping.state)) {
          newErrors['shipping.state'] = 'State is required';
        }
        if (!validateRequired(formData.shipping.zipCode)) {
          newErrors['shipping.zipCode'] = 'ZIP code is required';
        }
        break;
        
      case 2: // Billing Information
        if (!formData.billing.sameAsShipping) {
          if (!validateRequired(formData.billing.firstName)) {
            newErrors['billing.firstName'] = 'First name is required';
          }
          if (!validateRequired(formData.billing.lastName)) {
            newErrors['billing.lastName'] = 'Last name is required';
          }
          if (!validateRequired(formData.billing.address)) {
            newErrors['billing.address'] = 'Address is required';
          }
          if (!validateRequired(formData.billing.city)) {
            newErrors['billing.city'] = 'City is required';
          }
          if (!validateRequired(formData.billing.state)) {
            newErrors['billing.state'] = 'State is required';
          }
          if (!validateRequired(formData.billing.zipCode)) {
            newErrors['billing.zipCode'] = 'ZIP code is required';
          }
        }
        break;
        
      case 3: // Payment Information
        if (formData.payment.method === 'card') {
          if (!validateCreditCard(formData.payment.cardNumber)) {
            newErrors['payment.cardNumber'] = 'Valid card number is required';
          }
          if (!validateRequired(formData.payment.expiryDate)) {
            newErrors['payment.expiryDate'] = 'Expiry date is required';
          }
          if (!validateRequired(formData.payment.cvv)) {
            newErrors['payment.cvv'] = 'CVV is required';
          }
          if (!validateRequired(formData.payment.nameOnCard)) {
            newErrors['payment.nameOnCard'] = 'Name on card is required';
          }
        }
        break;
    }
    
    errors = newErrors;
    return Object.keys(newErrors).length === 0;
  }
  
  function nextStep() {
    if (validateStep(currentStep)) {
      if (currentStep < totalSteps) {
        currentStep++;
      }
    } else {
      toastStore.add({
        type: 'error',
        message: 'Please fix the errors before continuing'
      });
    }
  }
  
  function prevStep() {
    if (currentStep > 1) {
      currentStep--;
    }
  }
  
  async function handleSubmit() {
    if (!validateStep(3) || isSubmitting) return;
    
    isSubmitting = true;
    
    try {
      await onSubmit(formData);
      toastStore.add({
        type: 'success',
        message: 'Order placed successfully!'
      });
    } catch (error) {
      toastStore.add({
        type: 'error',
        message: error.message || 'Failed to place order. Please try again.'
      });
    } finally {
      isSubmitting = false;
    }
  }
  
  function formatCardNumber(value) {
    return value.replace(/\s/g, '').replace(/(.{4})/g, '$1 ').trim();
  }
  
  function formatExpiryDate(value) {
    const v = value.replace(/\D/g, '');
    if (v.length >= 2) {
      return v.substring(0, 2) + '/' + v.substring(2, 4);
    }
    return v;
  }
</script>

<div class="max-w-4xl mx-auto space-y-8 {className}">
  <!-- Progress Indicator -->
  <div class="glass-panel rounded-2xl p-6">
    <div class="flex items-center justify-between mb-4">
      <h1 class="text-2xl font-display font-bold text-gray-900 dark:text-white">
        Checkout
      </h1>
      <div class="text-sm text-gray-600 dark:text-gray-400">
        Step {currentStep} of {totalSteps}
      </div>
    </div>
    
    <!-- Progress Bar -->
    <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 overflow-hidden">
      <div 
        class="h-full bg-gradient-to-r from-primary-500 to-primary-600 transition-all duration-500 ease-out"
        style="width: {progressPercentage}%"
      ></div>
    </div>
    
    <!-- Step Labels -->
    <div class="flex justify-between mt-4">
      <div class="flex items-center gap-2 {currentStep >= 1 ? 'text-primary-600 dark:text-primary-400' : 'text-gray-400'}">
        <div class="w-6 h-6 rounded-full {currentStep >= 1 ? 'bg-primary-600 text-white' : 'bg-gray-300 text-gray-600'} 
                    flex items-center justify-center text-xs font-medium">
          1
        </div>
        <span class="text-sm font-medium">Shipping</span>
      </div>
      
      <div class="flex items-center gap-2 {currentStep >= 2 ? 'text-primary-600 dark:text-primary-400' : 'text-gray-400'}">
        <div class="w-6 h-6 rounded-full {currentStep >= 2 ? 'bg-primary-600 text-white' : 'bg-gray-300 text-gray-600'} 
                    flex items-center justify-center text-xs font-medium">
          2
        </div>
        <span class="text-sm font-medium">Billing</span>
      </div>
      
      <div class="flex items-center gap-2 {currentStep >= 3 ? 'text-primary-600 dark:text-primary-400' : 'text-gray-400'}">
        <div class="w-6 h-6 rounded-full {currentStep >= 3 ? 'bg-primary-600 text-white' : 'bg-gray-300 text-gray-600'} 
                    flex items-center justify-center text-xs font-medium">
          3
        </div>
        <span class="text-sm font-medium">Payment</span>
      </div>
    </div>
  </div>
  
  <!-- Form Content -->
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
    <!-- Main Form -->
    <div class="lg:col-span-2">
      <div class="glass-panel rounded-3xl p-8 space-y-8">
        {#if currentStep === 1}
          <!-- Step 1: Shipping Information -->
          <div class="space-y-6">
            <h2 class="text-xl font-display font-semibold text-gray-900 dark:text-white">
              Shipping Information
            </h2>
            
            <!-- Contact Information -->
            <div class="space-y-4">
              <h3 class="font-medium text-gray-900 dark:text-white">Contact</h3>
              
              <input
                type="email"
                bind:value={formData.shipping.email}
                placeholder="Email address"
                class="input-primary w-full {errors['shipping.email'] ? 'border-red-500' : ''}"
              />
              {#if errors['shipping.email']}
                <p class="text-red-600 dark:text-red-400 text-sm">{errors['shipping.email']}</p>
              {/if}
              
              <input
                type="tel"
                bind:value={formData.shipping.phone}
                placeholder="Phone number"
                class="input-primary w-full {errors['shipping.phone'] ? 'border-red-500' : ''}"
              />
              {#if errors['shipping.phone']}
                <p class="text-red-600 dark:text-red-400 text-sm">{errors['shipping.phone']}</p>
              {/if}
            </div>
            
            <!-- Name -->
            <div class="grid grid-cols-2 gap-4">
              <div>
                <input
                  type="text"
                  bind:value={formData.shipping.firstName}
                  placeholder="First name"
                  class="input-primary w-full {errors['shipping.firstName'] ? 'border-red-500' : ''}"
                />
                {#if errors['shipping.firstName']}
                  <p class="text-red-600 dark:text-red-400 text-sm mt-1">{errors['shipping.firstName']}</p>
                {/if}
              </div>
              
              <div>
                <input
                  type="text"
                  bind:value={formData.shipping.lastName}
                  placeholder="Last name"
                  class="input-primary w-full {errors['shipping.lastName'] ? 'border-red-500' : ''}"
                />
                {#if errors['shipping.lastName']}
                  <p class="text-red-600 dark:text-red-400 text-sm mt-1">{errors['shipping.lastName']}</p>
                {/if}
              </div>
            </div>
            
            <!-- Address -->
            <div class="space-y-4">
              <input
                type="text"
                bind:value={formData.shipping.address}
                placeholder="Street address"
                class="input-primary w-full {errors['shipping.address'] ? 'border-red-500' : ''}"
              />
              {#if errors['shipping.address']}
                <p class="text-red-600 dark:text-red-400 text-sm">{errors['shipping.address']}</p>
              {/if}
              
              <input
                type="text"
                bind:value={formData.shipping.apartment}
                placeholder="Apartment, suite, etc. (optional)"
                class="input-primary w-full"
              />
              
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <input
                    type="text"
                    bind:value={formData.shipping.city}
                    placeholder="City"
                    class="input-primary w-full {errors['shipping.city'] ? 'border-red-500' : ''}"
                  />
                  {#if errors['shipping.city']}
                    <p class="text-red-600 dark:text-red-400 text-sm mt-1">{errors['shipping.city']}</p>
                  {/if}
                </div>
                
                <div>
                  <select
                    bind:value={formData.shipping.state}
                    class="input-primary w-full {errors['shipping.state'] ? 'border-red-500' : ''}"
                  >
                    <option value="">Select state</option>
                    <option value="CA">California</option>
                    <option value="NY">New York</option>
                    <option value="TX">Texas</option>
                    <option value="FL">Florida</option>
                  </select>
                  {#if errors['shipping.state']}
                    <p class="text-red-600 dark:text-red-400 text-sm mt-1">{errors['shipping.state']}</p>
                  {/if}
                </div>
              </div>
              
              <input
                type="text"
                bind:value={formData.shipping.zipCode}
                placeholder="ZIP code"
                class="input-primary w-full {errors['shipping.zipCode'] ? 'border-red-500' : ''}"
              />
              {#if errors['shipping.zipCode']}
                <p class="text-red-600 dark:text-red-400 text-sm">{errors['shipping.zipCode']}</p>
              {/if}
            </div>
          </div>
        {:else if currentStep === 2}
          <!-- Step 2: Billing Information -->
          <div class="space-y-6">
            <h2 class="text-xl font-display font-semibold text-gray-900 dark:text-white">
              Billing Information
            </h2>
            
            <!-- Same as shipping checkbox -->
            <label class="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                bind:checked={formData.billing.sameAsShipping}
                class="w-4 h-4 text-primary-600 bg-gray-100 border-gray-300 rounded focus:ring-primary-500 focus:ring-2"
              />
              <span class="text-gray-900 dark:text-white">Same as shipping address</span>
            </label>
            
            {#if !formData.billing.sameAsShipping}
              <!-- Billing Address Fields -->
              <div class="space-y-4">
                <div class="grid grid-cols-2 gap-4">
                  <input
                    type="text"
                    bind:value={formData.billing.firstName}
                    placeholder="First name"
                    class="input-primary w-full {errors['billing.firstName'] ? 'border-red-500' : ''}"
                  />
                  <input
                    type="text"
                    bind:value={formData.billing.lastName}
                    placeholder="Last name"
                    class="input-primary w-full {errors['billing.lastName'] ? 'border-red-500' : ''}"
                  />
                </div>
                
                <input
                  type="text"
                  bind:value={formData.billing.address}
                  placeholder="Street address"
                  class="input-primary w-full {errors['billing.address'] ? 'border-red-500' : ''}"
                />
                
                <input
                  type="text"
                  bind:value={formData.billing.apartment}
                  placeholder="Apartment, suite, etc. (optional)"
                  class="input-primary w-full"
                />
                
                <div class="grid grid-cols-2 gap-4">
                  <input
                    type="text"
                    bind:value={formData.billing.city}
                    placeholder="City"
                    class="input-primary w-full {errors['billing.city'] ? 'border-red-500' : ''}"
                  />
                  
                  <select
                    bind:value={formData.billing.state}
                    class="input-primary w-full {errors['billing.state'] ? 'border-red-500' : ''}"
                  >
                    <option value="">Select state</option>
                    <option value="CA">California</option>
                    <option value="NY">New York</option>
                    <option value="TX">Texas</option>
                    <option value="FL">Florida</option>
                  </select>
                </div>
                
                <input
                  type="text"
                  bind:value={formData.billing.zipCode}
                  placeholder="ZIP code"
                  class="input-primary w-full {errors['billing.zipCode'] ? 'border-red-500' : ''}"
                />
              </div>
            {/if}
          </div>
        {:else if currentStep === 3}
          <!-- Step 3: Payment Information -->
          <div class="space-y-6">
            <h2 class="text-xl font-display font-semibold text-gray-900 dark:text-white">
              Payment Information
            </h2>
            
            <!-- Payment Method -->
            <div class="space-y-4">
              <h3 class="font-medium text-gray-900 dark:text-white">Payment Method</h3>
              
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <label class="flex items-center justify-center gap-3 p-4 border-2 rounded-xl cursor-pointer transition-colors
                             {formData.payment.method === 'card' ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20' : 'border-gray-200 dark:border-gray-700'}">
                  <input
                    type="radio"
                    bind:group={formData.payment.method}
                    value="card"
                    class="text-primary-600 focus:ring-primary-500"
                  />
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
                  </svg>
                  <span class="font-medium">Card</span>
                </label>
                
                <label class="flex items-center justify-center gap-3 p-4 border-2 rounded-xl cursor-pointer transition-colors
                             {formData.payment.method === 'paypal' ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20' : 'border-gray-200 dark:border-gray-700'}">
                  <input
                    type="radio"
                    bind:group={formData.payment.method}
                    value="paypal"
                    class="text-primary-600 focus:ring-primary-500"
                  />
                  <span class="font-medium text-blue-600">PayPal</span>
                </label>
                
                <label class="flex items-center justify-center gap-3 p-4 border-2 rounded-xl cursor-pointer transition-colors
                             {formData.payment.method === 'apple' ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20' : 'border-gray-200 dark:border-gray-700'}">
                  <input
                    type="radio"
                    bind:group={formData.payment.method}
                    value="apple"
                    class="text-primary-600 focus:ring-primary-500"
                  />
                  <span class="font-medium">Apple Pay</span>
                </label>
              </div>
            </div>
            
            {#if formData.payment.method === 'card'}
              <!-- Credit Card Fields -->
              <div class="space-y-4">
                <input
                  type="text"
                  bind:value={formData.payment.nameOnCard}
                  placeholder="Name on card"
                  class="input-primary w-full {errors['payment.nameOnCard'] ? 'border-red-500' : ''}"
                />
                {#if errors['payment.nameOnCard']}
                  <p class="text-red-600 dark:text-red-400 text-sm">{errors['payment.nameOnCard']}</p>
                {/if}
                
                <input
                  type="text"
                  bind:value={formData.payment.cardNumber}
                  on:input={(e) => formData.payment.cardNumber = formatCardNumber(e.target.value)}
                  placeholder="Card number"
                  maxlength="19"
                  class="input-primary w-full {errors['payment.cardNumber'] ? 'border-red-500' : ''}"
                />
                {#if errors['payment.cardNumber']}
                  <p class="text-red-600 dark:text-red-400 text-sm">{errors['payment.cardNumber']}</p>
                {/if}
                
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <input
                      type="text"
                      bind:value={formData.payment.expiryDate}
                      on:input={(e) => formData.payment.expiryDate = formatExpiryDate(e.target.value)}
                      placeholder="MM/YY"
                      maxlength="5"
                      class="input-primary w-full {errors['payment.expiryDate'] ? 'border-red-500' : ''}"
                    />
                    {#if errors['payment.expiryDate']}
                      <p class="text-red-600 dark:text-red-400 text-sm mt-1">{errors['payment.expiryDate']}</p>
                    {/if}
                  </div>
                  
                  <div>
                    <input
                      type="text"
                      bind:value={formData.payment.cvv}
                      placeholder="CVV"
                      maxlength="4"
                      class="input-primary w-full {errors['payment.cvv'] ? 'border-red-500' : ''}"
                    />
                    {#if errors['payment.cvv']}
                      <p class="text-red-600 dark:text-red-400 text-sm mt-1">{errors['payment.cvv']}</p>
                    {/if}
                  </div>
                </div>
              </div>
            {/if}
            
            <!-- Additional Options -->
            <div class="space-y-4 pt-6 border-t border-gray-200 dark:border-gray-700">
              <label class="flex items-center gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  bind:checked={formData.options.createAccount}
                  class="w-4 h-4 text-primary-600 bg-gray-100 border-gray-300 rounded focus:ring-primary-500 focus:ring-2"
                />
                <span class="text-gray-900 dark:text-white">Create an account for faster checkout</span>
              </label>
              
              <label class="flex items-center gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  bind:checked={formData.options.newsletter}
                  class="w-4 h-4 text-primary-600 bg-gray-100 border-gray-300 rounded focus:ring-primary-500 focus:ring-2"
                />
                <span class="text-gray-900 dark:text-white">Subscribe to our newsletter for deals and updates</span>
              </label>
            </div>
          </div>
        {/if}
        
        <!-- Navigation Buttons -->
        <div class="flex justify-between pt-6 border-t border-gray-200 dark:border-gray-700">
          <button
            onclick={prevStep}
            disabled={currentStep === 1}
            class="btn-secondary px-6 py-3 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Back
          </button>
          
          {#if currentStep < totalSteps}
            <button
              onclick={nextStep}
              class="btn-primary px-6 py-3 group relative overflow-hidden"
            >
              <span class="relative z-10 flex items-center gap-2">
                Continue
                <svg class="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </span>
              <div class="absolute inset-0 bg-gradient-to-r from-primary-600 to-primary-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </button>
          {:else}
            <button
              onclick={handleSubmit}
              disabled={isSubmitting}
              class="btn-primary px-8 py-3 group relative overflow-hidden disabled:opacity-50"
            >
              <span class="relative z-10 flex items-center gap-2">
                {#if isSubmitting}
                  <svg class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Processing...
                {:else}
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                  Complete Order
                {/if}
              </span>
              <div class="absolute inset-0 bg-gradient-to-r from-green-600 to-green-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </button>
          {/if}
        </div>
      </div>
    </div>
    
    <!-- Order Summary Sidebar -->
    <div class="lg:col-span-1">
      <div class="glass-panel rounded-3xl p-6 sticky top-6">
        <h3 class="text-lg font-display font-semibold text-gray-900 dark:text-white mb-6">
          Order Summary
        </h3>
        
        <!-- Items -->
        <div class="space-y-4 mb-6">
          {#each items as item}
            <div class="flex items-center gap-3">
              <div class="w-12 h-12 rounded-lg bg-gray-100 dark:bg-gray-800 flex-shrink-0">
                {#if item.image}
                  <img src={item.image} alt={item.name} class="w-full h-full object-cover rounded-lg" />
                {:else}
                  <div class="w-full h-full flex items-center justify-center">
                    <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                {/if}
              </div>
              
              <div class="flex-1 min-w-0">
                <h4 class="font-medium text-gray-900 dark:text-white text-sm leading-tight">
                  {item.name}
                </h4>
                <p class="text-xs text-gray-500 dark:text-gray-400">
                  Qty: {item.quantity}
                </p>
              </div>
              
              <div class="text-sm font-medium text-gray-900 dark:text-white">
                {formatPrice(item.price * item.quantity)}
              </div>
            </div>
          {/each}
        </div>
        
        <!-- Totals -->
        <div class="space-y-3 border-t border-gray-200 dark:border-gray-700 pt-6">
          <div class="flex justify-between text-sm">
            <span class="text-gray-600 dark:text-gray-400">Subtotal</span>
            <span class="font-medium text-gray-900 dark:text-white">{formatPrice(subtotal)}</span>
          </div>
          
          <div class="flex justify-between text-sm">
            <span class="text-gray-600 dark:text-gray-400">Shipping</span>
            <span class="font-medium text-gray-900 dark:text-white">{formatPrice(shipping)}</span>
          </div>
          
          <div class="flex justify-between text-sm">
            <span class="text-gray-600 dark:text-gray-400">Tax</span>
            <span class="font-medium text-gray-900 dark:text-white">{formatPrice(tax)}</span>
          </div>
          
          <div class="flex justify-between text-lg font-semibold text-gray-900 dark:text-white pt-3 border-t border-gray-200 dark:border-gray-700">
            <span>Total</span>
            <span>{formatPrice(total)}</span>
          </div>
        </div>
        
        <!-- Security Notice -->
        <div class="flex items-center gap-2 mt-6 p-3 bg-green-50 dark:bg-green-900/20 rounded-xl">
          <svg class="w-5 h-5 text-green-600 dark:text-green-400 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
          </svg>
          <div class="text-xs text-green-800 dark:text-green-300">
            <div class="font-medium">Secure Checkout</div>
            <div>Your payment info is protected with 256-bit SSL encryption</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>