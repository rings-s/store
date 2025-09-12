<!--
  @component RegisterPage
  Premium registration page with comprehensive form validation and user experience.
  Features password strength indicator, email verification, and social registration.
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
  import Badge from '$lib/components/ui/Badge.svelte';
  
  // Store access
  const authStore = getAuthStore();
  
  // Reactive state using Svelte 5 runes
  let mounted = $state(false);
  let isLoading = $state(false);
  let showPassword = $state(false);
  let showConfirmPassword = $state(false);
  let agreedToTerms = $state(false);
  let currentStep = $state(1); // 1: form, 2: verification
  
  // Form data
  let formData = $state({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  
  // Form validation
  let errors = $state({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    confirmPassword: '',
    terms: '',
    general: ''
  });
  
  // Password strength
  let passwordStrength = $state({
    score: 0,
    feedback: []
  });
  
  // Derived values
  const isAuthenticated = $derived(authStore?.isAuthenticated || false);
  const redirectUrl = $derived(() => {
    const redirect = $page.url.searchParams.get('redirect');
    return redirect ? decodeURIComponent(redirect) : '/';
  });
  
  const passwordStrengthColor = $derived(() => {
    if (passwordStrength.score <= 1) return 'text-red-500';
    if (passwordStrength.score <= 2) return 'text-yellow-500';
    if (passwordStrength.score <= 3) return 'text-blue-500';
    return 'text-green-500';
  });
  
  const passwordStrengthLabel = $derived(() => {
    if (passwordStrength.score <= 1) return 'Weak';
    if (passwordStrength.score <= 2) return 'Fair';
    if (passwordStrength.score <= 3) return 'Good';
    return 'Strong';
  });
  
  // Validation functions
  function validateName(name, field) {
    if (!name) return `${field} is required`;
    if (name.length < 2) return `${field} must be at least 2 characters`;
    if (name.length > 50) return `${field} must be less than 50 characters`;
    if (!/^[a-zA-Z\s'-]+$/.test(name)) return `${field} contains invalid characters`;
    return '';
  }
  
  function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email) return 'Email is required';
    if (!emailRegex.test(email)) return 'Please enter a valid email address';
    if (email.length > 254) return 'Email address is too long';
    return '';
  }
  
  function validatePassword(password) {
    if (!password) return 'Password is required';
    if (password.length < 8) return 'Password must be at least 8 characters';
    if (password.length > 128) return 'Password is too long';
    
    const hasLower = /[a-z]/.test(password);
    const hasUpper = /[A-Z]/.test(password);
    const hasNumber = /\d/.test(password);
    const hasSpecial = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password);
    
    if (!hasLower) return 'Password must contain at least one lowercase letter';
    if (!hasUpper) return 'Password must contain at least one uppercase letter';
    if (!hasNumber) return 'Password must contain at least one number';
    if (!hasSpecial) return 'Password must contain at least one special character';
    
    return '';
  }
  
  function validateConfirmPassword(password, confirmPassword) {
    if (!confirmPassword) return 'Please confirm your password';
    if (password !== confirmPassword) return 'Passwords do not match';
    return '';
  }
  
  function calculatePasswordStrength(password) {
    let score = 0;
    const feedback = [];
    
    if (password.length >= 8) score++;
    else feedback.push('Use at least 8 characters');
    
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) score++;
    else feedback.push('Mix uppercase and lowercase letters');
    
    if (/\d/.test(password)) score++;
    else feedback.push('Include numbers');
    
    if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) score++;
    else feedback.push('Include special characters');
    
    if (password.length >= 12) score++;
    else if (password.length >= 8) feedback.push('Consider using 12+ characters');
    
    passwordStrength = { score, feedback };
  }
  
  function validateForm() {
    const firstNameError = validateName(formData.first_name, 'First name');
    const lastNameError = validateName(formData.last_name, 'Last name');
    const emailError = validateEmail(formData.email);
    const passwordError = validatePassword(formData.password);
    const confirmPasswordError = validateConfirmPassword(formData.password, formData.confirmPassword);
    const termsError = !agreedToTerms ? 'You must agree to the terms and conditions' : '';
    
    errors = {
      first_name: firstNameError,
      last_name: lastNameError,
      email: emailError,
      password: passwordError,
      confirmPassword: confirmPasswordError,
      terms: termsError,
      general: ''
    };
    
    return !firstNameError && !lastNameError && !emailError && 
           !passwordError && !confirmPasswordError && !termsError;
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
      const userData = {
        first_name: formData.first_name.trim(),
        last_name: formData.last_name.trim(),
        email: formData.email.trim().toLowerCase(),
        password: formData.password
      };
      
      await authStore.register(userData);
      
      // Show verification step
      currentStep = 2;
      
      toastStore.add({
        type: 'success',
        message: 'Account created successfully! Please check your email to verify your account.'
      });
      
    } catch (error) {
      console.error('Registration failed:', error);
      
      // Handle different error types
      if (error.message?.includes('email') && error.message?.includes('exists')) {
        errors.email = 'An account with this email already exists';
        errors.general = 'Please use a different email address or sign in instead.';
      } else if (error.message?.includes('validation')) {
        errors.general = 'Please check your information and try again.';
      } else {
        errors.general = 'Registration failed. Please check your connection and try again.';
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
  async function handleSocialRegister(provider) {
    console.log(`Social registration with ${provider} - Integration needed`);
    toastStore.add({
      type: 'info',
      message: `${provider} registration will be available soon`
    });
  }
  
  // Navigate to login
  function goToLogin() {
    const currentRedirect = $page.url.searchParams.get('redirect');
    const loginUrl = '/auth/login' + (currentRedirect ? `?redirect=${currentRedirect}` : '');
    goto(loginUrl);
  }
  
  // Real-time validation
  function handleFirstNameInput() {
    if (errors.first_name && formData.first_name) {
      errors.first_name = validateName(formData.first_name, 'First name');
    }
  }
  
  function handleLastNameInput() {
    if (errors.last_name && formData.last_name) {
      errors.last_name = validateName(formData.last_name, 'Last name');
    }
  }
  
  function handleEmailInput() {
    if (errors.email && formData.email) {
      errors.email = validateEmail(formData.email);
    }
  }
  
  function handlePasswordInput() {
    calculatePasswordStrength(formData.password);
    
    if (errors.password && formData.password) {
      errors.password = validatePassword(formData.password);
    }
    
    if (errors.confirmPassword && formData.confirmPassword) {
      errors.confirmPassword = validateConfirmPassword(formData.password, formData.confirmPassword);
    }
  }
  
  function handleConfirmPasswordInput() {
    if (errors.confirmPassword && formData.confirmPassword) {
      errors.confirmPassword = validateConfirmPassword(formData.password, formData.confirmPassword);
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
    
    // Focus first name input
    const firstNameInput = document.querySelector('input[name="first_name"]');
    firstNameInput?.focus();
  });
</script>

<svelte:head>
  <title>Create Account - Premium Store</title>
  <meta name="description" content="Create your account to access exclusive features, track orders, and enjoy personalized shopping" />
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
        
        {#if currentStep === 1}
          <!-- Registration Form -->
          
          <!-- Header -->
          <div class="text-center mb-8">
            <h1 class="text-3xl font-display font-bold text-gray-900 dark:text-white">
              Create your account
            </h1>
            <p class="mt-2 text-gray-600 dark:text-gray-400">
              Join thousands of satisfied customers
            </p>
          </div>
          
          <!-- Social Registration -->
          <div class="mb-6">
            <div class="grid grid-cols-2 gap-3">
              <Button
                variant="ghost"
                onclick={() => handleSocialRegister('Google')}
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
                onclick={() => handleSocialRegister('Facebook')}
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
                    Or create account with email
                  </span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Registration Form -->
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
            
            <!-- Name Fields -->
            <div class="grid grid-cols-2 gap-4">
              <Input
                type="text"
                name="first_name"
                label="First name"
                bind:value={formData.first_name}
                error={errors.first_name}
                placeholder="John"
                required
                disabled={isLoading}
                oninput={handleFirstNameInput}
              />
              
              <Input
                type="text"
                name="last_name"
                label="Last name"
                bind:value={formData.last_name}
                error={errors.last_name}
                placeholder="Doe"
                required
                disabled={isLoading}
                oninput={handleLastNameInput}
              />
            </div>
            
            <!-- Email -->
            <div>
              <Input
                type="email"
                name="email"
                label="Email address"
                bind:value={formData.email}
                error={errors.email}
                placeholder="john.doe@example.com"
                required
                disabled={isLoading}
                oninput={handleEmailInput}
              />
            </div>
            
            <!-- Password -->
            <div>
              <Input
                type={showPassword ? 'text' : 'password'}
                name="password"
                label="Password"
                bind:value={formData.password}
                error={errors.password}
                placeholder="Create a strong password"
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
              
              <!-- Password Strength Indicator -->
              {#if formData.password}
                <div class="mt-2">
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-sm text-gray-600 dark:text-gray-400">Password strength:</span>
                    <Badge variant={passwordStrength.score > 3 ? 'success' : passwordStrength.score > 2 ? 'warning' : 'danger'} size="sm">
                      {passwordStrengthLabel}
                    </Badge>
                  </div>
                  <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div 
                      class="h-2 rounded-full transition-all duration-300 {passwordStrength.score > 3 ? 'bg-green-500' : passwordStrength.score > 2 ? 'bg-yellow-500' : 'bg-red-500'}"
                      style="width: {(passwordStrength.score / 5) * 100}%"
                    ></div>
                  </div>
                  {#if passwordStrength.feedback.length > 0}
                    <ul class="mt-2 text-xs text-gray-500 dark:text-gray-400 space-y-1">
                      {#each passwordStrength.feedback as feedback}
                        <li class="flex items-center">
                          <svg class="w-3 h-3 mr-1 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                          </svg>
                          {feedback}
                        </li>
                      {/each}
                    </ul>
                  {/if}
                </div>
              {/if}
            </div>
            
            <!-- Confirm Password -->
            <div>
              <Input
                type={showConfirmPassword ? 'text' : 'password'}
                name="confirmPassword"
                label="Confirm password"
                bind:value={formData.confirmPassword}
                error={errors.confirmPassword}
                placeholder="Confirm your password"
                required
                disabled={isLoading}
                oninput={handleConfirmPasswordInput}
              >
                <button
                  type="button"
                  slot="suffix"
                  onclick={() => showConfirmPassword = !showConfirmPassword}
                  class="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                  aria-label={showConfirmPassword ? 'Hide password' : 'Show password'}
                >
                  {#if showConfirmPassword}
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
            
            <!-- Terms Agreement -->
            <div class="space-y-3">
              <label class="flex items-start">
                <input
                  type="checkbox"
                  bind:checked={agreedToTerms}
                  disabled={isLoading}
                  class="w-4 h-4 mt-0.5 text-primary-600 border-gray-300 dark:border-gray-600 rounded focus:ring-primary-500 mr-3"
                />
                <span class="text-sm text-gray-600 dark:text-gray-400">
                  I agree to the 
                  <a href="/legal/terms" target="_blank" class="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-medium">
                    Terms of Service
                  </a>
                  and
                  <a href="/legal/privacy" target="_blank" class="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-medium">
                    Privacy Policy
                  </a>
                </span>
              </label>
              
              {#if errors.terms}
                <p class="text-sm text-red-600 dark:text-red-400">{errors.terms}</p>
              {/if}
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
                Creating account...
              {:else}
                Create account
              {/if}
            </Button>
          </form>
          
          <!-- Login Link -->
          <div class="mt-8 text-center">
            <p class="text-sm text-gray-600 dark:text-gray-400">
              Already have an account?
              <button
                onclick={goToLogin}
                disabled={isLoading}
                class="font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 ml-1"
              >
                Sign in instead
              </button>
            </p>
          </div>
          
        {:else if currentStep === 2}
          <!-- Email Verification Step -->
          <div class="text-center">
            <div class="w-16 h-16 mx-auto mb-6 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center">
              <svg class="w-8 h-8 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            
            <h2 class="text-2xl font-display font-bold text-gray-900 dark:text-white mb-4">
              Check your email
            </h2>
            
            <p class="text-gray-600 dark:text-gray-400 mb-6 max-w-sm mx-auto">
              We've sent a verification link to <strong>{formData.email}</strong>. 
              Click the link in the email to complete your registration.
            </p>
            
            <div class="space-y-4">
              <Button
                variant="primary"
                onclick={goToLogin}
                class="hover-lift"
              >
                Continue to Sign In
              </Button>
              
              <p class="text-sm text-gray-500 dark:text-gray-400">
                Didn't receive the email? Check your spam folder or
                <button class="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-medium">
                  resend verification email
                </button>
              </p>
            </div>
          </div>
        {/if}
        
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