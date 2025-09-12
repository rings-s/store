<!--
  @component Toast
  Individual toast notification component that integrates with the global toast store.
  Supports various types, animations, and interactions.
  
  @prop toast - Toast object from the toast store
  @prop position - Toast position for animation direction
-->
<script>
  import { createEventDispatcher, onMount, onDestroy } from 'svelte';
  import { toastStore } from '$lib/stores/toast.svelte.js';

  const dispatch = createEventDispatcher();

  /** @type {import('$lib/stores/toast.svelte.js').Toast} */
  export let toast;
  
  /** @type {string} */
  export let position = 'top-right';

  // Local state
  let toastElement;
  let isPaused = false;
  let remainingTime = toast.duration;
  let pauseTime = null;
  let mounted = false;

  // Animation state
  let isVisible = false;
  let isExiting = false;

  // Type-based styling and icons
  $: typeConfig = {
    success: {
      icon: 'check-circle',
      bgColor: 'bg-success-50 dark:bg-success-900/20',
      borderColor: 'border-success-200 dark:border-success-800',
      iconColor: 'text-success-600 dark:text-success-400',
      progressColor: 'bg-success-500'
    },
    error: {
      icon: 'x-circle', 
      bgColor: 'bg-error-50 dark:bg-error-900/20',
      borderColor: 'border-error-200 dark:border-error-800',
      iconColor: 'text-error-600 dark:text-error-400',
      progressColor: 'bg-error-500'
    },
    warning: {
      icon: 'exclamation-triangle',
      bgColor: 'bg-warning-50 dark:bg-warning-900/20',
      borderColor: 'border-warning-200 dark:border-warning-800',
      iconColor: 'text-warning-600 dark:text-warning-400',
      progressColor: 'bg-warning-500'
    },
    info: {
      icon: 'information-circle',
      bgColor: 'bg-blue-50 dark:bg-blue-900/20',
      borderColor: 'border-blue-200 dark:border-blue-800',
      iconColor: 'text-blue-600 dark:text-blue-400',
      progressColor: 'bg-blue-500'
    },
    loading: {
      icon: 'loading',
      bgColor: 'bg-gray-50 dark:bg-dark-100',
      borderColor: 'border-gray-200 dark:border-dark-200',
      iconColor: 'text-gray-600 dark:text-gray-400',
      progressColor: 'bg-primary-500'
    }
  }[toast.type];

  // Animation direction based on position
  $: animationDirection = {
    'top-left': 'animate-slide-right',
    'top-center': 'animate-slide-down',
    'top-right': 'animate-slide-left',
    'bottom-left': 'animate-slide-right',
    'bottom-center': 'animate-slide-up',
    'bottom-right': 'animate-slide-left'
  }[position];

  // Handle mouse events for auto-dismiss pause/resume
  function handleMouseEnter() {
    if (toast.duration > 0 && !isPaused) {
      isPaused = true;
      pauseTime = Date.now();
      toastStore.pause(toast.id);
    }
  }

  function handleMouseLeave() {
    if (toast.duration > 0 && isPaused) {
      isPaused = false;
      const elapsed = Date.now() - pauseTime;
      remainingTime = Math.max(0, remainingTime - elapsed);
      
      if (remainingTime > 0) {
        toastStore.resume(toast.id, remainingTime);
      } else {
        handleDismiss();
      }
      pauseTime = null;
    }
  }

  // Handle dismiss
  function handleDismiss() {
    if (isExiting) return;
    
    isExiting = true;
    
    // Wait for exit animation before removing
    setTimeout(() => {
      toastStore.remove(toast.id);
      dispatch('dismiss', toast);
    }, 150);
  }

  // Handle action click
  function handleAction() {
    if (toast.action && toast.action.handler) {
      toast.action.handler();
    }
    if (!toast.action?.persist) {
      handleDismiss();
    }
  }

  // Mount animation
  onMount(() => {
    mounted = true;
    // Delay to ensure element is in DOM for animation
    requestAnimationFrame(() => {
      isVisible = true;
    });
  });

  // Cleanup
  onDestroy(() => {
    if (toast.timeoutId) {
      clearTimeout(toast.timeoutId);
    }
  });
