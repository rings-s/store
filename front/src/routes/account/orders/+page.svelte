<!--
  @component OrdersPage
  Premium orders history page with comprehensive order management and tracking.
  Features order filtering, detailed order views, and reorder functionality.
-->
<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { getAuthStore } from '$lib/stores/auth.svelte.js';
  import { toastStore } from '$lib/stores/toast.svelte.js';
  import Button from '$lib/components/ui/Button.svelte';
  import Input from '$lib/components/ui/Input.svelte';
  import Card from '$lib/components/ui/Card.svelte';
  import Badge from '$lib/components/ui/Badge.svelte';
  import Modal from '$lib/components/ui/Modal.svelte';
  import Spinner from '$lib/components/ui/Spinner.svelte';
  import Select from '$lib/components/ui/Select.svelte';
  
  // Store access
  const authStore = getAuthStore();
  
  // Reactive state using Svelte 5 runes
  let mounted = $state(false);
  let isLoading = $state(false);
  let searchQuery = $state('');
  let statusFilter = $state('all');
  let selectedOrder = $state(null);
  let showOrderModal = $state(false);
  
  // Orders data (mock - replace with actual API)
  let orders = $state([
    {
      id: 'ORD-2024-001',
      date: '2024-01-15',
      status: 'delivered',
      total: 149.99,
      items: [
        { name: 'Premium Wireless Headphones', quantity: 1, price: 149.99, image: '/api/placeholder/80/80' }
      ],
      shipping_address: '123 Main St, City, State 12345',
      tracking_number: '1Z999AA1234567890'
    },
    {
      id: 'ORD-2024-002',
      date: '2024-01-20',
      status: 'shipped',
      total: 299.97,
      items: [
        { name: 'Smart Watch Series 8', quantity: 1, price: 299.97, image: '/api/placeholder/80/80' }
      ],
      shipping_address: '123 Main St, City, State 12345',
      tracking_number: '1Z999AA1234567891'
    },
    {
      id: 'ORD-2024-003',
      date: '2024-01-25',
      status: 'processing',
      total: 79.99,
      items: [
        { name: 'Wireless Mouse', quantity: 1, price: 49.99, image: '/api/placeholder/80/80' },
        { name: 'Keyboard Cover', quantity: 1, price: 29.99, image: '/api/placeholder/80/80' }
      ],
      shipping_address: '123 Main St, City, State 12345'
    },
    {
      id: 'ORD-2024-004',
      date: '2024-02-01',
      status: 'cancelled',
      total: 199.99,
      items: [
        { name: 'Gaming Controller', quantity: 1, price: 199.99, image: '/api/placeholder/80/80' }
      ],
      shipping_address: '123 Main St, City, State 12345',
      cancelled_reason: 'Customer request'
    }
  ]);
  
  // Derived values
  const isAuthenticated = $derived(authStore?.isAuthenticated || false);
  
  // Filter and search orders
  const filteredOrders = $derived(() => {
    let filtered = orders;
    
    // Filter by status
    if (statusFilter !== 'all') {
      filtered = filtered.filter(order => order.status === statusFilter);
    }
    
    // Search by order ID or item name
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(order => 
        order.id.toLowerCase().includes(query) ||
        order.items.some(item => item.name.toLowerCase().includes(query))
      );
    }
    
    // Sort by date (newest first)
    return filtered.sort((a, b) => new Date(b.date) - new Date(a.date));
  });
  
  // Status configuration
  const statusConfig = {
    processing: { 
      label: 'Processing', 
      color: 'warning',
      icon: 'clock'
    },
    shipped: { 
      label: 'Shipped', 
      color: 'primary',
      icon: 'truck'
    },
    delivered: { 
      label: 'Delivered', 
      color: 'success',
      icon: 'check'
    },
    cancelled: { 
      label: 'Cancelled', 
      color: 'danger',
      icon: 'x'
    }
  };
  
  const filterOptions = [
    { value: 'all', label: 'All Orders' },
    { value: 'processing', label: 'Processing' },
    { value: 'shipped', label: 'Shipped' },
    { value: 'delivered', label: 'Delivered' },
    { value: 'cancelled', label: 'Cancelled' }
  ];
  
  // Order actions
  function viewOrder(order) {
    selectedOrder = order;
    showOrderModal = true;
  }
  
  async function reorderItems(order) {
    try {
      // Add items to cart (mock implementation)
      console.log('Reordering items from order:', order.id);
      
      toastStore.add({
        type: 'success',
        message: `Items from order ${order.id} added to cart`
      });
      
      // Optionally redirect to cart
      // goto('/cart');
      
    } catch (error) {
      console.error('Reorder failed:', error);
      toastStore.add({
        type: 'error',
        message: 'Failed to add items to cart. Please try again.'
      });
    }
  }
  
  function trackOrder(order) {
    if (order.tracking_number) {
      // Open tracking page (could be external or internal)
      window.open(`/track/${order.tracking_number}`, '_blank');
    }
  }
  
  function downloadInvoice(order) {
    console.log('Downloading invoice for order:', order.id);
    // Implement invoice download
  }
  
  function cancelOrder(order) {
    console.log('Cancelling order:', order.id);
    // Implement order cancellation
  }
  
  // Get status icon
  function getStatusIcon(status) {
    const iconMap = {
      clock: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />',
      truck: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />',
      check: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />',
      x: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />'
    };
    return iconMap[statusConfig[status]?.icon] || iconMap.clock;
  }
  
  // Format date
  function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }
  
  // Authentication guard
  function checkAuth() {
    if (!isAuthenticated) {
      goto('/auth/login?redirect=' + encodeURIComponent('/account/orders'));
      return false;
    }
    return true;
  }
  
  // Load orders from API
  async function loadOrders() {
    isLoading = true;
    
    try {
      // In real app, fetch from API
      // const response = await ordersAPI.getOrders();
      // orders = response.data;
      
      await new Promise(resolve => setTimeout(resolve, 500)); // Simulate API call
      
    } catch (error) {
      console.error('Failed to load orders:', error);
      toastStore.add({
        type: 'error',
        message: 'Failed to load orders. Please try again.'
      });
    } finally {
      isLoading = false;
    }
  }
  
  // Lifecycle
  onMount(() => {
    mounted = true;
    
    if (!checkAuth()) return;
    
    loadOrders();
  });
