<!--
  @component ProductDetail
  Premium product detail page with comprehensive product information.
  Features image gallery, specifications, reviews, and purchase options.
  
  @prop product - Product object with full details
  @prop loading - Loading state (optional)
  @prop relatedProducts - Array of related products (optional)
  @prop className - Additional CSS classes
-->
<script>
  import ProductImages from './ProductImages.svelte';
  import ProductReviews from './ProductReviews.svelte';
  import ProductCard from './ProductCard.svelte';
  import Badge from '../ui/Badge.svelte';
  import { formatPrice, formatDate } from '$lib/utils/format';
  import { toastStore } from '$lib/stores/toast.svelte.js';
  
  let { 
    product, 
    loading = false,
    relatedProducts = [],
    className = '' 
  } = $props();
  
  // State management with Svelte 5 runes
  let selectedVariant = $state(null);
  let quantity = $state(1);
  let activeTab = $state('description');
  let showFullDescription = $state(false);
  let isAddingToCart = $state(false);
  let isAddingToWishlist = $state(false);
  
  // Computed values
  const currentProduct = $derived(() => selectedVariant || product);
  
  const isInStock = $derived(() => 
    currentProduct()?.stock_quantity > 0 || currentProduct()?.in_stock
  );
  
  const stockLevel = $derived(() => {
    const stock = currentProduct()?.stock_quantity || 0;
    if (stock === 0) return 'out-of-stock';
    if (stock <= 5) return 'low-stock';
    if (stock <= 20) return 'medium-stock';
    return 'high-stock';
  });
  
  const stockMessage = $derived(() => {
    const stock = currentProduct()?.stock_quantity || 0;
    const level = stockLevel();
    
    switch (level) {
      case 'out-of-stock': return 'Out of stock';
      case 'low-stock': return `Only ${stock} left in stock`;
      case 'medium-stock': return `${stock} in stock`;
      default: return 'In stock';
    }
  });
  
  const currentPrice = $derived(() => 
    currentProduct()?.sale_price || currentProduct()?.price || 0
  );
  
  const originalPrice = $derived(() => {
    const product = currentProduct();
    return product?.sale_price ? product.price : null;
  });
  
  const discount = $derived(() => {
    const original = originalPrice();
    const current = currentPrice();
    return original && original > current 
      ? Math.round(((original - current) / original) * 100)
      : 0;
  });
  
  const specifications = $derived(() => 
    currentProduct()?.specifications || product?.specifications || {}
  );
  
  // Functions
  async function addToCart() {
    if (!isInStock() || isAddingToCart) return;
    
    isAddingToCart = true;
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      toastStore.add({
        type: 'success',
        message: `${quantity} × ${currentProduct().name} added to cart!`
      });
      
    } catch (error) {
      toastStore.add({
        type: 'error',
        message: 'Failed to add to cart. Please try again.'
      });
    } finally {
      isAddingToCart = false;
    }
  }
  
  async function addToWishlist() {
    if (isAddingToWishlist) return;
    
    isAddingToWishlist = true;
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500));
      
      toastStore.add({
        type: 'success',
        message: `${currentProduct().name} added to wishlist!`
      });
      
    } catch (error) {
      toastStore.add({
        type: 'error',
        message: 'Failed to add to wishlist. Please try again.'
      });
    } finally {
      isAddingToWishlist = false;
    }
  }
  
  function selectVariant(variant) {
    selectedVariant = variant;
    quantity = 1; // Reset quantity when changing variants
  }
  
  function updateQuantity(change) {
    const newQuantity = quantity + change;
    const maxQuantity = currentProduct()?.stock_quantity || 99;
    
    if (newQuantity >= 1 && newQuantity <= maxQuantity) {
      quantity = newQuantity;
    }
  }
</script>

