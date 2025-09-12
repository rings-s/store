<script>
  import { page } from '$app/stores';
  import { ShoppingBag, Heart, Share2, Shield, Truck, RefreshCw } from 'lucide-svelte';
  import { productsAPI } from '$lib/api/products';
  import { getCartStore } from '$lib/stores/cart.svelte.js';
  import { formatCurrency } from '$lib/utils/format';
  import ProductImages from '$lib/components/product/ProductImages.svelte';
  import ProductReviews from '$lib/components/product/ProductReviews.svelte';
  import Button from '$lib/components/ui/Button.svelte';
  import Input from '$lib/components/ui/Input.svelte';
  
  const cart = getCartStore();
  
  let product = $state(null);
  let quantity = $state(1);
  let loading = $state(true);
  let activeTab = $state('description');
  
  $effect(async () => {
    loading = true;
    try {
      product = await productsAPI.getProduct($page.params.slug);
    } finally {
      loading = false;
    }
  });
  
  async function handleAddToCart() {
    await cart.addItem(product.id, quantity);
  }
</script>

{#if loading}
  <div class="container mx-auto px-4 py-8">
    <div class="animate-pulse">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
        <div class="aspect-square bg-gray-200 dark:bg-dark-200 rounded-2xl"></div>
        <div class="space-y-4">
          <div class="h-8 bg-gray-200 dark:bg-dark-200 rounded w-3/4"></div>
          <div class="h-4 bg-gray-200 dark:bg-dark-200 rounded w-1/2"></div>
          <div class="h-24 bg-gray-200 dark:bg-dark-200 rounded"></div>
        </div>
      </div>
    </div>
  </div>
{:else if product}
  <div class="container mx-auto px-4 py-8">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
      <!-- Images -->
      <div>
        <ProductImages images={product.images} />
      </div>
      
      <!-- Details -->
      <div class="space-y-6">
        <!-- Category & Title -->
        <div>
          <p class="text-sm font-medium text-primary-600 dark:text-primary-400 uppercase tracking-wider mb-2">
            {product.category.name}
          </p>
          <h1 class="text-3xl font-display font-bold text-gray-900 dark:text-white mb-4">
            {product.name}
          </h1>
          
          <!-- Price -->
          <div class="flex items-baseline gap-3">
            <span class="text-3xl font-bold text-gray-900 dark:text-white">
              {formatCurrency(product.price)}
            </span>
            {#if product.compare_price}
              <span class="text-xl text-gray-500 line-through">
                {formatCurrency(product.compare_price)}
              </span>
              <span class="px-2 py-1 bg-red-100 text-red-600 text-sm font-medium rounded-lg">
                Save {product.discount_percentage}%
              </span>
            {/if}
          </div>
        </div>
        
        <!-- Add to Cart -->
        <div class="space-y-4 pb-6 border-b border-gray-200 dark:border-dark-200">
          <div class="flex items-center gap-4">
            <div class="flex items-center gap-2">
              <button
                onclick={() => quantity = Math.max(1, quantity - 1)}
                class="w-10 h-10 rounded-xl border-2 border-gray-200 dark:border-dark-200 hover:border-primary-500 transition-colors"
              >
                -
              </button>
              <input
                type="number"
                bind:value={quantity}
                min="1"
                class="w-16 text-center bg-transparent"
              />
              <button
                onclick={() => quantity++}
                class="w-10 h-10 rounded-xl border-2 border-gray-200 dark:border-dark-200 hover:border-primary-500 transition-colors"
              >
                +
              </button>
            </div>
            
            <Button
              variant="primary"
              icon={ShoppingBag}
              onclick={handleAddToCart}
              class="flex-1"
            >
              Add to Cart
            </Button>
            
            <button class="p-3 border-2 border-gray-200 dark:border-dark-200 rounded-xl hover:border-primary-500 transition-colors">
              <Heart class="w-5 h-5" />
            </button>
          </div>
          
          <div class="flex gap-2">
            <button class="flex-1 py-3 border-2 border-gray-200 dark:border-dark-200 rounded-xl hover:border-primary-500 transition-colors flex items-center justify-center gap-2">
              <Share2 class="w-4 h-4" />
              Share
            </button>
          </div>
        </div>
        
        <!-- Features -->
        <div class="grid grid-cols-3 gap-4">
          <div class="text-center p-4 bg-gray-50 dark:bg-dark-200 rounded-xl">
            <Truck class="w-6 h-6 mx-auto mb-2 text-primary-600" />
            <p class="text-sm font-medium text-gray-900 dark:text-white">Free Shipping</p>
            <p class="text-xs text-gray-500">On orders over $50</p>
          </div>
          <div class="text-center p-4 bg-gray-50 dark:bg-dark-200 rounded-xl">
            <Shield class="w-6 h-6 mx-auto mb-2 text-primary-600" />
            <p class="text-sm font-medium text-gray-900 dark:text-white">Secure Payment</p>
            <p class="text-xs text-gray-500">SSL Encrypted</p>
          </div>
          <div class="text-center p-4 bg-gray-50 dark:bg-dark-200 rounded-xl">
            <RefreshCw class="w-6 h-6 mx-auto mb-2 text-primary-600" />
            <p class="text-sm font-medium text-gray-900 dark:text-white">Easy Returns</p>
            <p class="text-xs text-gray-500">30 day policy</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Tabs -->
    <div class="mt-12">
      <div class="border-b border-gray-200 dark:border-dark-200">
        <nav class="flex gap-8">
          <button
            onclick={() => activeTab = 'description'}
            class="pb-4 px-1 border-b-2 font-medium transition-colors {activeTab === 'description' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500'}"
          >
            Description
          </button>
          <button
            onclick={() => activeTab = 'reviews'}
            class="pb-4 px-1 border-b-2 font-medium transition-colors {activeTab === 'reviews' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500'}"
          >
            Reviews
          </button>
        </nav>
      </div>
      
      <div class="py-8">
        {#if activeTab === 'description'}
          <div class="prose prose-lg dark:prose-invert max-w-none">
            {@html product.description}
          </div>
        {:else if activeTab === 'reviews'}
          <ProductReviews productId={product.id} reviews={product.reviews || []} />
        {/if}
      </div>
    </div>
  </div>
{/if}