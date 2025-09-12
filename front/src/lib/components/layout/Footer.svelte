<!--
  @component Footer
  Premium e-commerce footer with links, newsletter signup, and branding.
  Features multi-column layout, social links, and trust indicators.
  
  @prop showNewsletter - Whether to display newsletter signup
  @prop showSocial - Whether to display social media links
  @prop showPayment - Whether to display payment methods
  @prop showTrust - Whether to display trust indicators
-->
<script>
  import { createEventDispatcher } from 'svelte';
  
  const dispatch = createEventDispatcher();

  /** @type {boolean} */
  export let showNewsletter = true;
  
  /** @type {boolean} */
  export let showSocial = true;
  
  /** @type {boolean} */
  export let showPayment = true;
  
  /** @type {boolean} */
  export let showTrust = true;

  // Reactive state using Svelte 5 runes
  let newsletterEmail = $state('');
  let isSubscribing = $state(false);
  let subscriptionStatus = $state(''); // 'success', 'error', or ''

  // Footer navigation sections
  const navigationSections = $state([
    {
      title: 'Shop',
      links: [
        { label: 'All Products', href: '/products' },
        { label: 'New Arrivals', href: '/products?filter=new' },
        { label: 'Best Sellers', href: '/products?filter=bestsellers' },
        { label: 'On Sale', href: '/products?filter=sale' },
        { label: 'Categories', href: '/categories' }
      ]
    },
    {
      title: 'Customer Service',
      links: [
        { label: 'Help Center', href: '/help' },
        { label: 'Contact Us', href: '/contact' },
        { label: 'Shipping Info', href: '/shipping' },
        { label: 'Returns', href: '/returns' },
        { label: 'Size Guide', href: '/size-guide' }
      ]
    },
    {
      title: 'Account',
      links: [
        { label: 'My Account', href: '/account' },
        { label: 'Order History', href: '/account/orders' },
        { label: 'Wishlist', href: '/account/wishlist' },
        { label: 'Track Order', href: '/track' },
        { label: 'Login', href: '/auth/login' }
      ]
    },
    {
      title: 'Company',
      links: [
        { label: 'About Us', href: '/about' },
        { label: 'Careers', href: '/careers' },
        { label: 'Press', href: '/press' },
        { label: 'Blog', href: '/blog' },
        { label: 'Sustainability', href: '/sustainability' }
      ]
    }
  ]);

  // Social media links
  const socialLinks = $state([
    { name: 'Facebook', href: 'https://facebook.com', icon: 'facebook' },
    { name: 'Instagram', href: 'https://instagram.com', icon: 'instagram' },
    { name: 'Twitter', href: 'https://twitter.com', icon: 'twitter' },
    { name: 'YouTube', href: 'https://youtube.com', icon: 'youtube' },
    { name: 'TikTok', href: 'https://tiktok.com', icon: 'tiktok' }
  ]);

  // Payment methods
  const paymentMethods = $state([
    'Visa', 'Mastercard', 'American Express', 'PayPal', 'Apple Pay', 'Google Pay'
  ]);

  // Legal links
  const legalLinks = $state([
    { label: 'Privacy Policy', href: '/privacy' },
    { label: 'Terms of Service', href: '/terms' },
    { label: 'Cookie Policy', href: '/cookies' },
    { label: 'Accessibility', href: '/accessibility' }
  ]);

  // Newsletter subscription
  async function handleNewsletterSubmit() {
    if (!newsletterEmail.trim() || isSubscribing) return;

    isSubscribing = true;
    subscriptionStatus = '';

    try {
      // Mock API call - replace with actual newsletter service
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      dispatch('newsletterSubscribe', { email: newsletterEmail.trim() });
      subscriptionStatus = 'success';
      newsletterEmail = '';
      
      // Reset status after 5 seconds
      setTimeout(() => {
        subscriptionStatus = '';
      }, 5000);
    } catch (error) {
      subscriptionStatus = 'error';
      console.error('Newsletter subscription failed:', error);
    } finally {
      isSubscribing = false;
    }
  }

  function handleNewsletterKeydown(event) {
    if (event.key === 'Enter') {
      handleNewsletterSubmit();
    }
  }

  // Social media click handler
  function handleSocialClick(social) {
    dispatch('socialClick', { platform: social.name, url: social.href });
  }

  // Current year for copyright
  const currentYear = new Date().getFullYear();
