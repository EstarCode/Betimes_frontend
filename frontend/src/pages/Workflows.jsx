import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { FiPlus, FiCheck, FiX, FiClock, FiAlertCircle } from 'react-icons/fi'
import axios from 'axios'

const Workflows = () => {
  const [workflows, setWorkflows] = useState([])
  const [templates, setTemplates] = useState([])
  const [loading, setLoading] = useState(true)
  const [showCreateModal, setShowCreateModal] = useState(false)

  useEffect(() => {
    fetchWorkflows()
    fetchTemplates()
  }, [])

  const fetchWorkflows = async () => {
    try {
      const response = await axios.get('/api/v1/workflows/instances/')
      setWorkflows(response.data.results || response.data)
    } catch (error) {
      console.error('Failed to fetch workflows:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchTemplates = async () => {
    try {
      const response = await axios.get('/api/v1/workflows/templates/')
      setTemplates(response.data.results || response.data)
    } catch (error) {
      console.error('Failed to fetch templates:', error)
    }
  }

  const handleApprove = async (workflowId, approvalId) => {
    try {
      await axios.post(`/api/v1/workflows/instances/${workflowId}/approve/`, {
        approval_id: approvalId,
        comments: 'Approved'
      })
      fetchWorkflows()
    } catch (error) {
      console.error('Failed to approve:', error)
    }
  }

  const handleReject = async (workflowId, approvalId) => {
    try {
      await axios.post(`/api/v1/workflows/instances/${workflowId}/reject/`, {
        approval_id: approvalId,
        comments: 'Rejected'
      })
      fetchWorkflows()
    } catch (error) {
      console.error('Failed to reject:', error)
    }
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'approved':
        return <FiCheck className="text-green-500" />
      case 'rejected':
        return <FiX className="text-red-500" />
      case 'pending':
        return <FiClock className="text-yellow-500" />
      case 'escalated':
        return <FiAlertCircle className="text-orange-500" />
      default:
        return <FiClock className="text-gray-500" />
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'approved':
        return 'bg-green-100 text-green-700'
      case 'rejected':
        return 'bg-red-100 text-red-700'
      case 'pending':
      case 'in_review':
        return 'bg-yellow-100 text-yellow-700'
      case 'escalated':
        return 'bg-orange-100 text-orange-700'
      default:
        return 'bg-gray-100 text-gray-700'
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Workflow Management</h1>
            <p className="text-gray-600 mt-2">Manage document approval workflows</p>
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          >
            <FiPlus />
            <span>Create Workflow</span>
          </button>
        </div>

        {/* Workflow Templates */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Workflow Templates</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {templates.map((template) => (
              <motion.div
                key={template.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white rounded-lg p-6 shadow-sm border border-gray-200"
              >
                <h3 className="font-semibold text-gray-900 mb-2">{template.name}</h3>
                <p className="text-sm text-gray-600 mb-4">{template.description}</p>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-500">{template.approval_type}</span>
                  <span className="text-blue-600 font-medium">{template.steps?.length || 0} steps</span>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Active Workflows */}
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Active Workflows</h2>
          <div className="space-y-4">
            {workflows.length === 0 ? (
              <div className="bg-white rounded-lg p-12 text-center">
                <p className="text-gray-600">No active workflows</p>
              </div>
            ) : (
              workflows.map((workflow) => (
                <motion.div
                  key={workflow.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-white rounded-lg p-6 shadow-sm border border-gray-200"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-1">
                        {workflow.template?.name || 'Workflow'}
                      </h3>
                      <p className="text-sm text-gray-600">
                        Document: {workflow.document?.filename || 'N/A'}
                      </p>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(workflow.status)}`}>
                      {workflow.status}
                    </span>
                  </div>

                  {/* Approval Steps */}
                  <div className="space-y-3">
                    {workflow.approvals?.map((approval, index) => (
                      <div
                        key={approval.id}
                        className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                      >
                        <div className="flex items-center space-x-3">
                          {getStatusIcon(approval.status)}
                          <div>
                            <p className="text-sm font-medium text-gray-900">
                              Step {index + 1}: {approval.approver?.email || 'Pending'}
                            </p>
                            <p className="text-xs text-gray-500">
                              {approval.approved_at
                                ? `Completed ${new Date(approval.approved_at).toLocaleDateString()}`
                                : 'Awaiting approval'}
                            </p>
                          </div>
                        </div>

                        {approval.status === 'pending' && (
                          <div className="flex space-x-2">
                            <button
                              onClick={() => handleApprove(workflow.id, approval.id)}
                              className="px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700"
                            >
                              Approve
                            </button>
                            <button
                              onClick={() => handleReject(workflow.id, approval.id)}
                              className="px-3 py-1 bg-red-600 text-white text-sm rounded hover:bg-red-700"
                            >
                              Reject
                            </button>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </motion.div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Workflows
