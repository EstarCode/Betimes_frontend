import api from './api'

/**
 * Upload Service with Chunked Upload Support
 * Supports large files up to 10GB
 * Resumable uploads with progress tracking
 */
export const uploadService = {
  /**
   * Initialize chunked upload
   * @param {File} file - File to upload
   * @param {Object} metadata - File metadata
   */
  initializeUpload: async (file, metadata = {}) => {
    const response = await api.post('/uploads/initialize/', {
      filename: file.name,
      file_size: file.size,
      content_type: file.type,
      chunk_size: metadata.chunkSize || 5242880, // 5MB default
      ...metadata,
    })
    return response.data
  },

  /**
   * Upload file chunk
   * @param {string} uploadId - Upload ID
   * @param {number} chunkIndex - Chunk index
   * @param {Blob} chunk - File chunk
   * @param {Function} onProgress - Progress callback
   */
  uploadChunk: async (uploadId, chunkIndex, chunk, onProgress) => {
    const formData = new FormData()
    formData.append('chunk', chunk)
    formData.append('chunk_index', chunkIndex)

    const response = await api.post(`/uploads/${uploadId}/chunk/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          )
          onProgress(percentCompleted)
        }
      },
    })
    return response.data
  },

  /**
   * Complete chunked upload
   * @param {string} uploadId - Upload ID
   */
  completeUpload: async (uploadId) => {
    const response = await api.post(`/uploads/${uploadId}/complete/`)
    return response.data
  },

  /**
   * Abort upload
   * @param {string} uploadId - Upload ID
   */
  abortUpload: async (uploadId) => {
    const response = await api.delete(`/uploads/${uploadId}/`)
    return response.data
  },

  /**
   * Get upload status
   * @param {string} uploadId - Upload ID
   */
  getUploadStatus: async (uploadId) => {
    const response = await api.get(`/uploads/${uploadId}/status/`)
    return response.data
  },

  /**
   * Upload file with chunking (helper method)
   * @param {File} file - File to upload
   * @param {Object} options - Upload options
   * @param {Function} onProgress - Progress callback
   */
  uploadFile: async (file, options = {}, onProgress) => {
    const chunkSize = options.chunkSize || 5242880 // 5MB
    const totalChunks = Math.ceil(file.size / chunkSize)

    // Initialize upload
    const { upload_id } = await uploadService.initializeUpload(file, {
      ...options,
      chunkSize,
    })

    try {
      // Upload chunks
      for (let i = 0; i < totalChunks; i++) {
        const start = i * chunkSize
        const end = Math.min(start + chunkSize, file.size)
        const chunk = file.slice(start, end)

        await uploadService.uploadChunk(upload_id, i, chunk, (chunkProgress) => {
          if (onProgress) {
            const overallProgress = Math.round(
              ((i + chunkProgress / 100) / totalChunks) * 100
            )
            onProgress(overallProgress)
          }
        })
      }

      // Complete upload
      const result = await uploadService.completeUpload(upload_id)
      return result
    } catch (error) {
      // Abort upload on error
      await uploadService.abortUpload(upload_id)
      throw error
    }
  },

  /**
   * Simple file upload (for small files)
   * @param {File} file - File to upload
   * @param {Object} metadata - File metadata
   */
  simpleUpload: async (file, metadata = {}) => {
    const formData = new FormData()
    formData.append('file', file)
    
    Object.keys(metadata).forEach((key) => {
      formData.append(key, metadata[key])
    })

    const response = await api.post('/uploads/simple/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  /**
   * Get all uploads
   * @param {Object} filters - Filter options
   */
  getUploads: async (filters = {}) => {
    const params = new URLSearchParams()
    if (filters.status) params.append('status', filters.status)
    if (filters.page) params.append('page', filters.page)

    const response = await api.get(`/uploads/?${params.toString()}`)
    return response.data
  },

  /**
   * Delete upload
   * @param {string} uploadId - Upload ID
   */
  deleteUpload: async (uploadId) => {
    const response = await api.delete(`/uploads/${uploadId}/`)
    return response.data
  },
}
