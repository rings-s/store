<script>
    import { Filter, Grid, List } from 'lucide-svelte';
    import { productsAPI } from '$lib/api/products';
    import ProductGrid from '$lib/components/product/ProductGrid.svelte';
    import Button from '$lib/components/ui/Button.svelte';
    import Select from '$lib/components/ui/Select.svelte';
    
    let products = $state([]);
    let categories = $state([]);
    let loading = $state(true);
    let viewMode = $state('grid');
    let selectedCategory = $state('');
    let sortBy = $state('-created_at');
    let showFilters = $state(false);
    
    const sortOptions = [
      { value: '-created_at', label: 'Newest First' },
      { value: 'price', label: 'Price: Low to High' },
      { value: '-price', label: 'Price: High to Low' },
      { value: 'name', label: 'Name: A-Z' }
    ];
    
    async function loadProducts() {
      loading = true;
      try {
        const params = {
          ordering: sortBy,
          ...(selectedCategory && { category: selectedCategory })
        };
        products = await productsAPI.getProducts(params);
      } finally {
        loading = false;
      }
    }
    
    $effect(() => {
      loadProducts();
    });
    
    $effect(async () => {
      categories = await productsAPI.getCategories();
    });
  </script>
  
  <div class="container mx-auto px-4 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-4xl font-display font-bold text-gray-900 dark:text-white mb-4">
        All Products
      </h1>
      <p class="text-gray-600 dark:text-gray-400">
        Explore our complete collection
      </p>
    </div>
    
    <!-- Toolbar -->
    <div class="flex flex-wrap items-center justify-between gap-4 mb-8">
      <div class="flex items-center gap-2">
        <Button
          variant={showFilters ? 'primary' : 'secondary'}
          icon={Filter}
          onclick={() => showFilters = !showFilters}
        >
          Filters
        </Button>
        
        <div class="flex bg-gray-100 dark:bg-dark-200 rounded-xl p-1">
          <button
            onclick={() => viewMode = 'grid'}
            class="p-2 rounded-lg {viewMode === 'grid' ? 'bg-white dark:bg-dark-100 shadow' : ''}"
          >
            <Grid class="w-5 h-5" />
          </button>
          <button
            onclick={() => viewMode = 'list'}
            class="p-2 rounded-lg {viewMode === 'list' ? 'bg-white dark:bg-dark-100 shadow' : ''}"
          >
            <List class="w-5 h-5" />
          </button>
        </div>
      </div>
      
      <div class="flex items-center gap-4">
        <Select
          bind:value={sortBy}
          options={sortOptions}
          class="w-48"
        />
      </div>
    </div>
    
    <!-- Filters Sidebar -->
    {#if showFilters}
      <aside class="mb-8 p-6 bg-white dark:bg-dark-100 rounded-2xl animate-slide-down">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Category
            </label>
            <Select
              bind:value={selectedCategory}
              options={[
                { value: '', label: 'All Categories' },
                ...categories.map(c => ({ value: c.id, label: c.name }))
              ]}
            />
          </div>
        </div>
      </aside>
    {/if}
    
    <!-- Products -->
    <ProductGrid {products} {loading} columns={viewMode === 'grid' ? 4 : 2} />
  </div>