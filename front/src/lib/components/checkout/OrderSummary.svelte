<!--
  @component OrderSummary
  Premium order confirmation and tracking component.
  Features order details, status tracking, and customer actions.
  
  @prop order - Order object with full details
  @prop loading - Loading state (optional)
  @prop onTrackOrder - Order tracking handler (optional)
  @prop onReorder - Reorder handler (optional)
  @prop className - Additional CSS classes
-->
<script>
  import Badge from '../ui/Badge.svelte';
  import { formatPrice, formatDate } from '$lib/utils/format';
  import { toastStore } from '$lib/stores/toast.svelte.js';
  
  let { 
    order,
    loading = false,
    onTrackOrder = () => {},
    onReorder = () => {},
    className = '' 
  } = $props();
  
  // State management with Svelte 5 runes
  let isTracking = $state(false);
  let isReordering = $state(false);
  let showFullAddress = $state(false);
  
  // Computed values
  const statusConfig = $derived(() => {
    const status = order?.status?.toLowerCase() || 'pending';
    const configs = {
      pending: { 
        variant: 'warning', 
        icon: 'clock',
        message: 'Your order is being processed',
        color: 'text-yellow-600 dark:text-yellow-400'
      },
      confirmed: { 
        variant: 'info', 
        icon: 'check',
        message: 'Order confirmed and being prepared',
        color: 'text-blue-600 dark:text-blue-400'
      },
      shipped: { 
        variant: 'primary', 
        icon: 'truck',
        message: 'Your order is on its way',
        color: 'text-primary-600 dark:text-primary-400'
      },
      delivered: { 
        variant: 'success', 
        icon: 'check-circle',
        message: 'Order delivered successfully',
        color: 'text-green-600 dark:text-green-400'
      },
      cancelled: { 
        variant: 'danger', 
        icon: 'x-circle',
        message: 'Order was cancelled',
        color: 'text-red-600 dark:text-red-400'
      }
    };
    return configs[status] || configs.pending;
  });
  
  const canTrack = $derived(() => 
    order?.tracking_number && ['shipped', 'delivered'].includes(order?.status?.toLowerCase())
  );
  
  const canReorder = $derived(() => 
    order?.status && ['delivered', 'cancelled'].includes(order?.status?.toLowerCase())
  );
  
  const estimatedDelivery = $derived(() => {
    if (!order?.estimated_delivery) return null;
    const deliveryDate = new Date(order.estimated_delivery);
    const now = new Date();
    const diffTime = deliveryDate - now;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays < 0) return 'Delivery date has passed';
    if (diffDays === 0) return 'Expected today';
    if (diffDays === 1) return 'Expected tomorrow';
    return `Expected in ${diffDays} days`;
  });
  
  // Functions
  async function handleTrackOrder() {
    if (!canTrack || isTracking) return;
    
    isTracking = true;
    
    try {
      await onTrackOrder(order.tracking_number);
      toastStore.add({
        type: 'info',
        message: 'Opening tracking information...'
      });
    } catch (error) {
      toastStore.add({
        type: 'error',
        message: 'Failed to track order. Please try again.'
      });
    } finally {
      isTracking = false;
    }
  }
  
  async function handleReorder() {
    if (!canReorder || isReordering) return;
    
    isReordering = true;
    
    try {
      await onReorder(order.id);
      toastStore.add({
        type: 'success',
        message: 'Items added to cart successfully!'
      });
    } catch (error) {
      toastStore.add({
        type: 'error',
        message: 'Failed to reorder. Please try again.'
      });
    } finally {
      isReordering = false;
    }
  }
  
  function copyOrderNumber() {
    navigator.clipboard.writeText(order.order_number);
    toastStore.add({
      type: 'success',
      message: 'Order number copied to clipboard!'
    });
  }
  
  function getStatusIcon(iconType) {
    const icons = {
      clock: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z',
      check: 'M5 13l4 4L19 7',
      truck: 'M9 17a2 2 0 11-4 0 2 2 0 014 0zM21 17a2 2 0 11-4 0 2 2 0 014 0zM13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0',
      'check-circle': 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
      'x-circle': 'M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z'
    };
    return icons[iconType] || icons.clock;
  }
