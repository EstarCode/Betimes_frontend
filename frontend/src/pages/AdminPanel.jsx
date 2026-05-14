import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { FiUsers, FiSettings, FiActivity, FiDatabase, FiShield } from 'react-icons/fi'
import axios from 'axios'

const AdminPanel = () => {
  const [activeTab, setActiveTab] = useState('users')
  const [users, setUsers] = useState([])
  const [auditLogs, setAuditLogs] = useState([])
  const [systemMetrics, setSystemMetrics] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [activeTab])

  const fetchData = async () => {
    setLoading(true)
    try {
      if (activeTab === 'users') {
        const response = await axios.get('/api/v1/auth/users/')
        setUsers(response.data.results || response.data)
      } else if (activeTab === 'audit') {
        const response = await axios.get('/api/v1/audit/logs/')
        setAuditLogs(response.data.results || response.data)
      } else if (activeTab === 'metrics') {
        const response = await axios.get('/api/v1/dashboard/metrics/')
        setSystemMetrics(response.data)
      }
    } catch (error) {
      console.error('Failed to fetch data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleRoleChange = async (userId, newRole) => {
    try {
      await axios.patch(`/api/v1/auth/users/${userId}/`, { role: newRole })
      fetchData()
    } catch (error) {
      console.error('Failed to update role:', error)
    }
  }

  const handleDeactivateUser = async (userId) => {
    try {
      await axios.post(`/api/v1/auth/users/${userId}/deactivate/`)
      fetchData()
    } catch (error) {
      console.error('Failed to deactivate user:', error)
    }
  }

  const tabs = [
    { id: 'users', label: 'User Management', icon: FiUsers },
    { id: 'audit', label: 'Audit Logs', icon: FiShield },
    { id: 'metrics', label: 'System Metrics', icon: FiActivity },
    { id: 'storage', label: 'Storage', icon: FiDatabase },
    { id: 'settings', label: 'Settings', icon: FiSettings },
  ]

  const roles = ['Super_Admin', 'Admin', 'Manager', 'Reviewer', 'Processor', 'Viewer']

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Admin Panel</h1>
          <p className="text-gray-600 mt-2">Manage users, workflows, and system settings</p>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-6">
          <div className="flex border-b border-gray-200">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 px-6 py-4 font-medium transition-colors ${
                    activeTab === tab.id
                      ? 'text-blue-600 border-b-2 border-blue-600'
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
            {loading ? (
              <div className="flex items-center justify-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              </div>
            ) : (
              <>
                {/* User Management */}
                {activeTab === 'users' && (
                  <div>
                    <div className="flex justify-between items-center mb-6">
                      <h2 className="text-xl font-semibold text-gray-900">Users</h2>
                      <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                        Add User
                      </button>
                    </div>
                    <div className="overflow-x-auto">
                      <table className="w-full">
                        <thead>
                          <tr className="border-b border-gray-200">
                            <th className="text-left py-3 px-4 font-semibold text-gray-700">Email</th>
                            <th className="text-left py-3 px-4 font-semibold text-gray-700">Name</th>
                            <th className="text-left py-3 px-4 font-semibold text-gray-700">Role</th>
                            <th className="text-left py-3 px-4 font-semibold text-gray-700">MFA</th>
                            <th className="text-left py-3 px-4 font-semibold text-gray-700">Status</th>
                            <th className="text-left py-3 px-4 font-semibold text-gray-700">Actions</th>
                          </tr>
                        </thead>
                        <tbody>
                          {users.map((user) => (
                            <tr key={user.id} className="border-b border-gray-100">
                              <td className="py-3 px-4 text-sm text-gray-900">{user.email}</td>
                              <td className="py-3 px-4 text-sm text-gray-900">
                                {user.first_name} {user.last_name}
                              </td>
                              <td className="py-3 px-4">
                                <select
                                  value={user.role}
                                  onChange={(e) => handleRoleChange(user.id, e.target.value)}
                                  className="text-sm border border-gray-300 rounded px-2 py-1"
                                >
                                  {roles.map((role) => (
                                    <option key={role} value={role}>
                                      {role}
                                    </option>
                                  ))}
                                </select>
                              </td>
                              <td className="py-3 px-4">
                                <span
                                  className={`px-2 py-1 rounded-full text-xs ${
                                    user.mfa_enabled
                                      ? 'bg-green-100 text-green-700'
                                      : 'bg-gray-100 text-gray-700'
                                  }`}
                                >
                                  {user.mfa_enabled ? 'Enabled' : 'Disabled'}
                                </span>
                              </td>
                              <td className="py-3 px-4">
                                <span
                                  className={`px-2 py-1 rounded-full text-xs ${
                                    user.is_active
                                      ? 'bg-green-100 text-green-700'
                                      : 'bg-red-100 text-red-700'
                                  }`}
                                >
                                  {user.is_active ? 'Active' : 'Inactive'}
                                </span>
                              </td>
                              <td className="py-3 px-4">
                                <button
                                  onClick={() => handleDeactivateUser(user.id)}
                                  className="text-sm text-red-600 hover:text-red-700"
                                >
                                  Deactivate
                                </button>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}

                {/* Audit Logs */}
                {activeTab === 'audit' && (
                  <div>
                    <h2 className="text-xl font-semibold text-gray-900 mb-6">Audit Logs</h2>
                    <div className="space-y-3">
                      {auditLogs.map((log) => (
                        <div
                          key={log.id}
                          className="bg-gray-50 rounded-lg p-4 border border-gray-200"
                        >
                          <div className="flex items-start justify-between">
                            <div>
                              <p className="font-medium text-gray-900">{log.event_type}</p>
                              <p className="text-sm text-gray-600 mt-1">{log.description}</p>
                              <p className="text-xs text-gray-500 mt-2">
                                {log.user?.email} • {new Date(log.timestamp).toLocaleString()}
                              </p>
                            </div>
                            <span className="text-xs text-gray-500">{log.ip_address}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* System Metrics */}
                {activeTab === 'metrics' && systemMetrics && (
                  <div>
                    <h2 className="text-xl font-semibold text-gray-900 mb-6">System Metrics</h2>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      <div className="bg-blue-50 rounded-lg p-6">
                        <p className="text-sm text-blue-600 font-medium mb-2">Total Uploads</p>
                        <p className="text-3xl font-bold text-blue-900">
                          {systemMetrics.total_uploads || 0}
                        </p>
                      </div>
                      <div className="bg-green-50 rounded-lg p-6">
                        <p className="text-sm text-green-600 font-medium mb-2">Active Users</p>
                        <p className="text-3xl font-bold text-green-900">
                          {systemMetrics.active_users || 0}
                        </p>
                      </div>
                      <div className="bg-purple-50 rounded-lg p-6">
                        <p className="text-sm text-purple-600 font-medium mb-2">Storage Used</p>
                        <p className="text-3xl font-bold text-purple-900">
                          {((systemMetrics.storage_used || 0) / 1024 / 1024 / 1024).toFixed(2)} GB
                        </p>
                      </div>
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default AdminPanel
