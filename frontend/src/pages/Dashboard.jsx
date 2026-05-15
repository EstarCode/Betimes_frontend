import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { FiFile, FiClock, FiTrendingDown, FiUsers, FiActivity, FiDatabase, FiCheckCircle, FiAlertCircle } from 'react-icons/fi'
import axios from 'axios'

const Dashboard = () => {
  const [metrics, setMetrics] = useState(null)
  const [recentActivity, setRecentActivity] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
    const interval = setInterval(fetchDashboardData, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  const fetchDashboardData = async () => {
    try {
      const [metricsRes, activityRes] = await Promise.all([
        axios.get('/api/v1/dashboard/metrics/'),
        axios.get('/api/v1/dashboard/activity/')
      ])
      setMetrics(metricsRes.data)
      setRecentActivity(activityRes.data.results || activityRes.data)
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const stats = [
    {
      icon: <FiFile className="text-3xl" />,
      label: 'Total Documents',
      value: metrics?.total_uploads || 0,
      change: '+12%',
      color: 'from-teal-500 to-teal-600',
      bgColor: 'from-teal-50 to-teal-100'
    },
    {
      icon: <FiActivity className="text-3xl" />,
      label: 'Processing Jobs',
      value: metrics?.processing_jobs || 0,
      change: '5 pending',
      color: 'from-purple-500 to-purple-600',
      bgColor: 'from-purple-50 to-purple-100'
    },
    {
      icon: <FiUsers className="text-3xl" />,
      label: 'Active Users',
      value: metrics?.active_users || 0,
      change: '+8%',
      color: 'from-emerald-500 to-emerald-600',
      bgColor: 'from-emerald-50 to-emerald-100'
    },
    {
      icon: <FiDatabase className="text-3xl" />,
      label: 'Storage Used',
      value: `${((metrics?.storage_used || 0) / 1024 / 1024 / 1024).toFixed(2)} GB`,
      change: '75% capacity',
      color: 'from-coral-500 to-orange-600',
      bgColor: 'from-coral-50 to-orange-100'
    },
  ]

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-teal-50 via-purple-50 to-coral-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-teal-600 mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-teal-50 via-purple-50 to-coral-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold bg-gradient-to-r from-teal-600 to-purple-600 bg-clip-text text-transparent mb-2">
            Dashboard
          </h1>
          <p className="text-gray-600">Real-time system metrics and activity monitoring</p>
        </motion.div>

        {/* Stats Grid with Glassmorphism */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="backdrop-blur-xl bg-white/70 rounded-3xl shadow-xl border border-white/20 p-6 hover:shadow-2xl transition-all duration-300"
            >
              <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${stat.bgColor} flex items-center justify-center mb-4`}>
                <div className={`bg-gradient-to-br ${stat.color} bg-clip-text text-transparent`}>
                  {stat.icon}
                </div>
              </div>
              <p className="text-sm text-gray-600 mb-1">{stat.label}</p>
              <p className="text-3xl font-bold text-gray-900 mb-1">{stat.value}</p>
              <p className="text-xs text-green-600 font-medium">{stat.change}</p>
            </motion.div>
          ))}
        </div>

        {/* Charts and Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* System Health */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="lg:col-span-2 backdrop-blur-xl bg-white/70 rounded-3xl shadow-xl border border-white/20 p-6"
          >
            <h2 className="text-2xl font-bold text-gray-900 mb-6">System Health</h2>
            <div className="space-y-4">
              {[
                { label: 'API Response Time', value: 95, status: 'good', metric: '< 100ms' },
                { label: 'Queue Processing Rate', value: 88, status: 'good', metric: '1.2K/min' },
                { label: 'Error Rate', value: 2, status: 'excellent', metric: '0.02%' },
                { label: 'CPU Usage', value: 45, status: 'good', metric: '45%' },
              ].map((item, index) => (
                <div key={index}>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-gray-700">{item.label}</span>
                    <span className="text-sm text-gray-600">{item.metric}</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${item.value}%` }}
                      transition={{ duration: 1, delay: index * 0.1 }}
                      className={`h-3 rounded-full ${
                        item.status === 'excellent' ? 'bg-gradient-to-r from-emerald-400 to-emerald-600' :
                        item.status === 'good' ? 'bg-gradient-to-r from-teal-400 to-teal-600' :
                        'bg-gradient-to-r from-amber-400 to-amber-600'
                      }`}
                    />
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Quick Actions */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="backdrop-blur-xl bg-white/70 rounded-3xl shadow-xl border border-white/20 p-6"
          >
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Quick Actions</h2>
            <div className="space-y-3">
              {[
                { label: 'Upload Document', icon: FiFile, color: 'blue' },
                { label: 'Create Workflow', icon: FiActivity, color: 'purple' },
                { label: 'View Reports', icon: FiTrendingDown, color: 'green' },
                { label: 'Manage Users', icon: FiUsers, color: 'orange' },
              ].map((action, index) => {
                const Icon = action.icon
                return (
                  <motion.button
                    key={index}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    className={`w-full flex items-center space-x-3 p-4 rounded-2xl bg-gradient-to-r from-${action.color}-50 to-${action.color}-100 hover:shadow-lg transition-all`}
                  >
                    <Icon className={`text-${action.color}-600 text-xl`} />
                    <span className="font-medium text-gray-900">{action.label}</span>
                  </motion.button>
                )
              })}
            </div>
          </motion.div>
        </div>

        {/* Recent Activity */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="backdrop-blur-xl bg-white/70 rounded-3xl shadow-xl border border-white/20 p-6"
        >
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Recent Activity</h2>
          <div className="space-y-3">
            {recentActivity.length === 0 ? (
              <p className="text-center text-gray-600 py-8">No recent activity</p>
            ) : (
              recentActivity.slice(0, 10).map((activity, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className="flex items-center justify-between p-4 bg-white/50 rounded-2xl hover:bg-white/80 transition-all"
                >
                  <div className="flex items-center space-x-3">
                    {activity.status === 'completed' ? (
                      <FiCheckCircle className="text-green-500 text-xl" />
                    ) : (
                      <FiAlertCircle className="text-yellow-500 text-xl" />
                    )}
                    <div>
                      <p className="font-medium text-gray-900">{activity.action}</p>
                      <p className="text-sm text-gray-600">{activity.user?.email}</p>
                    </div>
                  </div>
                  <span className="text-xs text-gray-500">
                    {new Date(activity.timestamp).toLocaleTimeString()}
                  </span>
                </motion.div>
              ))
            )}
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default Dashboard
