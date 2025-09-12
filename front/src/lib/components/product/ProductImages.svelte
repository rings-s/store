<!--
  @component ProductImages
  Premium product image gallery with zoom, navigation, and fullscreen support.
  Features keyboard navigation, accessibility, and smooth transitions.
  
  @prop images - Array of image objects with src and alt properties
  @prop aspect - Image aspect ratio: 'square' | 'portrait' | 'landscape'
  @prop showThumbnails - Whether to show thumbnail navigation
  @prop showZoom - Whether to enable zoom functionality
  @prop showFullscreen - Whether to show fullscreen option
-->
<script>
  import { createEventDispatcher, onMount, onDestroy } from 'svelte';
  
  const dispatch = createEventDispatcher();
  
  /** @type {Array<{src: string, alt: string}>} */
  export let images = [];
  
  /** @type {'square' | 'portrait' | 'landscape'} */
  export let aspect = 'square';
  
  /** @type {boolean} */
  export let showThumbnails = true;
  
  /** @type {boolean} */
  export let showZoom = true;
  
  /** @type {boolean} */
  export let showFullscreen = true;

  // Reactive state using Svelte 5 runes
  let currentIndex = $state(0);
  let isFullscreen = $state(false);
  let isZoomed = $state(false);
  let imageLoaded = $state(false);
  let mousePosition = $state({ x: 50, y: 50 });
  let mainImageRef = $state();
  
  // Computed values
  const currentImage = $derived(() => images[currentIndex]);
  const hasMultipleImages = $derived(() => images.length > 1);
  
  // Aspect ratio classes
  const aspectClasses = $derived(() => ({
    square: 'aspect-square',
    portrait: 'aspect-[4/5]', 
    landscape: 'aspect-[5/4]'
  })[aspect]);

  // Navigation functions
  function nextImage() {
    if (hasMultipleImages) {
      currentIndex = (currentIndex + 1) % images.length;
      imageLoaded = false;
      dispatch('imageChange', { index: currentIndex, image: currentImage });
    }
  }
  
  function prevImage() {
    if (hasMultipleImages) {
      currentIndex = currentIndex === 0 ? images.length - 1 : currentIndex - 1;
      imageLoaded = false;
      dispatch('imageChange', { index: currentIndex, image: currentImage });
    }
  }
  
  function goToImage(index) {
    if (index !== currentIndex) {
      currentIndex = index;
      imageLoaded = false;
      dispatch('imageChange', { index: currentIndex, image: currentImage });
    }
  }

  // Image interactions
  function handleImageLoad() {
    imageLoaded = true;
  }

  function toggleZoom() {
    if (!showZoom) return;
    isZoomed = !isZoomed;
    dispatch('zoomToggle', { isZoomed });
  }

  function toggleFullscreen() {
    if (!showFullscreen) return;
    isFullscreen = !isFullscreen;
    dispatch('fullscreenToggle', { isFullscreen });
  }

  function handleMouseMove(event) {
    if (!isZoomed || !mainImageRef) return;
    
    const rect = mainImageRef.getBoundingClientRect();
    const x = ((event.clientX - rect.left) / rect.width) * 100;
    const y = ((event.clientY - rect.top) / rect.height) * 100;
    
    mousePosition = { x: Math.max(0, Math.min(100, x)), y: Math.max(0, Math.min(100, y)) };
  }

  // Keyboard navigation
  function handleKeydown(event) {
    if (!hasMultipleImages) return;
    
    switch (event.key) {
      case 'ArrowLeft':
        event.preventDefault();
        prevImage();
        break;
      case 'ArrowRight':
        event.preventDefault();
        nextImage();
        break;
      case 'Escape':
        if (isFullscreen) {
          isFullscreen = false;
        } else if (isZoomed) {
          isZoomed = false;
        }
        break;
      case 'Enter':
      case ' ':
        if (showZoom) {
          event.preventDefault();
          toggleZoom();
        }
        break;
    }
  }

  // Touch support for mobile
  let touchStartX = $state(0);
  
  function handleTouchStart(event) {
    touchStartX = event.touches[0].clientX;
  }
  
  function handleTouchEnd(event) {
    const touchEndX = event.changedTouches[0].clientX;
    const diff = touchStartX - touchEndX;
    
    if (Math.abs(diff) > 50) { // Minimum swipe distance
      if (diff > 0) {
        nextImage();
      } else {
        prevImage();
      }
    }
  }

  // Lifecycle
  onMount(() => {
    if (typeof document !== 'undefined') {
      document.addEventListener('keydown', handleKeydown);
    }
  });

  onDestroy(() => {
    if (typeof document !== 'undefined') {
      document.removeEventListener('keydown', handleKeydown);
    }
  });
