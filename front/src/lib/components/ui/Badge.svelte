<!--
  @component Badge
  A flexible badge component for status indicators, labels, and notifications.
  Supports various colors, sizes, shapes, and animations.
  
  @prop variant - Color variant: 'default' | 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'info'
  @prop size - Size variant: 'xs' | 'sm' | 'md' | 'lg'
  @prop shape - Shape variant: 'pill' | 'rounded' | 'square'
  @prop outline - Whether to use outline style
  @prop pulse - Whether to show pulse animation
  @prop dismissible - Whether the badge can be dismissed
  @prop icon - Optional icon to display (left side)
  @prop iconRight - Optional icon to display (right side)
  @prop className - Additional CSS classes
-->
<script>
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  /** @type {'default' | 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'info'} */
  export let variant = 'default';
  
  /** @type {'xs' | 'sm' | 'md' | 'lg'} */
  export let size = 'md';
  
  /** @type {'pill' | 'rounded' | 'square'} */
  export let shape = 'pill';
  
  /** @type {boolean} */
  export let outline = false;
  
  /** @type {boolean} */
  export let pulse = false;
  
  /** @type {boolean} */
  export let dismissible = false;
  
  /** @type {string | null} */
  export let icon = null;
  
  /** @type {string | null} */
  export let iconRight = null;
  
  /** @type {string} */
  export let className = '';

  // State
  let dismissed = false;

  // Base classes
  $: baseClasses = [
    'inline-flex',
    'items-center',
    'justify-center',
    'font-medium',
    'transition-all',
    'duration-200',
    'ease-out',
    'select-none',
    'gpu-accelerated'
  ].join(' ');

  // Variant classes
  $: variantClasses = outline ? outlineVariantClasses[variant] : solidVariantClasses[variant];

  $: solidVariantClasses = {
    default: 'bg-gray-100 text-gray-800 dark:bg-dark-200 dark:text-dark-800',
    primary: 'bg-primary-100 text-primary-800 dark:bg-primary-900/50 dark:text-primary-200',
    secondary: 'bg-gray-100 text-gray-700 dark:bg-dark-200 dark:text-dark-700',
    success: 'bg-success-100 text-success-800 dark:bg-success-900/50 dark:text-success-200',
    warning: 'bg-warning-100 text-warning-800 dark:bg-warning-900/50 dark:text-warning-200',
    error: 'bg-error-100 text-error-800 dark:bg-error-900/50 dark:text-error-200',
    info: 'bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-200'
  };

  $: outlineVariantClasses = {
    default: 'border border-gray-300 text-gray-700 dark:border-dark-300 dark:text-dark-700',
    primary: 'border border-primary-300 text-primary-700 dark:border-primary-700 dark:text-primary-300',
    secondary: 'border border-gray-300 text-gray-600 dark:border-dark-300 dark:text-dark-600',
    success: 'border border-success-300 text-success-700 dark:border-success-700 dark:text-success-300',
    warning: 'border border-warning-300 text-warning-700 dark:border-warning-700 dark:text-warning-300',
    error: 'border border-error-300 text-error-700 dark:border-error-700 dark:text-error-300',
    info: 'border border-blue-300 text-blue-700 dark:border-blue-700 dark:text-blue-300'
  };

  // Size classes
  $: sizeClasses = {
    xs: 'px-2 py-0.5 text-xs gap-1',
    sm: 'px-2.5 py-0.5 text-sm gap-1',
    md: 'px-3 py-1 text-sm gap-1.5',
    lg: 'px-4 py-1.5 text-base gap-2'
  }[size];

  // Shape classes
  $: shapeClasses = {
    pill: 'rounded-full',
    rounded: 'rounded-lg',
    square: 'rounded-none'
  }[shape];

  // Icon size classes
  $: iconSizeClasses = {
    xs: 'w-3 h-3',
    sm: 'w-3.5 h-3.5',
    md: 'w-4 h-4',
    lg: 'w-5 h-5'
  }[size];

  // Animation classes
  $: animationClasses = pulse ? 'animate-pulse-glow' : '';

  // Dismissible classes
  $: dismissibleClasses = dismissible ? 'pr-1.5' : '';

  // Combined classes
  $: combinedClasses = [
    baseClasses,
    variantClasses,
    sizeClasses,
    shapeClasses,
    animationClasses,
    dismissibleClasses,
    className
  ].filter(Boolean).join(' ');

  // Handle dismiss
  function handleDismiss(event) {
    event.stopPropagation();
    dismissed = true;
    dispatch('dismiss');
  }

  // Handle click
  function handleClick(event) {
    dispatch('click', event);
  }
</script>

{#if !dismissed}
  <span
    class={combinedClasses}
    role="status"
    aria-live="polite"
    on:click={handleClick}
    {...$$restProps}
  >
    <!-- Left Icon -->
    {#if icon}
      <svg 
        class={iconSizeClasses} 
        fill="currentColor" 
        viewBox="0 0 20 20"
        aria-hidden="true"
      >
        {#if icon === 'check'}
          <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
        {:else if icon === 'x'}
          <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
        {:else if icon === 'exclamation'}
          <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
        {:else if icon === 'info'}
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
        {:else if icon === 'star'}
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        {:else}
          <!-- Default dot icon -->
          <circle cx="10" cy="10" r="3" />
        {/if}
      </svg>
    {/if}

    <!-- Content -->
    <slot />

    <!-- Right Icon -->
    {#if iconRight}
      <svg 
        class={iconSizeClasses} 
        fill="currentColor" 
        viewBox="0 0 20 20"
        aria-hidden="true"
      >
        <!-- Add right icon paths here similar to left icon -->
        <circle cx="10" cy="10" r="3" />
      </svg>
    {/if}

    <!-- Dismiss Button -->
    {#if dismissible}
      <button
        type="button"
        class="ml-1 inline-flex items-center justify-center flex-shrink-0 rounded-full hover:bg-black/10 dark:hover:bg-white/10 focus:outline-none focus:bg-black/10 dark:focus:bg-white/10 transition-colors duration-150"
        class:w-4={size === 'xs' || size === 'sm'}
        class:h-4={size === 'xs' || size === 'sm'}
        class:w-5={size === 'md' || size === 'lg'}
        class:h-5={size === 'md' || size === 'lg'}
        aria-label="Remove badge"
        on:click={handleDismiss}
      >
        <svg 
          class="w-3 h-3" 
          fill="currentColor" 
          viewBox="0 0 20 20"
          aria-hidden="true"
        >
          <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
        </svg>
      </button>
    {/if}
  </span>
{/if}

<style>
  /* Pulse glow animation */
  @keyframes pulse-glow {
    0%, 100% { 
      opacity: 1; 
      transform: scale(1);
    }
    50% { 
      opacity: 0.8; 
      transform: scale(1.05);
    }
  }

  /* High contrast mode adjustments */
  @media (prefers-contrast: high) {
    :global(.badge) {
      border-width: 2px !important;
      font-weight: 600 !important;
    }
  }

  /* Reduced motion preferences */
  @media (prefers-reduced-motion: reduce) {
    :global(.badge) {
      animation: none !important;
      transition-duration: 0.01ms !important;
    }
  }
</style>