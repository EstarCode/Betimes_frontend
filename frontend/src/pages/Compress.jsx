import { useState } from 'react'
import { motion } from 'framer-motion'
import { toast } from 'react-toastify'
import { FiDownload, FiCheck } from 'react-icons/fi'
import FileUploader from '../components/FileUploader'
import { compressionService } from '../services/compressionService'

const Compress = () => {
  const [file, setFile] = useState(null)
  const [compressionLevel, setCompressionLevel] = useState('medium')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)

  const compressionLevels = [
    { value: 'low', label: 'Low', description: 'High quality, small reduction' },
    { value: 'medium', label: 'Medium', description: 'Balanced quality and size' },
    { value: 'high', label: 'High', description: 'Maximum reduction' },
  ]

  const handleFileSelect = (selectedFile) => {
    setFile(selectedFile)
    setResult(null)
  }

  const handleCompress = async () => {
    if (!file) {
      toast.error('Please select a file')
      return
    }

    setLoading(true)

    try {
      const response = await compressionService.compressPDF(file, compressionLevel)
      setResult(response.data)
      toast.success('Compression started! Processing your file...')
      
      // Poll for job status
      pollJobStatus(response.data.id)
    } catch (error) {
      toast.error('Compression failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const pollJobStatus = async (jobId) => {
    const interval = setInterval(async () => {
      try {
        const response = await compressionService.getJob(jobId)
        const job = response.data
        
        if (job.status === 'completed') {
          setResult(job)
          toast.success('Compression completed!')
          clearInterval(interval)
        } else if (job.status === 'failed') {
          toast.error('Compression failed')
          clearInterval(interval)
        }
      } catch (error) {
        clearInterval(interval)
      }
    }, 3000)
  }

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-gradient-to-br from-teal-50 via-purple-50 to-coral-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-teal-600 to-purple-600 bg-clip-text text-transparent mb-4">
              Compress PDF
            </h1>
            <p className="text-xl text-gray-600">
              Reduce PDF file size while maintaining quality
            </p>
          </div>

          <div className="backdrop-blur-xl bg-white/70 rounded-3xl shadow-xl border border-white/20 p-6 mb-8">
            <FileUploader onFileSelect={handleFileSelect} acceptedFileTypes=".pdf" />
          </div>

          {file && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="backdrop-blur-xl bg-white/70 rounded-3xl shadow-xl border border-white/20 p-6 mb-8"
            >
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Compression Level
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {compressionLevels.map((level) => (
                  <button
                    key={level.value}
                    onClick={() => setCompressionLevel(level.value)}
                    className={`
                      p-4 rounded-lg border-2 transition-all duration-200 text-left
                      ${
                        compressionLevel === level.value
                          ? 'border-teal-500 bg-teal-50'
                          : 'border-gray-200 hover:border-teal-300'
                      }
                    `}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-semibold text-gray-900">{level.label}</span>
                      {compressionLevel === level.value && (
                        <FiCheck className="text-teal-600" />
                      )}
                    </div>
                    <p className="text-sm text-gray-600">{level.description}</p>
                  </button>
                ))}
              </div>

              <button
                onClick={handleCompress}
                disabled={loading}
                className="w-full bg-gradient-to-r from-teal-600 to-purple-600 text-white py-3 rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50 mt-6"
              >
                {loading ? 'Compressing...' : 'Compress PDF'}
              </button>
            </motion.div>
          )}

          {result && result.status === 'completed' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="backdrop-blur-xl bg-white/70 rounded-3xl shadow-xl border border-white/20 p-6 bg-emerald-50 border-emerald-200"
            >
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Compression Complete!
              </h3>
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div>
                  <p className="text-sm text-gray-600">Original Size</p>
                  <p className="text-xl font-semibold text-gray-900">
                    {(result.original_size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Compressed Size</p>
                  <p className="text-xl font-semibold text-gray-900">
                    {(result.compressed_size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Reduction</p>
                  <p className="text-xl font-semibold text-emerald-600">
                    {result.compression_ratio}%
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Processing Time</p>
                  <p className="text-xl font-semibold text-gray-900">
                    {result.processing_time.toFixed(2)}s
                  </p>
                </div>
              </div>
              <a
                href={result.compressed_file_url}
                download
                className="w-full bg-gradient-to-r from-teal-600 to-purple-600 text-white py-3 rounded-lg font-semibold hover:shadow-lg transition-all flex items-center justify-center space-x-2"
              >
                <FiDownload />
                <span>Download Compressed PDF</span>
              </a>
            </motion.div>
          )}
        </motion.div>
      </div>
    </div>
  )
}

export default Compress
