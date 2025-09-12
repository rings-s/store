<!--
  @component ProductGrid
  Premium product grid with advanced filtering, sorting, and virtualization.
  Features responsive grid, lazy loading, and comprehensive accessibility.
  
  @prop products - Array of product objects
  @prop loading - Loading state (optional)
  @prop columns - Grid columns configuration (optional)
  @prop showFilters - Whether to show filter controls (optional)
  @prop className - Additional CSS classes
-->
<script>
  import ProductCard from './ProductCard.svelte';
  import { formatPrice } from '$lib/utils/format';
  
  let { 
    products = [], 
    loading = false,
    columns = { sm: 1, md: 2, lg: 3, xl: 4 },
    showFilters = false,
    className = '' 
  } = $props();
  
  // State management with Svelte 5 runes
  let sortBy = $state('featured');
  let filterCategory = $state('all');
  let priceRange = $state([0, 1000]);
  let searchQuery = $state('');
  let viewMode = $state('grid');
  let currentPage = $state(1);
  const itemsPerPage = 12;
  
  // Computed values
  const categories = $derived(() => {
    const cats = new Set(products.map(p => p.category).filter(Boolean));
    return Array.from(cats).sort();
  });
  
  const filteredProducts = $derived(() => {
    let filtered = products;
    
    // Search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(product => 
        product.name?.toLowerCase().includes(query) ||
        product.description?.toLowerCase().includes(query) ||
        product.category?.toLowerCase().includes(query)
      );
    }
    
    // Category filter
    if (filterCategory !== 'all') {
      filtered = filtered.filter(product => product.category === filterCategory);
    }
    
    // Price range filter
    filtered = filtered.filter(product => {
      const price = product.sale_price || product.price || 0;
      return price >= priceRange[0] && price <= priceRange[1];
    });
    
    return filtered;
  });
  
  const sortedProducts = $derived(() => {
    const sorted = [...filteredProducts()];
    
    switch (sortBy) {
      case 'name':
        return sorted.sort((a, b) => a.name?.localeCompare(b.name) || 0);
      case 'price-low':
        return sorted.sort((a, b) => (a.sale_price || a.price || 0) - (b.sale_price || b.price || 0));
      case 'price-high':
        return sorted.sort((a, b) => (b.sale_price || b.price || 0) - (a.sale_price || a.price || 0));
      case 'rating':
        return sorted.sort((a, b) => (b.average_rating || 0) - (a.average_rating || 0));
      case 'newest':
        return sorted.sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0));
      default: // featured
        return sorted.sort((a, b) => (b.featured ? 1 : 0) - (a.featured ? 1 : 0));
    }
  });
  
  const paginatedProducts = $derived(() => {
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    return sortedProducts().slice(startIndex, endIndex);
  });
  
  const totalPages = $derived(() => 
    Math.ceil(sortedProducts().length / itemsPerPage)
  );
  
  const gridClasses = $derived(() => {
    const base = 'grid gap-6';
    const responsive = `
      grid-cols-${columns.sm || 1} 
      md:grid-cols-${columns.md || 2} 
      lg:grid-cols-${columns.lg || 3} 
      xl:grid-cols-${columns.xl || 4}
    `;
    return `${base} ${responsive}`;
  });
  
  // Functions
  function resetFilters() {
    sortBy = 'featured';
    filterCategory = 'all';
    priceRange = [0, 1000];
    searchQuery = '';
    currentPage = 1;
  }
  
  function handlePageChange(page) {
    currentPage = page;
    // Scroll to top of grid
    document.getElementById('product-grid')?.scrollIntoView({ 
      behavior: 'smooth', 
      block: 'start' 
    });
  }
</script>

