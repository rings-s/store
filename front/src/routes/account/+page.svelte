<!--
  @component AccountPage
  Premium account dashboard with profile management and quick access to account features.
  Features comprehensive profile editing, order history, and account settings.
-->
<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { getAuthStore } from '$lib/stores/auth.svelte.js';
  import { getCartStore } from '$lib/stores/cart.svelte.js';
  import { toastStore } from '$lib/stores/toast.svelte.js';
  import Button from '$lib/components/ui/Button.svelte';
  import Input from '$lib/components/ui/Input.svelte';
  import Card from '$lib/components/ui/Card.svelte';
  import Badge from '$lib/components/ui/Badge.svelte';
  import Modal from '$lib/components/ui/Modal.svelte';
  import Spinner from '$lib/components/ui/Spinner.svelte';
  
  // Store access
  const authStore = getAuthStore();
  const cartStore = getCartStore();
  
  // Reactive state using Svelte 5 runes
  let mounted = $state(false);
  let isLoading = $state(false);
  let isEditing = $state(false);
  let showChangePasswordModal = $state(false);
  
  // Form data for profile editing
  let profileData = $state({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    date_of_birth: '',
    bio: ''
  });
  
  // Change password form
  let passwordData = $state({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });
  
  // Form validation
  let errors = $state({
    profile: {},
    password: {}
  });
  
  // Derived values from stores
  const user = $derived(authStore?.user || null);
  const isAuthenticated = $derived(authStore?.isAuthenticated || false);
  const cartCount = $derived(cartStore?.itemsCount || 0);
  
  // Account stats (mock data - replace with actual API calls)
  let accountStats = $state({
    totalOrders: 12,
    totalSpent: 1247.50,
    memberSince: '2024-01-15',
    loyaltyPoints: 2450,
    wishlistItems: 8,
    recentOrders: []
  });
  
  // Quick actions
  const quickActions = [
    {
      title: 'View Orders',
      description: 'Track your recent purchases',
      icon: 'package',
      href: '/account/orders',
      badge: accountStats.totalOrders > 0 ? accountStats.totalOrders : null
    },
    {
      title: 'Wishlist',
      description: 'Items you want to buy later',
      icon: 'heart',
      href: '/account/wishlist',
      badge: accountStats.wishlistItems > 0 ? accountStats.wishlistItems : null
    },
    {
      title: 'Addresses',
      description: 'Manage shipping addresses',
      icon: 'location',
      href: '/account/addresses'
    },
    {
      title: 'Payment Methods',
      description: 'Manage your payment options',
      icon: 'credit-card',
      href: '/account/payment-methods'
    }
  ];
  
  // Initialize profile data from user
  function initializeProfileData() {
    if (user) {
      profileData = {
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        email: user.email || '',
        phone: user.phone || '',
        date_of_birth: user.date_of_birth || '',
        bio: user.bio || ''
      };
    }
  }
  
  // Handle profile edit
  function startEditing() {
    initializeProfileData();
    isEditing = true;
  }
  
  function cancelEditing() {
    initializeProfileData();
    isEditing = false;
    errors.profile = {};
  }
  
  async function saveProfile() {
    if (isLoading) return;
    
    isLoading = true;
    errors.profile = {};
    
    try {
      // Validate profile data
      if (!profileData.first_name?.trim()) {
        errors.profile.first_name = 'First name is required';
      }
      if (!profileData.last_name?.trim()) {
        errors.profile.last_name = 'Last name is required';
      }
      if (!profileData.email?.trim()) {
        errors.profile.email = 'Email is required';
      }
      
      if (Object.keys(errors.profile).length > 0) {
        return;
      }
      
      // Update profile via auth store
      await authStore.updateProfile(profileData);
      
      isEditing = false;
      
      toastStore.add({
        type: 'success',
        message: 'Profile updated successfully'
      });
      
    } catch (error) {
      console.error('Failed to update profile:', error);
      toastStore.add({
        type: 'error',
        message: 'Failed to update profile. Please try again.'
      });
    } finally {
      isLoading = false;
    }
  }
  
  // Handle password change
  async function changePassword() {
    if (isLoading) return;
    
    isLoading = true;
    errors.password = {};
    
    try {
      // Validate password data
      if (!passwordData.current_password) {
        errors.password.current_password = 'Current password is required';
      }
      if (!passwordData.new_password) {
        errors.password.new_password = 'New password is required';
      } else if (passwordData.new_password.length < 8) {
        errors.password.new_password = 'Password must be at least 8 characters';
      }
      if (passwordData.new_password !== passwordData.confirm_password) {
        errors.password.confirm_password = 'Passwords do not match';
      }
      
      if (Object.keys(errors.password).length > 0) {
        return;
      }
      
      // Change password via API
      // await authStore.changePassword(passwordData.current_password, passwordData.new_password);
      
      // Reset form and close modal
      passwordData = {
        current_password: '',
        new_password: '',
        confirm_password: ''
      };
      showChangePasswordModal = false;
      
      toastStore.add({
        type: 'success',
        message: 'Password changed successfully'
      });
      
    } catch (error) {
      console.error('Failed to change password:', error);
      toastStore.add({
        type: 'error',
        message: 'Failed to change password. Please check your current password and try again.'
      });
    } finally {
      isLoading = false;
    }
  }
  
  // Handle logout
  async function handleLogout() {
    try {
      await authStore.logout();
      goto('/');
      toastStore.add({
        type: 'success',
        message: 'You have been signed out successfully'
      });
    } catch (error) {
      console.error('Logout failed:', error);
    }
  }
  
  // Get icon SVG
  function getIconSVG(iconName) {
    const icons = {
      package: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />',
      heart: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />',
      location: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />',
      'credit-card': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />'
    };
    return icons[iconName] || '';
  }
  
  // Authentication guard
  function checkAuth() {
    if (!isAuthenticated) {
      goto('/auth/login?redirect=' + encodeURIComponent('/account'));
      return false;
    }
    return true;
  }
  
  // Lifecycle
  onMount(() => {
    mounted = true;
    
    if (!checkAuth()) return;
    
    initializeProfileData();
    
    // Load account stats (mock implementation)
    // In real app, fetch from API
    // loadAccountStats();
  });
