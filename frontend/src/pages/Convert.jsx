import { useState } from 'react'
import { motion } from 'framer-motion'
import { toast } from 'react-toastify'
import FileUploader from '../components/FileUploader'

const Convert = () => {
  const [file, setFile] = useState(null)
  const [conversionType, setConversionType] = useState('word_to_pdf')

  const conversionTypes = [
    { value: 'word_to_pdf', label: 'Word to PDF', accept: '.doc,.docx' },
    { value: 'image_to_pdf', label: 'Image to PDF', accept: '.jpg,.jpeg,.png' },
    { value: 'pdf_to_word', label: 'PDF to Word', accept: '.pdf' },
    { value: 'pdf_to_image', label: 'PDF to Image', accept: '.pdf' },
    { value: 'excel_to_pdf', label: 'Excel to PDF', accept: '.xlsx,.xls' },
    { value: 'ppt_to_pdf', label: 'PowerPoint to PDF', accept: '.pptx,.ppt' },
  ]

  const selectedType = conversionTypes.find(t => t.value === conversionType)

  const handleFileSelect = (selectedFile) => {
    setFile(selectedFile)
  }

  const handleConvert = () => {
    if (!file) {
      toast.error('Please select a file')
      return
    }
    toast.info('Conversion feature coming soon!')
  }

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-secondary-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-secondary-900 mb-4">
              Convert Files
            </h1>
            <p className="text-xl text-secondary-600">
              Convert between PDF and other formats
            </p>
          </div>

          <div className="card mb-8">
            <h3 className="text-lg font-semibold text-secondary-900 mb-4">
              Select Conversion Type
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
              {conversionTypes.map((type) => (
                <button
                  key={type.value}
                  onClick={() => setConversionType(type.value)}
                  className={`
                    p-4 rounded-lg border-2 transition-all duration-200
                    ${
                      conversionType === type.value
                        ? 'border-primary bg-primary-50'
                        : 'border-secondary-200 hover:border-primary-300'
                    }
                  `}
                >
                  <span className="font-medium text-secondary-900">{type.label}</span>
                </button>
              ))}
            </div>

            <FileUploader 
              onFileSelect={handleFileSelect} 
              acceptedFileTypes={selectedType?.accept}
            />

            {file && (
              <button
                onClick={handleConvert}
                className="w-full btn-primary mt-6"
              >
                Convert File
              </button>
            )}
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default Convert
