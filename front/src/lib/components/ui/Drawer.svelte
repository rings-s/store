<!--
  @component Drawer
  A flexible drawer/panel component with premium animations and accessibility.
  Supports multiple positions, overlay modes, and responsive behavior.
  
  @prop open - Whether the drawer is open
  @prop position - Position: 'left' | 'right' | 'top' | 'bottom'
  @prop size - Size variant: 'sm' | 'md' | 'lg' | 'xl' | 'full'
  @prop overlay - Whether to show backdrop overlay
  @prop persistent - Whether drawer stays open until explicitly closed
  @prop backdrop - Backdrop behavior: 'blur' | 'dark' | 'none'
  @prop class - Additional CSS classes
-->
<script>
  import { createEventDispatcher, onMount, onDestroy } from 'svelte';

  const dispatch = createEventDispatcher();

  // Use Svelte 5 $props() runes syntax
  let {
    /** @type {boolean} */
    open = false,
    /** @type {'left' | 'right' | 'top' | 'bottom'} */
    position = 'right',
    /** @type {'sm' | 'md' | 'lg' | 'xl' | 'full'} */
    size = 'md',
    /** @type {boolean} */
    overlay = true,
    /** @type {boolean} */
    persistent = false,
    /** @type {'blur' | 'dark' | 'none'} */
    backdrop = 'blur',
    /** @type {string} */
    class: extraClass = ''
  } = $props();

  // Reactive state using Svelte 5 runes pattern
  let mounted = $state(false);
  let isVisible = $state(false);
  let isAnimating = $state(false);
  let drawerElement = $state();

  // Position-based classes
  const positionClasses = $derived(() => ({
    left: {
      container: 'inset-y-0 left-0 flex',
      panel: 'translate-x-0',
      hidden: '-translate-x-full',
      enter: 'translate-x-0',
      leave: '-translate-x-full'
    },
    right: {
      container: 'inset-y-0 right-0 flex',
      panel: 'translate-x-0',
      hidden: 'translate-x-full',
      enter: 'translate-x-0',
      leave: 'translate-x-full'
    },
    top: {
      container: 'inset-x-0 top-0 flex flex-col',
      panel: 'translate-y-0',
      hidden: '-translate-y-full',
      enter: 'translate-y-0',
      leave: '-translate-y-full'
    },
    bottom: {
      container: 'inset-x-0 bottom-0 flex flex-col',
      panel: 'translate-y-0',
      hidden: 'translate-y-full',
      enter: 'translate-y-0',
      leave: 'translate-y-full'
    }
  })[position]);

  // Size classes
  const sizeClasses = $derived(() => ({
    left: {
      sm: 'w-64 max-w-xs',
      md: 'w-80 max-w-sm',
      lg: 'w-96 max-w-md',
      xl: 'w-[28rem] max-w-lg',
      full: 'w-full'
    },
    right: {
      sm: 'w-64 max-w-xs',
      md: 'w-80 max-w-sm',
      lg: 'w-96 max-w-md',
      xl: 'w-[28rem] max-w-lg',
      full: 'w-full'
    },
    top: {
      sm: 'h-32',
      md: 'h-48',
      lg: 'h-64',
      xl: 'h-80',
      full: 'h-full'
    },
    bottom: {
      sm: 'h-32',
      md: 'h-48',
      lg: 'h-64',
      xl: 'h-80',
      full: 'h-full'
    }
  })[position][size]);

  // Backdrop classes
  const backdropClasses = $derived(() => ({
    blur: 'backdrop-blur-sm bg-black/20 dark:bg-black/40',
    dark: 'bg-black/50 dark:bg-black/70',
    none: 'bg-transparent pointer-events-none'
  })[backdrop]);

  // Panel classes
  const panelClasses = $derived(() => [
    'relative flex flex-col glass shadow-premium border border-white/20 dark:border-dark-200/20',
    'transition-transform duration-300 ease-premium',
    'gpu-accelerated',
    sizeClasses,
    isVisible && !isAnimating ? positionClasses.panel : positionClasses.hidden,
    className
  ].filter(Boolean).join(' '));

  // Handle open state changes
  $effect(() => {
    if (open && mounted) {
      showDrawer();
    } else if (!open && mounted) {
      hideDrawer();
    }
  });

  // Show drawer with animation
  function showDrawer() {
    if (isVisible) return;
    
    isAnimating = true;
    isVisible = true;
    
    // Focus management
    requestAnimationFrame(() => {
      const focusableElement = drawerElement?.querySelector('[tabindex="0"], button, input, textarea, select, a[href]');
      focusableElement?.focus();
    });
    
    // Animation completion
    setTimeout(() => {
      isAnimating = false;
      dispatch('opened');
    }, 300);
    
    // Prevent body scroll
    if (typeof document !== 'undefined') {
      document.body.style.overflow = 'hidden';
    }
  }

  // Hide drawer with animation
  function hideDrawer() {
    if (!isVisible) return;
    
    isAnimating = true;
    
    setTimeout(() => {
      isVisible = false;
      isAnimating = false;
      dispatch('closed');
      
      // Restore body scroll
      if (typeof document !== 'undefined') {
        document.body.style.overflow = '';
      }
    }, 300);
  }

  // Handle backdrop click
  function handleBackdropClick(event) {
    if (persistent) return;
    if (event.target === event.currentTarget) {
      close();
    }
  }

  // Handle escape key
  function handleKeydown(event) {
    if (event.key === 'Escape' && !persistent) {
      close();
    }
  }

  // Public close method
  function close() {
    dispatch('close');
  }

  // Lifecycle
  onMount(() => {
    mounted = true;
    
    if (open) {
      showDrawer();
    }
    
    // Global event listeners
    if (typeof document !== 'undefined') {
      document.addEventListener('keydown', handleKeydown);
    }
  });

  onDestroy(() => {
    // Cleanup
    if (typeof document !== 'undefined') {
      document.removeEventListener('keydown', handleKeydown);
      document.body.style.overflow = '';
    }
  });
