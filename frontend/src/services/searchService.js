import api from './api'

/**
 * Search Engine Service
 * Full-text search with PostgreSQL
 * Performance: < 2 seconds for 10,000+ documents
 */
export const searchService = {
  /**
   * Search documents
   * @param {string} query - Search query
   * @param {Object} filters - Search filters
   */
  search: async (query, filters = {}) => {
    const params = new URLSearchParams()
    params.append('q', query)
    
    // Filters
    if (filters.fileType) params.append('file_type', filters.fileType)
    if (filters.owner) params.append('owner', filters.owner)
    if (filters.dateFrom) params.append('date_from', filters.dateFrom)
    if (filters.dateTo) params.append('date_to', filters.dateTo)
    if (filters.minSize) params.append('min_size', filters.minSize)
    if (filters.maxSize) params.append('max_size', filters.maxSize)
    if (filters.tags) params.append('tags', filters.tags.join(','))
    if (filters.page) params.append('page', filters.page)
    if (filters.pageSize) params.append('page_size', filters.pageSize)

    const response = await api.get(`/search/?${params.toString()}`)
    return response.data
  },

  /**
   * Advanced search with multiple criteria
   * @param {Object} criteria - Search criteria
   */
  advancedSearch: async (criteria) => {
    const response = await api.post('/search/advanced/', criteria)
    return response.data
  },

  /**
   * Get search suggestions (autocomplete)
   * @param {string} query - Partial query
   */
  getSuggestions: async (query) => {
    const response = await api.get(`/search/suggestions/?q=${encodeURIComponent(query)}`)
    return response.data
  },

  /**
   * Get search history
   * @param {number} limit - Number of results
   */
  getHistory: async (limit = 10) => {
    const response = await api.get(`/search/history/?limit=${limit}`)
    return response.data
  },

  /**
   * Clear search history
   */
  clearHistory: async () => {
    const response = await api.delete('/search/history/')
    return response.data
  },

  /**
   * Save search query
   * @param {string} name - Search name
   * @param {Object} query - Search query and filters
   */
  saveSearch: async (name, query) => {
    const response = await api.post('/search/saved/', { name, query })
    return response.data
  },

  /**
   * Get saved searches
   */
  getSavedSearches: async () => {
    const response = await api.get('/search/saved/')
    return response.data
  },

  /**
   * Delete saved search
   * @param {string} searchId - Search ID
   */
  deleteSavedSearch: async (searchId) => {
    const response = await api.delete(`/search/saved/${searchId}/`)
    return response.data
  },

  /**
   * Get popular searches
   * @param {number} limit - Number of results
   */
  getPopularSearches: async (limit = 10) => {
    const response = await api.get(`/search/popular/?limit=${limit}`)
    return response.data
  },
}
