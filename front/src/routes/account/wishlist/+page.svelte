<!--
  @component WishlistPage
  Premium wishlist management page with product grid, filtering, and wishlist actions.
  Features move to cart functionality and wishlist sharing capabilities.
-->
<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { getAuthStore } from '$lib/stores/auth.svelte.js';
  import { getCartStore } from '$lib/stores/cart.svelte.js';
  import { toastStore } from '$lib/stores/toast.svelte.js';
  import Button from '$lib/components/ui/Button.svelte';
  import Input from '$lib/components/ui/Input.svelte';
  import Card from '$lib/components/ui/Card.svelte';
  import Spinner from '$lib/components/ui/Spinner.svelte';
  import Modal from '$lib/components/ui/Modal.svelte';
  
  // Store access
  const authStore = getAuthStore();
  const cartStore = getCartStore();
  
  // Reactive state using Svelte 5 runes
  let mounted = $state(false);
  let isLoading = $state(true);
  let isUpdatingWishlist = $state(false);
  let showShareModal = $state(false);
  let shareUrl = $state('');
  let searchTerm = $state('');
  let sortBy = $state('date_added');
  let filterBy = $state('all');
  
  // Wishlist data
  let wishlistItems = $state([]);
  let wishlistStats = $state({
    totalItems: 0,
    totalValue: 0,
    itemsOnSale: 0,
    avgRating: 0
  });
  
  // Derived values
  const isAuthenticated = $derived(authStore?.isAuthenticated || false);
  const user = $derived(authStore?.user || null);
  
  // Filter and search logic
  const filteredItems = $derived(() => {
    let items = wishlistItems || [];
    
    // Search filter
    if (searchTerm.trim()) {
      const search = searchTerm.toLowerCase();
      items = items.filter(item => 
        item.product.name.toLowerCase().includes(search) ||
        item.product.description.toLowerCase().includes(search) ||
        item.product.category.name.toLowerCase().includes(search)
      );
    }
    
    // Category filter
    if (filterBy !== 'all') {
      if (filterBy === 'on_sale') {
        items = items.filter(item => item.product.sale_price > 0);
      } else if (filterBy === 'out_of_stock') {
        items = items.filter(item => item.product.stock_quantity <= 0);
      } else if (filterBy === 'in_stock') {
        items = items.filter(item => item.product.stock_quantity > 0);
      } else {
        items = items.filter(item => item.product.category.slug === filterBy);
      }
    }
    
    // Sort items
    switch (sortBy) {
      case 'name':
        items.sort((a, b) => a.product.name.localeCompare(b.product.name));
        break;
      case 'price_low':
        items.sort((a, b) => 
          (a.product.sale_price || a.product.price) - (b.product.sale_price || b.product.price)
        );
        break;
      case 'price_high':
        items.sort((a, b) => 
          (b.product.sale_price || b.product.price) - (a.product.sale_price || a.product.price)
        );
        break;
      case 'rating':
        items.sort((a, b) => (b.product.average_rating || 0) - (a.product.average_rating || 0));
        break;
      case 'date_added':
      default:
        items.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
        break;
    }
    
    return items;
  });
  
  const categories = $derived(() => {
    if (!wishlistItems) return [];
    const cats = new Set(wishlistItems.map(item => item.product.category));
    return Array.from(cats);
  });
  
  // Load wishlist data
  async function loadWishlist() {
    if (!isAuthenticated) {
      goto('/auth/login?redirect=/account/wishlist');
      return;
    }
    
    isLoading = true;
    
    try {
      // Mock API call - replace with actual API endpoint
      const response = await fetch('/api/wishlist/', {
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (!response.ok) throw new Error('Failed to load wishlist');
      
      const data = await response.json();
      wishlistItems = data.results || [];
      
      // Calculate statistics
      const stats = wishlistItems.reduce((acc, item) => {
        const price = item.product.sale_price || item.product.price;
        acc.totalValue += price;
        if (item.product.sale_price > 0) acc.itemsOnSale++;
        acc.avgRating += item.product.average_rating || 0;
        return acc;
      }, { totalValue: 0, itemsOnSale: 0, avgRating: 0 });
      
      wishlistStats = {
        totalItems: wishlistItems.length,
        totalValue: stats.totalValue,
        itemsOnSale: stats.itemsOnSale,
        avgRating: wishlistItems.length > 0 ? stats.avgRating / wishlistItems.length : 0
      };
      
    } catch (error) {
      console.error('Error loading wishlist:', error);
      toastStore.add({
        type: 'error',
        message: 'Failed to load wishlist. Please try again.'
      });
    } finally {
      isLoading = false;
    }
  }
  
  // Remove item from wishlist
  async function removeFromWishlist(itemId) {
    isUpdatingWishlist = true;
    
    try {
      const response = await fetch(`/api/wishlist/${itemId}/`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (!response.ok) throw new Error('Failed to remove item');
      
      wishlistItems = wishlistItems.filter(item => item.id !== itemId);
      
      toastStore.add({
        type: 'success',
        message: 'Item removed from wishlist'
      });
      
    } catch (error) {
      console.error('Error removing from wishlist:', error);
      toastStore.add({
        type: 'error',
        message: 'Failed to remove item from wishlist'
      });
    } finally {
      isUpdatingWishlist = false;
    }
  }
  
  // Add to cart from wishlist
  async function addToCart(product) {
    try {
      await cartStore.addItem(product.id, 1);
      
      toastStore.add({
        type: 'success',
        message: `${product.name} added to cart`
      });
      
    } catch (error) {
      console.error('Error adding to cart:', error);
      toastStore.add({
        type: 'error',
        message: 'Failed to add item to cart'
      });
    }
  }
  
  // Move all to cart
  async function moveAllToCart() {
    isUpdatingWishlist = true;
    
    try {
      const inStockItems = filteredItems.filter(item => item.product.stock_quantity > 0);
      
      for (const item of inStockItems) {
        await cartStore.addItem(item.product.id, 1);
      }
      
      toastStore.add({
        type: 'success',
        message: `${inStockItems.length} items added to cart`
      });
      
    } catch (error) {
      console.error('Error moving items to cart:', error);
      toastStore.add({
        type: 'error',
        message: 'Failed to add some items to cart'
      });
    } finally {
      isUpdatingWishlist = false;
    }
  }
  
  // Clear entire wishlist
  async function clearWishlist() {
    if (!confirm('Are you sure you want to clear your entire wishlist?')) {
      return;
    }
    
    isUpdatingWishlist = true;
    
    try {
      const response = await fetch('/api/wishlist/clear/', {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (!response.ok) throw new Error('Failed to clear wishlist');
      
      wishlistItems = [];
      wishlistStats = { totalItems: 0, totalValue: 0, itemsOnSale: 0, avgRating: 0 };
      
      toastStore.add({
        type: 'success',
        message: 'Wishlist cleared successfully'
      });
      
    } catch (error) {
      console.error('Error clearing wishlist:', error);
      toastStore.add({
        type: 'error',
        message: 'Failed to clear wishlist'
      });
    } finally {
      isUpdatingWishlist = false;
    }
  }
  
  // Share wishlist
  function shareWishlist() {
    const url = `${window.location.origin}/wishlist/shared/${user.id}`;
    shareUrl = url;
    showShareModal = true;
  }
  
  // Copy share URL
  async function copyShareUrl() {
    try {
      await navigator.clipboard.writeText(shareUrl);
      toastStore.add({
        type: 'success',
        message: 'Share URL copied to clipboard'
      });
    } catch (error) {
      console.error('Error copying URL:', error);
      toastStore.add({
        type: 'error',
        message: 'Failed to copy URL'
      });
    }
  }
  
  // Lifecycle
  onMount(() => {
    mounted = true;
    loadWishlist();
  });
</script>

<svelte:head>
  <title>My Wishlist - Premium Store</title>
  <meta name="description" content="Manage your wishlist and save your favorite products for later" />
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100 dark:from-dark-50 dark:via-dark-100 dark:to-dark-200">
  <div class="container mx-auto px-4 py-8">
    <!-- Header Section -->
    <div class="mb-8">
      <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
        <div>
          <h1 class="text-4xl font-display font-bold text-gray-900 dark:text-white mb-2">
            My Wishlist
          </h1>
          <p class="text-gray-600 dark:text-gray-400">
            Keep track of your favorite items and save them for later
          </p>
        </div>
        
        <!-- Wishlist Stats -->
        {#if !isLoading && wishlistItems.length > 0}
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="text-center p-3 bg-white/80 dark:bg-dark-100/80 rounded-xl glass">
              <div class="text-2xl font-bold text-primary-600 dark:text-primary-400">
                {wishlistStats.totalItems}
              </div>
              <div class="text-xs text-gray-600 dark:text-gray-400">Items</div>
            </div>
            <div class="text-center p-3 bg-white/80 dark:bg-dark-100/80 rounded-xl glass">
              <div class="text-2xl font-bold text-green-600 dark:text-green-400">
                ${wishlistStats.totalValue.toFixed(2)}
              </div>
              <div class="text-xs text-gray-600 dark:text-gray-400">Total Value</div>
            </div>
            <div class="text-center p-3 bg-white/80 dark:bg-dark-100/80 rounded-xl glass">
              <div class="text-2xl font-bold text-red-600 dark:text-red-400">
                {wishlistStats.itemsOnSale}
              </div>
              <div class="text-xs text-gray-600 dark:text-gray-400">On Sale</div>
            </div>
            <div class="text-center p-3 bg-white/80 dark:bg-dark-100/80 rounded-xl glass">
              <div class="text-2xl font-bold text-yellow-600 dark:text-yellow-400">
                {wishlistStats.avgRating.toFixed(1)}★
              </div>
              <div class="text-xs text-gray-600 dark:text-gray-400">Avg Rating</div>
            </div>
          </div>
        {/if}
      </div>
    </div>
    
    {#if isLoading}
      <!-- Loading State -->
      <div class="flex items-center justify-center py-20">
        <div class="text-center">
          <Spinner size="lg" class="mb-4" />
          <p class="text-gray-600 dark:text-gray-400">Loading your wishlist...</p>
        </div>
      </div>
      
    {:else if wishlistItems.length === 0}
      <!-- Empty State -->
      <div class="text-center py-20">
        <div class="w-24 h-24 mx-auto mb-6 bg-gradient-to-r from-primary-600 to-primary-700 rounded-full flex items-center justify-center">
          <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
          </svg>
        </div>
        <h2 class="text-2xl font-display font-bold text-gray-900 dark:text-white mb-4">
          Your wishlist is empty
        </h2>
        <p class="text-gray-600 dark:text-gray-400 mb-8 max-w-md mx-auto">
          Start adding products to your wishlist to keep track of items you want to buy later
        </p>
        <Button href="/products" class="hover-lift">
          Browse Products
        </Button>
      </div>
      
    {:else}
      <!-- Filters and Actions -->
      <div class="mb-8">
        <Card class="glass p-6">
          <div class="flex flex-col lg:flex-row gap-4">
            <!-- Search -->
            <div class="flex-1">
              <Input
                type="search"
                placeholder="Search wishlist..."
                bind:value={searchTerm}
                icon="search"
              />
            </div>
            
            <!-- Filter by category -->
            <div class="lg:w-48">
              <select
                bind:value={filterBy}
                class="w-full px-4 py-3 bg-white/80 dark:bg-dark-100/80 border border-gray-200 dark:border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="all">All Categories</option>
                <option value="on_sale">On Sale</option>
                <option value="in_stock">In Stock</option>
                <option value="out_of_stock">Out of Stock</option>
                {#each categories as category}
                  <option value={category.slug}>{category.name}</option>
                {/each}
              </select>
            </div>
            
            <!-- Sort -->
            <div class="lg:w-48">
              <select
                bind:value={sortBy}
                class="w-full px-4 py-3 bg-white/80 dark:bg-dark-100/80 border border-gray-200 dark:border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="date_added">Date Added</option>
                <option value="name">Name A-Z</option>
                <option value="price_low">Price: Low to High</option>
                <option value="price_high">Price: High to Low</option>
                <option value="rating">Highest Rated</option>
              </select>
            </div>
            
            <!-- Actions -->
            <div class="flex gap-2">
              <Button
                variant="outline"
                onclick={shareWishlist}
                disabled={isUpdatingWishlist}
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
                </svg>
                Share
              </Button>
              <Button
                variant="primary"
                onclick={moveAllToCart}
                disabled={isUpdatingWishlist || filteredItems.filter(item => item.product.stock_quantity > 0).length === 0}
                loading={isUpdatingWishlist}
              >
                Add All to Cart
              </Button>
              <Button
                variant="ghost"
                onclick={clearWishlist}
                disabled={isUpdatingWishlist}
                class="text-red-600 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300"
              >
                Clear All
              </Button>
            </div>
          </div>
        </Card>
      </div>
      
      <!-- Wishlist Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {#each filteredItems as item (item.id)}
          <Card class="glass hover-lift group overflow-hidden">
            <!-- Product Image -->
            <div class="relative aspect-square overflow-hidden rounded-t-xl">
              <img
                src={item.product.image || '/images/placeholder-product.webp'}
                alt={item.product.name}
                class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                loading="lazy"
              />
              
              <!-- Sale Badge -->
              {#if item.product.sale_price > 0}
                <div class="absolute top-3 left-3 bg-red-500 text-white px-2 py-1 rounded-full text-xs font-medium">
                  Sale
                </div>
              {/if}
              
              <!-- Stock Status -->
              {#if item.product.stock_quantity <= 0}
                <div class="absolute top-3 right-3 bg-gray-800 text-white px-2 py-1 rounded-full text-xs font-medium">
                  Out of Stock
                </div>
              {/if}
              
              <!-- Quick Actions -->
              <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                <div class="flex gap-2">
                  <Button
                    variant="white"
                    size="sm"
                    onclick={() => goto(`/products/${item.product.slug}`)}
                    class="magnetic"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  </Button>
                  {#if item.product.stock_quantity > 0}
                    <Button
                      variant="white"
                      size="sm"
                      onclick={() => addToCart(item.product)}
                      class="magnetic"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17M17 13a2 2 0 11-4 0 2 2 0 014 0zM9 19a1 1 0 11-2 0 1 1 0 012 0zM20 19a1 1 0 11-2 0 1 1 0 012 0z" />
                      </svg>
                    </Button>
                  {/if}
                </div>
              </div>
            </div>
            
            <!-- Product Info -->
            <div class="p-6">
              <div class="mb-2">
                <span class="text-sm text-primary-600 dark:text-primary-400 font-medium">
                  {item.product.category.name}
                </span>
              </div>
              
              <h3 class="font-display font-semibold text-gray-900 dark:text-white mb-2 line-clamp-2">
                {item.product.name}
              </h3>
              
              <!-- Rating -->
              {#if item.product.average_rating > 0}
                <div class="flex items-center gap-2 mb-3">
                  <div class="flex text-yellow-400">
                    {#each Array(5) as _, i}
                      <svg class="w-4 h-4 {i < item.product.average_rating ? 'fill-current' : 'fill-gray-300 dark:fill-gray-600'}" viewBox="0 0 20 20">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.286 3.957a1 1 0 00.95.69h4.162c.969 0 1.371 1.24.588 1.81l-3.37 2.448a1 1 0 00-.364 1.118l1.286 3.957c.3.921-.755 1.688-1.54 1.118l-3.37-2.448a1 1 0 00-1.175 0l-3.37 2.448c-.784.57-1.838-.197-1.539-1.118l1.286-3.957a1 1 0 00-.364-1.118L2.049 9.384c-.783-.57-.38-1.81.588-1.81h4.162a1 1 0 00.95-.69l1.286-3.957z" />
                      </svg>
                    {/each}
                  </div>
                  <span class="text-sm text-gray-600 dark:text-gray-400">
                    ({item.product.review_count || 0})
                  </span>
                </div>
              {/if}
              
              <!-- Price -->
              <div class="flex items-center justify-between mb-4">
                <div>
                  {#if item.product.sale_price > 0}
                    <span class="text-lg font-bold text-red-600 dark:text-red-400">
                      ${item.product.sale_price}
                    </span>
                    <span class="text-sm text-gray-500 dark:text-gray-400 line-through ml-2">
                      ${item.product.price}
                    </span>
                  {:else}
                    <span class="text-lg font-bold text-gray-900 dark:text-white">
                      ${item.product.price}
                    </span>
                  {/if}
                </div>
                
                <button
                  onclick={() => removeFromWishlist(item.id)}
                  disabled={isUpdatingWishlist}
                  class="p-2 text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition-colors disabled:opacity-50"
                  aria-label="Remove from wishlist"
                >
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" clip-rule="evenodd" />
                    <path fill-rule="evenodd" d="M4 5a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd" />
                  </svg>
                </button>
              </div>
              
              <!-- Actions -->
              <div class="flex gap-2">
                {#if item.product.stock_quantity > 0}
                  <Button
                    variant="primary"
                    size="sm"
                    fullWidth
                    onclick={() => addToCart(item.product)}
                    class="hover-scale"
                  >
                    Add to Cart
                  </Button>
                {:else}
                  <Button
                    variant="outline"
                    size="sm"
                    fullWidth
                    disabled
                  >
                    Out of Stock
                  </Button>
                {/if}
              </div>
              
              <!-- Added Date -->
              <div class="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
                <p class="text-xs text-gray-500 dark:text-gray-400">
                  Added {new Date(item.created_at).toLocaleDateString()}
                </p>
              </div>
            </div>
          </Card>
        {/each}
      </div>
      
      <!-- Results Info -->
      {#if searchTerm || filterBy !== 'all'}
        <div class="mt-8 text-center">
          <p class="text-gray-600 dark:text-gray-400">
            Showing {filteredItems.length} of {wishlistItems.length} items
            {#if searchTerm}
              for "{searchTerm}"
            {/if}
          </p>
        </div>
      {/if}
    {/if}
  </div>
</div>

<!-- Share Modal -->
<Modal bind:show={showShareModal} title="Share Your Wishlist">
  <div class="space-y-6">
    <div>
      <p class="text-gray-600 dark:text-gray-400 mb-4">
        Share your wishlist with friends and family. They can view your favorite items and even purchase them for you!
      </p>
      
      <div class="flex gap-2">
        <Input
          type="text"
          value={shareUrl}
          readonly
          class="flex-1"
        />
        <Button onclick={copyShareUrl}>
          Copy
        </Button>
      </div>
    </div>
    
    <div class="border-t border-gray-200 dark:border-gray-700 pt-6">
      <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">
        Share on social media:
      </p>
      
      <div class="flex gap-3">
        <Button
          variant="outline"
          size="sm"
          onclick={() => window.open(`https://twitter.com/intent/tweet?text=Check out my wishlist!&url=${encodeURIComponent(shareUrl)}`, '_blank')}
        >
          Twitter
        </Button>
        <Button
          variant="outline"
          size="sm"
          onclick={() => window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`, '_blank')}
        >
          Facebook
        </Button>
        <Button
          variant="outline"
          size="sm"
          onclick={() => window.open(`mailto:?subject=Check out my wishlist&body=${encodeURIComponent(shareUrl)}`, '_blank')}
        >
          Email
        </Button>
      </div>
    </div>
  </div>
</Modal>

<style>
  .line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  
  /* Custom scrollbar for better UX */
  :global(.overflow-y-auto::-webkit-scrollbar) {
    width: 6px;
  }
  
  :global(.overflow-y-auto::-webkit-scrollbar-track) {
    background: var(--color-gray-100);
    border-radius: 3px;
  }
  
  :global(.overflow-y-auto::-webkit-scrollbar-thumb) {
    background: var(--color-gray-300);
    border-radius: 3px;
  }
  
  :global(.dark .overflow-y-auto::-webkit-scrollbar-track) {
    background: var(--color-gray-800);
  }
  
  :global(.dark .overflow-y-auto::-webkit-scrollbar-thumb) {
    background: var(--color-gray-600);
  }
</style>