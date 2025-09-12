<script>
    import { Star } from 'lucide-svelte';
    
    export let value = 0;
    export let max = 5;
    export let interactive = false;
    export let size = 'md';
    
    const sizes = {
      sm: 'w-4 h-4',
      md: 'w-5 h-5',
      lg: 'w-6 h-6'
    };
    
    function handleClick(rating) {
      if (interactive) {
        value = rating;
      }
    }
  </script>
  
  <div class="flex items-center gap-1">
    {#each Array(max) as _, i}
      <button
        type="button"
        disabled={!interactive}
        on:click={() => handleClick(i + 1)}
        class="{interactive ? 'cursor-pointer' : 'cursor-default'}"
      >
        <Star
          class="{sizes[size]} {i < value ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300'}"
        />
      </button>
    {/each}
  </div>