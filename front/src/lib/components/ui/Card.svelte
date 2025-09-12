<!--
  @component Card
  A flexible container component with glass morphism and neumorphic design variants.
  Supports hover effects, various sizes, and interactive states.
  
  @prop variant - Design variant: 'default' | 'glass' | 'neumorph' | 'elevated' | 'outlined'
  @prop size - Size variant: 'sm' | 'md' | 'lg' | 'xl' 
  @prop interactive - Whether the card is interactive (hoverable/clickable)
  @prop href - Optional URL for link behavior
  @prop padding - Padding variant: 'none' | 'sm' | 'md' | 'lg'
  @prop className - Additional CSS classes
  @prop onclick - Click handler function
  @prop disabled - Whether the card is disabled
-->
<script>
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  /** @type {'default' | 'glass' | 'neumorph' | 'elevated' | 'outlined'} */
  export let variant = 'default';
  
  /** @type {'sm' | 'md' | 'lg' | 'xl'} */
  export let size = 'md';
  
  /** @type {boolean} */
  export let interactive = false;
  
  /** @type {string | null} */
  export let href = null;
  
  /** @type {'none' | 'sm' | 'md' | 'lg'} */
  export let padding = 'md';
  
  /** @type {string} */
  export let className = '';
  
  /** @type {boolean} */
  export let disabled = false;

  // Base classes
  $: baseClasses = [
    'relative',
    'rounded-xl',
    'transition-all',
    'duration-300',
    'ease-out',
    'gpu-accelerated'
  ].join(' ');

  // Variant classes
  $: variantClasses = {
    default: 'bg-white dark:bg-dark-100 border border-gray-200 dark:border-dark-200 shadow-elevation-1',
    glass: 'glass border-white/20 dark:border-dark-200/20',
    neumorph: 'neumorph border-gray-100/50 dark:border-dark-200/50',
    elevated: 'bg-white dark:bg-dark-100 shadow-elevation-3 border-0',
    outlined: 'bg-transparent border-2 border-gray-300 dark:border-dark-300 shadow-none'
  }[variant];

  // Size classes
  $: sizeClasses = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg',
    xl: 'text-xl'
  }[size];

  // Padding classes
  $: paddingClasses = {
    none: 'p-0',
    sm: 'p-3',
    md: 'p-4 sm:p-6',
    lg: 'p-6 sm:p-8'
  }[padding];

  // Interactive classes
  $: interactiveClasses = interactive && !disabled 
    ? 'cursor-pointer hover-lift focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 focus-visible:ring-offset-white dark:focus-visible:ring-offset-dark-100'
    : '';

  // Disabled classes  
  $: disabledClasses = disabled 
    ? 'opacity-50 cursor-not-allowed pointer-events-none'
    : '';

  // Combined classes
  $: combinedClasses = [
    baseClasses,
    variantClasses,
    sizeClasses,
    paddingClasses,
    interactiveClasses,
    disabledClasses,
    className
  ].filter(Boolean).join(' ');

  // Component tag
  $: component = href ? 'a' : 'div';

  // Handle click events
  function handleClick(event) {
    if (disabled) {
      event.preventDefault();
      return;
    }
    
    if (interactive) {
      dispatch('click', event);
    }
  }

  // Handle keyboard events
  function handleKeyDown(event) {
    if (disabled) return;
    
    if (interactive && (event.key === 'Enter' || event.key === ' ')) {
      event.preventDefault();
      dispatch('click', event);
    }
  }
</script>

{#if component === 'a'}
  <a
    {href}
    class={combinedClasses}
    tabindex={interactive && !disabled ? 0 : -1}
    role={interactive ? 'button' : null}
    aria-disabled={disabled}
    on:click={handleClick}
    on:keydown={handleKeyDown}
    {...$$restProps}
  >
    <slot />
  </a>
{:else}
  <div
    class={combinedClasses}
    tabindex={interactive && !disabled ? 0 : -1}
    role={interactive ? 'button' : null}
    aria-disabled={disabled}
    on:click={handleClick}
    on:keydown={handleKeyDown}
    {...$$restProps}
  >
    <slot />
  </div>
{/if}

<style>
  /* Additional premium effects */
  :global(.card-magnetic) {
    position: relative;
    overflow: hidden;
  }

  :global(.card-magnetic::before) {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, 
      color(display-p3 0.659 0.333 0.969 / 0.05), 
      color(display-p3 0.753 0.518 0.988 / 0.05));
    transform: translateX(-100%);
    transition: transform var(--transition-smooth) 300ms;
    pointer-events: none;
  }

  :global(.card-magnetic:hover::before) {
    transform: translateX(0);
  }

  /* High contrast mode adjustments */
  @media (prefers-contrast: high) {
    :global(.card) {
      border-width: 2px !important;
      border-style: solid !important;
    }
  }

  /* Reduced motion preferences */
  @media (prefers-reduced-motion: reduce) {
    :global(.card) {
      transition-duration: 0.01ms !important;
    }
  }
</style>