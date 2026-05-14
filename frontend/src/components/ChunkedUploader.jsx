import { useState, useCallback } from 'react'
import { motion } from 'framer-motion'
import { FiUploadCloud, FiFile, FiX, FiCheck, FiAlertCircle } from 'react-icons/fi'
import axios from 'axios'

const ChunkedUploader = ({ onUploadComplete, maxSize = 10737418240 }) => {
  const [files, setFiles] = useState([])
  const [uploading, setUploading] = useState(false)

  const CHUNK_SIZE = 10 * 1024 * 1024 // 10MB chunks

  const handleFileSelect = (e) => {
    const selectedFiles = Array.from(e.target.files).slice(0, 50)
    const fileObjects = selectedFiles.map(file => ({
      file,
      id: Math.random().toString(36).substr(2, 9),
      progress: 0,
      status: 'pending', // pending, uploading, completed, failed
      uploadedChunks: 0,
      totalChunks: Math.ceil(file.size / CHUNK_SIZE),
      error: null
    }))
    setFiles(prev => [...prev, ...fileObjects])
  }

  const uploadFileInChunks = async (fileObj) => {
    const { file, id } = fileObj
    const totalChunks = Math.ceil(file.size / CHUNK_SIZE)
    
    try {
      // Initialize upload
      const initResponse = await axios.post('/api/v1/uploads/initialize/', {
        filename: file.name,
        file_size: file.size,
        total_chunks: totalChunks,
        content_type: file.type
      })

      const uploadId = initResponse.data.upload_id

      // Upload chunks in parallel (4 concurrent)
      const chunkPromises = []
      for (let chunkIndex = 0; chunkIndex < totalChunks; chunkIndex++) {
        const start = chunkIndex * CHUNK_SIZE
        const end = Math.min(start + CHUNK_SIZE, file.size)
        const chunk = file.slice(start, end)

        const formData = new FormData()
        formData.append('upload_id', uploadId)
        formData.append('chunk_index', chunkIndex)
        formData.append('chunk', chunk)

        const promise = axios.post('/api/v1/uploads/chunk/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
          onUploadProgress: (progressEvent) => {
            const chunkProgress = (progressEvent.loaded / progressEvent.total) * 100
            const totalProgress = ((chunkIndex + chunkProgress / 100) / totalChunks) * 100
            updateFileProgress(id, totalProgress, chunkIndex + 1)
          }
        })

        chunkPromises.push(promise)

        // Limit concurrent uploads to 4
        if (chunkPromises.length >= 4) {
          await Promise.all(chunkPromises)
          chunkPromises.length = 0
        }
      }

      // Wait for remaining chunks
      if (chunkPromises.length > 0) {
        await Promise.all(chunkPromises)
      }

      // Complete upload
      const completeResponse = await axios.post('/api/v1/uploads/complete/', {
        upload_id: uploadId
      })

      updateFileStatus(id, 'completed')
      if (onUploadComplete) {
        onUploadComplete(completeResponse.data)
      }

      return completeResponse.data
    } catch (error) {
      updateFileStatus(id, 'failed', error.response?.data?.error || error.message)
      throw error
    }
  }

  const updateFileProgress = (id, progress, uploadedChunks) => {
    setFiles(prev => prev.map(f => 
      f.id === id ? { ...f, progress, uploadedChunks, status: 'uploading' } : f
    ))
  }

  const updateFileStatus = (id, status, error = null) => {
    setFiles(prev => prev.map(f => 
      f.id === id ? { ...f, status, error } : f
    ))
  }

  const handleUploadAll = async () => {
    setUploading(true)
    const pendingFiles = files.filter(f => f.status === 'pending')
    
    try {
      await Promise.all(pendingFiles.map(uploadFileInChunks))
    } catch (error) {
      console.error('Upload error:', error)
    } finally {
      setUploading(false)
    }
  }

  const removeFile = (id) => {
    setFiles(prev => prev.filter(f => f.id !== id))
  }

  const formatBytes = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
  }

  return (
    <div className="w-full space-y-4">
      {/* Upload Area */}
      <div className="relative">
        <input
          type="file"
          multiple
          onChange={handleFileSelect}
          className="hidden"
          id="chunked-file-input"
          accept="*"
        />
        <label
          htmlFor="chunked-file-input"
          className="block border-2 border-dashed border-gray-300 rounded-xl p-12 text-center cursor-pointer hover:border-blue-500 transition-all"
        >
          <FiUploadCloud className="mx-auto text-5xl text-blue-500 mb-4" />
          <p className="text-lg font-medium text-gray-900 mb-2">
            Drag & drop files here or click to browse
          </p>
          <p className="text-sm text-gray-600">
            Upload up to 50 files, max 10GB each
          </p>
        </label>
      </div>

      {/* File List */}
      {files.length > 0 && (
        <div className="space-y-3">
          {files.map((fileObj) => (
            <motion.div
              key={fileObj.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-lg p-4 shadow-sm border border-gray-200"
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center space-x-3 flex-1">
                  <FiFile className="text-blue-500 text-xl" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {fileObj.file.name}
                    </p>
                    <p className="text-xs text-gray-500">
                      {formatBytes(fileObj.file.size)} • {fileObj.uploadedChunks}/{fileObj.totalChunks} chunks
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  {fileObj.status === 'completed' && (
                    <FiCheck className="text-green-500 text-xl" />
                  )}
                  {fileObj.status === 'failed' && (
                    <FiAlertCircle className="text-red-500 text-xl" />
                  )}
                  {fileObj.status === 'pending' && (
                    <button
                      onClick={() => removeFile(fileObj.id)}
                      className="text-gray-400 hover:text-red-500"
                    >
                      <FiX className="text-xl" />
                    </button>
                  )}
                </div>
              </div>

              {/* Progress Bar */}
              {(fileObj.status === 'uploading' || fileObj.status === 'completed') && (
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all ${
                      fileObj.status === 'completed' ? 'bg-green-500' : 'bg-blue-500'
                    }`}
                    style={{ width: `${fileObj.progress}%` }}
                  />
                </div>
              )}

              {fileObj.error && (
                <p className="text-xs text-red-500 mt-2">{fileObj.error}</p>
              )}
            </motion.div>
          ))}
        </div>
      )}

      {/* Upload Button */}
      {files.some(f => f.status === 'pending') && (
        <button
          onClick={handleUploadAll}
          disabled={uploading}
          className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {uploading ? 'Uploading...' : `Upload ${files.filter(f => f.status === 'pending').length} File(s)`}
        </button>
      )}
    </div>
  )
}

export default ChunkedUploader
