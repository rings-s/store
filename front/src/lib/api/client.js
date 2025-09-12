/**
 * @fileoverview Base API client with interceptors, error handling, and token management
 */

import { goto } from '$app/navigation';
import { browser } from '$app/environment';

// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';
const DEFAULT_TIMEOUT = 10000;

// Request/Response Types
const CONTENT_TYPES = {
  JSON: 'application/json',
  FORM_DATA: 'multipart/form-data',
  URL_ENCODED: 'application/x-www-form-urlencoded'
};

/**
 * Custom API Error class
 */
export class ApiError extends Error {
  constructor(message, status, data = null) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.data = data;
  }
}

/**
 * Token management utilities
 */
export const tokenManager = {
  getTokens() {
    if (!browser) return { access: null, refresh: null };
    
    return {
      access: localStorage.getItem('accessToken'),
      refresh: localStorage.getItem('refreshToken')
    };
  },

  setTokens(access, refresh) {
    if (!browser) return;
    
    if (access) localStorage.setItem('accessToken', access);
    if (refresh) localStorage.setItem('refreshToken', refresh);
  },

  clearTokens() {
    if (!browser) return;
    
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  },

  isTokenExpired(token) {
    if (!token) return true;
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return Date.now() >= payload.exp * 1000;
    } catch {
      return true;
    }
  }
};

/**
 * HTTP Request class with interceptors
 */
class HTTPClient {
  constructor(baseURL = API_BASE_URL) {
    this.baseURL = baseURL;
    this.defaultHeaders = {
      'Content-Type': CONTENT_TYPES.JSON,
      'Accept': CONTENT_TYPES.JSON
    };
    this.requestInterceptors = [];
    this.responseInterceptors = [];
    this.isRefreshing = false;
    this.refreshQueue = [];
  }

  // Add request interceptor
  addRequestInterceptor(interceptor) {
    this.requestInterceptors.push(interceptor);
  }

  // Add response interceptor
  addResponseInterceptor(interceptor) {
    this.responseInterceptors.push(interceptor);
  }

  // Execute request interceptors
  async executeRequestInterceptors(config) {
    for (const interceptor of this.requestInterceptors) {
      config = await interceptor(config);
    }
    return config;
  }

  // Execute response interceptors
  async executeResponseInterceptors(response, config) {
    for (const interceptor of this.responseInterceptors) {
      response = await interceptor(response, config);
    }
    return response;
  }

  // Build URL with query parameters
  buildURL(endpoint, params = {}) {
    const url = new URL(endpoint, this.baseURL);
    Object.keys(params).forEach(key => {
      if (params[key] !== undefined && params[key] !== null) {
        url.searchParams.append(key, params[key]);
      }
    });
    return url.toString();
  }

  // Prepare request headers
  prepareHeaders(headers = {}, contentType = CONTENT_TYPES.JSON) {
    const finalHeaders = { ...this.defaultHeaders, ...headers };
    
    if (contentType) {
      finalHeaders['Content-Type'] = contentType;
    }

    // Add auth token if available
    const { access } = tokenManager.getTokens();
    if (access && !tokenManager.isTokenExpired(access)) {
      finalHeaders['Authorization'] = `Bearer ${access}`;
    }

    return finalHeaders;
  }

  // Prepare request body
  prepareBody(data, contentType = CONTENT_TYPES.JSON) {
    if (!data) return null;

    switch (contentType) {
      case CONTENT_TYPES.JSON:
        return JSON.stringify(data);
      case CONTENT_TYPES.FORM_DATA:
        const formData = new FormData();
        Object.keys(data).forEach(key => {
          if (data[key] !== null && data[key] !== undefined) {
            formData.append(key, data[key]);
          }
        });
        return formData;
      case CONTENT_TYPES.URL_ENCODED:
        return new URLSearchParams(data).toString();
      default:
        return data;
    }
  }

