import api from './api'

/**
 * PDF Tools Service
 * Features: Split, Merge, Rotate, Extract Pages, Reorder
 * International Standards: ISO 32000-2:2020 (PDF 2.0)
 */
export const pdfToolsService = {
  /**
   * Split PDF by page range
   * @param {File} file - PDF file
   * @param {Array} ranges - Array of page ranges [{start: 1, end: 5}, {start: 10, end: 15}]
   */
  splitByRange: async (file, ranges) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('ranges', JSON.stringify(ranges))

    const response = await api.post('/pdf-tools/split/range/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  /**
   * Split PDF by bookmarks
   * @param {File} file - PDF file
   * @param {number} level - Bookmark level to split at (default: 1)
   */
  splitByBookmarks: async (file, level = 1) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('level', level)

    const response = await api.post('/pdf-tools/split/bookmarks/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  /**
   * Merge multiple PDFs
   * @param {File[]} files - Array of PDF files (max 100)
   * @param {Object} options - Merge options
   */
  merge: async (files, options = {}) => {
    if (files.length > 100) {
      throw new Error('Maximum 100 PDFs can be merged at once')
    }

    const formData = new FormData()
    files.forEach((file, index) => {
      formData.append('files', file)
    })
    
    // Options
    if (options.addTableOfContents) {
      formData.append('add_toc', 'true')
    }
    if (options.addPageNumbers) {
      formData.append('add_page_numbers', 'true')
    }
    if (options.outputFilename) {
      formData.append('output_filename', options.outputFilename)
    }

    const response = await api.post('/pdf-tools/merge/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  /**
   * Extract specific pages from PDF
   * @param {File} file - PDF file
   * @param {Array} pages - Array of page numbers [1, 3, 5, 7]
   */
  extractPages: async (file, pages) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('pages', JSON.stringify(pages))

    const response = await api.post('/pdf-tools/extract/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  /**
   * Rotate PDF pages
   * @param {File} file - PDF file
   * @param {Object} rotations - Page rotations {1: 90, 2: 180, 3: 270}
   */
  rotate: async (file, rotations) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('rotations', JSON.stringify(rotations))

    const response = await api.post('/pdf-tools/rotate/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  /**
   * Reorder PDF pages
   * @param {File} file - PDF file
   * @param {Array} order - New page order [3, 1, 2, 5, 4]
   */
  reorder: async (file, order) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('order', JSON.stringify(order))

    const response = await api.post('/pdf-tools/reorder/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  /**
   * Delete pages from PDF
   * @param {File} file - PDF file
   * @param {Array} pages - Pages to delete [2, 4, 6]
   */
  deletePages: async (file, pages) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('pages', JSON.stringify(pages))

    const response = await api.post('/pdf-tools/delete/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  /**
   * Get PDF information
   * @param {File} file - PDF file
   */
  getInfo: async (file) => {
    const formData = new FormData()
    formData.append('file', file)

    const response = await api.post('/pdf-tools/info/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  /**
   * Get PDF bookmarks/outline
   * @param {File} file - PDF file
   */
  getBookmarks: async (file) => {
    const formData = new FormData()
    formData.append('file', file)

    const response = await api.post('/pdf-tools/bookmarks/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  /**
   * Get job status
   * @param {string} jobId - Job ID
   */
  getJob: async (jobId) => {
    const response = await api.get(`/pdf-tools/jobs/${jobId}/`)
    return response.data
  },

  /**
   * Download processed PDF
   * @param {string} jobId - Job ID
   */
  downloadFile: async (jobId) => {
    const response = await api.get(`/pdf-tools/jobs/${jobId}/download/`, {
      responseType: 'blob',
    })
    return response.data
  },

  /**
   * Delete job
   * @param {string} jobId - Job ID
   */
  deleteJob: async (jobId) => {
    const response = await api.delete(`/pdf-tools/jobs/${jobId}/`)
    return response.data
  },
}