</script>

<svelte:head>
  <title>My Account - Premium Store</title>
  <meta name="description" content="Manage your account settings, view orders, and update your profile information" />
</svelte:head>

{#if !isAuthenticated}
  <!-- Authentication Required -->
  <div class="min-h-screen bg-gray-50 dark:bg-dark-50 flex items-center justify-center">
    <Card class="glass max-w-md mx-auto text-center">
      <h2 class="text-2xl font-display font-bold text-gray-900 dark:text-white mb-4">
        Sign In Required
      </h2>
      <p class="text-gray-600 dark:text-gray-400 mb-6">
        Please sign in to access your account.
      </p>
      <Button variant="primary" href="/auth/login?redirect=/account">
        Sign In
      </Button>
    </Card>
  </div>
  
{:else}
  <!-- Account Dashboard -->
  <div class="min-h-screen bg-gray-50 dark:bg-dark-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <!-- Page Header -->
      <div class="mb-8">
        <nav class="flex mb-4" aria-label="Breadcrumb">
          <ol class="flex items-center space-x-2 text-sm">
            <li>
              <a href="/" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300">
                Home
              </a>
            </li>
            <li class="text-gray-400">/</li>
            <li class="text-gray-900 dark:text-white font-medium">My Account</li>
          </ol>
        </nav>
        
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-display font-bold text-gray-900 dark:text-white">
              Welcome back{user?.first_name ? `, ${user.first_name}` : ''}!
            </h1>
            <p class="mt-2 text-gray-600 dark:text-gray-400">
              Manage your account and track your orders
            </p>
          </div>
          
          <Button
            variant="ghost"
            onclick={handleLogout}
            class="text-gray-500 hover:text-gray-700"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            Sign Out
          </Button>
        </div>
      </div>
      
      <!-- Account Overview -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        <!-- Profile Section -->
        <div class="lg:col-span-2 space-y-6">
          
          <!-- Profile Information -->
          <Card class="glass">
            <div class="p-6">
              <div class="flex items-center justify-between mb-6">
                <h2 class="text-xl font-semibold text-gray-900 dark:text-white">
                  Profile Information
                </h2>
                {#if !isEditing}
                  <Button
                    variant="ghost"
                    size="sm"
                    onclick={startEditing}
                  >
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                    </svg>
                    Edit Profile
                  </Button>
                {/if}
              </div>
              
              {#if isEditing}
                <!-- Edit Mode -->
                <form class="space-y-4">
                  <div class="grid grid-cols-2 gap-4">
                    <Input
                      label="First Name"
                      bind:value={profileData.first_name}
                      error={errors.profile.first_name}
                      disabled={isLoading}
                    />
                    <Input
                      label="Last Name"
                      bind:value={profileData.last_name}
                      error={errors.profile.last_name}
                      disabled={isLoading}
                    />
                  </div>
                  
                  <Input
                    type="email"
                    label="Email Address"
                    bind:value={profileData.email}
                    error={errors.profile.email}
                    disabled={isLoading}
                  />
                  
                  <Input
                    type="tel"
                    label="Phone Number"
                    bind:value={profileData.phone}
                    placeholder="+1 (555) 123-4567"
                    disabled={isLoading}
                  />
                  
                  <Input
                    type="date"
                    label="Date of Birth"
                    bind:value={profileData.date_of_birth}
                    disabled={isLoading}
                  />
                  
                  <div class="flex items-center justify-end space-x-3">
                    <Button
                      variant="ghost"
                      onclick={cancelEditing}
                      disabled={isLoading}
                    >
                      Cancel
                    </Button>
                    <Button
                      variant="primary"
                      onclick={saveProfile}
                      loading={isLoading}
                    >
                      Save Changes
                    </Button>
                  </div>
                </form>
              {:else}
                <!-- View Mode -->
                <div class="space-y-4">
                  <div class="flex items-center">
                    <div class="w-16 h-16 bg-gradient-to-r from-primary-500 to-primary-600 rounded-full flex items-center justify-center mr-4">
                      <span class="text-white text-xl font-semibold">
                        {(user?.first_name?.charAt(0) || '') + (user?.last_name?.charAt(0) || '')}
                      </span>
                    </div>
                    <div>
                      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                        {user?.first_name || ''} {user?.last_name || ''}
                      </h3>
                      <p class="text-gray-600 dark:text-gray-400">{user?.email || ''}</p>
                    </div>
                  </div>
                  
                  <div class="grid grid-cols-2 gap-4">
                    <div>
                      <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Member Since</label>
                      <p class="text-gray-900 dark:text-white">
                        {new Date(accountStats.memberSince).toLocaleDateString('en-US', { 
                          year: 'numeric', 
                          month: 'long' 
                        })}
                      </p>
                    </div>
                    <div>
                      <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Loyalty Points</label>
                      <p class="text-gray-900 dark:text-white flex items-center">
                        <svg class="w-4 h-4 text-yellow-500 mr-1" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                        </svg>
                        {accountStats.loyaltyPoints.toLocaleString()}
                      </p>
                    </div>
                  </div>
                </div>
              {/if}
            </div>
          </Card>
          
          <!-- Account Stats -->
          <Card class="glass">
            <div class="p-6">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Account Overview
              </h3>
              
              <div class="grid grid-cols-3 gap-4">
                <div class="text-center">
                  <div class="text-2xl font-bold text-primary-600 dark:text-primary-400">
                    {accountStats.totalOrders}
                  </div>
                  <div class="text-sm text-gray-600 dark:text-gray-400">Total Orders</div>
                </div>
                
                <div class="text-center">
                  <div class="text-2xl font-bold text-green-600 dark:text-green-400">
                    ${accountStats.totalSpent.toFixed(2)}
                  </div>
                  <div class="text-sm text-gray-600 dark:text-gray-400">Total Spent</div>
                </div>
                
                <div class="text-center">
                  <div class="text-2xl font-bold text-purple-600 dark:text-purple-400">
                    {accountStats.wishlistItems}
                  </div>
                  <div class="text-sm text-gray-600 dark:text-gray-400">Wishlist Items</div>
                </div>
              </div>
            </div>
          </Card>
          
        </div>
        
        <!-- Quick Actions Sidebar -->
        <div class="space-y-6">
          
          <!-- Quick Actions -->
          <Card class="glass">
            <div class="p-6">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Quick Actions
              </h3>
              
              <div class="space-y-3">
                {#each quickActions as action}
                  <a
                    href={action.href}
                    class="block p-3 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors group"
                  >
                    <div class="flex items-center justify-between">
                      <div class="flex items-center">
                        <svg class="w-5 h-5 text-gray-400 group-hover:text-primary-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          {@html getIconSVG(action.icon)}
                        </svg>
                        <div>
                          <div class="font-medium text-gray-900 dark:text-white group-hover:text-primary-600">
                            {action.title}
                          </div>
                          <div class="text-sm text-gray-500 dark:text-gray-400">
                            {action.description}
                          </div>
                        </div>
                      </div>
                      {#if action.badge}
                        <Badge variant="primary" size="sm">{action.badge}</Badge>
                      {/if}
                    </div>
                  </a>
                {/each}
              </div>
            </div>
          </Card>
          
          <!-- Security Settings -->
          <Card class="glass">
            <div class="p-6">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Security
              </h3>
              
              <div class="space-y-3">
                <Button
                  variant="ghost"
                  fullWidth
                  onclick={() => showChangePasswordModal = true}
                  class="justify-start"
                >
                  <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m0 0a2 2 0 012 2m-2-2a2 2 0 00-2-2m0 0a2 2 0 00-2-2m2 2V7a2 2 0 00-2-2" />
                  </svg>
                  Change Password
                </Button>
                
                <Button
                  variant="ghost"
                  fullWidth
                  onclick={() => console.log('Two-factor setup')}
                  class="justify-start"
                >
                  <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                  Two-Factor Authentication
                </Button>
              </div>
            </div>
          </Card>
          
        </div>
        
      </div>
    </div>
  </div>
  
  <!-- Change Password Modal -->
  <Modal bind:open={showChangePasswordModal} title="Change Password" size="sm">
    <form class="space-y-4">
      <Input
        type="password"
        label="Current Password"
        bind:value={passwordData.current_password}
        error={errors.password.current_password}
        disabled={isLoading}
      />
      
      <Input
        type="password"
        label="New Password"
        bind:value={passwordData.new_password}
        error={errors.password.new_password}
        disabled={isLoading}
      />
      
      <Input
        type="password"
        label="Confirm New Password"
        bind:value={passwordData.confirm_password}
        error={errors.password.confirm_password}
        disabled={isLoading}
      />
    </form>
    
    <div slot="footer" class="flex items-center justify-end space-x-3">
      <Button
        variant="ghost"
        onclick={() => showChangePasswordModal = false}
        disabled={isLoading}
      >
        Cancel
      </Button>
      <Button
        variant="primary"
        onclick={changePassword}
        loading={isLoading}
      >
        Change Password
      </Button>
    </div>
  </Modal>
{/if}