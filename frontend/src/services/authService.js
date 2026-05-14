import api, { startTokenRefresh, stopTokenRefresh } from './api'

export const authService = {
  // User Registration - ISO/IEC 27001 compliant
  register: async (userData) => {
    const response = await api.post('/auth/register/', userData)
    return response.data
  },

  // User Login with JWT - RFC 6749 OAuth 2.0
  login: async (credentials) => {
    const response = await api.post('/auth/login/', credentials)
    const { access, refresh, user } = response.data
    
    // Store tokens securely
    localStorage.setItem('token', access)
    localStorage.setItem('refreshToken', refresh)
    localStorage.setItem('user', JSON.stringify(user))
    
    // Start automatic token refresh
    startTokenRefresh()
    
    return response.data
  },

  // User Logout
  logout: async () => {
    try {
      const refreshToken = localStorage.getItem('refreshToken')
      if (refreshToken) {
        await api.post('/auth/logout/', { refresh: refreshToken })
      }
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      // Clear local storage
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('user')
      
      // Stop token refresh
      stopTokenRefresh()
    }
  },

  // Get User Profile
  getProfile: async () => {
    const response = await api.get('/auth/profile/')
    return response.data
  },

  // Update User Profile
  updateProfile: async (userData) => {
    const response = await api.patch('/auth/profile/', userData)
    localStorage.setItem('user', JSON.stringify(response.data))
    return response.data
  },

  // Change Password - NIST SP 800-63B compliant
  changePassword: async (passwordData) => {
    const response = await api.post('/auth/change-password/', passwordData)
    return response.data
  },

  // Request Password Reset
  requestPasswordReset: async (email) => {
    const response = await api.post('/auth/password-reset/', { email })
    return response.data
  },

  // Confirm Password Reset
  confirmPasswordReset: async (token, newPassword) => {
    const response = await api.post('/auth/password-reset/confirm/', {
      token,
      new_password: newPassword,
    })
    return response.data
  },

  // MFA - Multi-Factor Authentication (RFC 6238 TOTP)
  mfa: {
    // Enable MFA
    enable: async () => {
      const response = await api.post('/auth/mfa/enable/')
      return response.data // Returns QR code and secret
    },

    // Verify MFA Setup
    verify: async (code) => {
      const response = await api.post('/auth/mfa/verify/', { code })
      return response.data // Returns backup codes
    },

    // Disable MFA
    disable: async (password) => {
      const response = await api.post('/auth/mfa/disable/', { password })
      return response.data
    },

    // Verify MFA Code during login
    verifyLogin: async (code) => {
      const response = await api.post('/auth/mfa/verify-login/', { code })
      return response.data
    },

    // Regenerate Backup Codes
    regenerateBackupCodes: async () => {
      const response = await api.post('/auth/mfa/regenerate-backup-codes/')
      return response.data
    },
  },

  // Session Management
  session: {
    // Get Active Sessions
    getSessions: async () => {
      const response = await api.get('/auth/sessions/')
      return response.data
    },

    // Revoke Session
    revokeSession: async (sessionId) => {
      const response = await api.delete(`/auth/sessions/${sessionId}/`)
      return response.data
    },

    // Revoke All Sessions (except current)
    revokeAllSessions: async () => {
      const response = await api.post('/auth/sessions/revoke-all/')
      return response.data
    },
  },

  // Check if user is authenticated
  isAuthenticated: () => {
    const token = localStorage.getItem('token')
    const user = localStorage.getItem('user')
    return !!(token && user)
  },

  // Get current user from localStorage
  getCurrentUser: () => {
    const userStr = localStorage.getItem('user')
    return userStr ? JSON.parse(userStr) : null
  },
}
