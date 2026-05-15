import { useState } from 'react'
import { motion } from 'framer-motion'
import { FiScissors, FiLayers, FiRotateCw, FiFile } from 'react-icons/fi'
import axios from 'axios'

const PDFTools = () => {
  const [activeTab, setActiveTab] = useState('split')
  const [selectedFile, setSelectedFile] = useState(null)
  const [processing, setProcessing] = useState(false)
  const [result, setResult] = useState(null)

  // Split state
  const [splitRanges, setSplitRanges] = useState([{ start: 1, end: 5, name: 'part1.pdf' }])
  
  // Merge state
  const [mergeFiles, setMergeFiles] = useState([])
  const [createTOC, setCreateTOC] = useState(true)

  // Rotate state
  const [rotation, setRotation] = useState(90)
  const [rotatePages, setRotatePages] = useState('')

  const handleFileSelect = (e) => {
    const file = e.target.files[0]
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file)
      setResult(null)
    } else {
      alert('Please select a PDF file')
    }
  }

  const handleSplitByRange = async () => {
    if (!selectedFile) {
      alert('Please select a PDF file')
      return
    }

    setProcessing(true)
    try {
      const formData = new FormData()
      formData.append('file', selectedFile)
      formData.append('page_ranges', JSON.stringify(splitRanges))

      const response = await axios.post('/api/v1/tools/pdf/split-by-range/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      setResult(response.data)
    } catch (error) {
      console.error('Split failed:', error)
      alert('Split failed: ' + (error.response?.data?.error || error.message))
    } finally {
      setProcessing(false)
    }
  }

  const handleSplitByBookmarks = async () => {
    if (!selectedFile) {
      alert('Please select a PDF file')
      return
    }

    setProcessing(true)
    try {
      const formData = new FormData()
      formData.append('file', selectedFile)

      const response = await axios.post('/api/v1/tools/pdf/split-by-bookmarks/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      setResult(response.data)
    } catch (error) {
      console.error('Split failed:', error)
      alert('Split failed: ' + (error.response?.data?.error || error.message))
    } finally {
      setProcessing(false)
    }
  }

  const handleMerge = async () => {
    if (mergeFiles.length < 2) {
      alert('Please select at least 2 PDF files to merge')
      return
    }

    setProcessing(true)
    try {
      const formData = new FormData()
      mergeFiles.forEach((file, index) => {
        formData.append(`file_${index}`, file)
      })
      formData.append('create_toc', createTOC)

      const response = await axios.post('/api/v1/tools/pdf/merge/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      setResult(response.data)
    } catch (error) {
      console.error('Merge failed:', error)
      alert('Merge failed: ' + (error.response?.data?.error || error.message))
    } finally {
      setProcessing(false)
    }
  }

  const handleRotate = async () => {
    if (!selectedFile) {
      alert('Please select a PDF file')
      return
    }

    setProcessing(true)
    try {
      const formData = new FormData()
      formData.append('file', selectedFile)
      formData.append('rotation', rotation)
      if (rotatePages) {
        formData.append('pages', rotatePages)
      }

      const response = await axios.post('/api/v1/tools/pdf/rotate/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      setResult(response.data)
    } catch (error) {
      console.error('Rotate failed:', error)
      alert('Rotate failed: ' + (error.response?.data?.error || error.message))
    } finally {
      setProcessing(false)
    }
  }

  const addSplitRange = () => {
    setSplitRanges([...splitRanges, { start: 1, end: 1, name: `part${splitRanges.length + 1}.pdf` }])
  }

  const removeSplitRange = (index) => {
    setSplitRanges(splitRanges.filter((_, i) => i !== index))
  }

  const updateSplitRange = (index, field, value) => {
    const updated = [...splitRanges]
    updated[index][field] = value
    setSplitRanges(updated)
  }

  const tabs = [
    { id: 'split', label: 'Split PDF', icon: FiScissors },
    { id: 'merge', label: 'Merge PDFs', icon: FiLayers },
    { id: 'rotate', label: 'Rotate Pages', icon: FiRotateCw },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-teal-50 via-purple-50 to-coral-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold bg-gradient-to-r from-teal-600 to-purple-600 bg-clip-text text-transparent mb-2">
            PDF Tools
          </h1>
          <p className="text-gray-600">Split, merge, and manipulate PDF documents</p>
        </motion.div>

        {/* Tabs */}
        <div className="backdrop-blur-xl bg-white/70 rounded-3xl shadow-xl border border-white/20 mb-6">
          <div className="flex border-b border-gray-200">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => {
                    setActiveTab(tab.id)
                    setResult(null)
                  }}
                  className={`flex items-center space-x-2 px-6 py-4 font-medium transition-colors ${
                    activeTab === tab.id
                      ? 'text-teal-600 border-b-2 border-teal-600'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  <Icon />
                  <span>{tab.label}</span>
                </button>
              )
            })}
          </div>

          <div className="p-6">
            {/* Split Tab */}
            {activeTab === 'split' && (
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Select PDF File
                  </label>
                  <input
                    type="file"
                    accept="application/pdf"
                    onChange={handleFileSelect}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                  />
                  {selectedFile && (
                    <p className="mt-2 text-sm text-gray-600">Selected: {selectedFile.name}</p>
                  )}
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-4">Split by Page Ranges</h3>
                  {splitRanges.map((range, index) => (
                    <div key={index} className="flex items-center space-x-4 mb-3">
                      <input
                        type="number"
                        placeholder="Start"
                        value={range.start}
                        onChange={(e) => updateSplitRange(index, 'start', parseInt(e.target.value))}
                        className="w-24 px-3 py-2 border border-gray-300 rounded-lg"
                        min="1"
                      />
                      <span>to</span>
                      <input
                        type="number"
                        placeholder="End"
                        value={range.end}
                        onChange={(e) => updateSplitRange(index, 'end', parseInt(e.target.value))}
                        className="w-24 px-3 py-2 border border-gray-300 rounded-lg"
                        min="1"
                      />
                      <input
                        type="text"
                        placeholder="Output name"
                        value={range.name}
                        onChange={(e) => updateSplitRange(index, 'name', e.target.value)}
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-lg"
                      />
                      {splitRanges.length > 1 && (
                        <button
                          onClick={() => removeSplitRange(index)}
                          className="px-3 py-2 text-red-600 hover:bg-red-50 rounded-lg"
                        >
                          Remove
                        </button>
                      )}
                    </div>
                  ))}
                  <button
                    onClick={addSplitRange}
                    className="mt-2 px-4 py-2 text-teal-600 hover:bg-teal-50 rounded-lg"
                  >
                    + Add Range
                  </button>
                </div>

                <div className="flex space-x-4">
                  <button
                    onClick={handleSplitByRange}
                    disabled={processing || !selectedFile}
                    className="flex-1 bg-teal-600 text-white py-3 rounded-lg font-medium hover:bg-teal-700 disabled:opacity-50"
                  >
                    {processing ? 'Processing...' : 'Split by Ranges'}
                  </button>
                  <button
                    onClick={handleSplitByBookmarks}
                    disabled={processing || !selectedFile}
                    className="flex-1 bg-purple-600 text-white py-3 rounded-lg font-medium hover:bg-purple-700 disabled:opacity-50"
                  >
                    {processing ? 'Processing...' : 'Split by Bookmarks'}
                  </button>
                </div>
              </div>
            )}

            {/* Merge Tab */}
            {activeTab === 'merge' && (
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Select PDF Files (2-100 files)
                  </label>
                  <input
                    type="file"
                    accept="application/pdf"
                    multiple
                    onChange={(e) => setMergeFiles(Array.from(e.target.files))}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                  />
                  {mergeFiles.length > 0 && (
                    <div className="mt-4 space-y-2">
                      {mergeFiles.map((file, index) => (
                        <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                          <span className="text-sm">{index + 1}. {file.name}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                <div className="flex items-center">
                  <input
                    type="checkbox"
                    checked={createTOC}
                    onChange={(e) => setCreateTOC(e.target.checked)}
                    className="mr-2"
                  />
                  <label className="text-sm text-gray-700">Create Table of Contents</label>
                </div>

                <button
                  onClick={handleMerge}
                  disabled={processing || mergeFiles.length < 2}
                  className="w-full bg-teal-600 text-white py-3 rounded-lg font-medium hover:bg-teal-700 disabled:opacity-50"
                >
                  {processing ? 'Processing...' : `Merge ${mergeFiles.length} Files`}
                </button>
              </div>
            )}

            {/* Rotate Tab */}
            {activeTab === 'rotate' && (
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Select PDF File
                  </label>
                  <input
                    type="file"
                    accept="application/pdf"
                    onChange={handleFileSelect}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Rotation Angle
                  </label>
                  <select
                    value={rotation}
                    onChange={(e) => setRotation(parseInt(e.target.value))}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                  >
                    <option value={90}>90° Clockwise</option>
                    <option value={180}>180°</option>
                    <option value={270}>270° (90° Counter-clockwise)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Pages to Rotate (optional, leave empty for all pages)
                  </label>
                  <input
                    type="text"
                    placeholder="e.g., 1,3,5-10"
                    value={rotatePages}
                    onChange={(e) => setRotatePages(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                  />
                  <p className="mt-1 text-xs text-gray-500">
                    Enter page numbers separated by commas, or ranges with hyphens
                  </p>
                </div>

                <button
                  onClick={handleRotate}
                  disabled={processing || !selectedFile}
                  className="w-full bg-teal-600 text-white py-3 rounded-lg font-medium hover:bg-teal-700 disabled:opacity-50"
                >
                  {processing ? 'Processing...' : 'Rotate Pages'}
                </button>
              </div>
            )}

            {/* Result Display */}
            {result && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-6 p-6 bg-green-50 border border-green-200 rounded-lg"
              >
                <h3 className="text-lg font-semibold text-green-900 mb-4">
                  ✓ Operation Completed Successfully
                </h3>
                <div className="space-y-2 text-sm text-green-800">
                  {result.output_files && (
                    <div>
                      <p className="font-medium">Output Files: {result.output_files.length}</p>
                      {result.output_files.map((file, index) => (
                        <p key={index} className="ml-4">• {file.name}</p>
                      ))}
                    </div>
                  )}
                  {result.total_pages && <p>Total Pages: {result.total_pages}</p>}
                  {result.output_path && <p>Output: {result.output_path}</p>}
                </div>
              </motion.div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default PDFTools
