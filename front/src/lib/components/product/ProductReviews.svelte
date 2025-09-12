<!--
  @component ProductReviews
  Premium product reviews component with enhanced UX and comprehensive functionality.
  Features interactive reviews, filtering, sorting, review submission, and accessibility.
  
  @prop productId - Product identifier for reviews
  @prop reviews - Array of review objects
  @prop canReview - Whether user can submit review (optional)
  @prop className - Additional CSS classes
-->
<script>
  import { formatDate } from '$lib/utils/format';
  import { toastStore } from '$lib/stores/toast.svelte.js';
  
  let { 
    productId, 
    reviews = [], 
    canReview = true, 
    className = '' 
  } = $props();
  
  // State management with Svelte 5 runes
  let showReviewForm = $state(false);
  let rating = $state(5);
  let comment = $state('');
  let reviewTitle = $state('');
  let sortBy = $state('newest');
  let filterRating = $state(0);
  let isSubmitting = $state(false);
  let expandedReviews = $state(new Set());
  
  // Computed values
  const averageRating = $derived(() => 
    reviews.length 
      ? reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length 
      : 0
  );
  
  const ratingDistribution = $derived(() => {
    const dist = { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 };
    reviews.forEach(review => {
      if (dist[review.rating] !== undefined) {
        dist[review.rating]++;
      }
    });
    return dist;
  });
  
  const filteredAndSortedReviews = $derived(() => {
    let filtered = filterRating > 0 
      ? reviews.filter(review => review.rating === filterRating)
      : reviews;
        
    return filtered.sort((a, b) => {
      switch (sortBy) {
        case 'oldest':
          return new Date(a.created_at) - new Date(b.created_at);
        case 'rating-high':
          return b.rating - a.rating;
        case 'rating-low':
          return a.rating - b.rating;
        case 'helpful':
          return (b.helpful_count || 0) - (a.helpful_count || 0);
        default: // newest
          return new Date(b.created_at) - new Date(a.created_at);
      }
    });
  });
  
  const formValid = $derived(() => 
    comment.trim().length >= 10 && reviewTitle.trim().length >= 3
  );
  
  // Functions
  function toggleExpandReview(reviewId) {
    const newExpanded = new Set(expandedReviews);
    if (newExpanded.has(reviewId)) {
      newExpanded.delete(reviewId);
    } else {
      newExpanded.add(reviewId);
    }
    expandedReviews = newExpanded;
  }
  
  function markHelpful(reviewId) {
    // Simulate API call
    toastStore.add({
      type: 'success',
      message: 'Thank you for your feedback!'
    });
  }
  
  async function submitReview() {
    if (!formValid || isSubmitting) return;
    
    isSubmitting = true;
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      toastStore.add({
        type: 'success',
        message: 'Review submitted successfully!'
      });
      
      // Reset form
      showReviewForm = false;
      rating = 5;
      comment = '';
      reviewTitle = '';
      
    } catch (error) {
      toastStore.add({
        type: 'error',
        message: 'Failed to submit review. Please try again.'
      });
    } finally {
      isSubmitting = false;
    }
  }
</script>