</script>

<footer class="bg-gradient-to-b from-white/50 to-gray-50/80 dark:from-dark-100/50 dark:to-dark-200/80 border-t border-white/20 dark:border-dark-200/20">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    
    <!-- Main Footer Content -->
    <div class="py-12 lg:py-16">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-8 lg:gap-12">
        
        <!-- Brand Section -->
        <div class="lg:col-span-2">
          <!-- Logo -->
          <div class="flex items-center space-x-2 mb-4">
            <div class="w-10 h-10 bg-gradient-primary rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                <path fill-rule="evenodd" d="M10 2L3 7v11a1 1 0 001 1h3a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1h3a1 1 0 001-1V7l-7-5z" clip-rule="evenodd" />
              </svg>
            </div>
            <span class="text-2xl font-bold bg-gradient-primary bg-clip-text text-transparent">
              Store
            </span>
          </div>
          
          <!-- Description -->
          <p class="text-gray-600 dark:text-dark-600 mb-6 max-w-md leading-relaxed">
            Discover premium products crafted with care. We're committed to quality, sustainability, and exceptional customer experience.
          </p>
          
          <!-- Newsletter Signup -->
          {#if showNewsletter}
            <div class="mb-6">
              <h3 class="text-sm font-semibold text-gray-900 dark:text-dark-900 mb-2">
                Stay Updated
              </h3>
              <p class="text-sm text-gray-600 dark:text-dark-600 mb-3">
                Get the latest news and exclusive offers.
              </p>
              
              <div class="flex flex-col sm:flex-row gap-2 max-w-md">
                <div class="flex-1 relative">
                  <input
                    type="email"
                    placeholder="Enter your email"
                    bind:value={newsletterEmail}
                    on:keydown={handleNewsletterKeydown}
                    disabled={isSubscribing}
                    class="w-full px-4 py-2.5 glass rounded-lg border border-white/20 dark:border-dark-200/20 text-gray-900 dark:text-dark-900 placeholder-gray-500 dark:placeholder-dark-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200 disabled:opacity-50"
                  />
                </div>
                <button
                  type="button"
                  on:click={handleNewsletterSubmit}
                  disabled={!newsletterEmail.trim() || isSubscribing}
                  class="px-6 py-2.5 bg-gradient-primary text-white rounded-lg font-medium hover:shadow-lg hover:shadow-primary-500/25 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isSubscribing ? 'Subscribing...' : 'Subscribe'}
                </button>
              </div>
              
              <!-- Subscription Status -->
              {#if subscriptionStatus === 'success'}
                <p class="text-sm text-success-600 dark:text-success-400 mt-2 flex items-center">
                  <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  Successfully subscribed!
                </p>
              {:else if subscriptionStatus === 'error'}
                <p class="text-sm text-error-600 dark:text-error-400 mt-2 flex items-center">
                  <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L10 10.586l2.293-2.293a1 1 0 111.414 1.414L11.414 12l2.293 2.293a1 1 0 01-1.414 1.414L10 13.414l-2.293 2.293a1 1 0 01-1.414-1.414L9.586 12 7.293 9.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                  Subscription failed. Please try again.
                </p>
              {/if}
            </div>
          {/if}
          
          <!-- Social Links -->
          {#if showSocial}
            <div>
              <h3 class="text-sm font-semibold text-gray-900 dark:text-dark-900 mb-3">
                Follow Us
              </h3>
              <div class="flex space-x-3">
                {#each socialLinks as social}
                  <button
                    type="button"
                    on:click={() => handleSocialClick(social)}
                    class="w-10 h-10 rounded-lg glass border border-white/20 dark:border-dark-200/20 flex items-center justify-center text-gray-600 dark:text-dark-600 hover:text-primary-600 dark:hover:text-primary-400 hover:border-primary-300 dark:hover:border-primary-600 transition-all duration-200"
                    aria-label={`Follow us on ${social.name}`}
                  >
                    {#if social.icon === 'facebook'}
                      <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                        <path fill-rule="evenodd" d="M20 10c0-5.523-4.477-10-10-10S0 4.477 0 10c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V10h2.54V7.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V10h2.773l-.443 2.89h-2.33v6.988C16.343 19.128 20 14.991 20 10z" clip-rule="evenodd" />
                      </svg>
                    {:else if social.icon === 'instagram'}
                      <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                        <path fill-rule="evenodd" d="M10 0C4.477 0 0 4.484 0 10.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0110 4.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.203 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.942.359.31.678.921.678 1.856 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0020 10.017C20 4.484 15.522 0 10 0z" clip-rule="evenodd" />
                      </svg>
                    {:else if social.icon === 'twitter'}
                      <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                        <path d="M6.29 18.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0020 3.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.073 4.073 0 01.8 7.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 010 16.407a11.616 11.616 0 006.29 1.84" />
                      </svg>
                    {:else if social.icon === 'youtube'}
                      <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                        <path fill-rule="evenodd" d="M2.166 4.999A11.854 11.854 0 0010 1.944 11.854 11.854 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                      </svg>
                    {:else if social.icon === 'tiktok'}
                      <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                        <path d="M9.197 6.963v10.93H6.581V9.97c-1.054.069-1.869.267-2.446.594v-2.49c.577-.327 1.392-.525 2.446-.594V4.5h2.616v2.463z" />
                      </svg>
                    {/if}
                  </button>
                {/each}
              </div>
            </div>
          {/if}
        </div>

        <!-- Navigation Sections -->
        {#each navigationSections as section}
          <div>
            <h3 class="text-sm font-semibold text-gray-900 dark:text-dark-900 mb-4">
              {section.title}
            </h3>
            <ul class="space-y-3">
              {#each section.links as link}
                <li>
                  <a
                    href={link.href}
                    class="text-sm text-gray-600 dark:text-dark-600 hover:text-gray-900 dark:hover:text-dark-900 transition-colors duration-150"
                  >
                    {link.label}
                  </a>
                </li>
              {/each}
            </ul>
          </div>
        {/each}
      </div>
    </div>
    
    <!-- Bottom Section -->
    <div class="border-t border-white/20 dark:border-dark-200/20 py-8">
      <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-6 lg:space-y-0">
        
        <!-- Copyright -->
        <div class="text-sm text-gray-600 dark:text-dark-600">
          <p>&copy; {currentYear} Store. All rights reserved.</p>
        </div>
        
        <!-- Legal Links -->
        <div class="flex flex-wrap gap-x-6 gap-y-2">
          {#each legalLinks as link}
            <a
              href={link.href}
              class="text-sm text-gray-600 dark:text-dark-600 hover:text-gray-900 dark:hover:text-dark-900 transition-colors duration-150"
            >
              {link.label}
            </a>
          {/each}
        </div>
        
        <!-- Payment Methods & Trust Indicators -->
        {#if showPayment || showTrust}
          <div class="flex items-center space-x-6">
            
            <!-- Payment Methods -->
            {#if showPayment}
              <div class="flex items-center space-x-2">
                <span class="text-xs text-gray-500 dark:text-dark-500">Payment:</span>
                <div class="flex items-center space-x-1">
                  {#each paymentMethods.slice(0, 4) as method}
                    <div class="w-8 h-5 bg-gray-200 dark:bg-dark-300 rounded flex items-center justify-center">
                      <span class="text-xs font-medium text-gray-600 dark:text-dark-600">
                        {method === 'American Express' ? 'AE' : method.slice(0, 2)}
                      </span>
                    </div>
                  {/each}
                  <span class="text-xs text-gray-500 dark:text-dark-500">+2</span>
                </div>
              </div>
            {/if}
            
            <!-- Trust Indicators -->
            {#if showTrust}
              <div class="flex items-center space-x-2">
                <!-- SSL Badge -->
                <div class="flex items-center space-x-1">
                  <svg class="w-4 h-4 text-success-600 dark:text-success-400" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                    <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
                  </svg>
                  <span class="text-xs text-gray-600 dark:text-dark-600">SSL Secure</span>
                </div>
              </div>
            {/if}
          </div>
        {/if}
      </div>
    </div>
  </div>
</footer>

<style>
  /* Enhance glass effect */
  .glass {
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
  }
  
  /* High contrast mode adjustments */
  @media (prefers-contrast: high) {
    .glass {
      border-width: 2px !important;
      backdrop-filter: none !important;
      background: var(--color-white) !important;
    }
    
    :global(.dark) .glass {
      background: var(--color-dark-100) !important;
    }
  }

  /* Focus visible enhancements */
  :global(a:focus-visible, button:focus-visible) {
    outline: 2px solid var(--color-primary-500);
    outline-offset: 2px;
  }
</style>