</script>

{#if loading}
  <!-- Loading State -->
  <div class="animate-pulse space-y-6 {className}">
    <div class="glass-panel rounded-3xl p-8 space-y-6">
      <div class="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/3"></div>
      <div class="space-y-4">
        <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded"></div>
        <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-2/3"></div>
        <div class="h-20 bg-gray-200 dark:bg-gray-700 rounded"></div>
      </div>
    </div>
  </div>
{:else if order}
  <div class="max-w-4xl mx-auto space-y-8 {className}">
    <!-- Order Header -->
    <div class="glass-panel rounded-3xl p-8">
      <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
        <div class="space-y-4">
          <div class="flex items-center gap-3">
            <h1 class="text-3xl font-display font-bold text-gray-900 dark:text-white">
              Order Confirmation
            </h1>
            <Badge variant={statusConfig().variant} size="lg">
              {order.status}
            </Badge>
          </div>
          
          <div class="flex items-center gap-4">
            <button
              onclick={copyOrderNumber}
              class="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors group"
            >
              <span class="font-mono text-lg">#{order.order_number}</span>
              <svg class="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
            </button>
            
            <div class="text-sm text-gray-500 dark:text-gray-400">
              Placed on {formatDate(order.created_at)}
            </div>
          </div>
        </div>
        
        <!-- Action Buttons -->
        <div class="flex flex-col sm:flex-row gap-3">
          {#if canTrack}
            <button
              onclick={handleTrackOrder}
              disabled={isTracking}
              class="btn-secondary group relative overflow-hidden disabled:opacity-50"
            >
              <span class="relative z-10 flex items-center gap-2">
                {#if isTracking}
                  <svg class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                {:else}
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                  </svg>
                {/if}
                Track Order
              </span>
            </button>
          {/if}
          
          {#if canReorder}
            <button
              onclick={handleReorder}
              disabled={isReordering}
              class="btn-primary group relative overflow-hidden disabled:opacity-50"
            >
              <span class="relative z-10 flex items-center gap-2">
                {#if isReordering}
                  <svg class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                {:else}
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                {/if}
                Reorder
              </span>
              <div class="absolute inset-0 bg-gradient-to-r from-primary-600 to-primary-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </button>
          {/if}
        </div>
      </div>
    </div>
    
    <!-- Order Status & Timeline -->
    <div class="glass-panel rounded-3xl p-8">
      <div class="flex items-center gap-4 mb-6">
        <div class={`w-12 h-12 rounded-full flex items-center justify-center ${statusConfig().color} bg-current bg-opacity-10`}>
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={getStatusIcon(statusConfig().icon)} />
          </svg>
        </div>
        
        <div class="flex-1">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-1">
            {statusConfig().message}
          </h3>
          {#if estimatedDelivery()}
            <p class="text-gray-600 dark:text-gray-400">
              {estimatedDelivery()}
            </p>
          {/if}
        </div>
        
        {#if order.tracking_number}
          <div class="text-right">
            <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">Tracking Number</div>
            <div class="font-mono text-sm font-medium text-gray-900 dark:text-white">
              {order.tracking_number}
            </div>
          </div>
        {/if}
      </div>
      
      <!-- Progress Timeline -->
      <div class="flex justify-between items-center">
        {#each ['pending', 'confirmed', 'shipped', 'delivered'] as step, index}
          {@const isCompleted = ['confirmed', 'shipped', 'delivered'].slice(0, ['pending', 'confirmed', 'shipped', 'delivered'].indexOf(order?.status?.toLowerCase() || 'pending') + 1).includes(step)}
          {@const isCurrent = step === (order?.status?.toLowerCase() || 'pending')}
          
          <div class="flex flex-col items-center flex-1">
            <div class={`w-8 h-8 rounded-full flex items-center justify-center border-2 transition-all duration-300 ${
              isCompleted || isCurrent 
                ? 'bg-primary-600 border-primary-600 text-white' 
                : 'bg-gray-200 border-gray-300 text-gray-400 dark:bg-gray-700 dark:border-gray-600'
            }`}>
              {#if isCompleted && !isCurrent}
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
              {:else}
                <div class="w-2 h-2 rounded-full bg-current"></div>
              {/if}
            </div>
            
            <div class="text-xs font-medium text-center mt-2 capitalize {
              isCompleted || isCurrent ? 'text-primary-600 dark:text-primary-400' : 'text-gray-400'
            }">
              {step}
            </div>
          </div>
          
          {#if index < 3}
            <div class={`flex-1 h-0.5 mx-2 transition-all duration-300 ${
              isCompleted ? 'bg-primary-600' : 'bg-gray-200 dark:bg-gray-700'
            }`}></div>
          {/if}
        {/each}
      </div>
    </div>
    
    <!-- Order Items -->
    <div class="glass-panel rounded-3xl p-8">
      <h3 class="text-xl font-display font-semibold text-gray-900 dark:text-white mb-6">
        Order Items ({order.items?.length || 0})
      </h3>
      
      <div class="space-y-4">
        {#each order.items || [] as item}
          <div class="flex items-center gap-4 p-4 bg-gray-50 dark:bg-gray-800/50 rounded-xl">
            <div class="w-16 h-16 rounded-lg bg-gray-200 dark:bg-gray-700 flex-shrink-0 overflow-hidden">
              {#if item.image}
                <img src={item.image} alt={item.name} class="w-full h-full object-cover" />
              {:else}
                <div class="w-full h-full flex items-center justify-center">
                  <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
              {/if}
            </div>
            
            <div class="flex-1">
              <h4 class="font-semibold text-gray-900 dark:text-white mb-1">
                {item.name}
              </h4>
              {#if item.variant}
                <p class="text-sm text-gray-600 dark:text-gray-400 mb-1">
                  {item.variant}
                </p>
              {/if}
              <div class="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400">
                <span>Qty: {item.quantity}</span>
                <span>•</span>
                <span>{formatPrice(item.price)} each</span>
              </div>
            </div>
            
            <div class="text-right">
              <div class="font-semibold text-gray-900 dark:text-white">
                {formatPrice(item.price * item.quantity)}
              </div>
            </div>
          </div>
        {/each}
      </div>
    </div>
    
    <!-- Order Summary & Addresses -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Order Summary -->
      <div class="glass-panel rounded-3xl p-8">
        <h3 class="text-xl font-display font-semibold text-gray-900 dark:text-white mb-6">
          Order Summary
        </h3>
        
        <div class="space-y-3">
          <div class="flex justify-between">
            <span class="text-gray-600 dark:text-gray-400">Subtotal</span>
            <span class="font-medium text-gray-900 dark:text-white">{formatPrice(order.subtotal)}</span>
          </div>
          
          {#if order.discount > 0}
            <div class="flex justify-between text-green-600 dark:text-green-400">
              <span>Discount</span>
              <span>-{formatPrice(order.discount)}</span>
            </div>
          {/if}
          
          <div class="flex justify-between">
            <span class="text-gray-600 dark:text-gray-400">Shipping</span>
            <span class="font-medium text-gray-900 dark:text-white">
              {order.shipping_cost > 0 ? formatPrice(order.shipping_cost) : 'Free'}
            </span>
          </div>
          
          <div class="flex justify-between">
            <span class="text-gray-600 dark:text-gray-400">Tax</span>
            <span class="font-medium text-gray-900 dark:text-white">{formatPrice(order.tax)}</span>
          </div>
          
          <div class="border-t border-gray-200 dark:border-gray-700 pt-3">
            <div class="flex justify-between text-lg font-semibold text-gray-900 dark:text-white">
              <span>Total</span>
              <span>{formatPrice(order.total)}</span>
            </div>
          </div>
          
          {#if order.payment_method}
            <div class="border-t border-gray-200 dark:border-gray-700 pt-3">
              <div class="flex justify-between text-sm">
                <span class="text-gray-600 dark:text-gray-400">Payment Method</span>
                <span class="font-medium text-gray-900 dark:text-white capitalize">
                  {order.payment_method}
                </span>
              </div>
            </div>
          {/if}
        </div>
      </div>
      
      <!-- Addresses -->
      <div class="space-y-6">
        <!-- Shipping Address -->
        <div class="glass-panel rounded-3xl p-8">
          <h3 class="text-xl font-display font-semibold text-gray-900 dark:text-white mb-4">
            Shipping Address
          </h3>
          
          {#if order.shipping_address}
            <div class="space-y-2 text-gray-600 dark:text-gray-400">
              <div class="font-medium text-gray-900 dark:text-white">
                {order.shipping_address.first_name} {order.shipping_address.last_name}
              </div>
              <div>{order.shipping_address.address}</div>
              {#if order.shipping_address.apartment}
                <div>{order.shipping_address.apartment}</div>
              {/if}
              <div>
                {order.shipping_address.city}, {order.shipping_address.state} {order.shipping_address.zip_code}
              </div>
              {#if order.shipping_address.phone}
                <div class="pt-2 border-t border-gray-200 dark:border-gray-700">
                  Phone: {order.shipping_address.phone}
                </div>
              {/if}
            </div>
          {/if}
        </div>
        
        <!-- Billing Address -->
        {#if order.billing_address && !order.billing_same_as_shipping}
          <div class="glass-panel rounded-3xl p-8">
            <h3 class="text-xl font-display font-semibold text-gray-900 dark:text-white mb-4">
              Billing Address
            </h3>
            
            <div class="space-y-2 text-gray-600 dark:text-gray-400">
              <div class="font-medium text-gray-900 dark:text-white">
                {order.billing_address.first_name} {order.billing_address.last_name}
              </div>
              <div>{order.billing_address.address}</div>
              {#if order.billing_address.apartment}
                <div>{order.billing_address.apartment}</div>
              {/if}
              <div>
                {order.billing_address.city}, {order.billing_address.state} {order.billing_address.zip_code}
              </div>
            </div>
          </div>
        {/if}
      </div>
    </div>
    
    <!-- Contact Support -->
    <div class="glass-panel rounded-3xl p-8 text-center">
      <div class="max-w-md mx-auto">
        <h3 class="text-lg font-display font-semibold text-gray-900 dark:text-white mb-2">
          Need Help?
        </h3>
        <p class="text-gray-600 dark:text-gray-400 mb-6">
          Questions about your order? Our customer support team is here to help.
        </p>
        
        <div class="flex flex-col sm:flex-row gap-3 justify-center">
          <a
            href="/contact"
            class="btn-secondary"
          >
            Contact Support
          </a>
          
          <a
            href="mailto:support@example.com?subject=Order #{order.order_number}"
            class="btn-primary group relative overflow-hidden"
          >
            <span class="relative z-10 flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              Email Us
            </span>
            <div class="absolute inset-0 bg-gradient-to-r from-primary-600 to-primary-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          </a>
        </div>
      </div>
    </div>
  </div>
{:else}
  <!-- Error State -->
  <div class="text-center py-16 {className}">
    <div class="glass-panel rounded-3xl p-12 max-w-md mx-auto">
      <svg class="w-20 h-20 mx-auto text-gray-400 dark:text-gray-600 mb-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <h3 class="text-xl font-display font-semibold text-gray-900 dark:text-white mb-3">
        Order Not Found
      </h3>
      <p class="text-gray-600 dark:text-gray-400 mb-6">
        We couldn't find the order you're looking for. Please check your order number and try again.
      </p>
      <a href="/account/orders" class="btn-primary">
        View All Orders
      </a>
    </div>
  </div>
{/if}