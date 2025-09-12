<script>
    import { ChevronDown } from 'lucide-svelte';
    import { clsx } from 'clsx';
    
    let {
      label = '',
      value = $bindable(''),
      options = [],
      placeholder = 'Select an option',
      error = '',
      required = false,
      disabled = false,
      class: className = ''
    } = $props();
  
    let isOpen = $state(false);
    let selectId = `select-${crypto.randomUUID()}`;
  
    const selectClass = clsx(
      'w-full px-4 py-3 bg-gray-50 dark:bg-dark-200 rounded-xl',
      'border-2 transition-all duration-200 cursor-pointer',
      'focus:outline-none focus:bg-white dark:focus:bg-dark-100',
      'disabled:opacity-50 disabled:cursor-not-allowed',
      'flex items-center justify-between',
      error ? 'border-red-500' : 'border-transparent hover:border-primary-500',
      className
    );
  
    function handleSelect(optionValue) {
      value = optionValue;
      isOpen = false;
    }
  
    $effect(() => {
      function handleClickOutside(e) {
        if (!e.target.closest(`#${selectId}`)) {
          isOpen = false;
        }
      }
      
      if (isOpen) {
        document.addEventListener('click', handleClickOutside);
        return () => document.removeEventListener('click', handleClickOutside);
      }
    });
  </script>
  
  <div class="space-y-2" id={selectId}>
    {#if label}
      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
        {label}
        {#if required}
          <span class="text-red-500 ml-1">*</span>
        {/if}
      </label>
    {/if}
    
    <div class="relative">
      <button
        type="button"
        {disabled}
        onclick={() => isOpen = !isOpen}
        class={selectClass}
      >
        <span class={value ? 'text-gray-900 dark:text-white' : 'text-gray-500'}>
          {options.find(o => o.value === value)?.label || placeholder}
        </span>
        <ChevronDown class="w-5 h-5 text-gray-400 transition-transform {isOpen ? 'rotate-180' : ''}" />
      </button>
      
      {#if isOpen}
        <div class="absolute top-full left-0 right-0 mt-2 bg-white dark:bg-dark-100 rounded-xl shadow-2xl border border-gray-200 dark:border-dark-200 z-50 overflow-hidden animate-slide-down">
          {#each options as option}
            <button
              type="button"
              onclick={() => handleSelect(option.value)}
              class="w-full px-4 py-3 text-left hover:bg-gray-50 dark:hover:bg-dark-200 transition-colors {value === option.value ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-600' : 'text-gray-700 dark:text-gray-300'}"
            >
              {option.label}
            </button>
          {/each}
        </div>
      {/if}
    </div>
    
    {#if error}
      <p class="text-sm text-red-500">{error}</p>
    {/if}
  </div>