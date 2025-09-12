<script>
    import { clsx } from 'clsx';
    
    let {
      type = 'text',
      label = '',
      value = $bindable(''),
      placeholder = '',
      error = '',
      hint = '',
      required = false,
      disabled = false,
      icon = null,
      class: className = '',
      ...restProps
    } = $props();
  
    let focused = $state(false);
    let inputId = `input-${crypto.randomUUID()}`;
  
    const inputClass = clsx(
      'w-full px-4 py-3 bg-gray-50 dark:bg-dark-200 rounded-xl',
      'border-2 transition-all duration-200',
      'focus:outline-none focus:bg-white dark:focus:bg-dark-100',
      'disabled:opacity-50 disabled:cursor-not-allowed',
      error ? 'border-red-500 focus:border-red-500' : 'border-transparent focus:border-primary-500',
      icon && 'pl-12',
      className
    );
  </script>
  
  <div class="space-y-2">
    {#if label}
      <label for={inputId} class="block text-sm font-medium text-gray-700 dark:text-gray-300">
        {label}
        {#if required}
          <span class="text-red-500 ml-1">*</span>
        {/if}
      </label>
    {/if}
    
    <div class="relative">
      {#if icon}
        <div class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
          <svelte:component this={icon} class="w-5 h-5" />
        </div>
      {/if}
      
      <input
        id={inputId}
        {type}
        bind:value
        {placeholder}
        {required}
        {disabled}
        class={inputClass}
        onfocus={() => focused = true}
        onblur={() => focused = false}
        {...restProps}
      />
    </div>
    
    {#if error}
      <p class="text-sm text-red-500 flex items-center gap-1">
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>
        {error}
      </p>
    {:else if hint}
      <p class="text-sm text-gray-500 dark:text-gray-400">{hint}</p>
    {/if}
  </div>