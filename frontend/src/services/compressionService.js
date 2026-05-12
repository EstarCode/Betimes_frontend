import api from './api'

export const compressionService = {
  compressPDF: async (file, compressionLevel = 'medium') => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('compression_level', compressionLevel)

    const response = await api.post('/compress/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  getJobs: async () => {
    const response = await api.get('/compress/jobs/')
    return response.data
  },

  getJob: async (jobId) => {
    const response = await api.get(`/compress/jobs/${jobId}/`)
    return response.data
  },

  deleteJob: async (jobId) => {
    const response = await api.delete(`/compress/jobs/${jobId}/delete/`)
    return response.data
  },
}
