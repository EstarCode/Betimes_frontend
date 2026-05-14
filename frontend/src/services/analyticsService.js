import api from './api'

/**
 * Analytics Service
 * Real-time metrics and reporting
 * Compliance: GDPR, ISO/IEC 27001
 */
export const analyticsService = {
  /**
   * Get dashboard metrics
   * @param {Object} filters - Time range and filters
   */
  getDashboardMetrics: async (filters = {}) => {
    const params = new URLSearchParams()
    if (filters.startDate) params.append('start_date', filters.startDate)
    if (filters.endDate) params.append('end_date', filters.endDate)
    if (filters.granularity) params.append('granularity', filters.granularity)

    const response = await api.get(`/analytics/dashboard/?${params.toString()}`)
    return response.data
  },

  /**
   * Get document statistics
   * @param {Object} filters - Filter options
   */
  getDocumentStats: async (filters = {}) => {
    const params = new URLSearchParams()
    if (filters.startDate) params.append('start_date', filters.startDate)
    if (filters.endDate) params.append('end_date', filters.endDate)
    if (filters.fileType) params.append('file_type', filters.fileType)

    const response = await api.get(`/analytics/documents/?${params.toString()}`)
    return response.data
  },

  /**
   * Get user activity
   * @param {Object} filters - Filter options
   */
  getUserActivity: async (filters = {}) => {
    const params = new URLSearchParams()
    if (filters.startDate) params.append('start_date', filters.startDate)
    if (filters.endDate) params.append('end_date', filters.endDate)
    if (filters.userId) params.append('user_id', filters.userId)

    const response = await api.get(`/analytics/activity/?${params.toString()}`)
    return response.data
  },

  /**
   * Get conversion statistics
   * @param {Object} filters - Filter options
   */
  getConversionStats: async (filters = {}) => {
    const params = new URLSearchParams()
    if (filters.startDate) params.append('start_date', filters.startDate)
    if (filters.endDate) params.append('end_date', filters.endDate)

    const response = await api.get(`/analytics/conversions/?${params.toString()}`)
    return response.data
  },

  /**
   * Get storage usage
   */
  getStorageUsage: async () => {
    const response = await api.get('/analytics/storage/')
    return response.data
  },

  /**
   * Get API usage statistics
   * @param {Object} filters - Filter options
   */
  getApiUsage: async (filters = {}) => {
    const params = new URLSearchParams()
    if (filters.startDate) params.append('start_date', filters.startDate)
    if (filters.endDate) params.append('end_date', filters.endDate)

    const response = await api.get(`/analytics/api-usage/?${params.toString()}`)
    return response.data
  },

  /**
   * Get error statistics
   * @param {Object} filters - Filter options
   */
  getErrorStats: async (filters = {}) => {
    const params = new URLSearchParams()
    if (filters.startDate) params.append('start_date', filters.startDate)
    if (filters.endDate) params.append('end_date', filters.endDate)

    const response = await api.get(`/analytics/errors/?${params.toString()}`)
    return response.data
  },

  /**
   * Get performance metrics
   * @param {Object} filters - Filter options
   */
  getPerformanceMetrics: async (filters = {}) => {
    const params = new URLSearchParams()
    if (filters.startDate) params.append('start_date', filters.startDate)
    if (filters.endDate) params.append('end_date', filters.endDate)

    const response = await api.get(`/analytics/performance/?${params.toString()}`)
    return response.data
  },

  /**
   * Export analytics report
   * @param {string} reportType - Report type (pdf, csv, xlsx)
   * @param {Object} filters - Filter options
   */
  exportReport: async (reportType, filters = {}) => {
    const params = new URLSearchParams()
    params.append('format', reportType)
    if (filters.startDate) params.append('start_date', filters.startDate)
    if (filters.endDate) params.append('end_date', filters.endDate)

    const response = await api.get(`/analytics/export/?${params.toString()}`, {
      responseType: 'blob',
    })
    return response.data
  },

  /**
   * Track custom event
   * @param {string} eventName - Event name
   * @param {Object} eventData - Event data
   */
  trackEvent: async (eventName, eventData = {}) => {
    const response = await api.post('/analytics/events/', {
      event_name: eventName,
      event_data: eventData,
      timestamp: new Date().toISOString(),
    })
    return response.data
  },
}