</script>

<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
<div
  bind:this={toastElement}
  role="alert"
  aria-live="polite"
  aria-atomic="true"
  class="relative max-w-sm w-full glass shadow-premium rounded-xl border overflow-hidden transition-all duration-300 ease-out {typeConfig.bgColor} {typeConfig.borderColor}"
  class:opacity-0={!isVisible && !isExiting}
  class:opacity-100={isVisible && !isExiting}
  class:animate-scale-out={isExiting}
  class:{animationDirection}={isVisible && !isExiting}
  on:mouseenter={handleMouseEnter}
  on:mouseleave={handleMouseLeave}
  on:keydown={(e) => e.key === 'Escape' && toast.dismissible && handleDismiss()}
>
  <!-- Progress bar for auto-dismiss -->
  {#if toast.duration > 0 && !isPaused}
    <div class="absolute top-0 left-0 h-1 {typeConfig.progressColor} transition-all duration-100 ease-linear" 
         style="width: {((toast.duration - remainingTime) / toast.duration) * 100}%">
    </div>
  {/if}

  <div class="flex items-start gap-3 p-4">
    <!-- Icon -->
    <div class="flex-shrink-0 {typeConfig.iconColor}">
      {#if typeConfig.icon === 'check-circle'}
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
        </svg>
      {:else if typeConfig.icon === 'x-circle'}
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
        </svg>
      {:else if typeConfig.icon === 'exclamation-triangle'}
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
          <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>
      {:else if typeConfig.icon === 'information-circle'}
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
        </svg>
      {:else if typeConfig.icon === 'loading'}
        <svg class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24" aria-hidden="true">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      {/if}
    </div>

    <!-- Content -->
    <div class="flex-1 min-w-0">
      {#if toast.title}
        <p class="font-medium text-gray-900 dark:text-dark-900 text-sm leading-5">
          {toast.title}
        </p>
      {/if}
      
      {#if toast.message}
        <p class="text-gray-700 dark:text-dark-700 text-sm leading-5" 
           class:mt-1={toast.title}>
          {toast.message}
        </p>
      {/if}

      <!-- Action Button -->
      {#if toast.action}
        <button
          type="button"
          class="mt-3 text-sm font-medium {typeConfig.iconColor} hover:underline focus:outline-none focus:underline transition-all duration-150"
          on:click={handleAction}
        >
          {toast.action.label}
        </button>
      {/if}
    </div>

    <!-- Dismiss Button -->
    {#if toast.dismissible}
      <button
        type="button"
        class="flex-shrink-0 p-1 rounded-full text-gray-400 hover:text-gray-600 dark:text-dark-400 dark:hover:text-dark-600 focus:outline-none focus:text-gray-600 dark:focus:text-dark-600 transition-colors duration-150"
        aria-label="Dismiss notification"
        on:click={handleDismiss}
      >
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
          <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
        </svg>
      </button>
    {/if}
  </div>
</div>

<style>
  /* Custom animations */
  @keyframes scale-out {
    0% {
      transform: scale(1);
      opacity: 1;
    }
    100% {
      transform: scale(0.95);
      opacity: 0;
    }
  }

  /* Animation classes */
  :global(.animate-scale-out) {
    animation: scale-out 0.15s ease-in forwards;
  }

  /* Progress bar animation */
  .progress-bar {
    animation: progress linear;
  }

  /* High contrast adjustments */
  @media (prefers-contrast: high) {
    .toast {
      border-width: 2px !important;
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .toast {
      animation: none !important;
      transition-duration: 0.01ms !important;
    }
  }
</style>