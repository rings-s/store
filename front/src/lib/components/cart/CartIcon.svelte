<!--
  @component CartIcon
  Premium cart icon with item count badge and smooth animations.
  Features accessible interactions and real-time cart updates.
  
  @prop itemCount - Number of items in cart (optional)
  @prop loading - Loading state (optional)
  @prop onClick - Click handler function (optional)
  @prop size - Icon size variant (optional)
  @prop className - Additional CSS classes
-->
<script>
  let { 
    itemCount = 0, 
    loading = false,
    onClick = () => {},
    size = 'md',
    className = '' 
  } = $props();
  
  // Computed values
  const sizeClasses = $derived(() => {
    switch (size) {
      case 'sm': return 'w-5 h-5';
      case 'lg': return 'w-8 h-8';
      default: return 'w-6 h-6';
    }
  });
  
  const badgeClasses = $derived(() => {
    switch (size) {
      case 'sm': return 'w-4 h-4 text-xs';
      case 'lg': return 'w-6 h-6 text-sm';
      default: return 'w-5 h-5 text-xs';
    }
  });
  
  const hasItems = $derived(() => itemCount > 0);
  const displayCount = $derived(() => itemCount > 99 ? '99+' : itemCount.toString());
</script>

<button
  onclick={onClick}
  disabled={loading}
  class="relative p-2 rounded-xl text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white 
         hover:bg-gray-100 dark:hover:bg-gray-800 transition-all duration-200 
         focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 
         disabled:opacity-50 disabled:cursor-not-allowed group {className}"
  aria-label="Shopping cart ({itemCount} item{itemCount !== 1 ? 's' : ''})"
>
  <!-- Cart Icon -->
  <div class="relative">
    {#if loading}
      <!-- Loading Spinner -->
      <svg class="{sizeClasses} animate-spin" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    {:else}
      <!-- Shopping Cart Icon -->
      <svg 
        class="{sizeClasses} transition-transform group-hover:scale-110 group-active:scale-95" 
        fill="none" 
        stroke="currentColor" 
        viewBox="0 0 24 24"
        aria-hidden="true"
      >
        <path 
          stroke-linecap="round" 
          stroke-linejoin="round" 
          stroke-width="2" 
          d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13h10M17 13v6a2 2 0 01-2 2H9a2 2 0 01-2-2v-6.01M17 13l-5-5-5 5" 
        />
      </svg>
    {/if}
    
    <!-- Item Count Badge -->
    {#if hasItems && !loading}
      <div 
        class="absolute -top-1 -right-1 bg-primary-600 text-white rounded-full flex items-center justify-center 
               font-semibold leading-none {badgeClasses}
               animate-scale-in transform transition-all duration-200"
        style="min-width: {size === 'sm' ? '16px' : size === 'lg' ? '24px' : '20px'}"
      >
        <span class="animate-bounce-subtle">
          {displayCount}
        </span>
      </div>
    {/if}
    
    <!-- Pulse Effect for New Items -->
    {#if hasItems && !loading}
      <div 
        class="absolute inset-0 rounded-full bg-primary-500/20 animate-ping"
        style="animation-duration: 1s; animation-iteration-count: 1;"
      ></div>
    {/if}
  </div>
  
  <!-- Hover Tooltip -->
  <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-1 
              bg-gray-900 dark:bg-gray-700 text-white text-xs rounded-lg 
              opacity-0 group-hover:opacity-100 transition-opacity duration-200 
              pointer-events-none whitespace-nowrap z-10">
    <span>
      {#if itemCount === 0}
        Cart is empty
      {:else}
        {itemCount} item{itemCount !== 1 ? 's' : ''} in cart
      {/if}
    </span>
    <!-- Tooltip Arrow -->
    <div class="absolute top-full left-1/2 transform -translate-x-1/2 border-4 
                border-transparent border-t-gray-900 dark:border-t-gray-700"></div>
  </div>
</button>

<style>
  @keyframes scale-in {
    0% {
      transform: scale(0);
    }
    50% {
      transform: scale(1.1);
    }
    100% {
      transform: scale(1);
    }
  }
  
  @keyframes bounce-subtle {
    0%, 20%, 50%, 80%, 100% {
      transform: translateY(0);
    }
    40% {
      transform: translateY(-2px);
    }
    60% {
      transform: translateY(-1px);
    }
  }
  
  .animate-scale-in {
    animation: scale-in 0.3s ease-out;
  }
  
  .animate-bounce-subtle {
    animation: bounce-subtle 0.6s ease-in-out;
  }
  
  /* High contrast mode adjustments */
  @media (prefers-contrast: high) {
    button {
      border: 1px solid currentColor;
    }
  }
  
  /* Reduced motion preferences */
  @media (prefers-reduced-motion: reduce) {
    .animate-scale-in,
    .animate-bounce-subtle,
    .animate-ping,
    .transition-transform,
    .transition-all,
    .group-hover\\:scale-110,
    .group-active\\:scale-95 {
      animation: none !important;
      transition: none !important;
      transform: none !important;
    }
  }
</style>