<!-- src/routes/+layout.svelte -->
<script>
	import '../app.css';
	import { setAuthStore } from '$lib/stores/auth.svelte.js';
	import { setCartStore } from '$lib/stores/cart.svelte.js';
	import { setThemeStore } from '$lib/stores/theme.svelte.js';
	import { setWishlistStore } from '$lib/stores/wishlist.svelte.js';
	import Header from '$lib/components/layout/Header.svelte';
	import CartDrawer from '$lib/components/cart/CartDrawer.svelte';
	import ToastContainer from '$lib/components/ui/ToastContainer.svelte';
	
	setAuthStore();
	setCartStore();
	setThemeStore();
	setWishlistStore();
	
	let { children } = $props();
  </script>
  
  <div class="min-h-screen bg-gray-50 dark:bg-dark-50">
	<Header />
	
	<main>
	  {@render children()}
	</main>
	
	<CartDrawer />
	<ToastContainer />
  </div>