</script>

<svelte:head>
  <title>My Orders - Premium Store</title>
  <meta name="description" content="View and manage your order history, track shipments, and reorder favorite items" />
</svelte:head>

{#if !isAuthenticated}
  <!-- Authentication Required -->
  <div class="min-h-screen bg-gray-50 dark:bg-dark-50 flex items-center justify-center">
    <Card class="glass max-w-md mx-auto text-center">
      <h2 class="text-2xl font-display font-bold text-gray-900 dark:text-white mb-4">
        Sign In Required
      </h2>
      <p class="text-gray-600 dark:text-gray-400 mb-6">
        Please sign in to view your orders.
      </p>
      <Button variant="primary" href="/auth/login?redirect=/account/orders">
        Sign In
      </Button>
    </Card>
  </div>
  
{:else}
  <!-- Orders Page -->
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
              <a href="/account" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300">
                Account
              </a>
            </li>
            <li class="text-gray-400">/</li>
            <li class="text-gray-900 dark:text-white font-medium">Orders</li>
          </ol>
        </nav>
        
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-display font-bold text-gray-900 dark:text-white">
              Order History
            </h1>
            <p class="mt-2 text-gray-600 dark:text-gray-400">
              Track and manage your orders
            </p>
          </div>
          
          <Button variant="primary" href="/products">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l-1 12H6L5 9z" />
            </svg>
            Shop Now
          </Button>
        </div>
      </div>
      
      <!-- Filters and Search -->
      <Card class="glass mb-8">
        <div class="p-6">
          <div class="flex flex-col sm:flex-row gap-4">
            <!-- Search -->
            <div class="flex-1">
              <Input
                type="search"
                placeholder="Search orders by ID or item name..."
                bind:value={searchQuery}
                icon="search"
              />
            </div>
            
            <!-- Status Filter -->
            <div class="sm:w-48">
              <Select
                options={filterOptions}
                bind:value={statusFilter}
                placeholder="Filter by status"
              />
            </div>
          </div>
        </div>
      </Card>
      
      {#if isLoading}
        <!-- Loading State -->
        <div class="flex justify-center items-center py-16">
          <div class="text-center">
            <Spinner size="lg" />
            <p class="mt-4 text-gray-600 dark:text-gray-400">Loading your orders...</p>
          </div>
        </div>
        
      {:else if filteredOrders.length === 0}
        <!-- Empty State -->
        <Card class="glass text-center py-16">
          <div class="w-24 h-24 mx-auto mb-6 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center">
            <svg class="w-12 h-12 text-gray-400 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
            </svg>
          </div>
          
          <h2 class="text-2xl font-display font-semibold text-gray-900 dark:text-white mb-3">
            {searchQuery || statusFilter !== 'all' ? 'No matching orders' : 'No orders yet'}
          </h2>
          
          <p class="text-gray-600 dark:text-gray-400 mb-8 max-w-sm mx-auto">
            {searchQuery || statusFilter !== 'all' 
              ? 'Try adjusting your search or filter criteria'
              : 'Start shopping to see your orders here'
            }
          </p>
          
          {#if searchQuery || statusFilter !== 'all'}
            <Button
              variant="ghost"
              onclick={() => { searchQuery = ''; statusFilter = 'all'; }}
            >
              Clear Filters
            </Button>
          {:else}
            <Button variant="primary" href="/products">
              Start Shopping
            </Button>
          {/if}
        </Card>
        
      {:else}
        <!-- Orders List -->
        <div class="space-y-6">
          {#each filteredOrders as order (order.id)}
            <Card class="glass hover-lift">
              <div class="p-6">
                <!-- Order Header -->
                <div class="flex items-center justify-between mb-4">
                  <div class="flex items-center space-x-4">
                    <div>
                      <h3 class="font-semibold text-gray-900 dark:text-white">
                        Order {order.id}
                      </h3>
                      <p class="text-sm text-gray-600 dark:text-gray-400">
                        Placed on {formatDate(order.date)}
                      </p>
                    </div>
                    
                    <Badge variant={statusConfig[order.status].color}>
                      <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        {@html getStatusIcon(order.status)}
                      </svg>
                      {statusConfig[order.status].label}
                    </Badge>
                  </div>
                  
                  <div class="text-right">
                    <div class="text-lg font-semibold text-gray-900 dark:text-white">
                      ${order.total.toFixed(2)}
                    </div>
                    <div class="text-sm text-gray-500 dark:text-gray-400">
                      {order.items.length} item{order.items.length !== 1 ? 's' : ''}
                    </div>
                  </div>
                </div>
                
                <!-- Order Items Preview -->
                <div class="flex items-center space-x-3 mb-4">
                  {#each order.items.slice(0, 3) as item}
                    <div class="w-12 h-12 bg-gray-200 dark:bg-gray-700 rounded-lg overflow-hidden">
                      <img 
                        src={item.image} 
                        alt={item.name}
                        class="w-full h-full object-cover"
                      />
                    </div>
                  {/each}
                  
                  {#if order.items.length > 3}
                    <div class="w-12 h-12 bg-gray-100 dark:bg-gray-800 rounded-lg flex items-center justify-center">
                      <span class="text-xs text-gray-500 dark:text-gray-400">
                        +{order.items.length - 3}
                      </span>
                    </div>
                  {/if}
                  
                  <div class="flex-1">
                    <p class="text-sm text-gray-600 dark:text-gray-400">
                      {order.items[0].name}
                      {#if order.items.length > 1}
                        <span class="text-gray-400">and {order.items.length - 1} more item{order.items.length > 2 ? 's' : ''}</span>
                      {/if}
                    </p>
                  </div>
                </div>
                
                <!-- Order Actions -->
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-3">
                    <Button
                      variant="primary"
                      size="sm"
                      onclick={() => viewOrder(order)}
                    >
                      View Details
                    </Button>
                    
                    {#if order.tracking_number && order.status === 'shipped'}
                      <Button
                        variant="ghost"
                        size="sm"
                        onclick={() => trackOrder(order)}
                      >
                        Track Package
                      </Button>
                    {/if}
                    
                    {#if order.status === 'delivered'}
                      <Button
                        variant="ghost"
                        size="sm"
                        onclick={() => reorderItems(order)}
                      >
                        Reorder
                      </Button>
                    {/if}
                  </div>
                  
                  <div class="flex items-center space-x-2">
                    {#if order.status !== 'cancelled'}
                      <button
                        onclick={() => downloadInvoice(order)}
                        class="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                        title="Download Invoice"
                      >
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      </button>
                    {/if}
                    
                    {#if order.status === 'processing'}
                      <button
                        onclick={() => cancelOrder(order)}
                        class="p-2 text-red-400 hover:text-red-600 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
                        title="Cancel Order"
                      >
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    {/if}
                  </div>
                </div>
              </div>
            </Card>
          {/each}
        </div>
      {/if}
    </div>
  </div>
  
  <!-- Order Details Modal -->
  {#if selectedOrder}
    <Modal bind:open={showOrderModal} title={`Order ${selectedOrder.id}`} size="lg">
      <div class="space-y-6">
        <!-- Order Status -->
        <div class="flex items-center justify-between">
          <Badge variant={statusConfig[selectedOrder.status].color} class="text-base">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {@html getStatusIcon(selectedOrder.status)}
            </svg>
            {statusConfig[selectedOrder.status].label}
          </Badge>
          
          <div class="text-right">
            <div class="text-lg font-semibold text-gray-900 dark:text-white">
              ${selectedOrder.total.toFixed(2)}
            </div>
            <div class="text-sm text-gray-500 dark:text-gray-400">
              {formatDate(selectedOrder.date)}
            </div>
          </div>
        </div>
        
        <!-- Order Items -->
        <div>
          <h3 class="font-semibold text-gray-900 dark:text-white mb-3">Order Items</h3>
          <div class="space-y-3">
            {#each selectedOrder.items as item}
              <div class="flex items-center space-x-4 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                <img 
                  src={item.image} 
                  alt={item.name}
                  class="w-16 h-16 object-cover rounded-lg"
                />
                <div class="flex-1">
                  <h4 class="font-medium text-gray-900 dark:text-white">{item.name}</h4>
                  <p class="text-sm text-gray-600 dark:text-gray-400">
                    Quantity: {item.quantity} × ${item.price.toFixed(2)}
                  </p>
                </div>
                <div class="text-right">
                  <div class="font-semibold text-gray-900 dark:text-white">
                    ${(item.quantity * item.price).toFixed(2)}
                  </div>
                </div>
              </div>
            {/each}
          </div>
        </div>
        
        <!-- Shipping Information -->
        <div>
          <h3 class="font-semibold text-gray-900 dark:text-white mb-3">Shipping Information</h3>
          <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
            <p class="text-gray-900 dark:text-white">{selectedOrder.shipping_address}</p>
            {#if selectedOrder.tracking_number}
              <p class="text-sm text-gray-600 dark:text-gray-400 mt-2">
                Tracking: <span class="font-mono">{selectedOrder.tracking_number}</span>
              </p>
            {/if}
          </div>
        </div>
        
        {#if selectedOrder.cancelled_reason}
          <!-- Cancellation Reason -->
          <div>
            <h3 class="font-semibold text-gray-900 dark:text-white mb-3">Cancellation Reason</h3>
            <div class="bg-red-50 dark:bg-red-900/20 rounded-lg p-4">
              <p class="text-red-700 dark:text-red-300">{selectedOrder.cancelled_reason}</p>
            </div>
          </div>
        {/if}
      </div>
      
      <div slot="footer" class="flex items-center justify-end space-x-3">
        {#if selectedOrder.status === 'delivered'}
          <Button
            variant="ghost"
            onclick={() => reorderItems(selectedOrder)}
          >
            Reorder Items
          </Button>
        {/if}
        
        {#if selectedOrder.tracking_number}
          <Button
            variant="primary"
            onclick={() => trackOrder(selectedOrder)}
          >
            Track Package
          </Button>
        {/if}
      </div>
    </Modal>
  {/if}
{/if}