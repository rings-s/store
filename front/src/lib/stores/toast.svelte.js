/**
 * @fileoverview Toast notification store using Svelte 5 runes
 */

// Simple ID generation
const generateId = () => `toast_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

// Toast types and configuration
export const TOAST_TYPES = {
  SUCCESS: 'success',
  ERROR: 'error',
  WARNING: 'warning',
  INFO: 'info',
  LOADING: 'loading'
};

export const TOAST_POSITIONS = {
  TOP_LEFT: 'top-left',
  TOP_CENTER: 'top-center',
  TOP_RIGHT: 'top-right',
  BOTTOM_LEFT: 'bottom-left',
  BOTTOM_CENTER: 'bottom-center',
  BOTTOM_RIGHT: 'bottom-right'
};

const DEFAULT_DURATION = 5000; // 5 seconds
const DEFAULT_POSITION = TOAST_POSITIONS.TOP_RIGHT;

/**
 * Toast configuration interface
 * @typedef {Object} ToastConfig
 * @property {string} type - Toast type (success, error, warning, info, loading)
 * @property {string} title - Toast title
 * @property {string} message - Toast message
 * @property {number} duration - Auto-dismiss duration in ms (0 for no auto-dismiss)
 * @property {boolean} dismissible - Whether toast can be manually dismissed
 * @property {string} position - Toast position on screen
 * @property {Object} action - Optional action button configuration
 * @property {any} data - Optional data payload
 */

/**
 * Create toast store with Svelte 5 runes
 */
function createToastStore() {
  // Internal state
  let toasts = $state([]);
  let position = $state(DEFAULT_POSITION);

  // Getters (derived state)
  const getToasts = () => toasts;
  const getPosition = () => position;
  const getToastsByPosition = (pos) => toasts.filter(toast => toast.position === pos);
  const getToastById = (id) => toasts.find(toast => toast.id === id);
  
  // Count toasts by type
  const getToastCounts = () => {
    return toasts.reduce((acc, toast) => {
      acc[toast.type] = (acc[toast.type] || 0) + 1;
      return acc;
    }, {});
  };

  // Internal methods
  const createToast = (config) => {
    const toast = {
      id: generateId(),
      type: config.type || TOAST_TYPES.INFO,
      title: config.title || '',
      message: config.message || '',
      duration: config.duration !== undefined ? config.duration : DEFAULT_DURATION,
      dismissible: config.dismissible !== false,
      position: config.position || position,
      action: config.action || null,
      data: config.data || null,
      createdAt: Date.now(),
      timeoutId: null
    };

    // Auto-dismiss if duration > 0
    if (toast.duration > 0) {
      toast.timeoutId = setTimeout(() => {
        remove(toast.id);
      }, toast.duration);
    }

    return toast;
  };

  const clearTimeout = (toast) => {
    if (toast.timeoutId) {
      window.clearTimeout(toast.timeoutId);
      toast.timeoutId = null;
    }
  };

  // Public API
  const add = (config) => {
    const toast = createToast(config);
    toasts = [...toasts, toast];
    return toast.id;
  };

  const remove = (id) => {
    const toast = getToastById(id);
    if (toast) {
      clearTimeout(toast);
      toasts = toasts.filter(t => t.id !== id);
    }
  };

  const removeAll = () => {
    toasts.forEach(clearTimeout);
    toasts = [];
  };

  const removeByType = (type) => {
    const toastsToRemove = toasts.filter(t => t.type === type);
    toastsToRemove.forEach(toast => {
      clearTimeout(toast);
    });
    toasts = toasts.filter(t => t.type !== type);
  };

  const update = (id, config) => {
    const toastIndex = toasts.findIndex(t => t.id === id);
    if (toastIndex >= 0) {
      const existingToast = toasts[toastIndex];
      clearTimeout(existingToast);
      
      const updatedToast = {
        ...existingToast,
        ...config,
        id // Preserve original ID
      };

      // Reset timeout if duration changed
      if (updatedToast.duration > 0) {
        updatedToast.timeoutId = setTimeout(() => {
          remove(id);
        }, updatedToast.duration);
      }

      toasts[toastIndex] = updatedToast;
      toasts = [...toasts]; // Trigger reactivity
    }
  };

  const setPosition = (newPosition) => {
    if (Object.values(TOAST_POSITIONS).includes(newPosition)) {
      position = newPosition;
    }
  };

  // Pause/Resume auto-dismiss
  const pause = (id) => {
    const toast = getToastById(id);
    if (toast && toast.timeoutId) {
      clearTimeout(toast);
    }
  };

  const resume = (id, remainingTime) => {
    const toast = getToastById(id);
    if (toast && remainingTime > 0) {
      toast.timeoutId = setTimeout(() => {
        remove(id);
      }, remainingTime);
    }
  };

  // Convenience methods for different toast types
  const success = (title, message, config = {}) => {
    return add({
      type: TOAST_TYPES.SUCCESS,
      title,
      message,
      ...config
    });
  };

  const error = (title, message, config = {}) => {
    return add({
      type: TOAST_TYPES.ERROR,
      title,
      message,
      duration: config.duration !== undefined ? config.duration : 8000, // Longer for errors
      ...config
    });
  };

  const warning = (title, message, config = {}) => {
    return add({
      type: TOAST_TYPES.WARNING,
      title,
      message,
      ...config
    });
  };

  const info = (title, message, config = {}) => {
    return add({
      type: TOAST_TYPES.INFO,
      title,
      message,
      ...config
    });
  };

  const loading = (title, message, config = {}) => {
    return add({
      type: TOAST_TYPES.LOADING,
      title,
      message,
      duration: 0, // No auto-dismiss for loading toasts
      dismissible: false,
      ...config
    });
  };

  // Promise-based loading toast
  const promise = async (promise, messages) => {
    const {
      loading: loadingMsg = 'Loading...',
      success: successMsg = 'Success!',
      error: errorMsg = 'Something went wrong'
    } = messages;

    const loadingId = loading('', loadingMsg);

    try {
      const result = await promise;
      remove(loadingId);
      success('', successMsg);
      return result;
    } catch (error) {
      remove(loadingId);
      this.error('', typeof errorMsg === 'function' ? errorMsg(error) : errorMsg);
      throw error;
    }
  };

  return {
    // State accessors
    get toasts() { return getToasts(); },
    get position() { return getPosition(); },
    
    // Methods
    add,
    remove,
    removeAll,
    removeByType,
    update,
    setPosition,
    pause,
    resume,
    getToastsByPosition,
    getToastById,
    getToastCounts,
    
    // Convenience methods
    success,
    error,
    warning,
    info,
    loading,
    promise
  };
}

// Create and export singleton instance
export const toastStore = createToastStore();

// Types and constants already exported above (lines 9 and 17)