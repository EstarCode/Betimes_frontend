import api from './api'

/**
 * Notification Service
 * Multi-channel notifications: Email, SMS, In-App, Push
 * Compliance: CAN-SPAM Act, GDPR
 */
export const notificationService = {
  /**
   * Get all notifications
   * @param {Object} filters - Filter options
   */
  getNotifications: async (filters = {}) => {
    const params = new URLSearchParams()
    if (filters.read !== undefined) params.append('read', filters.read)
    if (filters.type) params.append('type', filters.type)
    if (filters.page) params.append('page', filters.page)

    const response = await api.get(`/notifications/?${params.toString()}`)
    return response.data
  },

  /**
   * Get notification by ID
   * @param {string} notificationId - Notification ID
   */
  getNotification: async (notificationId) => {
    const response = await api.get(`/notifications/${notificationId}/`)
    return response.data
  },

  /**
   * Mark notification as read
   * @param {string} notificationId - Notification ID
   */
  markAsRead: async (notificationId) => {
    const response = await api.patch(`/notifications/${notificationId}/`, {
      read: true,
    })
    return response.data
  },

  /**
   * Mark all notifications as read
   */
  markAllAsRead: async () => {
    const response = await api.post('/notifications/mark-all-read/')
    return response.data
  },

  /**
   * Delete notification
   * @param {string} notificationId - Notification ID
   */
  deleteNotification: async (notificationId) => {
    const response = await api.delete(`/notifications/${notificationId}/`)
    return response.data
  },

  /**
   * Get unread count
   */
  getUnreadCount: async () => {
    const response = await api.get('/notifications/unread-count/')
    return response.data
  },

  /**
   * Get notification preferences
   */
  getPreferences: async () => {
    const response = await api.get('/notifications/preferences/')
    return response.data
  },

  /**
   * Update notification preferences
   * @param {Object} preferences - Notification preferences
   */
  updatePreferences: async (preferences) => {
    const response = await api.patch('/notifications/preferences/', preferences)
    return response.data
  },

  /**
   * Subscribe to push notifications
   * @param {Object} subscription - Push subscription object
   */
  subscribePush: async (subscription) => {
    const response = await api.post('/notifications/push/subscribe/', subscription)
    return response.data
  },

  /**
   * Unsubscribe from push notifications
   */
  unsubscribePush: async () => {
    const response = await api.post('/notifications/push/unsubscribe/')
    return response.data
  },

  /**
   * Test notification
   * @param {string} channel - Notification channel (email, sms, push, in_app)
   */
  testNotification: async (channel) => {
    const response = await api.post('/notifications/test/', { channel })
    return response.data
  },

  /**
   * Get notification history
   * @param {Object} filters - Filter options
   */
  getHistory: async (filters = {}) => {
    const params = new URLSearchParams()
    if (filters.startDate) params.append('start_date', filters.startDate)
    if (filters.endDate) params.append('end_date', filters.endDate)
    if (filters.type) params.append('type', filters.type)
    if (filters.page) params.append('page', filters.page)

    const response = await api.get(`/notifications/history/?${params.toString()}`)
    return response.data
  },
}
