<!--
  @component LoginPage
  Premium login page with social authentication and advanced security features.
  Features form validation, password reset, and seamless redirect handling.
-->
<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { getAuthStore } from '$lib/stores/auth.svelte.js';
  import { toastStore } from '$lib/stores/toast.svelte.js';
  import Button from '$lib/components/ui/Button.svelte';
  import Input from '$lib/components/ui/Input.svelte';
  import Card from '$lib/components/ui/Card.svelte';
  import Spinner from '$lib/components/ui/Spinner.svelte';
  
  // Store access
  const authStore = getAuthStore();
  
  // Reactive state using Svelte 5 runes
  let mounted = $state(false);
  let isLoading = $state(false);
  let showPassword = $state(false);
  let rememberMe = $state(true);
  
  // Form data
  let formData = $state({
    email: '',
    password: ''
  });
  
  // Form validation
  let errors = $state({
    email: '',
    password: '',
    general: ''
  });
  
  // Derived values
  const isAuthenticated = $derived(authStore?.isAuthenticated || false);
  const redirectUrl = $derived(() => {
    const redirect = $page.url.searchParams.get('redirect');
    return redirect ? decodeURIComponent(redirect) : '/';
  });
  
  // Form validation functions
  function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email) return 'Email is required';
    if (!emailRegex.test(email)) return 'Please enter a valid email address';
    return '';
  }
  
  function validatePassword(password) {
    if (!password) return 'Password is required';
    if (password.length < 6) return 'Password must be at least 6 characters';
    return '';
  }
  
  function validateForm() {
    const emailError = validateEmail(formData.email);
    const passwordError = validatePassword(formData.password);
    
    errors = {
      email: emailError,
      password: passwordError,
      general: ''
    };
    
    return !emailError && !passwordError;
  }
  
  // Handle form submission
  async function handleSubmit(event) {
    event.preventDefault();
    
    if (isLoading) return;
    
    // Clear previous errors
    errors.general = '';
    
    // Validate form
    if (!validateForm()) {
      return;
    }
    
    isLoading = true;
    
    try {
      await authStore.login(formData.email, formData.password);
      
      toastStore.add({
        type: 'success',
        message: 'Welcome back! You have been successfully signed in.'
      });
      
      // Redirect to intended page or home
      goto(redirectUrl);
      
    } catch (error) {
      console.error('Login failed:', error);
      
      // Handle different error types
      if (error.message?.includes('credentials')) {
        errors.general = 'Invalid email or password. Please try again.';
      } else if (error.message?.includes('verification')) {
        errors.general = 'Please verify your email address before signing in.';
      } else if (error.message?.includes('blocked')) {
        errors.general = 'Your account has been temporarily blocked. Please contact support.';
      } else {
        errors.general = 'Sign in failed. Please check your connection and try again.';
      }
      
      toastStore.add({
        type: 'error',
        message: errors.general
      });
      
    } finally {
      isLoading = false;
    }
  }
  
  // Social authentication handlers
  async function handleSocialLogin(provider) {
    console.log(`Social login with ${provider} - Integration needed`);
    toastStore.add({
      type: 'info',
      message: `${provider} sign in will be available soon`
    });
  }
  
  // Password reset
  function handleForgotPassword() {
    goto('/auth/reset-password' + (formData.email ? `?email=${encodeURIComponent(formData.email)}` : ''));
  }
  
  // Navigate to register
  function goToRegister() {
    const currentRedirect = $page.url.searchParams.get('redirect');
    const registerUrl = '/auth/register' + (currentRedirect ? `?redirect=${currentRedirect}` : '');
    goto(registerUrl);
  }
  
  // Real-time validation
  function handleEmailInput() {
    if (errors.email && formData.email) {
      errors.email = validateEmail(formData.email);
    }
  }
  
  function handlePasswordInput() {
    if (errors.password && formData.password) {
      errors.password = validatePassword(formData.password);
    }
  }
  
  // Lifecycle
  onMount(() => {
    mounted = true;
    
    // Redirect if already authenticated
    if (isAuthenticated) {
      goto(redirectUrl);
      return;
    }
    
    // Focus email input
    const emailInput = document.querySelector('input[type="email"]');
    emailInput?.focus();
  });
</script>

