# SvelteKit Online Store Frontend Structure

online-store-frontend/
├── src/
│   ├── lib/
│   │   ├── api/
│   │   │   ├── client.js
│   │   │   ├── auth.js
│   │   │   ├── products.js
│   │   │   ├── cart.js
│   │   │   ├── orders.js
│   │   │   └── reviews.js
│   │   ├── stores/
│   │   │   ├── auth.svelte.js
│   │   │   ├── cart.svelte.js
│   │   │   ├── wishlist.svelte.js
│   │   │   └── toast.svelte.js
│   │   ├── utils/
│   │   │   ├── format.js
│   │   │   ├── validators.js
│   │   │   └── constants.js
│   │   └── components/
│   │       ├── layout/
│   │       │   ├── Header.svelte
│   │       │   ├── Footer.svelte
│   │       │   ├── Navigation.svelte
│   │       │   └── MobileMenu.svelte
│   │       ├── product/
│   │       │   ├── ProductCard.svelte
│   │       │   ├── ProductGrid.svelte
│   │       │   ├── ProductDetail.svelte
│   │       │   ├── ProductImages.svelte
│   │       │   └── ProductReviews.svelte
│   │       ├── cart/
│   │       │   ├── CartItem.svelte
│   │       │   ├── CartSummary.svelte
│   │       │   ├── CartDrawer.svelte
│   │       │   └── CartIcon.svelte
│   │       ├── ui/
│   │       │   ├── Button.svelte
│   │       │   ├── Input.svelte
│   │       │   ├── Card.svelte
│   │       │   ├── Modal.svelte
│   │       │   ├── Toast.svelte
│   │       │   ├── Spinner.svelte
│   │       │   ├── Rating.svelte
│   │       │   └── Badge.svelte
│   │       └── checkout/
│   │           ├── CheckoutForm.svelte
│   │           └── OrderSummary.svelte
│   ├── routes/
│   │   ├── +layout.svelte
│   │   ├── +page.svelte
│   │   ├── products/
│   │   │   ├── +page.svelte
│   │   │   └── [slug]/
│   │   │       └── +page.svelte
│   │   ├── cart/
│   │   │   └── +page.svelte
│   │   ├── checkout/
│   │   │   └── +page.svelte
│   │   ├── auth/
│   │   │   ├── login/
│   │   │   │   └── +page.svelte
│   │   │   └── register/
│   │   │       └── +page.svelte
│   │   ├── account/
│   │   │   ├── +page.svelte
│   │   │   ├── orders/
│   │   │   │   └── +page.svelte
│   │   │   └── wishlist/
│   │   │       └── +page.svelte
│   │   └── api/
│   │       └── [...path]/
│   │           └── +server.js
│   ├── app.html
│   ├── app.css
│   └── hooks.client.js
├── static/
│   └── favicon.png
├── package.json
├── vite.config.js
├── svelte.config.js
└── .env.example