{#if loading}
  <!-- Loading State -->
  <div class="animate-pulse space-y-8 {className}">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
      <!-- Image Skeleton -->
      <div class="aspect-square bg-gray-200 dark:bg-gray-700 rounded-3xl"></div>
      
      <!-- Details Skeleton -->
      <div class="space-y-6">
        <div class="space-y-4">
          <div class="h-8 bg-gray-200 dark:bg-gray-700 rounded w-3/4"></div>
          <div class="h-6 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
          <div class="h-10 bg-gray-200 dark:bg-gray-700 rounded w-1/3"></div>
        </div>
        
        <div class="space-y-3">
          <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded"></div>
          <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-5/6"></div>
          <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-2/3"></div>
        </div>
        
        <div class="flex gap-3">
          <div class="h-12 bg-gray-200 dark:bg-gray-700 rounded flex-1"></div>
          <div class="h-12 bg-gray-200 dark:bg-gray-700 rounded w-12"></div>
        </div>
      </div>
    </div>
  </div>
{:else if product}
  <div class="space-y-12 {className}">
    <!-- Product Overview -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
      <!-- Product Images -->
      <div class="space-y-6">
        <ProductImages 
          images={currentProduct().images || []} 
          alt={currentProduct().name}
        />
        
        <!-- Product Features -->
        {#if currentProduct().features?.length > 0}
          <div class="glass-panel rounded-2xl p-6">
            <h3 class="font-display font-semibold text-gray-900 dark:text-white mb-4">
              Key Features
            </h3>
            <ul class="space-y-2">
              {#each currentProduct().features as feature}
                <li class="flex items-start gap-3">
                  <svg class="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  <span class="text-gray-700 dark:text-gray-300">{feature}</span>
                </li>
              {/each}
            </ul>
          </div>
        {/if}
      </div>
      
      <!-- Product Information -->
      <div class="space-y-8">
        <!-- Header -->
        <div class="space-y-4">
          <!-- Category & Brand -->
          <div class="flex items-center gap-3">
            {#if product.category}
              <Badge variant="secondary" size="sm">
                {product.category}
              </Badge>
            {/if}
            {#if product.brand}
              <span class="text-sm text-gray-600 dark:text-gray-400">
                by {product.brand}
              </span>
            {/if}
          </div>
          
          <!-- Title -->
          <h1 class="text-3xl lg:text-4xl font-display font-bold text-gray-900 dark:text-white leading-tight">
            {product.name}
          </h1>
          
          <!-- Rating & Reviews -->
          {#if product.average_rating || product.review_count}
            <div class="flex items-center gap-4">
              <div class="flex items-center gap-2">
                <div class="flex">
                  {#each Array(5) as _, i}
                    <svg 
                      class="w-5 h-5 {i < Math.round(product.average_rating || 0) ? 'text-yellow-400 fill-yellow-400' : 'text-gray-300 dark:text-gray-600'}" 
                      fill="currentColor" 
                      viewBox="0 0 20 20"
                    >
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    </svg>
                  {/each}
                </div>
                <span class="text-gray-600 dark:text-gray-400">
                  {product.average_rating?.toFixed(1) || '0.0'} ({product.review_count || 0} reviews)
                </span>
              </div>
              <a href="#reviews" class="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 text-sm font-medium">
                See all reviews
              </a>
            </div>
          {/if}
          
          <!-- Pricing -->
          <div class="flex items-center gap-4">
            <div class="text-3xl font-display font-bold text-gray-900 dark:text-white">
              {formatPrice(currentPrice())}
            </div>
            {#if originalPrice()}
              <div class="text-xl text-gray-500 dark:text-gray-400 line-through">
                {formatPrice(originalPrice())}
              </div>
              <Badge variant="success" size="sm">
                Save {discount()}%
              </Badge>
            {/if}
          </div>
          
          <!-- Stock Status -->
          <div class="flex items-center gap-2">
            <div class="w-3 h-3 rounded-full {stockLevel() === 'out-of-stock' ? 'bg-red-400' : 
              stockLevel() === 'low-stock' ? 'bg-yellow-400' : 'bg-green-400'}"></div>
            <span class="text-sm font-medium {stockLevel() === 'out-of-stock' ? 'text-red-600 dark:text-red-400' : 
              stockLevel() === 'low-stock' ? 'text-yellow-600 dark:text-yellow-400' : 'text-green-600 dark:text-green-400'}">
              {stockMessage()}
            </span>
          </div>
        </div>
        
        <!-- Variants -->
        {#if product.variants?.length > 0}
          <div class="space-y-4">
            <h3 class="font-medium text-gray-900 dark:text-white">
              Available Options
            </h3>
            <div class="grid grid-cols-2 gap-3">
              <button
                onclick={() => selectVariant(null)}
                class="p-4 rounded-xl border-2 transition-all {!selectedVariant 
                  ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20' 
                  : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'}"
              >
                <div class="text-sm font-medium text-gray-900 dark:text-white">
                  Standard
                </div>
                <div class="text-lg font-bold text-gray-900 dark:text-white">
                  {formatPrice(product.sale_price || product.price)}
                </div>
              </button>
              
              {#each product.variants as variant}
                <button
                  onclick={() => selectVariant(variant)}
                  class="p-4 rounded-xl border-2 transition-all {selectedVariant?.id === variant.id 
                    ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20' 
                    : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'}"
                >
                  <div class="text-sm font-medium text-gray-900 dark:text-white">
                    {variant.name}
                  </div>
                  <div class="text-lg font-bold text-gray-900 dark:text-white">
                    {formatPrice(variant.sale_price || variant.price)}
                  </div>
                  {#if variant.stock_quantity <= 5 && variant.stock_quantity > 0}
                    <div class="text-xs text-yellow-600 dark:text-yellow-400">
                      Only {variant.stock_quantity} left
                    </div>
                  {/if}
                </button>
              {/each}
            </div>
          </div>
        {/if}
        
        <!-- Quantity & Actions -->
        <div class="space-y-6">
          <!-- Quantity Selector -->
          <div class="flex items-center gap-4">
            <span class="font-medium text-gray-900 dark:text-white">Quantity:</span>
            <div class="flex items-center bg-gray-100 dark:bg-gray-800 rounded-lg">
              <button
                onclick={() => updateQuantity(-1)}
                disabled={quantity <= 1}
                class="p-2 hover:bg-gray-200 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-l-lg transition-colors"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
                </svg>
              </button>
              <div class="px-4 py-2 min-w-12 text-center font-medium">
                {quantity}
              </div>
              <button
                onclick={() => updateQuantity(1)}
                disabled={quantity >= (currentProduct()?.stock_quantity || 99)}
                class="p-2 hover:bg-gray-200 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-r-lg transition-colors"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
              </button>
            </div>
          </div>
          
          <!-- Action Buttons -->
          <div class="flex flex-col sm:flex-row gap-4">
            <button
              onclick={addToCart}
              disabled={!isInStock() || isAddingToCart}
              class="btn-primary flex-1 group relative overflow-hidden disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span class="relative z-10 flex items-center justify-center gap-2">
                {#if isAddingToCart}
                  <svg class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Adding...
                {:else}
                  <svg class="w-5 h-5 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13h10M17 13v6a2 2 0 01-2 2H9a2 2 0 01-2-2v-6.01M17 13l-5-5-5 5" />
                  </svg>
                  {isInStock() ? 'Add to Cart' : 'Out of Stock'}
                {/if}
              </span>
            </button>
            
            <button
              onclick={addToWishlist}
              disabled={isAddingToWishlist}
              class="btn-secondary flex items-center justify-center gap-2 px-6 group"
            >
              {#if isAddingToWishlist}
                <svg class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              {:else}
                <svg class="w-5 h-5 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
                Wishlist
              {/if}
            </button>
          </div>
        </div>
        
        <!-- Trust Indicators -->
        <div class="glass-panel rounded-2xl p-6">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="flex items-center gap-3">
              <svg class="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <div class="font-medium text-gray-900 dark:text-white text-sm">
                  Secure Payment
                </div>
                <div class="text-xs text-gray-600 dark:text-gray-400">
                  SSL encrypted checkout
                </div>
              </div>
            </div>
            
            <div class="flex items-center gap-3">
              <svg class="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
              </svg>
              <div>
                <div class="font-medium text-gray-900 dark:text-white text-sm">
                  Free Returns
                </div>
                <div class="text-xs text-gray-600 dark:text-gray-400">
                  30-day return policy
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Product Details Tabs -->
    <div class="space-y-8">
      <!-- Tab Navigation -->
      <div class="border-b border-gray-200 dark:border-gray-700">
        <nav class="flex space-x-8">
          {#each ['description', 'specifications', 'shipping'] as tab}
            <button
              onclick={() => activeTab = tab}
              class="py-4 px-1 border-b-2 font-medium text-sm transition-colors {activeTab === tab 
                ? 'border-primary-500 text-primary-600 dark:text-primary-400' 
                : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600'}"
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          {/each}
        </nav>
      </div>
      
      <!-- Tab Content -->
      <div class="glass-panel rounded-3xl p-8">
        {#if activeTab === 'description'}
          <div class="prose prose-lg max-w-none dark:prose-invert">
            <h3 class="text-2xl font-display font-semibold text-gray-900 dark:text-white mb-6">
              Product Description
            </h3>
            
            {#if product.description}
              <div class="text-gray-700 dark:text-gray-300 leading-relaxed">
                {#if showFullDescription}
                  {@html product.description}
                {:else}
                  {@html product.description.substring(0, 500)}
                  {#if product.description.length > 500}
                    <span>...</span>
                    <button
                      onclick={() => showFullDescription = true}
                      class="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-medium ml-2"
                    >
                      Read more
                    </button>
                  {/if}
                {/if}
                
                {#if showFullDescription && product.description.length > 500}
                  <button
                    onclick={() => showFullDescription = false}
                    class="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-medium ml-2"
                  >
                    Show less
                  </button>
                {/if}
              </div>
            {:else}
              <p class="text-gray-500 dark:text-gray-400">
                No description available for this product.
              </p>
            {/if}
          </div>
        {:else if activeTab === 'specifications'}
          <div>
            <h3 class="text-2xl font-display font-semibold text-gray-900 dark:text-white mb-6">
              Specifications
            </h3>
            
            {#if Object.keys(specifications()).length > 0}
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                {#each Object.entries(specifications()) as [key, value]}
                  <div class="flex justify-between py-3 border-b border-gray-200 dark:border-gray-700 last:border-b-0">
                    <span class="font-medium text-gray-900 dark:text-white">
                      {key.charAt(0).toUpperCase() + key.slice(1).replace(/_/g, ' ')}
                    </span>
                    <span class="text-gray-600 dark:text-gray-400">
                      {value}
                    </span>
                  </div>
                {/each}
              </div>
            {:else}
              <p class="text-gray-500 dark:text-gray-400">
                No specifications available for this product.
              </p>
            {/if}
          </div>
        {:else if activeTab === 'shipping'}
          <div>
            <h3 class="text-2xl font-display font-semibold text-gray-900 dark:text-white mb-6">
              Shipping & Returns
            </h3>
            
            <div class="space-y-6">
              <div>
                <h4 class="font-semibold text-gray-900 dark:text-white mb-2">
                  Shipping Information
                </h4>
                <ul class="space-y-2 text-gray-600 dark:text-gray-400">
                  <li>• Free shipping on orders over $50</li>
                  <li>• Standard delivery: 3-5 business days</li>
                  <li>• Express delivery: 1-2 business days (additional cost)</li>
                  <li>• International shipping available</li>
                </ul>
              </div>
              
              <div>
                <h4 class="font-semibold text-gray-900 dark:text-white mb-2">
                  Return Policy
                </h4>
                <ul class="space-y-2 text-gray-600 dark:text-gray-400">
                  <li>• 30-day return policy</li>
                  <li>• Items must be in original condition</li>
                  <li>• Free returns for defective items</li>
                  <li>• Refund processed within 5-7 business days</li>
                </ul>
              </div>
            </div>
          </div>
        {/if}
      </div>
    </div>
    
    <!-- Reviews Section -->
    <div id="reviews">
      <ProductReviews 
        productId={product.id} 
        reviews={product.reviews || []}
        canReview={true}
      />
    </div>
    
    <!-- Related Products -->
    {#if relatedProducts.length > 0}
      <div class="space-y-8">
        <h2 class="text-3xl font-display font-bold text-gray-900 dark:text-white">
          Related Products
        </h2>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {#each relatedProducts.slice(0, 4) as relatedProduct}
            <ProductCard product={relatedProduct} />
          {/each}
        </div>
      </div>
    {/if}
  </div>
{:else}
  <!-- Error State -->
  <div class="text-center py-16 {className}">
    <div class="glass-panel rounded-3xl p-12 max-w-md mx-auto">
      <svg class="w-20 h-20 mx-auto text-gray-400 dark:text-gray-600 mb-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <h3 class="text-xl font-display font-semibold text-gray-900 dark:text-white mb-3">
        Product Not Found
      </h3>
      <p class="text-gray-600 dark:text-gray-400 mb-6">
        The product you're looking for doesn't exist or has been removed.
      </p>
      <a href="/products" class="btn-primary">
        Browse Products
      </a>
    </div>
  </div>
{/if}