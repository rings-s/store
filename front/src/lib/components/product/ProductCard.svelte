<!--
  @component ProductCard
  Premium e-commerce product card with interactive features.
  Includes image hover effects, ratings, wishlist, and cart functionality.
  
  @prop product - Product data object
  @prop variant - Card style: 'default' | 'compact' | 'featured'
  @prop showQuickView - Whether to show quick view button
  @prop showWishlist - Whether to show wishlist functionality
  @prop showCompare - Whether to show compare functionality
  @prop loading - Whether the card is in loading state
-->
<script>
  import Badge from '../ui/Badge.svelte';
  
  // Props using Svelte 5 runes
  let {
    product = {
      id: '',
      name: '',
      description: '',
      price: 0,
      originalPrice: 0,
      images: [],
      rating: 0,
      reviewCount: 0,
      inStock: true,
      stockCount: 0,
      category: '',
      tags: [],
      variants: [],
      isNew: false,
      isBestseller: false,
      isOnSale: false
    },
    variant = 'default',
    showQuickView = true,
    showWishlist = true,
    showCompare = false,
    loading = false,
    onquickview,
    onaddtocart,
    onaddtowishlist,
    oncompare
  } = $props();

  // Reactive state using Svelte 5 runes
  let imageLoaded = $state(false);
  let imageError = $state(false);
  let currentImageIndex = $state(0);
  let isHovered = $state(false);
  let isWishlisted = $state(false);
  let isCompared = $state(false);
  let isAddingToCart = $state(false);

  // Computed values
  const primaryImage = $derived(() => product.images?.[currentImageIndex] || product.images?.[0] || '/placeholder-product.jpg');
  const hasDiscount = $derived(() => product.originalPrice && product.originalPrice > product.price);
  const discountPercentage = $derived(() => {
    if (!hasDiscount) return 0;
    return Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100);
  });

  // Card variant classes
  const cardClasses = $derived(() => {
    const base = 'group relative overflow-hidden transition-all duration-300 ease-premium cursor-pointer gpu-accelerated';
    
    const variants = {
      default: 'rounded-xl hover-lift',
      compact: 'rounded-lg',
      featured: 'rounded-2xl hover-lift-more'
    };
    
    return `${base} ${variants[variant]}`;
  });

  // Image aspect ratio classes
  const imageAspectClasses = $derived(() => ({
    default: 'aspect-[4/5]',
    compact: 'aspect-square',
    featured: 'aspect-[4/5]'
  })[variant]);

  // Handle image interactions
  function handleImageLoad() {
    imageLoaded = true;
    imageError = false;
  }

  function handleImageError() {
    imageError = true;
    imageLoaded = true;
  }

  function handleImageHover(index) {
    if (product.images?.length > 1) {
      currentImageIndex = index;
    }
  }

  // Handle product interactions
  function handleProductClick() {
    // No dispatch needed - handled by parent component navigation
  }

  function handleQuickView(event) {
    event.stopPropagation();
    onquickview?.(product);
  }

  function handleWishlistToggle(event) {
    event.stopPropagation();
    isWishlisted = !isWishlisted;
    onaddtowishlist?.(product);
  }

  function handleCompareToggle(event) {
    event.stopPropagation();
    isCompared = !isCompared;
    oncompare?.(product);
  }

  async function handleAddToCart(event) {
    event.stopPropagation();
    
    if (isAddingToCart || !product.inStock) return;
    
    isAddingToCart = true;
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500));
      onaddtocart?.(product, 1);
    } catch (error) {
      console.error('Failed to add to cart:', error);
    } finally {
      isAddingToCart = false;
    }
  }

  // Format currency
  function formatCurrency(price) {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price);
  }

  // Generate star rating
  function generateStars(rating) {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    
    for (let i = 0; i < fullStars; i++) {
      stars.push('full');
    }
    
    if (hasHalfStar) {
      stars.push('half');
    }
    
    while (stars.length < 5) {
      stars.push('empty');
    }
    
    return stars;
  }

  const stars = $derived(() => generateStars(product.rating));
</script>

<article 
  class={cardClasses}
  on:click={handleProductClick}
  on:mouseenter={() => isHovered = true}
  on:mouseleave={() => isHovered = false}
  role="button"
  tabindex="0"
  aria-label="View product: {product.name}"
  on:keydown={(e) => e.key === 'Enter' && handleProductClick()}