</script>

<div class="space-y-4">
  <!-- Main Image -->
  <div 
    bind:this={mainImageRef}
    class="relative {aspectClasses} rounded-2xl overflow-hidden glass border border-white/20 dark:border-dark-200/20 group cursor-pointer transition-all duration-300"
    class:cursor-zoom-in={showZoom && !isZoomed}
    class:cursor-zoom-out={showZoom && isZoomed}
    on:click={toggleZoom}
    on:mousemove={handleMouseMove}
    on:touchstart={handleTouchStart}
    on:touchend={handleTouchEnd}
    role="img"
    aria-label="Product image {currentIndex + 1} of {images.length}"
    tabindex="0"
  >
    {#if currentImage}
      <img
        src={currentImage.src}
        alt={currentImage.alt || `Product image ${currentIndex + 1}`}
        class="w-full h-full object-cover transition-all duration-500"
        class:opacity-0={!imageLoaded}
        class:opacity-100={imageLoaded}
        class:scale-150={isZoomed}
        style={isZoomed ? `transform-origin: ${mousePosition.x}% ${mousePosition.y}%` : ''}
        on:load={handleImageLoad}
        loading={currentIndex === 0 ? 'eager' : 'lazy'}
      />
    {:else}
      <!-- Placeholder -->
      <div class="w-full h-full bg-gradient-to-br from-gray-100 to-gray-200 dark:from-dark-200 dark:to-dark-300 flex items-center justify-center">
        <svg class="w-16 h-16 text-gray-400 dark:text-dark-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </div>
    {/if}
    
    <!-- Loading indicator -->
    {#if !imageLoaded}
      <div class="absolute inset-0 bg-gray-100 dark:bg-dark-200 animate-pulse flex items-center justify-center">
        <svg class="w-8 h-8 text-gray-400 dark:text-dark-400 animate-spin" fill="none" viewBox="0 0 24 24" aria-hidden="true">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>
    {/if}
    
    <!-- Navigation Arrows -->
    {#if hasMultipleImages}
      <button
        type="button"
        class="absolute left-4 top-1/2 -translate-y-1/2 w-10 h-10 glass border border-white/20 dark:border-dark-200/20 rounded-full flex items-center justify-center text-gray-700 dark:text-dark-700 hover:text-gray-900 dark:hover:text-dark-900 opacity-0 group-hover:opacity-100 transition-all duration-200 hover-lift-sm"
        on:click|stopPropagation={prevImage}
        aria-label="Previous image"
      >
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      
      <button
        type="button"
        class="absolute right-4 top-1/2 -translate-y-1/2 w-10 h-10 glass border border-white/20 dark:border-dark-200/20 rounded-full flex items-center justify-center text-gray-700 dark:text-dark-700 hover:text-gray-900 dark:hover:text-dark-900 opacity-0 group-hover:opacity-100 transition-all duration-200 hover-lift-sm"
        on:click|stopPropagation={nextImage}
        aria-label="Next image"
      >
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </button>
    {/if}
    
    <!-- Action Buttons -->
    <div class="absolute top-4 right-4 flex gap-2">
      {#if showZoom}
        <button
          type="button"
          class="w-10 h-10 glass border border-white/20 dark:border-dark-200/20 rounded-full flex items-center justify-center text-gray-700 dark:text-dark-700 hover:text-gray-900 dark:hover:text-dark-900 opacity-0 group-hover:opacity-100 transition-all duration-200"
          class:opacity-100={isZoomed}
          on:click|stopPropagation={toggleZoom}
          aria-label={isZoomed ? 'Zoom out' : 'Zoom in'}
        >
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            {#if isZoomed}
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM13 10h-6" />
            {:else}
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" />
            {/if}
          </svg>
        </button>
      {/if}
      
      {#if showFullscreen}
        <button
          type="button"
          class="w-10 h-10 glass border border-white/20 dark:border-dark-200/20 rounded-full flex items-center justify-center text-gray-700 dark:text-dark-700 hover:text-gray-900 dark:hover:text-dark-900 opacity-0 group-hover:opacity-100 transition-all duration-200"
          on:click|stopPropagation={toggleFullscreen}
          aria-label="View fullscreen"
        >
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
          </svg>
        </button>
      {/if}
    </div>
    
    <!-- Image counter -->
    {#if hasMultipleImages}
      <div class="absolute bottom-4 left-4 px-3 py-1 glass border border-white/20 dark:border-dark-200/20 rounded-full text-sm font-medium text-gray-700 dark:text-dark-700 opacity-0 group-hover:opacity-100 transition-all duration-200">
        {currentIndex + 1} / {images.length}
      </div>
    {/if}
  </div>
  
  <!-- Thumbnails -->
  {#if hasMultipleImages && showThumbnails}
    <div class="flex gap-2 overflow-x-auto scrollbar-thin pb-2" role="tablist" aria-label="Product image thumbnails">
      {#each images as image, index}
        <button
          type="button"
          class="flex-shrink-0 w-16 h-16 sm:w-20 sm:h-20 rounded-xl overflow-hidden border-2 transition-all duration-200 hover-lift-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
          class:border-primary-500={currentIndex === index}
          class:dark:border-primary-400={currentIndex === index}
          class:border-transparent={currentIndex !== index}
          class:opacity-50={currentIndex !== index}
          class:opacity-100={currentIndex === index}
          on:click={() => goToImage(index)}
          role="tab"
          aria-selected={currentIndex === index}
          aria-label="View image {index + 1}"
        >
          <img
            src={image.src}
            alt={`Thumbnail ${index + 1}`}
            class="w-full h-full object-cover transition-transform duration-200 hover:scale-105"
            loading="lazy"
          />
        </button>
      {/each}
    </div>
  {/if}
</div>

<!-- Fullscreen Modal -->
{#if isFullscreen}
  <div 
    class="fixed inset-0 z-50 bg-black/90 flex items-center justify-center"
    on:click|self={() => isFullscreen = false}
    role="dialog"
    aria-modal="true"
    aria-label="Fullscreen image view"
  >
    <!-- Close button -->
    <button
      type="button"
      class="absolute top-4 right-4 w-12 h-12 glass border border-white/20 rounded-full flex items-center justify-center text-white hover:text-gray-200 transition-colors duration-200 z-10"
      on:click={() => isFullscreen = false}
      aria-label="Close fullscreen"
    >
      <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
      </svg>
    </button>
    
    <!-- Fullscreen image -->
    {#if currentImage}
      <img
        src={currentImage.src}
        alt={currentImage.alt || `Product image ${currentIndex + 1}`}
        class="max-w-full max-h-full object-contain"
      />
    {/if}
    
    <!-- Navigation in fullscreen -->
    {#if hasMultipleImages}
      <button
        type="button"
        class="absolute left-4 top-1/2 -translate-y-1/2 w-12 h-12 glass border border-white/20 rounded-full flex items-center justify-center text-white hover:text-gray-200 transition-colors duration-200"
        on:click={prevImage}
        aria-label="Previous image"
      >
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      
      <button
        type="button"
        class="absolute right-4 top-1/2 -translate-y-1/2 w-12 h-12 glass border border-white/20 rounded-full flex items-center justify-center text-white hover:text-gray-200 transition-colors duration-200"
        on:click={nextImage}
        aria-label="Next image"
      >
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </button>
      
      <!-- Image counter in fullscreen -->
      <div class="absolute bottom-4 left-1/2 -translate-x-1/2 px-4 py-2 glass border border-white/20 rounded-full text-white font-medium">
        {currentIndex + 1} / {images.length}
      </div>
    {/if}
  </div>
{/if}

<style>
  .hover-lift-sm:hover {
    transform: translateY(-1px);
  }

  .scrollbar-thin {
    scrollbar-width: thin;
    scrollbar-color: rgba(156, 163, 175, 0.5) transparent;
  }

  .scrollbar-thin::-webkit-scrollbar {
    height: 4px;
  }

  .scrollbar-thin::-webkit-scrollbar-track {
    background: transparent;
  }

  .scrollbar-thin::-webkit-scrollbar-thumb {
    background-color: rgba(156, 163, 175, 0.5);
    border-radius: 2px;
  }

  .cursor-zoom-in {
    cursor: zoom-in;
  }

  .cursor-zoom-out {
    cursor: zoom-out;
  }

  /* Focus visible enhancements */
  :global(button:focus-visible) {
    outline: 2px solid var(--color-primary-500);
    outline-offset: 2px;
  }

  /* High contrast mode adjustments */
  @media (prefers-contrast: high) {
    .glass {
      border-width: 2px !important;
      backdrop-filter: none !important;
      background: rgba(255, 255, 255, 0.9) !important;
    }
    
    :global(.dark) .glass {
      background: rgba(17, 24, 39, 0.9) !important;
    }
  }

  /* Reduced motion preferences */
  @media (prefers-reduced-motion: reduce) {
    * {
      transition-duration: 0.01ms !important;
      animation-duration: 0.01ms !important;
    }
    
    .hover-lift-sm:hover {
      transform: none !important;
    }
  }
</style>