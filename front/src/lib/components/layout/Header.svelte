<!--
  @component Header
  Premium e-commerce header with navigation, search, cart, and user actions.
  Features responsive design, mobile menu, and accessibility.
  
  @prop sticky - Whether header is sticky on scroll
  @prop transparent - Whether header has transparent background
  @prop showSearch - Whether to display search functionality
  @prop showCart - Whether to display cart icon
  @prop showUserMenu - Whether to display user menu
-->
<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { getAuthStore } from '$lib/stores/auth.svelte.js';
  import { getCartStore } from '$lib/stores/cart.svelte.js';
  import Badge from '../ui/Badge.svelte';
  import Drawer from '../ui/Drawer.svelte';
  
  // Props using Svelte 5 runes
  let {
    sticky = true,
    transparent = false,
    showSearch = true,
    showCart = true,
    showUserMenu = true
  } = $props();

  // Store access
  const authStore = getAuthStore();
  const cartStore = getCartStore();

  // Reactive state using Svelte 5 runes
  let mounted = $state(false);
  let isScrolled = $state(false);
  let searchQuery = $state('');
  let showSearchModal = $state(false);
  let showMobileMenu = $state(false);
  let showUserDropdown = $state(false);
  let searchInputRef = $state();

  // Derived values from stores
  const cartItemCount = $derived(cartStore?.itemsCount || 0);
  const isAuthenticated = $derived(authStore?.isAuthenticated || false);
  const user = $derived(authStore?.user || null);

  // Navigation items
  const navigationItems = $state([
    { label: 'Home', href: '/', active: false },
    { label: 'Products', href: '/products', active: false, dropdown: [
      { label: 'All Products', href: '/products' },
      { label: 'Electronics', href: '/products?category=electronics' },
      { label: 'Clothing', href: '/products?category=clothing' },
      { label: 'Books', href: '/products?category=books' }
    ]},
    { label: 'Categories', href: '/categories', active: false },
    { label: 'About', href: '/about', active: false },
    { label: 'Contact', href: '/contact', active: false }
  ]);

  // Header classes with scroll and transparency effects
  const headerClasses = $derived(() => [
    'w-full transition-all duration-300 ease-premium z-40',
    sticky ? 'sticky top-0' : 'relative',
    transparent && !isScrolled 
      ? 'bg-transparent' 
      : 'glass border-b border-white/10 dark:border-dark-200/10 shadow-elevation-1',
    isScrolled ? 'backdrop-blur-xl bg-white/80 dark:bg-dark-100/80' : ''
  ].filter(Boolean).join(' '));

  // Search functionality
  function handleSearch() {
    if (searchQuery.trim()) {
      // Navigate to search results
      goto(`/products?search=${encodeURIComponent(searchQuery.trim())}`);
      showSearchModal = false;
    }
  }

  function handleSearchKeydown(event) {
    if (event.key === 'Enter') {
      handleSearch();
    } else if (event.key === 'Escape') {
      showSearchModal = false;
      searchQuery = '';
    }
  }

  // Mobile search modal
  function openSearchModal() {
    showSearchModal = true;
    setTimeout(() => searchInputRef?.focus(), 100);
  }

  // Cart functionality
  function handleCartClick() {
    // Navigate to cart page
    goto('/cart');
  }

  // User menu actions
  function handleLogin() {
    goto('/auth/login');
  }

  function handleLogout() {
    authStore?.logout();
    showUserDropdown = false;
    goto('/');
  }

  function handleProfile() {
    goto('/account');
    showUserDropdown = false;
  }

  // Scroll detection for header effects
  function handleScroll() {
    if (typeof window !== 'undefined') {
      isScrolled = window.scrollY > 20;
    }
  }

  // Close dropdowns when clicking outside
  function handleClickOutside(event) {
    if (showUserDropdown && !event.target.closest('[data-user-menu]')) {
      showUserDropdown = false;
    }
  }

  // Lifecycle
  onMount(() => {
    mounted = true;
    
    if (typeof window !== 'undefined') {
      window.addEventListener('scroll', handleScroll, { passive: true });
      document.addEventListener('click', handleClickOutside);
      
      // Initial scroll check
      handleScroll();
    }
    
    return () => {
      if (typeof window !== 'undefined') {
        window.removeEventListener('scroll', handleScroll);
        document.removeEventListener('click', handleClickOutside);
      }
    };
  });
</script>

