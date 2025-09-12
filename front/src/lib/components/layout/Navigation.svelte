<!--
  @component Navigation (Breadcrumb)
  Premium breadcrumb navigation component for site hierarchy.
  Features responsive design, accessibility, and premium animations.
  
  @prop items - Array of breadcrumb items with label and href
  @prop separator - Custom separator (default: chevron)
  @prop showHome - Whether to show home icon for first item
  @prop maxItems - Maximum items to show (with collapse)
  @prop className - Additional CSS classes
-->
<script>
  import { createEventDispatcher } from 'svelte';
  import { page } from '$app/stores';
  
  const dispatch = createEventDispatcher();

  /** @type {Array<{label: string, href: string, active?: boolean}>} */
  export let items = [];
  
  /** @type {string} */
  export let separator = 'chevron';
  
  /** @type {boolean} */
  export let showHome = true;
  
  /** @type {number} */
  export let maxItems = 0; // 0 means no limit
  
  /** @type {string} */
  export let className = '';

  // Reactive state using Svelte 5 runes
  let showCollapsed = $state(false);
  
  // Process items with current page detection
  const processedItems = $derived(() => {
    const currentPath = $page.url.pathname;
    return items.map((item, index) => ({
      ...item,
      active: item.href === currentPath || (index === items.length - 1),
      isLast: index === items.length - 1
    }));
  });

  // Handle item collapse for long breadcrumbs
  const displayItems = $derived(() => {
    if (maxItems <= 0 || processedItems.length <= maxItems) {
      return processedItems;
    }

    if (showCollapsed) {
      return processedItems;
    }

    // Show first item, ellipsis, and last few items
    const firstItem = processedItems[0];
    const lastItems = processedItems.slice(-(maxItems - 2));
    
    return [
      firstItem,
      { label: '...', href: '#', isEllipsis: true, active: false },
      ...lastItems
    ];
  });

  // Handle breadcrumb click
  function handleItemClick(item, event) {
    if (item.isEllipsis) {
      event.preventDefault();
      showCollapsed = true;
      return;
    }
    
    if (item.active) {
      event.preventDefault();
      return;
    }
    
    dispatch('navigate', { item, href: item.href });
  }

  // Generate structured data for SEO
  const structuredData = $derived(() => {
    if (processedItems.length === 0) return null;
    
    return JSON.stringify({
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": processedItems.map((item, index) => ({
        "@type": "ListItem",
        "position": index + 1,
        "name": item.label,
        "item": item.href === '#' ? undefined : `${$page.url.origin}${item.href}`
      }))
    });
  });

  // Separator icons
  const separatorIcons = {
    chevron: 'M8.22 5.22a.75.75 0 0 1 1.06 0l4.25 4.25a.75.75 0 0 1 0 1.06L9.28 14.78a.75.75 0 0 1-1.06-1.06L11.94 10 8.22 6.28a.75.75 0 0 1 0-1.06Z',
    slash: 'M13.78 4.22a.75.75 0 0 1 0 1.06l-4.25 4.25a.75.75 0 0 1-1.06 0L4.22 5.28a.75.75 0 0 1 1.06-1.06L8.5 7.44l3.22-3.22a.75.75 0 0 1 1.06 0Z',
    arrow: 'M12.97 5.47a.75.75 0 0 1 1.06 1.06L9.56 11l4.47 4.47a.75.75 0 1 1-1.06 1.06L8 11.56l-4.97 4.97a.75.75 0 0 1-1.06-1.06L6.44 11 1.97 6.53a.75.75 0 0 1 1.06-1.06L8 10.44l4.97-4.97Z'
  };

  const separatorPath = separatorIcons[separator] || separatorIcons.chevron;
</script>

<!-- Structured Data -->
{#if structuredData}
  {@html `<script type="application/ld+json">${structuredData}</script>`}
{/if}

{#if processedItems.length > 0}
  <nav 
    class="flex items-center space-x-1 text-sm {className}"
    aria-label="Breadcrumb"
  >
    <ol class="flex items-center space-x-1" role="list">
      {#each displayItems as item, index}
        <li class="flex items-center">
          <!-- Separator (not for first item) -->
          {#if index > 0}
            <svg 
              class="w-4 h-4 mx-2 text-gray-400 dark:text-dark-400 flex-shrink-0" 
              fill="currentColor" 
              viewBox="0 0 16 16"
              aria-hidden="true"
            >
              <path d={separatorPath} />
            </svg>
          {/if}

          <!-- Breadcrumb Item -->
          {#if item.isEllipsis}
            <!-- Ellipsis (expandable) -->
            <button
              type="button"
              class="px-2 py-1 rounded-md text-gray-500 dark:text-dark-500 hover:text-gray-700 dark:hover:text-dark-700 hover:bg-gray-100 dark:hover:bg-dark-200 transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-1"
              on:click={(e) => handleItemClick(item, e)}
              aria-label="Show all breadcrumb items"
            >
              {item.label}
            </button>
          {:else if item.active || item.isLast}
            <!-- Current/Last Item (not clickable) -->
            <span 
              class="font-medium text-gray-900 dark:text-dark-900 px-2 py-1"
              aria-current="page"
            >
              {#if showHome && index === 0}
                <span class="sr-only">Home: </span>
                <svg class="w-4 h-4 inline mr-1" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                  <path fill-rule="evenodd" d="M9.293 2.293a1 1 0 0 1 1.414 0l7 7A1 1 0 0 1 17 11h-1v6a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1v-3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v3a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-6H3a1 1 0 0 1-.707-1.707l7-7Z" clip-rule="evenodd" />
                </svg>
              {/if}
              {item.label}
            </span>
          {:else}
            <!-- Clickable Item -->
            <a
              href={item.href}
              class="px-2 py-1 rounded-md text-gray-600 dark:text-dark-600 hover:text-gray-900 dark:hover:text-dark-900 hover:bg-gray-100 dark:hover:bg-dark-200 transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-1"
              on:click={(e) => handleItemClick(item, e)}
            >
              {#if showHome && index === 0}
                <span class="sr-only">Home: </span>
                <svg class="w-4 h-4 inline mr-1" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                  <path fill-rule="evenodd" d="M9.293 2.293a1 1 0 0 1 1.414 0l7 7A1 1 0 0 1 17 11h-1v6a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1v-3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v3a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-6H3a1 1 0 0 1-.707-1.707l7-7Z" clip-rule="evenodd" />
                </svg>
              {/if}
              {item.label}
            </a>
          {/if}
        </li>
      {/each}
    </ol>
  </nav>
{/if}

<style>
  /* Focus visible enhancements */
  :global(a:focus-visible, button:focus-visible) {
    outline: 2px solid var(--color-primary-500);
    outline-offset: 1px;
  }

  /* High contrast mode adjustments */
  @media (prefers-contrast: high) {
    :global(.breadcrumb-item) {
      border: 1px solid currentColor;
    }
  }

  /* Reduced motion preferences */
  @media (prefers-reduced-motion: reduce) {
    * {
      transition-duration: 0.01ms !important;
    }
  }
</style>