<svelte:head>
  <title>Sign In - Premium Store</title>
  <meta name="description" content="Sign in to your account to access exclusive features and track your orders" />
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100 dark:from-dark-50 dark:via-dark-100 dark:to-dark-200 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
  <div class="sm:mx-auto sm:w-full sm:max-w-md">
    <!-- Logo and Header -->
    <div class="text-center mb-8">
      <a href="/" class="inline-flex items-center space-x-2 group">
        <div class="w-12 h-12 bg-gradient-to-r from-primary-600 to-primary-700 rounded-xl flex items-center justify-center group-hover:scale-105 transition-transform">
          <svg class="w-7 h-7 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 2L3 7v11a1 1 0 001 1h3a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1h3a1 1 0 001-1V7l-7-5z" clip-rule="evenodd" />
          </svg>
        </div>
        <span class="text-2xl font-display font-bold gradient-text">Premium Store</span>
      </a>
    </div>
    
    <Card class="glass shadow-premium hover-lift">
      <div class="p-8">
        <!-- Header -->
        <div class="text-center mb-8">
          <h1 class="text-3xl font-display font-bold text-gray-900 dark:text-white">
            Welcome back
          </h1>
          <p class="mt-2 text-gray-600 dark:text-gray-400">
            Sign in to your account to continue
          </p>
        </div>
        
        <!-- Social Login -->
        <div class="mb-6">
          <div class="grid grid-cols-2 gap-3">
            <Button
              variant="ghost"
              onclick={() => handleSocialLogin('Google')}
              disabled={isLoading}
              class="hover-scale"
            >
              <svg class="w-5 h-5 mr-2" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              Google
            </Button>
            <Button
              variant="ghost"
              onclick={() => handleSocialLogin('Facebook')}
              disabled={isLoading}
              class="hover-scale"
            >
              <svg class="w-5 h-5 mr-2" fill="#1877F2" viewBox="0 0 24 24">
                <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
              </svg>
              Facebook
            </Button>
          </div>
          
          <div class="mt-6">
            <div class="relative">
              <div class="absolute inset-0 flex items-center">
                <div class="w-full border-t border-gray-300 dark:border-gray-600" />
              </div>
              <div class="relative flex justify-center text-sm">
                <span class="px-2 bg-white dark:bg-dark-100 text-gray-500 dark:text-gray-400">
                  Or continue with email
                </span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Login Form -->
        <form onsubmit={handleSubmit} class="space-y-6">
          <!-- General Error -->
          {#if errors.general}
            <div class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl p-4">
              <div class="flex">
                <svg class="w-5 h-5 text-red-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
                <p class="text-sm text-red-600 dark:text-red-400">{errors.general}</p>
              </div>
            </div>
          {/if}
          
          <!-- Email -->
          <div>
            <Input
              type="email"
              label="Email address"
              bind:value={formData.email}
              error={errors.email}
              placeholder="Enter your email"
              required
              disabled={isLoading}
              oninput={handleEmailInput}
              icon="mail"
            />
          </div>
          
          <!-- Password -->
          <div>
            <Input
              type={showPassword ? 'text' : 'password'}
              label="Password"
              bind:value={formData.password}
              error={errors.password}
              placeholder="Enter your password"
              required
              disabled={isLoading}
              oninput={handlePasswordInput}
            >
              <button
                type="button"
                slot="suffix"
                onclick={() => showPassword = !showPassword}
                class="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                aria-label={showPassword ? 'Hide password' : 'Show password'}
              >
                {#if showPassword}
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L8.464 8.464l1.414-1.414M14.12 14.12l1.415 1.415" />
                  </svg>
                {:else}
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                {/if}
              </button>
            </Input>
          </div>
          
          <!-- Options Row -->
          <div class="flex items-center justify-between">
            <label class="flex items-center">
              <input
                type="checkbox"
                bind:checked={rememberMe}
                disabled={isLoading}
                class="w-4 h-4 text-primary-600 border-gray-300 dark:border-gray-600 rounded focus:ring-primary-500"
              />
              <span class="ml-2 text-sm text-gray-600 dark:text-gray-400">Remember me</span>
            </label>
            
            <button
              type="button"
              onclick={handleForgotPassword}
              disabled={isLoading}
              class="text-sm text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-medium"
            >
              Forgot password?
            </button>
          </div>
          
          <!-- Submit Button -->
          <Button
            type="submit"
            variant="primary"
            size="lg"
            fullWidth
            loading={isLoading}
            disabled={isLoading}
            class="hover-lift magnetic"
          >
            {#if isLoading}
              Signing in...
            {:else}
              Sign in
            {/if}
          </Button>
        </form>
        
        <!-- Register Link -->
        <div class="mt-8 text-center">
          <p class="text-sm text-gray-600 dark:text-gray-400">
            Don't have an account?
            <button
              onclick={goToRegister}
              disabled={isLoading}
              class="font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 ml-1"
            >
              Create one now
            </button>
          </p>
        </div>
      </div>
    </Card>
    
    <!-- Security Notice -->
    <div class="mt-8 text-center">
      <p class="text-xs text-gray-500 dark:text-gray-400">
        Protected by 256-bit SSL encryption. Your data is safe with us.
      </p>
    </div>
  </div>
</div>

<style>
  /* Custom focus styles for better accessibility */
  input:focus-visible {
    outline: 2px solid var(--color-primary-500);
    outline-offset: 2px;
  }
</style>