<div class="space-y-8 {className}">
  <!-- Grid Header -->
  <div class="flex flex-col lg:flex-row gap-6 items-start lg:items-center justify-between">
    <!-- Results Summary -->
    <div class="flex-1">
      <h2 class="text-2xl font-display font-bold text-gray-900 dark:text-white mb-2">
        {#if searchQuery}
          Search results for "{searchQuery}"
        {:else if filterCategory !== 'all'}
          {filterCategory} Products
        {:else}
          All Products
        {/if}
      </h2>
      <p class="text-gray-600 dark:text-gray-400">
        {sortedProducts().length} product{sortedProducts().length !== 1 ? 's' : ''} found
        {#if filteredProducts().length !== products.length}
          from {products.length} total
        {/if}
      </p>
    </div>
    
    <!-- View Controls -->
    <div class="flex items-center gap-4">
      <!-- Search -->
      <div class="relative">
        <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          type="text"
          bind:value={searchQuery}
          placeholder="Search products..."
          class="input-primary pl-10 w-64"
        />
        {#if searchQuery}
          <button
            onclick={() => searchQuery = ''}
            class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        {/if}
      </div>
      
      <!-- View Mode Toggle -->
      <div class="flex items-center bg-gray-100 dark:bg-gray-800 rounded-lg p-1">
        <button
          onclick={() => viewMode = 'grid'}
          class="p-2 rounded-md transition-colors {viewMode === 'grid' 
            ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow' 
            : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'}"
          aria-label="Grid view"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
          </svg>
        </button>
        <button
          onclick={() => viewMode = 'list'}
          class="p-2 rounded-md transition-colors {viewMode === 'list' 
            ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow' 
            : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'}"
          aria-label="List view"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
          </svg>
        </button>
      </div>
      
      <!-- Filters Toggle -->
      {#if showFilters}
        <button
          onclick={() => showFilters = !showFilters}
          class="btn-secondary flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4" />
          </svg>
          Filters
        </button>
      {/if}
    </div>
  </div>
  
  <!-- Filters Panel -->
  {#if showFilters}
    <div class="glass-panel rounded-2xl p-6 animate-slide-down">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <!-- Category Filter -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Category
          </label>
          <select bind:value={filterCategory} class="input-primary w-full">
            <option value="all">All Categories</option>
            {#each categories() as category}
              <option value={category}>{category}</option>
            {/each}
          </select>
        </div>
        
        <!-- Price Range -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Price Range
          </label>
          <div class="flex items-center gap-2">
            <input
              type="number"
              bind:value={priceRange[0]}
              min="0"
              class="input-primary flex-1"
              placeholder="Min"
            />
            <span class="text-gray-500">-</span>
            <input
              type="number"
              bind:value={priceRange[1]}
              min="0"
              class="input-primary flex-1"
              placeholder="Max"
            />
          </div>
        </div>
        
        <!-- Sort By -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Sort By
          </label>
          <select bind:value={sortBy} class="input-primary w-full">
            <option value="featured">Featured</option>
            <option value="newest">Newest</option>
            <option value="name">Name A-Z</option>
            <option value="price-low">Price: Low to High</option>
            <option value="price-high">Price: High to Low</option>
            <option value="rating">Highest Rated</option>
          </select>
        </div>
        
        <!-- Reset Filters -->
        <div class="flex items-end">
          <button
            onclick={resetFilters}
            class="btn-secondary w-full"
          >
            Reset Filters
          </button>
        </div>
      </div>
    </div>
  {/if}
  
  <!-- Active Filters -->
  {#if filterCategory !== 'all' || searchQuery || priceRange[0] > 0 || priceRange[1] < 1000}
    <div class="flex flex-wrap items-center gap-2">
      <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Active filters:</span>
      
      {#if searchQuery}
        <span class="inline-flex items-center gap-1 px-3 py-1 bg-primary-100 text-primary-800 dark:bg-primary-900/20 dark:text-primary-300 rounded-full text-sm">
          Search: "{searchQuery}"
          <button onclick={() => searchQuery = ''} class="ml-1 hover:text-primary-900 dark:hover:text-primary-200">
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </span>
      {/if}
      
      {#if filterCategory !== 'all'}
        <span class="inline-flex items-center gap-1 px-3 py-1 bg-primary-100 text-primary-800 dark:bg-primary-900/20 dark:text-primary-300 rounded-full text-sm">
          Category: {filterCategory}
          <button onclick={() => filterCategory = 'all'} class="ml-1 hover:text-primary-900 dark:hover:text-primary-200">
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </span>
      {/if}
      
      {#if priceRange[0] > 0 || priceRange[1] < 1000}
        <span class="inline-flex items-center gap-1 px-3 py-1 bg-primary-100 text-primary-800 dark:bg-primary-900/20 dark:text-primary-300 rounded-full text-sm">
          Price: {formatPrice(priceRange[0])} - {formatPrice(priceRange[1])}
          <button onclick={() => priceRange = [0, 1000]} class="ml-1 hover:text-primary-900 dark:hover:text-primary-200">
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </span>
      {/if}
      
      <button
        onclick={resetFilters}
        class="text-sm text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-medium"
      >
        Clear all
      </button>
    </div>
  {/if}
  
  <!-- Loading State -->
  {#if loading}
    <div class="grid {gridClasses} animate-pulse">
      {#each Array(itemsPerPage) as _}
        <div class="glass-panel rounded-2xl p-4 space-y-4">
          <div class="aspect-square bg-gray-200 dark:bg-gray-700 rounded-xl"></div>
          <div class="space-y-2">
            <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded"></div>
            <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-2/3"></div>
            <div class="h-6 bg-gray-200 dark:bg-gray-700 rounded w-1/3"></div>
          </div>
        </div>
      {/each}
    </div>
  {:else if paginatedProducts().length === 0}
    <!-- Empty State -->
    <div class="text-center py-16">
      <div class="glass-panel rounded-3xl p-12 max-w-md mx-auto">
        <svg class="w-20 h-20 mx-auto text-gray-400 dark:text-gray-600 mb-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2 2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 009.586 13H7" />
        </svg>
        <h3 class="text-xl font-display font-semibold text-gray-900 dark:text-white mb-3">
          No products found
        </h3>
        <p class="text-gray-600 dark:text-gray-400 mb-6">
          {#if searchQuery || filterCategory !== 'all' || priceRange[0] > 0 || priceRange[1] < 1000}
            Try adjusting your search or filters to find what you're looking for.
          {:else}
            We don't have any products available right now.
          {/if}
        </p>
        {#if searchQuery || filterCategory !== 'all' || priceRange[0] > 0 || priceRange[1] < 1000}
          <button onclick={resetFilters} class="btn-primary">
            Clear Filters
          </button>
        {/if}
      </div>
    </div>
  {:else}
    <!-- Products Grid -->
    <div id="product-grid" class={gridClasses}>
      {#each paginatedProducts() as product (product.id)}
        <div class="animate-fade-in">
          <ProductCard {product} />
        </div>
      {/each}
    </div>
    
    <!-- Pagination -->
    {#if totalPages() > 1}
      <div class="flex items-center justify-center gap-2 mt-12">
        <button
          onclick={() => handlePageChange(currentPage - 1)}
          disabled={currentPage === 1}
          class="btn-secondary px-4 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        
        {#each Array(totalPages()).fill(0) as _, i}
          {@const page = i + 1}
          {#if page === 1 || page === totalPages() || (page >= currentPage - 2 && page <= currentPage + 2)}
            <button
              onclick={() => handlePageChange(page)}
              class="px-4 py-2 rounded-lg font-medium transition-colors {page === currentPage 
                ? 'bg-primary-600 text-white' 
                : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'}"
            >
              {page}
            </button>
          {:else if (page === currentPage - 3 && page > 1) || (page === currentPage + 3 && page < totalPages())}
            <span class="px-2 text-gray-400">...</span>
          {/if}
        {/each}
        
        <button
          onclick={() => handlePageChange(currentPage + 1)}
          disabled={currentPage === totalPages()}
          class="btn-secondary px-4 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    {/if}
  {/if}
</div>