  // Refresh access token
  async refreshAccessToken() {
    const { refresh } = tokenManager.getTokens();
    if (!refresh) {
      throw new ApiError('No refresh token available', 401);
    }

    try {
      const response = await fetch(`${this.baseURL}/accounts/token/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': CONTENT_TYPES.JSON },
        body: JSON.stringify({ refresh })
      });

      if (!response.ok) {
        throw new ApiError('Token refresh failed', response.status);
      }

      const data = await response.json();
      tokenManager.setTokens(data.access, refresh);
      return data.access;
    } catch (error) {
      tokenManager.clearTokens();
      goto('/auth/login');
      throw error;
    }
  }

  // Main request method
  async request(method, endpoint, options = {}) {
    const {
      data,
      params,
      headers = {},
      contentType = CONTENT_TYPES.JSON,
      timeout = DEFAULT_TIMEOUT,
      retry = true
    } = options;

    let config = {
      method,
      url: this.buildURL(endpoint, params),
      headers: this.prepareHeaders(headers, contentType),
      body: this.prepareBody(data, contentType),
      signal: AbortSignal.timeout(timeout)
    };

    // Execute request interceptors
    config = await this.executeRequestInterceptors(config);

    try {
      let response = await fetch(config.url, {
        method: config.method,
        headers: config.headers,
        body: config.body,
        signal: config.signal
      });

      // Handle 401 with token refresh
      if (response.status === 401 && retry) {
        const { access } = tokenManager.getTokens();
        if (access && tokenManager.isTokenExpired(access)) {
          if (!this.isRefreshing) {
            this.isRefreshing = true;
            try {
              await this.refreshAccessToken();
              this.isRefreshing = false;
              
              // Process queued requests
              this.refreshQueue.forEach(({ resolve, config }) => {
                resolve(this.request(config.method, endpoint, { ...options, retry: false }));
              });
              this.refreshQueue = [];
              
              // Retry original request
              return this.request(method, endpoint, { ...options, retry: false });
            } catch (error) {
              this.isRefreshing = false;
              this.refreshQueue = [];
              throw error;
            }
          } else {
            // Queue request while refreshing
            return new Promise((resolve) => {
              this.refreshQueue.push({ resolve, config });
            });
          }
        }
      }

      // Execute response interceptors
      response = await this.executeResponseInterceptors(response, config);

      // Parse response data
      let responseData;
      const contentType = response.headers.get('content-type');
      
      if (contentType?.includes('application/json')) {
        responseData = await response.json();
      } else {
        responseData = await response.text();
      }

      // Handle error responses
      if (!response.ok) {
        throw new ApiError(
          responseData.message || responseData.detail || 'Request failed',
          response.status,
          responseData
        );
      }

      return {
        data: responseData,
        status: response.status,
        headers: response.headers
      };

    } catch (error) {
      if (error.name === 'AbortError') {
        throw new ApiError('Request timeout', 408);
      }
      throw error;
    }
  }

  // HTTP Methods
  get(endpoint, options = {}) {
    return this.request('GET', endpoint, options);
  }

  post(endpoint, data, options = {}) {
    return this.request('POST', endpoint, { ...options, data });
  }

  put(endpoint, data, options = {}) {
    return this.request('PUT', endpoint, { ...options, data });
  }

  patch(endpoint, data, options = {}) {
    return this.request('PATCH', endpoint, { ...options, data });
  }

  delete(endpoint, options = {}) {
    return this.request('DELETE', endpoint, options);
  }
}

// Create singleton instance
const apiClient = new HTTPClient();

// Add default interceptors
apiClient.addRequestInterceptor(async (config) => {
  // Log requests in development
  if (import.meta.env.DEV) {
    console.log(`🚀 ${config.method} ${config.url}`);
  }
  return config;
});

apiClient.addResponseInterceptor(async (response, config) => {
  // Log responses in development
  if (import.meta.env.DEV) {
    console.log(`✅ ${response.status} ${config.method} ${config.url}`);
  }
  return response;
});

export default apiClient;

// Export utilities
export { CONTENT_TYPES, API_BASE_URL };