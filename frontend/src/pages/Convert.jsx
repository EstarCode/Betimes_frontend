import { useState } from 'react'
import { motion } from 'framer-motion'
import { FiFileText, FiImage, FiFile } from 'react-icons/fi'
import axios from 'axios'
import ChunkedUploader from '../components/ChunkedUploader'

const Convert = () => {
  const [conversionType, setConversionType] = useState('pdf_to_word')
  const [converting, setConverting] = useState(false)
  const [result, setResult] = useState(null)

  const conversionTypes = [
    { value: 'pdf_to_word', label: 'PDF to Word', icon: FiFileText, accept: '.pdf' },
    { value: 'word_to_pdf', label: 'Word to PDF', icon: FiFileText, accept: '.doc,.docx' },
    { value: 'pdf_to_image', label: 'PDF to Image', icon: FiImage, accept: '.pdf' },
    { value: 'excel_to_pdf', label: 'Excel to PDF', icon: FiFile, accept: '.xlsx,.xls' },
    { value: 'ppt_to_pdf', label: 'PowerPoint to PDF', icon: FiFile, accept: '.pptx,.ppt' },
    { value: 'text_to_pdf', label: 'Text to PDF', icon: FiFileText, accept: '.txt' },
  ]

  const selectedType = conversionTypes.find(t => t.value === conversionType)

  const handleUploadComplete = async (uploadData) => {
    setConverting(true)
    try {
      const response = await axios.post('/api/v1/convert/', {
        document_id: uploadData.document_id,
        conversion_type: conversionType
      })
      setResult(response.data)
    } catch (error) {
      console.error('Conversion failed:', error)
      alert('Conversion failed. Please try again.')
    } finally {
      setConverting(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-50 py-12">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent mb-4">
              Document Conversion
            </h1>
            <p className="text-xl text-gray-600">
              Convert between PDF, Word, Excel, PowerPoint, and more
            </p>
          </div>

          {/* Glassmorphism Card */}
          <div className="backdrop-blur-xl bg-white/70 rounded-3xl shadow-2xl border border-white/20 p-8 mb-8">
            <h3 className="text-2xl font-semibold text-gray-900 mb-6">
              Select Conversion Type
            </h3>
            
            {/* Conversion Type Grid */}
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
              {conversionTypes.map((type) => {
                const Icon = type.icon
                return (
                  <motion.button
                    key={type.value}
                    onClick={() => setConversionType(type.value)}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className={`
                      p-6 rounded-2xl border-2 transition-all duration-300
                      ${
                        conversionType === type.value
                          ? 'border-blue-500 bg-gradient-to-br from-blue-50 to-purple-50 shadow-lg'
                          : 'border-gray-200 bg-white/50 hover:border-blue-300'
                      }
                    `}
                  >
                    <Icon className={`text-3xl mx-auto mb-3 ${
                      conversionType === type.value ? 'text-blue-600' : 'text-gray-600'
                    }`} />
                    <span className="font-medium text-gray-900 text-sm">{type.label}</span>
                  </motion.button>
                )
              })}
            </div>

            {/* Upload Area */}
            <ChunkedUploader onUploadComplete={handleUploadComplete} />

            {converting && (
              <div className="mt-6 text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                <p className="text-gray-600">Converting your document...</p>
              </div>
            )}

            {result && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-6 p-6 bg-green-50 rounded-2xl border border-green-200"
              >
                <p className="text-green-800 font-medium mb-4">✓ Conversion completed successfully!</p>
                <a
                  href={result.download_url}
                  download
                  className="inline-block bg-green-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-green-700"
                >
                  Download Converted File
                </a>
              </motion.div>
            )}
          </div>

          {/* Features */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              { title: 'High Quality', desc: 'Preserves formatting and layout' },
              { title: 'Fast Processing', desc: 'Convert files in seconds' },
              { title: 'Secure', desc: 'Files encrypted and auto-deleted' }
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="backdrop-blur-xl bg-white/60 rounded-2xl p-6 border border-white/20"
              >
                <h4 className="font-semibold text-gray-900 mb-2">{feature.title}</h4>
                <p className="text-sm text-gray-600">{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default Convert