</script>

<!-- Drawer Portal -->
{#if isVisible}
  <div class="fixed inset-0 z-50 flex">
    <!-- Backdrop -->
    {#if overlay}
      <div
        class="fixed inset-0 transition-opacity duration-300 ease-premium {backdropClasses}"
        class:opacity-100={isVisible && !isAnimating}
        class:opacity-0={!isVisible || isAnimating}
        onclick={handleBackdropClick}
        aria-hidden="true"
      ></div>
    {/if}

    <!-- Drawer Container -->
    <div class="fixed {positionClasses.container}" style="z-index: 51;">
      <!-- Drawer Panel -->
      <div
        bind:this={drawerElement}
        class={panelClasses}
        role="dialog"
        aria-modal="true"
        aria-labelledby="drawer-title"
        aria-describedby="drawer-description"
        tabindex="-1"
      >
        <!-- Default Close Button -->
        {#if !persistent}
          <button
            type="button"
            class="absolute top-4 right-4 p-2 rounded-full text-gray-400 hover:text-gray-600 dark:text-dark-400 dark:hover:text-dark-600 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 focus:ring-offset-white dark:focus:ring-offset-dark-100 transition-colors duration-150 z-10"
            aria-label="Close drawer"
            onclick={close}
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        {/if}

        <!-- Drawer Content -->
        <div class="flex-1 flex flex-col overflow-hidden">
          <slot />
        </div>
      </div>
    </div>
  </div>
{/if}

<style>
  /* Enhanced animations */
  .ease-premium {
    transition-timing-function: cubic-bezier(0.16, 1, 0.3, 1);
  }

  /* GPU acceleration */
  .gpu-accelerated {
    transform: translateZ(0);
    backface-visibility: hidden;
    perspective: 1000;
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
    .transition-transform,
    .transition-opacity {
      transition-duration: 0.01ms !important;
    }
  }

  /* Focus visible enhancements */
  :global(.drawer-panel:focus-visible) {
    outline: 2px solid var(--color-primary-500);
    outline-offset: -2px;
  }
</style>