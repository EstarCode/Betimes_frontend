import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { FiUploadCloud, FiFile } from 'react-icons/fi'
import { motion } from 'framer-motion'

const FileUploader = ({ onFileSelect, acceptedFileTypes = '.pdf', maxSize = 524288000 }) => {
  const onDrop = useCallback(
    (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        onFileSelect(acceptedFiles[0])
      }
    },
    [onFileSelect]
  )

  const { getRootProps, getInputProps, isDragActive, acceptedFiles } = useDropzone({
    onDrop,
    accept: acceptedFileTypes,
    maxSize,
    multiple: false,
  })

  return (
    <div className="w-full">
      <motion.div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-xl p-12 text-center cursor-pointer
          transition-all duration-200
          ${
            isDragActive
              ? 'border-primary bg-primary-50'
              : 'border-secondary-300 hover:border-primary hover:bg-secondary-50'
          }
        `}
        whileHover={{ scale: 1.01 }}
        whileTap={{ scale: 0.99 }}
      >
        <input {...getInputProps()} />
        
        <div className="flex flex-col items-center space-y-4">
          <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center">
            <FiUploadCloud className="text-primary text-3xl" />
          </div>
          
          {isDragActive ? (
            <p className="text-lg font-medium text-primary">Drop your file here...</p>
          ) : (
            <>
              <div>
                <p className="text-lg font-medium text-secondary-900 mb-1">
                  Drag & drop your file here
                </p>
                <p className="text-sm text-secondary-600">
                  or click to browse from your computer
                </p>
              </div>
              <p className="text-xs text-secondary-500">
                Maximum file size: {Math.round(maxSize / 1024 / 1024)}MB
              </p>
            </>
          )}
        </div>
      </motion.div>

      {acceptedFiles.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-4 p-4 bg-secondary-50 rounded-lg flex items-center space-x-3"
        >
          <FiFile className="text-primary text-xl" />
          <div className="flex-1">
            <p className="text-sm font-medium text-secondary-900">{acceptedFiles[0].name}</p>
            <p className="text-xs text-secondary-600">
              {(acceptedFiles[0].size / 1024 / 1024).toFixed(2)} MB
            </p>
          </div>
        </motion.div>
      )}
    </div>
  )
}

export default FileUploader
