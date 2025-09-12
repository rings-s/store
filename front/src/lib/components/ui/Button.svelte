<!-- src/lib/components/ui/Button.svelte -->
<script>
    import { clsx } from 'clsx';
    
    let {
      type = 'button',
      variant = 'primary',
      size = 'md',
      disabled = false,
      loading = false,
      fullWidth = false,
      icon = null,
      iconPosition = 'left',
      class: className = '',
      children,
      onclick,
      ...restProps
    } = $props();
  
    const variants = {
      primary: 'bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 text-white shadow-lg shadow-primary-500/25',
      secondary: 'bg-white dark:bg-dark-200 hover:bg-gray-50 dark:hover:bg-dark-300 text-gray-900 dark:text-dark-800 border border-gray-200 dark:border-dark-300',
      ghost: 'hover:bg-gray-100 dark:hover:bg-dark-200 text-gray-700 dark:text-dark-600',
      danger: 'bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white',
      success: 'bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white',
      glass: 'glass text-gray-900 dark:text-white hover:bg-white/90 dark:hover:bg-dark-100/90'
    };
  
    const sizes = {
      xs: 'px-2.5 py-1.5 text-xs',
      sm: 'px-3 py-2 text-sm',
      md: 'px-4 py-2.5 text-sm',
      lg: 'px-6 py-3 text-base',
      xl: 'px-8 py-4 text-lg'
    };
  
    const buttonClass = clsx(
      'relative inline-flex items-center justify-center font-medium rounded-xl transition-all duration-200',
      'transform active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none',
      'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-dark-100',
      variants[variant],
      sizes[size],
      fullWidth && 'w-full',
      className
    );
  </script>
  
  <button
    {type}
    {disabled}
    class={buttonClass}
    {onclick}
    {...restProps}
  >
    <span class="relative flex items-center gap-2">
      {#if loading}
        <svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
        </svg>
      {:else if icon && iconPosition === 'left'}
        <svelte:component this={icon} class="w-4 h-4" />
      {/if}
      
      {@render children?.()}
      
      {#if icon && iconPosition === 'right' && !loading}
        <svelte:component this={icon} class="w-4 h-4" />
      {/if}
    </span>
    
    <!-- Ripple effect -->
    <span class="absolute inset-0 rounded-xl overflow-hidden">
      <span class="absolute inset-0 bg-white opacity-0 hover:opacity-10 transition-opacity"></span>
    </span>
  </button>