<header class={headerClasses}>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between h-16 lg:h-20">
      
      <!-- Mobile menu button -->
      <div class="flex lg:hidden">
        <button
          type="button"
          class="p-2 rounded-lg text-gray-600 dark:text-dark-600 hover:text-gray-900 dark:hover:text-dark-900 hover:bg-gray-100 dark:hover:bg-dark-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors duration-150"
          aria-label="Open main menu"
          onclick={() => showMobileMenu = true}
        >
          <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>

      <!-- Logo -->
      <div class="flex-shrink-0 flex items-center">
        <a href="/" class="flex items-center space-x-2 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 rounded-lg p-1">
          <div class="w-8 h-8 bg-gradient-primary rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
              <path fill-rule="evenodd" d="M10 2L3 7v11a1 1 0 001 1h3a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1h3a1 1 0 001-1V7l-7-5z" clip-rule="evenodd" />
            </svg>
          </div>
          <span class="text-xl font-bold bg-gradient-primary bg-clip-text text-transparent hidden sm:block">
            Store
          </span>
        </a>
      </div>

      <!-- Desktop Navigation -->
      <nav class="hidden lg:flex lg:space-x-8 lg:ml-10">
        {#each navigationItems as item}
          <div class="relative group">
            <a
              href={item.href}
              class="text-gray-700 dark:text-dark-700 hover:text-gray-900 dark:hover:text-dark-900 px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
              class:text-primary-600={$page.url.pathname === item.href}
              class:dark:text-primary-400={$page.url.pathname === item.href}
            >
              {item.label}
              {#if item.dropdown}
                <svg class="ml-1 w-4 h-4 inline" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                  <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              {/if}
            </a>
            
            <!-- Dropdown menu -->
            {#if item.dropdown}
              <div class="absolute left-0 mt-2 w-48 rounded-xl glass border border-white/20 dark:border-dark-200/20 shadow-premium opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 ease-premium transform translate-y-2 group-hover:translate-y-0">
                <div class="py-2">
                  {#each item.dropdown as dropdownItem}
                    <a
                      href={dropdownItem.href}
                      class="block px-4 py-2 text-sm text-gray-700 dark:text-dark-700 hover:text-gray-900 dark:hover:text-dark-900 hover:bg-gray-100/50 dark:hover:bg-dark-200/50 transition-colors duration-150"
                    >
                      {dropdownItem.label}
                    </a>
                  {/each}
                </div>
              </div>
            {/if}
          </div>
        {/each}
      </nav>

      <!-- Search Bar (Desktop) -->
      {#if showSearch}
        <div class="hidden md:flex flex-1 max-w-lg mx-8">
          <div class="relative w-full">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400 dark:text-dark-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              type="search"
              placeholder="Search products..."
              bind:value={searchQuery}
              onkeydown={handleSearchKeydown}
              class="block w-full pl-10 pr-12 py-2.5 glass rounded-xl border border-white/20 dark:border-dark-200/20 text-gray-900 dark:text-dark-900 placeholder-gray-500 dark:placeholder-dark-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
            />
            {#if searchQuery}
              <button
                type="button"
                class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600 dark:text-dark-400 dark:hover:text-dark-600 transition-colors duration-150"
                onclick={() => searchQuery = ''}
                aria-label="Clear search"
              >
                <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                  <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>
            {/if}
          </div>
        </div>
      {/if}

      <!-- Right side actions -->
      <div class="flex items-center space-x-2 sm:space-x-4">
        
        <!-- Search button (Mobile) -->
        {#if showSearch}
          <button
            type="button"
            class="md:hidden p-2 rounded-lg text-gray-600 dark:text-dark-600 hover:text-gray-900 dark:hover:text-dark-900 hover:bg-gray-100 dark:hover:bg-dark-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors duration-150"
            aria-label="Search"
            onclick={openSearchModal}
          >
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </button>
        {/if}

        <!-- Cart -->
        {#if showCart}
          <button
            type="button"
            class="relative p-2 rounded-lg text-gray-600 dark:text-dark-600 hover:text-gray-900 dark:hover:text-dark-900 hover:bg-gray-100 dark:hover:bg-dark-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors duration-150"
            aria-label="Shopping cart"
            onclick={handleCartClick}
          >
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m6-5v6a2 2 0 11-4 0v-6m4 0V9a2 2 0 10-4 0v4.01" />
            </svg>
            {#if cartItemCount > 0}
              <Badge 
                variant="error" 
                size="xs" 
                className="absolute -top-1 -right-1 min-w-[18px] h-[18px] text-xs"
              >
                {cartItemCount > 99 ? '99+' : cartItemCount}
              </Badge>
            {/if}
          </button>
        {/if}

        <!-- User menu -->
        {#if showUserMenu}
          <div class="relative" data-user-menu>
            {#if isAuthenticated && user}
              <!-- Authenticated user -->
              <button
                type="button"
                class="flex items-center space-x-2 p-2 rounded-lg text-gray-600 dark:text-dark-600 hover:text-gray-900 dark:hover:text-dark-900 hover:bg-gray-100 dark:hover:bg-dark-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors duration-150"
                aria-label="User menu"
                onclick={() => showUserDropdown = !showUserDropdown}
              >
                <div class="w-8 h-8 rounded-full bg-gradient-primary flex items-center justify-center">
                  <span class="text-white text-sm font-medium">
                    {user.name?.charAt(0) || 'U'}
                  </span>
                </div>
                <svg class="hidden sm:block w-4 h-4" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                  <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>
            {:else}
              <!-- Guest user -->
              <button
                type="button"
                class="flex items-center space-x-2 px-4 py-2 rounded-lg glass border border-white/20 dark:border-dark-200/20 text-gray-700 dark:text-dark-700 hover:text-gray-900 dark:hover:text-dark-900 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-all duration-150 hover-lift"
                onclick={handleLogin}
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                <span class="hidden sm:block text-sm font-medium">Sign In</span>
              </button>
            {/if}

            <!-- User dropdown -->
            {#if showUserDropdown && isAuthenticated}
              <div class="absolute right-0 mt-2 w-48 rounded-xl glass border border-white/20 dark:border-dark-200/20 shadow-premium z-50">
                <div class="py-2">
                  <button
                    type="button"
                    class="block w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-dark-700 hover:text-gray-900 dark:hover:text-dark-900 hover:bg-gray-100/50 dark:hover:bg-dark-200/50 transition-colors duration-150"
                    onclick={handleProfile}
                  >
                    Profile
                  </button>
                  <a
                    href="/account/orders"
                    class="block px-4 py-2 text-sm text-gray-700 dark:text-dark-700 hover:text-gray-900 dark:hover:text-dark-900 hover:bg-gray-100/50 dark:hover:bg-dark-200/50 transition-colors duration-150"
                  >
                    Orders
                  </a>
                  <a
                    href="/account/wishlist"
                    class="block px-4 py-2 text-sm text-gray-700 dark:text-dark-700 hover:text-gray-900 dark:hover:text-dark-900 hover:bg-gray-100/50 dark:hover:bg-dark-200/50 transition-colors duration-150"
                  >
                    Wishlist
                  </a>
                  <hr class="my-2 border-gray-200 dark:border-dark-200" />
                  <button
                    type="button"
                    class="block w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-dark-700 hover:text-gray-900 dark:hover:text-dark-900 hover:bg-gray-100/50 dark:hover:bg-dark-200/50 transition-colors duration-150"
                    onclick={handleLogout}
                  >
                    Sign Out
                  </button>
                </div>
              </div>
            {/if}
          </div>
        {/if}
      </div>
    </div>
  </div>
</header>

<!-- Mobile Menu Drawer -->
<Drawer 
  bind:open={showMobileMenu} 
  position="left" 
  size="sm"
  backdrop="blur"
>
  <div class="p-6">
    <div class="flex items-center justify-between mb-6">
      <span class="text-lg font-bold">Menu</span>
    </div>
    
    <nav class="space-y-2">
      {#each navigationItems as item}
        <div>
          <a
            href={item.href}
            class="block px-3 py-2 rounded-lg text-gray-700 dark:text-dark-700 hover:text-gray-900 dark:hover:text-dark-900 hover:bg-gray-100 dark:hover:bg-dark-200 font-medium transition-colors duration-150"
            class:text-primary-600={$page.url.pathname === item.href}
            class:dark:text-primary-400={$page.url.pathname === item.href}
            onclick={() => showMobileMenu = false}
          >
            {item.label}
          </a>
          
          {#if item.dropdown}
            <div class="ml-4 mt-1 space-y-1">
              {#each item.dropdown as dropdownItem}
                <a
                  href={dropdownItem.href}
                  class="block px-3 py-1 rounded text-sm text-gray-600 dark:text-dark-600 hover:text-gray-900 dark:hover:text-dark-900 hover:bg-gray-100 dark:hover:bg-dark-200 transition-colors duration-150"
                  onclick={() => showMobileMenu = false}
                >
                  {dropdownItem.label}
                </a>
              {/each}
            </div>
          {/if}
        </div>
      {/each}
    </nav>
  </div>
</Drawer>

<!-- Mobile Search Modal -->
{#if showSearchModal}
  <div class="fixed inset-0 z-50 md:hidden">
    <div class="fixed inset-0 bg-black/20 backdrop-blur-sm" onclick={() => showSearchModal = false}></div>
    <div class="fixed top-0 left-0 right-0 glass border-b border-white/20 dark:border-dark-200/20 p-4">
      <div class="flex items-center space-x-4">
        <button
          type="button"
          class="p-2 rounded-lg text-gray-600 dark:text-dark-600 hover:text-gray-900 dark:hover:text-dark-900"
          onclick={() => showSearchModal = false}
          aria-label="Close search"
        >
          <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        
        <div class="flex-1 relative">
          <input
            bind:this={searchInputRef}
            type="search"
            placeholder="Search products..."
            bind:value={searchQuery}
            onkeydown={handleSearchKeydown}
            class="block w-full px-4 py-3 glass rounded-xl border border-white/20 dark:border-dark-200/20 text-gray-900 dark:text-dark-900 placeholder-gray-500 dark:placeholder-dark-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>
        
        {#if searchQuery}
          <button
            type="button"
            class="p-2 rounded-lg text-gray-600 dark:text-dark-600 hover:text-gray-900 dark:hover:text-dark-900"
            onclick={() => searchQuery = ''}
            aria-label="Clear search"
          >
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        {/if}
      </div>
    </div>
  </div>
{/if}

<style>
  .ease-premium {
    transition-timing-function: cubic-bezier(0.16, 1, 0.3, 1);
  }

  .hover-lift:hover {
    transform: translateY(-1px);
  }

  /* Focus visible enhancements */
  :global(a:focus-visible, button:focus-visible) {
    outline: 2px solid var(--color-primary-500);
    outline-offset: 2px;
  }
</style>