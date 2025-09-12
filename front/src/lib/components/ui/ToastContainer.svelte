<script>
    import { CheckCircle, XCircle, Info, AlertTriangle, X } from 'lucide-svelte';
    import { toastStore } from '$lib/stores/toast.svelte.js';
    import Button from './Button.svelte';
    
    const icons = {
      success: CheckCircle,
      error: XCircle,
      info: Info,
      warning: AlertTriangle
    };
    
    const colors = {
      success: 'from-green-500 to-green-600',
      error: 'from-red-500 to-red-600',
      info: 'from-blue-500 to-blue-600',
      warning: 'from-yellow-500 to-yellow-600'
    };
  </script>
  
  <div class="fixed bottom-4 right-4 z-50 space-y-3 pointer-events-none">
    {#each toastStore.toasts as item (item.id)}
      <div 
        class="flex items-center gap-3 p-4 bg-white dark:bg-dark-100 rounded-2xl shadow-2xl min-w-[320px] max-w-md pointer-events-auto animate-slide-left"
      >
        <div class="flex-shrink-0 w-10 h-10 rounded-xl bg-gradient-to-br {colors[item.type]} flex items-center justify-center">
          <svelte:component this={icons[item.type]} class="w-5 h-5 text-white" />
        </div>
        
        <div class="flex-1">
          <p class="text-gray-900 dark:text-white font-medium">{item.message}</p>
          {#if item.action}
            <button
              onclick={item.action.onClick}
              class="text-sm text-primary-600 hover:text-primary-700 font-medium mt-1"
            >
              {item.action.label}
            </button>
          {/if}
        </div>
        
        <button
          onclick={() => toastStore.remove(item.id)}
          class="p-1 hover:bg-gray-100 dark:hover:bg-dark-200 rounded-lg transition-colors"
        >
          <X class="w-4 h-4 text-gray-400" />
        </button>
      </div>
    {/each}
  </div>
  
  <style>
    @keyframes slide-left {
      from {
        transform: translateX(100%);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }
    
    .animate-slide-left {
      animation: slide-left 0.3s ease-out;
    }
  </style>