>
  {#if loading}
    <!-- Loading State -->
    <div class="glass border border-white/20 dark:border-dark-200/20 p-4 animate-pulse">
      <div class="bg-gray-200 dark:bg-dark-300 rounded-lg {imageAspectClasses} mb-4"></div>
      <div class="space-y-2">
        <div class="bg-gray-200 dark:bg-dark-300 rounded h-4 w-3/4"></div>
        <div class="bg-gray-200 dark:bg-dark-300 rounded h-4 w-1/2"></div>
        <div class="bg-gray-200 dark:bg-dark-300 rounded h-6 w-1/3"></div>
      </div>
    </div>
  {:else}
    <!-- Product Card -->
    <div class="glass border border-white/20 dark:border-dark-200/20 group-hover:border-primary-300 dark:group-hover:border-primary-600 transition-colors duration-300">
      
      <!-- Image Section -->
      <div class="relative {imageAspectClasses} overflow-hidden">
        <!-- Product Image -->
        <img
          src={primaryImage}
          alt={product.name}
          class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          class:opacity-0={!imageLoaded}
          class:opacity-100={imageLoaded}
          on:load={handleImageLoad}
          on:error={handleImageError}
        />
        
        <!-- Image Overlay on Hover -->
        <div 
          class="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
          class:opacity-100={isHovered}
        ></div>
        
        <!-- Badges -->
        <div class="absolute top-3 left-3 flex flex-col gap-2">
          {#if product.isNew}
            <Badge variant="info" size="sm">New</Badge>
          {/if}
          {#if product.isBestseller}
            <Badge variant="warning" size="sm">Bestseller</Badge>
          {/if}
          {#if hasDiscount}
            <Badge variant="error" size="sm">-{discountPercentage}%</Badge>
          {/if}
        </div>
        
        <!-- Action Buttons (Top Right) -->
        <div class="absolute top-3 right-3 flex flex-col gap-2">
          {#if showWishlist}
            <button
              type="button"
              class="w-9 h-9 rounded-full glass border border-white/20 dark:border-dark-200/20 flex items-center justify-center text-gray-600 dark:text-dark-600 hover:text-error-600 dark:hover:text-error-400 hover:bg-white/80 dark:hover:bg-dark-100/80 transition-all duration-200 opacity-0 group-hover:opacity-100 transform translate-y-2 group-hover:translate-y-0"
              class:text-error-600={isWishlisted}
              class:dark:text-error-400={isWishlisted}
              on:click={handleWishlistToggle}
              aria-label={isWishlisted ? 'Remove from wishlist' : 'Add to wishlist'}
            >
              <svg class="w-5 h-5" fill={isWishlisted ? 'currentColor' : 'none'} viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </button>
          {/if}
          
          {#if showCompare}
            <button
              type="button"
              class="w-9 h-9 rounded-full glass border border-white/20 dark:border-dark-200/20 flex items-center justify-center text-gray-600 dark:text-dark-600 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-white/80 dark:hover:bg-dark-100/80 transition-all duration-200 opacity-0 group-hover:opacity-100 transform translate-y-2 group-hover:translate-y-0"
              class:text-primary-600={isCompared}
              class:dark:text-primary-400={isCompared}
              on:click={handleCompareToggle}
              aria-label={isCompared ? 'Remove from comparison' : 'Add to comparison'}
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </button>
          {/if}
        </div>
        
        <!-- Quick View Button (Bottom Center) -->
        {#if showQuickView}
          <div class="absolute bottom-4 left-1/2 transform -translate-x-1/2">
            <button
              type="button"
              class="px-4 py-2 bg-white/90 dark:bg-dark-100/90 text-gray-900 dark:text-dark-900 rounded-lg font-medium hover:bg-white dark:hover:bg-dark-100 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-all duration-200 opacity-0 group-hover:opacity-100 transform translate-y-2 group-hover:translate-y-0 backdrop-blur-sm"
              on:click={handleQuickView}
            >
              Quick View
            </button>
          </div>
        {/if}
        
        <!-- Stock Status -->
        {#if !product.inStock}
          <div class="absolute inset-0 bg-white/80 dark:bg-dark-100/80 flex items-center justify-center">
            <span class="px-4 py-2 bg-gray-900/90 text-white rounded-lg font-medium">
              Out of Stock
            </span>
          </div>
        {/if}
        
        <!-- Image Thumbnails (for hover navigation) -->
        {#if product.images?.length > 1}
          <div class="absolute bottom-2 left-2 flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            {#each product.images.slice(0, 4) as image, index}
              <button
                type="button"
                class="w-2 h-2 rounded-full transition-colors duration-200"
                class:bg-white={index === currentImageIndex}
                class:bg-white/50={index !== currentImageIndex}
                on:mouseenter={() => handleImageHover(index)}
                aria-label="View image {index + 1}"
              ></button>
            {/each}
          </div>
        {/if}
      </div>
      
      <!-- Content Section -->
      <div class="p-4 space-y-3">
        <!-- Product Info -->
        <div class="space-y-2">
          <!-- Category -->
          {#if product.category}
            <p class="text-xs text-gray-500 dark:text-dark-500 uppercase tracking-wide">
              {product.category}
            </p>
          {/if}
          
          <!-- Title -->
          <h3 class="font-semibold text-gray-900 dark:text-dark-900 line-clamp-2 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors duration-200">
            {product.name}
          </h3>
          
          <!-- Description (only for featured variant) -->
          {#if variant === 'featured' && product.description}
            <p class="text-sm text-gray-600 dark:text-dark-600 line-clamp-2">
              {product.description}
            </p>
          {/if}
        </div>
        
        <!-- Rating -->
        {#if product.rating > 0}
          <div class="flex items-center gap-2">
            <div class="flex items-center">
              {#each stars as star}
                <svg class="w-4 h-4" viewBox="0 0 20 20" aria-hidden="true">
                  {#if star === 'full'}
                    <path class="fill-yellow-400" d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  {:else if star === 'half'}
                    <defs>
                      <linearGradient id="half-fill">
                        <stop offset="50%" stop-color="#facc15" />
                        <stop offset="50%" stop-color="#e5e7eb" />
                      </linearGradient>
                    </defs>
                    <path fill="url(#half-fill)" d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  {:else}
                    <path class="fill-gray-300 dark:fill-dark-300" d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  {/if}
                </svg>
              {/each}
            </div>
            {#if product.reviewCount > 0}
              <span class="text-sm text-gray-500 dark:text-dark-500">
                ({product.reviewCount})
              </span>
            {/if}
          </div>
        {/if}
        
        <!-- Price and Add to Cart -->
        <div class="flex items-center justify-between pt-2">
          <!-- Price -->
          <div class="flex items-center gap-2">
            <span class="text-lg font-bold text-gray-900 dark:text-dark-900">
              {formatCurrency(product.price)}
            </span>
            {#if hasDiscount}
              <span class="text-sm text-gray-500 dark:text-dark-500 line-through">
                {formatCurrency(product.originalPrice)}
              </span>
            {/if}
          </div>
          
          <!-- Add to Cart -->
          {#if product.inStock}
            <button
              type="button"
              class="p-2 rounded-lg bg-primary-600 hover:bg-primary-700 text-white focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed hover-lift-sm"
              disabled={isAddingToCart}
              on:click={handleAddToCart}
              aria-label="Add {product.name} to cart"
            >
              {#if isAddingToCart}
                <svg class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24" aria-hidden="true">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              {:else}
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m6-5v6a2 2 0 11-4 0v-6m4 0V9a2 2 0 10-4 0v4.01" />
                </svg>
              {/if}
            </button>
          {/if}
        </div>
        
        <!-- Stock Count (low stock warning) -->
        {#if product.inStock && product.stockCount > 0 && product.stockCount <= 5}
          <p class="text-xs text-warning-600 dark:text-warning-400">
            Only {product.stockCount} left in stock
          </p>
        {/if}
      </div>
    </div>
  {/if}
</article>

<style>
  .ease-premium {
    transition-timing-function: cubic-bezier(0.16, 1, 0.3, 1);
  }

  .gpu-accelerated {
    transform: translateZ(0);
    backface-visibility: hidden;
    perspective: 1000;
  }

  .hover-lift:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  }

  .hover-lift-more:hover {
    transform: translateY(-8px);
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  }

  .hover-lift-sm:hover {
    transform: translateY(-1px);
  }

  .line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  /* Focus visible enhancements */
  :global(article:focus-visible) {
    outline: 2px solid var(--color-primary-500);
    outline-offset: 2px;
  }

  /* High contrast mode adjustments */
  @media (prefers-contrast: high) {
    .glass {
      border-width: 2px !important;
      backdrop-filter: none !important;
      background: var(--color-white) !important;
    }
    
    :global(.dark) .glass {
      background: var(--color-dark-100) !important;
    }
  }

  /* Reduced motion preferences */
  @media (prefers-reduced-motion: reduce) {
    * {
      transition-duration: 0.01ms !important;
      animation-duration: 0.01ms !important;
    }
    
    .hover-lift:hover,
    .hover-lift-more:hover,
    .hover-lift-sm:hover {
      transform: none !important;
    }
  }
</style>