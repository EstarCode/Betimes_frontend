import api from './api'

/**
 * Workflow Service
 * Enterprise workflow management with approval chains
 * Compliance: ISO 9001 Quality Management
 */
export const workflowService = {
  /**
   * Get all workflows
   * @param {Object} filters - Filter options
   */
  getWorkflows: async (filters = {}) => {
    const params = new URLSearchParams()
    if (filters.status) params.append('status', filters.status)
    if (filters.type) params.append('type', filters.type)
    if (filters.page) params.append('page', filters.page)

    const response = await api.get(`/workflows/?${params.toString()}`)
    return response.data
  },

  /**
   * Get workflow by ID
   * @param {string} workflowId - Workflow ID
   */
  getWorkflow: async (workflowId) => {
    const response = await api.get(`/workflows/${workflowId}/`)
    return response.data
  },

  /**
   * Create new workflow
   * @param {Object} workflowData - Workflow data
   */
  createWorkflow: async (workflowData) => {
    const response = await api.post('/workflows/', workflowData)
    return response.data
  },

  /**
   * Update workflow
   * @param {string} workflowId - Workflow ID
   * @param {Object} workflowData - Updated workflow data
   */
  updateWorkflow: async (workflowId, workflowData) => {
    const response = await api.patch(`/workflows/${workflowId}/`, workflowData)
    return response.data
  },

  /**
   * Delete workflow
   * @param {string} workflowId - Workflow ID
   */
  deleteWorkflow: async (workflowId) => {
    const response = await api.delete(`/workflows/${workflowId}/`)
    return response.data
  },

  /**
   * Submit document to workflow
   * @param {string} workflowId - Workflow ID
   * @param {string} documentId - Document ID
   * @param {Object} metadata - Additional metadata
   */
  submitDocument: async (workflowId, documentId, metadata = {}) => {
    const response = await api.post(`/workflows/${workflowId}/submit/`, {
      document_id: documentId,
      metadata,
    })
    return response.data
  },

  /**
   * Approve workflow step
   * @param {string} workflowId - Workflow ID
   * @param {string} stepId - Step ID
   * @param {Object} data - Approval data
   */
  approve: async (workflowId, stepId, data = {}) => {
    const response = await api.post(`/workflows/${workflowId}/steps/${stepId}/approve/`, data)
    return response.data
  },

  /**
   * Reject workflow step
   * @param {string} workflowId - Workflow ID
   * @param {string} stepId - Step ID
   * @param {Object} data - Rejection data
   */
  reject: async (workflowId, stepId, data = {}) => {
    const response = await api.post(`/workflows/${workflowId}/steps/${stepId}/reject/`, data)
    return response.data
  },

  /**
   * Request changes in workflow
   * @param {string} workflowId - Workflow ID
   * @param {string} stepId - Step ID
   * @param {Object} data - Change request data
   */
  requestChanges: async (workflowId, stepId, data = {}) => {
    const response = await api.post(`/workflows/${workflowId}/steps/${stepId}/request-changes/`, data)
    return response.data
  },

  /**
   * Get workflow history
   * @param {string} workflowId - Workflow ID
   */
  getHistory: async (workflowId) => {
    const response = await api.get(`/workflows/${workflowId}/history/`)
    return response.data
  },

  /**
   * Get pending approvals for current user
   */
  getPendingApprovals: async () => {
    const response = await api.get('/workflows/pending/')
    return response.data
  },

  /**
   * Get workflow templates
   */
  getTemplates: async () => {
    const response = await api.get('/workflows/templates/')
    return response.data
  },

  /**
   * Create workflow from template
   * @param {string} templateId - Template ID
   * @param {Object} data - Workflow data
   */
  createFromTemplate: async (templateId, data) => {
    const response = await api.post(`/workflows/templates/${templateId}/create/`, data)
    return response.data
  },

  /**
   * Get workflow statistics
   * @param {string} workflowId - Workflow ID (optional)
   */
  getStatistics: async (workflowId = null) => {
    const url = workflowId 
      ? `/workflows/${workflowId}/statistics/`
      : '/workflows/statistics/'
    const response = await api.get(url)
    return response.data
  },
}
