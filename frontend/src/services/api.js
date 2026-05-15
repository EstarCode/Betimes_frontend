import axios from 'axios'
import { toast } from 'react-toastify'

// API Configuration - Production Ready
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
const TOKEN_REFRESH_INTERVAL = parseInt(import.meta.env.VITE_TOKEN_REFRESH_INTERVAL) || 300000 // 5 minutes

// Create axios instance with international standards
const api = axios.create({
  baseURL: API_URL,
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
  },
  withCredentials: true, // Enable CORS credentials
})

// Token refresh timer
let tokenRefreshTimer = null

// Start automatic token refresh
const startTokenRefresh = () => {
  if (tokenRefreshTimer) {
    clearInterval(tokenRefreshTimer)
  }
  
  tokenRefreshTimer = setInterval(async () => {
    const refreshToken = localStorage.getItem('refreshToken')
    if (refreshToken) {
      try {
        const response = await axios.post(`${API_URL}/v1/auth/token/refresh/`, {
          refresh: refreshToken,
        })
        const { access } = response.data
        localStorage.setItem('token', access)
      } catch (error) {
        console.error('Token refresh failed:', error)
        stopTokenRefresh()
      }
    }
  }, TOKEN_REFRESH_INTERVAL)
}

// Stop automatic token refresh
const stopTokenRefresh = () => {
  if (tokenRefreshTimer) {
    clearInterval(tokenRefreshTimer)
    tokenRefreshTimer = null
  }
}

// Request interceptor - Add auth token and security headers
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // Add request ID for tracking (RFC 7807 compliance)
    config.headers['X-Request-ID'] = `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
    
    // Add timestamp for request tracking
    config.metadata = { startTime: new Date() }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - Handle errors and token refresh
api.interceptors.response.use(
  (response) => {
    // Log response time for monitoring
    if (response.config.metadata) {
      const duration = new Date() - response.config.metadata.startTime
      console.debug(`API Request: ${response.config.url} - ${duration}ms`)
    }
    return response
  },
  async (error) => {
    const originalRequest = error.config

    // Handle network errors
    if (!error.response) {
      toast.error('Network error. Please check your connection.')
      return Promise.reject(error)
    }

    // Handle 401 errors (token expired) - RFC 6750 OAuth 2.0 Bearer Token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refreshToken')
        if (!refreshToken) {
          throw new Error('No refresh token available')
        }

        const response = await axios.post(`${API_URL}/auth/token/refresh/`, {
          refresh: refreshToken,
        })

        const { access, refresh } = response.data
        localStorage.setItem('token', access)
        if (refresh) {
          localStorage.setItem('refreshToken', refresh)
        }

        originalRequest.headers.Authorization = `Bearer ${access}`
        return api(originalRequest)
      } catch (refreshError) {
        // Clear tokens and redirect to login
        localStorage.removeItem('token')
        localStorage.removeItem('refreshToken')
        localStorage.removeItem('user')
        stopTokenRefresh()
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    // Handle 403 errors (forbidden)
    if (error.response?.status === 403) {
      toast.error('Access denied. You do not have permission to perform this action.')
    }

    // Handle 404 errors
    if (error.response?.status === 404) {
      toast.error('Resource not found.')
    }

    // Handle 429 errors (rate limiting)
    if (error.response?.status === 429) {
      const retryAfter = error.response.headers['retry-after']
      toast.error(`Too many requests. Please try again ${retryAfter ? `after ${retryAfter} seconds` : 'later'}.`)
    }

    // Handle 500+ errors (server errors)
    if (error.response?.status >= 500) {
      toast.error('Server error. Please try again later.')
    }

    // RFC 7807 Problem Details for HTTP APIs
    const errorData = error.response?.data
    if (errorData?.error) {
      const { type, title, detail, status, instance } = errorData.error
      console.error('API Error:', {
        type,
        title,
        detail,
        status,
        instance,
        requestId: error.config.headers['X-Request-ID']
      })
      
      // Show user-friendly error message
      if (detail && error.response?.status < 500) {
        toast.error(detail)
      }
    } else if (errorData?.message) {
      toast.error(errorData.message)
    }

    return Promise.reject(error)
  }
)

// Export API instance and utilities
export default api

export { startTokenRefresh, stopTokenRefresh, API_URL }