<div class="space-y-8 {className}">
  <!-- Reviews Summary Section -->
  <div class="glass-panel rounded-3xl p-8">
    <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
      <!-- Rating Overview -->
      <div class="flex-1">
        <h2 class="text-3xl font-display font-bold text-gray-900 dark:text-white mb-4">
          Customer Reviews
        </h2>
        
        <!-- Average Rating Display -->
        <div class="flex items-center gap-4 mb-6">
          <div class="text-5xl font-display font-bold text-primary-600 dark:text-primary-400">
            {averageRating().toFixed(1)}
          </div>
          <div class="flex-1">
            <div class="flex items-center gap-1 mb-2">
              {#each Array(5) as _, i}
                <svg 
                  class="w-6 h-6 {i < Math.round(averageRating()) ? 'text-yellow-400 fill-yellow-400' : 'text-gray-300 dark:text-gray-600'} 
                         transition-all duration-300 hover:scale-110" 
                  fill="currentColor" 
                  viewBox="0 0 20 20"
                  aria-hidden="true"
                >
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              {/each}
            </div>
            <div class="text-gray-600 dark:text-gray-400">
              Based on {reviews.length} review{reviews.length !== 1 ? 's' : ''}
            </div>
          </div>
        </div>
        
        <!-- Rating Distribution -->
        <div class="space-y-2">
          {#each [5, 4, 3, 2, 1] as stars}
            {@const count = ratingDistribution()[stars]}
            {@const percentage = reviews.length ? (count / reviews.length) * 100 : 0}
            <div class="flex items-center gap-3 text-sm">
              <span class="w-12 text-gray-600 dark:text-gray-400">{stars} stars</span>
              <div class="flex-1 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                <div 
                  class="h-full bg-gradient-to-r from-yellow-400 to-yellow-500 transition-all duration-500 ease-out"
                  style="width: {percentage}%"
                ></div>
              </div>
              <span class="w-8 text-gray-600 dark:text-gray-400 text-right">{count}</span>
            </div>
          {/each}
        </div>
      </div>
      
      <!-- Write Review Button -->
      {#if canReview}
        <div class="lg:flex-shrink-0">
          <button
            onclick={() => showReviewForm = !showReviewForm}
            class="btn-primary w-full lg:w-auto group relative overflow-hidden"
            aria-expanded={showReviewForm}
          >
            <span class="relative z-10 flex items-center gap-2">
              <svg class="w-5 h-5 transition-transform group-hover:scale-110" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
              </svg>
              {showReviewForm ? 'Cancel Review' : 'Write a Review'}
            </span>
            <div class="absolute inset-0 bg-gradient-to-r from-primary-600 to-primary-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          </button>
        </div>
      {/if}
    </div>
  </div>
  
  <!-- Review Form -->
  {#if showReviewForm && canReview}
    <div class="glass-panel rounded-3xl p-8 animate-slide-down">
      <h3 class="text-2xl font-display font-semibold text-gray-900 dark:text-white mb-6">
        Write Your Review
      </h3>
      
      <form onsubmit={(e) => { e.preventDefault(); submitReview(); }} class="space-y-6">
        <!-- Rating Selection -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
            Your Rating *
          </label>
          <div class="flex items-center gap-2">
            {#each Array(5) as _, i}
              <button
                type="button"
                onclick={() => rating = i + 1}
                class="group transition-transform hover:scale-110 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 rounded"
                aria-label="Rate {i + 1} out of 5 stars"
              >
                <svg 
                  class="w-8 h-8 {i < rating ? 'text-yellow-400 fill-yellow-400' : 'text-gray-300 dark:text-gray-600 hover:text-yellow-300'} 
                         transition-colors duration-200" 
                  fill="currentColor" 
                  viewBox="0 0 20 20"
                >
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              </button>
            {/each}
            <span class="ml-2 text-sm text-gray-600 dark:text-gray-400">
              ({rating} star{rating !== 1 ? 's' : ''})
            </span>
          </div>
        </div>
        
        <!-- Review Title -->
        <div>
          <label for="reviewTitle" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Review Title *
          </label>
          <input
            id="reviewTitle"
            type="text"
            bind:value={reviewTitle}
            placeholder="Summarize your experience"
            class="input-primary w-full"
            required
            minlength="3"
            maxlength="100"
          />
          <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">
            {reviewTitle.length}/100 characters (min. 3)
          </div>
        </div>
        
        <!-- Review Comment -->
        <div>
          <label for="reviewComment" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Your Review *
          </label>
          <textarea
            id="reviewComment"
            bind:value={comment}
            placeholder="Share your experience with this product..."
            rows="5"
            class="input-primary w-full resize-none"
            required
            minlength="10"
            maxlength="1000"
          ></textarea>
          <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">
            {comment.length}/1000 characters (min. 10)
          </div>
        </div>
        
        <!-- Form Actions -->
        <div class="flex flex-col sm:flex-row gap-3 justify-end">
          <button
            type="button"
            onclick={() => showReviewForm = false}
            class="btn-secondary order-2 sm:order-1"
            disabled={isSubmitting}
          >
            Cancel
          </button>
          <button
            type="submit"
            class="btn-primary order-1 sm:order-2 group relative overflow-hidden"
            disabled={!formValid || isSubmitting}
          >
            <span class="relative z-10 flex items-center gap-2">
              {#if isSubmitting}
                <svg class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Submitting...
              {:else}
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
                Submit Review
              {/if}
            </span>
            <div class="absolute inset-0 bg-gradient-to-r from-primary-600 to-primary-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          </button>
        </div>
      </form>
    </div>
  {/if}
  
  <!-- Filters and Sorting -->
  {#if reviews.length > 0}
    <div class="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
      <!-- Filter by Rating -->
      <div class="flex items-center gap-3">
        <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Filter:</span>
        <select 
          bind:value={filterRating}
          class="input-primary py-2 px-3 min-w-0 text-sm"
          aria-label="Filter reviews by rating"
        >
          <option value={0}>All Reviews</option>
          <option value={5}>5 Stars</option>
          <option value={4}>4 Stars</option>
          <option value={3}>3 Stars</option>
          <option value={2}>2 Stars</option>
          <option value={1}>1 Star</option>
        </select>
      </div>
      
      <!-- Sort Options -->
      <div class="flex items-center gap-3">
        <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Sort:</span>
        <select 
          bind:value={sortBy}
          class="input-primary py-2 px-3 min-w-0 text-sm"
          aria-label="Sort reviews"
        >
          <option value="newest">Newest First</option>
          <option value="oldest">Oldest First</option>
          <option value="rating-high">Highest Rated</option>
          <option value="rating-low">Lowest Rated</option>
          <option value="helpful">Most Helpful</option>
        </select>
      </div>
    </div>
  {/if}
  
  <!-- Reviews List -->
  {#if filteredAndSortedReviews().length > 0}
    <div class="space-y-6">
      {#each filteredAndSortedReviews() as review (review.id)}
        {@const isExpanded = expandedReviews.has(review.id)}
        {@const shouldShowExpand = review.comment && review.comment.length > 200}
        
        <article 
          class="glass-panel rounded-2xl p-6 space-y-4 transition-all duration-300 hover:shadow-lg hover:shadow-primary-500/10"
        >
          <!-- Review Header -->
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-2">
                <!-- User Avatar -->
                <div class="w-10 h-10 rounded-full bg-gradient-to-br from-primary-500 to-primary-600 flex items-center justify-center text-white font-semibold text-sm">
                  {review.user_name ? review.user_name.charAt(0).toUpperCase() : 'A'}
                </div>
                
                <div class="flex-1">
                  <div class="flex items-center gap-2 mb-1">
                    <span class="font-semibold text-gray-900 dark:text-white">
                      {review.user_name || 'Anonymous'}
                    </span>
                    {#if review.verified_purchase}
                      <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400">
                        <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                        </svg>
                        Verified Purchase
                      </span>
                    {/if}
                  </div>
                  
                  <!-- Rating -->
                  <div class="flex items-center gap-2">
                    <div class="flex">
                      {#each Array(5) as _, i}
                        <svg 
                          class="w-4 h-4 {i < review.rating ? 'text-yellow-400 fill-yellow-400' : 'text-gray-300 dark:text-gray-600'}" 
                          fill="currentColor" 
                          viewBox="0 0 20 20"
                          aria-hidden="true"
                        >
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                        </svg>
                      {/each}
                    </div>
                    <time class="text-sm text-gray-500 dark:text-gray-400">
                      {formatDate(review.created_at)}
                    </time>
                  </div>
                </div>
              </div>
              
              <!-- Review Title -->
              {#if review.title}
                <h4 class="font-semibold text-gray-900 dark:text-white mb-2">
                  {review.title}
                </h4>
              {/if}
            </div>
          </div>
          
          <!-- Review Content -->
          <div class="prose prose-sm max-w-none dark:prose-invert">
            <p class="text-gray-700 dark:text-gray-300 leading-relaxed">
              {#if shouldShowExpand && !isExpanded}
                {review.comment.substring(0, 200)}...
              {:else}
                {review.comment}
              {/if}
            </p>
            
            {#if shouldShowExpand}
              <button
                onclick={() => toggleExpandReview(review.id)}
                class="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 text-sm font-medium transition-colors mt-2"
              >
                {isExpanded ? 'Show less' : 'Read more'}
              </button>
            {/if}
          </div>
          
          <!-- Review Actions -->
          <div class="flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-700">
            <button
              onclick={() => markHelpful(review.id)}
              class="flex items-center gap-2 text-sm text-gray-500 hover:text-primary-600 dark:hover:text-primary-400 transition-colors group"
            >
              <svg class="w-4 h-4 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
              </svg>
              Helpful ({review.helpful_count || 0})
            </button>
            
            {#if review.images && review.images.length > 0}
              <div class="flex items-center gap-2">
                <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span class="text-sm text-gray-500">{review.images.length} image{review.images.length !== 1 ? 's' : ''}</span>
              </div>
            {/if}
          </div>
        </article>
      {/each}
    </div>
  {:else if filterRating > 0}
    <div class="text-center py-12">
      <div class="glass-panel rounded-3xl p-8 max-w-md mx-auto">
        <svg class="w-16 h-16 mx-auto text-gray-400 dark:text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
          No reviews found
        </h3>
        <p class="text-gray-600 dark:text-gray-400">
          No reviews match your current filter. Try adjusting the rating filter.
        </p>
      </div>
    </div>
  {:else}
    <div class="text-center py-12">
      <div class="glass-panel rounded-3xl p-8 max-w-md mx-auto">
        <svg class="w-16 h-16 mx-auto text-gray-400 dark:text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
        </svg>
        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
          No reviews yet
        </h3>
        <p class="text-gray-600 dark:text-gray-400 mb-4">
          Be the first to share your thoughts about this product.
        </p>
        {#if canReview}
          <button
            onclick={() => showReviewForm = true}
            class="btn-primary"
          >
            Write the first review
          </button>
        {/if}
      </div>
    </div>
  {/if}
</div>