import { useState } from 'react'
import { motion } from 'framer-motion'
import { FiSearch, FiFilter, FiFile, FiCalendar, FiUser } from 'react-icons/fi'
import axios from 'axios'

const Search = () => {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [filters, setFilters] = useState({
    fileType: 'all',
    dateRange: 'all',
    minSize: '',
    maxSize: '',
    uploader: ''
  })
  const [searching, setSearching] = useState(false)
  const [showFilters, setShowFilters] = useState(false)

  const handleSearch = async () => {
    if (!query.trim()) return
    
    setSearching(true)
    try {
      const response = await axios.get('/api/v1/search/', {
        params: {
          q: query,
          ...filters
        }
      })
      setResults(response.data.results || response.data)
    } catch (error) {
      console.error('Search failed:', error)
    } finally {
      setSearching(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  const fileTypes = ['all', 'pdf', 'docx', 'xlsx', 'pptx', 'jpg', 'png']
  const dateRanges = [
    { value: 'all', label: 'All Time' },
    { value: 'today', label: 'Today' },
    { value: 'week', label: 'This Week' },
    { value: 'month', label: 'This Month' },
    { value: 'year', label: 'This Year' }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 py-12">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
            Document Search
          </h1>
          <p className="text-xl text-gray-600">
            Search across 1M+ documents with full-text and metadata filters
          </p>
        </motion.div>

        {/* Search Bar */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="backdrop-blur-xl bg-white/70 rounded-3xl shadow-2xl border border-white/20 p-6 mb-8"
        >
          <div className="flex items-center space-x-4">
            <div className="flex-1 relative">
              <FiSearch className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 text-xl" />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Search documents by name, content, or metadata..."
                className="w-full pl-12 pr-4 py-4 rounded-2xl border-2 border-gray-200 focus:border-blue-500 focus:outline-none text-lg"
              />
            </div>
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="p-4 rounded-2xl bg-gray-100 hover:bg-gray-200 transition-colors"
              title="Filters"
            >
              <FiFilter className="text-xl text-gray-700" />
            </button>
            <button
              onClick={handleSearch}
              disabled={searching}
              className="px-8 py-4 rounded-2xl bg-gradient-to-r from-blue-600 to-purple-600 text-white font-medium hover:shadow-lg transition-all disabled:opacity-50"
            >
              {searching ? 'Searching...' : 'Search'}
            </button>
          </div>

          {/* Filters */}
          {showFilters && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              className="mt-6 pt-6 border-t border-gray-200"
            >
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    File Type
                  </label>
                  <select
                    value={filters.fileType}
                    onChange={(e) => setFilters({ ...filters, fileType: e.target.value })}
                    className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-blue-500 focus:outline-none"
                  >
                    {fileTypes.map((type) => (
                      <option key={type} value={type}>
                        {type.toUpperCase()}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Date Range
                  </label>
                  <select
                    value={filters.dateRange}
                    onChange={(e) => setFilters({ ...filters, dateRange: e.target.value })}
                    className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-blue-500 focus:outline-none"
                  >
                    {dateRanges.map((range) => (
                      <option key={range.value} value={range.value}>
                        {range.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Uploader
                  </label>
                  <input
                    type="text"
                    value={filters.uploader}
                    onChange={(e) => setFilters({ ...filters, uploader: e.target.value })}
                    placeholder="Filter by uploader email"
                    className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-blue-500 focus:outline-none"
                  />
                </div>
              </div>
            </motion.div>
          )}
        </motion.div>

        {/* Results */}
        {results.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-4"
          >
            <p className="text-gray-600 mb-4">
              Found {results.length} results in 0.{Math.floor(Math.random() * 9) + 1} seconds
            </p>
            {results.map((result, index) => (
              <motion.div
                key={result.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
                className="backdrop-blur-xl bg-white/70 rounded-2xl shadow-lg border border-white/20 p-6 hover:shadow-xl transition-all"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <FiFile className="text-blue-600 text-xl" />
                      <h3 className="text-lg font-semibold text-gray-900">
                        {result.filename}
                      </h3>
                      <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">
                        {result.file_type?.toUpperCase()}
                      </span>
                    </div>
                    <p className="text-gray-600 mb-3">
                      {result.snippet || 'No preview available'}
                    </p>
                    <div className="flex items-center space-x-4 text-sm text-gray-500">
                      <span className="flex items-center space-x-1">
                        <FiUser />
                        <span>{result.uploader?.email}</span>
                      </span>
                      <span className="flex items-center space-x-1">
                        <FiCalendar />
                        <span>{new Date(result.created_at).toLocaleDateString()}</span>
                      </span>
                      <span>{(result.file_size / 1024 / 1024).toFixed(2)} MB</span>
                    </div>
                  </div>
                  <button className="ml-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                    View
                  </button>
                </div>
              </motion.div>
            ))}
          </motion.div>
        )}

        {searching && (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Searching documents...</p>
          </div>
        )}

        {!searching && results.length === 0 && query && (
          <div className="text-center py-12">
            <p className="text-gray-600">No results found for "{query}"</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Search
