import api from './api'

/**
 * Document Conversion Service
 * Supports: PDF to DOCX, DOCX to PDF, Image to PDF, OCR
 * International Standards: ISO 32000 (PDF), ISO/IEC 29500 (DOCX)
 */
export const conversionService = {
  /**
   * Convert document between formats
   * @param {File} file - Source file
   * @param {string} targetFormat - Target format (pdf, docx, jpg, png)
   * @param {Object} options - Conversion options
   */
  convert: async (file, targetFormat, options = {}) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('target_format', targetFormat)
    
    // Add optional parameters
    if (options.quality) formData.append('quality', options.quality)
    if (options.dpi) formData.append('dpi', options.dpi)
    if (options.colorMode) formData.append('color_mode', options.colorMode)
    if (options.pageSize) formData.append('page_size', options.pageSize)

    const response = await api.post('/convert/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  /**
   * Perform OCR on image or PDF
   * @param {File} file - Image or PDF file
   * @param {Object} options - OCR options
   */
  ocr: async (file, options = {}) => {
    const formData = new FormData()
    formData.append('file', file)
    
    // OCR options
    if (options.language) formData.append('language', options.language) // ISO 639-1 language codes
    if (options.outputFormat) formData.append('output_format', options.outputFormat)
    if (options.preprocessImage) formData.append('preprocess_image', options.preprocessImage)

    const response = await api.post('/convert/ocr/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  /**
   * Get conversion job status
   * @param {string} jobId - Job ID
   */
  getJob: async (jobId) => {
    const response = await api.get(`/convert/jobs/${jobId}/`)
    return response.data
  },

  /**
   * Get all conversion jobs
   * @param {Object} filters - Filter options
   */
  getJobs: async (filters = {}) => {
    const params = new URLSearchParams()
    if (filters.status) params.append('status', filters.status)
    if (filters.format) params.append('format', filters.format)
    if (filters.page) params.append('page', filters.page)

    const response = await api.get(`/convert/jobs/?${params.toString()}`)
    return response.data
  },

  /**
   * Download converted file
   * @param {string} jobId - Job ID
   */
  downloadFile: async (jobId) => {
    const response = await api.get(`/convert/jobs/${jobId}/download/`, {
      responseType: 'blob',
    })
    return response.data
  },

  /**
   * Delete conversion job
   * @param {string} jobId - Job ID
   */
  deleteJob: async (jobId) => {
    const response = await api.delete(`/convert/jobs/${jobId}/`)
    return response.data
  },

  /**
   * Batch convert multiple files
   * @param {File[]} files - Array of files
   * @param {string} targetFormat - Target format
   * @param {Object} options - Conversion options
   */
  batchConvert: async (files, targetFormat, options = {}) => {
    const formData = new FormData()
    files.forEach((file) => {
      formData.append('files', file)
    })
    formData.append('target_format', targetFormat)
    
    // Add options
    Object.keys(options).forEach((key) => {
      formData.append(key, options[key])
    })

    const response = await api.post('/convert/batch/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  /**
   * Get supported formats
   */
  getSupportedFormats: async () => {
    const response = await api.get('/convert/formats/')
    return response.data
  },
}
