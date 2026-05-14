import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { FiZoomIn, FiZoomOut, FiRotateCw, FiDownload, FiChevronLeft, FiChevronRight } from 'react-icons/fi'

const DocumentViewer = ({ documentUrl, documentType = 'pdf' }) => {
  const [zoom, setZoom] = useState(100)
  const [rotation, setRotation] = useState(0)
  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [showThumbnails, setShowThumbnails] = useState(true)

  const handleZoomIn = () => {
    setZoom(prev => Math.min(prev + 25, 400))
  }

  const handleZoomOut = () => {
    setZoom(prev => Math.max(prev - 25, 25))
  }

  const handleRotate = () => {
    setRotation(prev => (prev + 90) % 360)
  }

  const handleDownload = () => {
    window.open(documentUrl, '_blank')
  }

  const handlePageChange = (page) => {
    setCurrentPage(Math.max(1, Math.min(page, totalPages)))
  }

  return (
    <div className="h-screen flex flex-col bg-gray-900">
      {/* Toolbar */}
      <div className="bg-gray-800 border-b border-gray-700 px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => setShowThumbnails(!showThumbnails)}
              className="text-white hover:text-blue-400 transition-colors"
            >
              Thumbnails
            </button>
            <div className="flex items-center space-x-2 text-white">
              <button
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={currentPage === 1}
                className="p-2 hover:bg-gray-700 rounded disabled:opacity-50"
              >
                <FiChevronLeft />
              </button>
              <span className="text-sm">
                {currentPage} / {totalPages}
              </span>
              <button
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={currentPage === totalPages}
                className="p-2 hover:bg-gray-700 rounded disabled:opacity-50"
              >
                <FiChevronRight />
              </button>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={handleZoomOut}
              className="p-2 text-white hover:bg-gray-700 rounded"
              title="Zoom Out"
            >
              <FiZoomOut />
            </button>
            <span className="text-white text-sm w-16 text-center">{zoom}%</span>
            <button
              onClick={handleZoomIn}
              className="p-2 text-white hover:bg-gray-700 rounded"
              title="Zoom In"
            >
              <FiZoomIn />
            </button>
            <button
              onClick={handleRotate}
              className="p-2 text-white hover:bg-gray-700 rounded"
              title="Rotate"
            >
              <FiRotateCw />
            </button>
            <button
              onClick={handleDownload}
              className="p-2 text-white hover:bg-gray-700 rounded"
              title="Download"
            >
              <FiDownload />
            </button>
          </div>
        </div>
      </div>

      {/* Viewer Area */}
      <div className="flex-1 flex overflow-hidden">
        {/* Thumbnail Sidebar */}
        {showThumbnails && (
          <div className="w-48 bg-gray-800 border-r border-gray-700 overflow-y-auto p-2">
            <div className="space-y-2">
              {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                <button
                  key={page}
                  onClick={() => setCurrentPage(page)}
                  className={`w-full p-2 rounded ${
                    currentPage === page ? 'bg-blue-600' : 'bg-gray-700 hover:bg-gray-600'
                  }`}
                >
                  <div className="aspect-[8.5/11] bg-white rounded mb-1"></div>
                  <p className="text-white text-xs text-center">{page}</p>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Document Display */}
        <div className="flex-1 overflow-auto bg-gray-900 flex items-center justify-center p-8">
          <motion.div
            style={{
              transform: `scale(${zoom / 100}) rotate(${rotation}deg)`,
              transformOrigin: 'center center'
            }}
            className="bg-white shadow-2xl"
          >
            {documentType === 'pdf' ? (
              <iframe
                src={documentUrl}
                className="w-[800px] h-[1100px]"
                title="Document Viewer"
              />
            ) : (
              <img
                src={documentUrl}
                alt="Document"
                className="max-w-full h-auto"
              />
            )}
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default DocumentViewer
