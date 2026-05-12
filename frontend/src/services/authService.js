import api from './api'

export const authService = {
  register: async (userData) => {
    const response = await api.post('/auth/register/', userData)
    return response.data
  },

  login: async (credentials) => {
    const response = await api.post('/auth/login/', credentials)
    return response.data
  },

  logout: () => {
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
  },

  getProfile: async () => {
    const response = await api.get('/auth/profile/')
    return response.data
  },

  updateProfile: async (userData) => {
    const response = await api.patch('/auth/profile/', userData)
    return response.data
  },

  requestPasswordReset: async (email) => {
    const response = await api.post('/auth/password-reset/', { email })
    return response.data
  },
}
