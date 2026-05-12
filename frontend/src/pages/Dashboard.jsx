import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { FiFile, FiClock, FiTrendingDown } from 'react-icons/fi'
import { compressionService } from '../services/compressionService'
import { authService } from '../services/authService'

const Dashboard = () => {
  const [jobs, setJobs] = useState([])
  const [analytics, setAnalytics] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const jobsResponse = await compressionService.getJobs()
      setJobs(jobsResponse.data?.results || jobsResponse.data || [])
      
      // Fetch user analytics
      const profileResponse = await authService.getProfile()
      setAnalytics({
        compression: {
          total_jobs: jobsResponse.data?.count || 0,
          avg_compression_ratio: 0
        },
        storage: {
          used: profileResponse.data?.storage_used || 0,
          limit: profileResponse.data?.storage_limit || 1073741824
        }
      })
    } catch (error) {
      console.error('Failed to fetch data:', error)
    } finally {
      setLoading(false)
    }
  }

  const stats = [
    {
      icon: <FiFile className="text-2xl" />,
      label: 'Total Jobs',
      value: analytics?.compression?.total_jobs || 0,
      color: 'bg-blue-100 text-blue-600'
    },
    {
      icon: <FiTrendingDown className="text-2xl" />,
      label: 'Avg Compression',
      value: `${analytics?.compression?.avg_compression_ratio?.toFixed(1) || 0}%`,
      color: 'bg-green-100 text-green-600'
    },
    {
      icon: <FiClock className="text-2xl" />,
      label: 'Storage Used',
      value: `${((analytics?.storage?.used || 0) / 1024 / 1024).toFixed(0)} MB`,
      color: 'bg-purple-100 text-purple-600'
    },
  ]

  if (loading) {
    return (
      <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-secondary-600">Loading...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-secondary-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h1 className="text-4xl font-bold text-secondary-900 mb-8">Dashboard</h1>

          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            {stats.map((stat, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="card"
              >
                <div className="flex items-center space-x-4">
                  <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${stat.color}`}>
                    {stat.icon}
                  </div>
                  <div>
                    <p className="text-sm text-secondary-600">{stat.label}</p>
                    <p className="text-2xl font-bold text-secondary-900">{stat.value}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Recent Jobs */}
          <div className="card">
            <h2 className="text-2xl font-bold text-secondary-900 mb-6">Recent Jobs</h2>
            {jobs.length === 0 ? (
              <p className="text-center text-secondary-600 py-8">
                No compression jobs yet. Start by compressing your first PDF!
              </p>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-secondary-200">
                      <th className="text-left py-3 px-4 text-sm font-semibold text-secondary-700">
                        Status
                      </th>
                      <th className="text-left py-3 px-4 text-sm font-semibold text-secondary-700">
                        Level
                      </th>
                      <th className="text-left py-3 px-4 text-sm font-semibold text-secondary-700">
                        Original Size
                      </th>
                      <th className="text-left py-3 px-4 text-sm font-semibold text-secondary-700">
                        Compressed Size
                      </th>
                      <th className="text-left py-3 px-4 text-sm font-semibold text-secondary-700">
                        Reduction
                      </th>
                      <th className="text-left py-3 px-4 text-sm font-semibold text-secondary-700">
                        Date
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {jobs.slice(0, 10).map((job) => (
                      <tr key={job.id} className="border-b border-secondary-100">
                        <td className="py-3 px-4">
                          <span className={`
                            px-2 py-1 rounded-full text-xs font-medium
                            ${job.status === 'completed' ? 'bg-green-100 text-green-700' : ''}
                            ${job.status === 'processing' ? 'bg-blue-100 text-blue-700' : ''}
                            ${job.status === 'failed' ? 'bg-red-100 text-red-700' : ''}
                            ${job.status === 'pending' ? 'bg-yellow-100 text-yellow-700' : ''}
                          `}>
                            {job.status}
                          </span>
                        </td>
                        <td className="py-3 px-4 text-sm text-secondary-900 capitalize">
                          {job.compression_level}
                        </td>
                        <td className="py-3 px-4 text-sm text-secondary-900">
                          {(job.original_size / 1024 / 1024).toFixed(2)} MB
                        </td>
                        <td className="py-3 px-4 text-sm text-secondary-900">
                          {job.compressed_size ? `${(job.compressed_size / 1024 / 1024).toFixed(2)} MB` : '-'}
                        </td>
                        <td className="py-3 px-4 text-sm font-semibold text-green-600">
                          {job.compression_ratio ? `${job.compression_ratio}%` : '-'}
                        </td>
                        <td className="py-3 px-4 text-sm text-secondary-600">
                          {new Date(job.created_at).toLocaleDateString()}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default Dashboard
