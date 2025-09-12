<script>
    import { X } from 'lucide-svelte';
    import { clsx } from 'clsx';
    import Button from './Button.svelte';
    
    let {
      open = $bindable(false),
      title = '',
      size = 'md',
      class: className = '',
      children,
      footer
    } = $props();
  
    const sizes = {
      sm: 'max-w-md',
      md: 'max-w-2xl',
      lg: 'max-w-4xl',
      xl: 'max-w-6xl',
      full: 'max-w-full mx-4'
    };
  
    const modalClass = clsx(
      'relative bg-white dark:bg-dark-100 rounded-3xl shadow-2xl',
      'max-h-[90vh] flex flex-col',
      sizes[size],
      className
    );
  
    function handleBackdropClick(e) {
      if (e.target === e.currentTarget) {
        open = false;
      }
    }
  
    $effect(() => {
      if (open) {
        document.body.style.overflow = 'hidden';
        return () => {
          document.body.style.overflow = '';
        };
      }
    });
  </script>
  
  {#if open}
    <div 
      class="fixed inset-0 z-50 flex items-center justify-center p-4"
      onclick={handleBackdropClick}
    >
      <!-- Backdrop -->
      <div class="absolute inset-0 bg-black/60 backdrop-blur-sm animate-fade-in" />
      
      <!-- Modal -->
      <div class={modalClass} style="animation: modal-scale-in 0.3s ease-out">
        <!-- Header -->
        {#if title}
          <div class="flex items-center justify-between p-6 border-b border-gray-200 dark:border-dark-200">
            <h2 class="text-xl font-display font-semibold text-gray-900 dark:text-white">
              {title}
            </h2>
            <button
              onclick={() => open = false}
              class="p-2 hover:bg-gray-100 dark:hover:bg-dark-200 rounded-xl transition-colors"
            >
              <X class="w-5 h-5 text-gray-500" />
            </button>
          </div>
        {/if}
        
        <!-- Content -->
        <div class="flex-1 overflow-y-auto p-6">
          {@render children?.()}
        </div>
        
        <!-- Footer -->
        {#if footer}
          <div class="p-6 border-t border-gray-200 dark:border-dark-200">
            {@render footer()}
          </div>
        {/if}
      </div>
    </div>
  {/if}
  
  <style>
    @keyframes modal-scale-in {
      from {
        transform: scale(0.95);
        opacity: 0;
      }
      to {
        transform: scale(1);
        opacity: 1;
      }
    }
    
    @keyframes fade-in {
      from {
        opacity: 0;
      }
      to {
        opacity: 1;
      }
    }
  </style>