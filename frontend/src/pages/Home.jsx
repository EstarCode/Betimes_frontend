import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { FiZap, FiShield, FiClock, FiCheck, FiUploadCloud, FiFileText, FiUsers, FiTrendingUp } from 'react-icons/fi'

const Home = () => {
  const features = [
    {
      icon: <FiUploadCloud className="text-4xl" />,
      title: 'Large File Support',
      description: 'Upload files up to 10GB with resumable chunked uploads',
      color: 'from-blue-500 to-blue-600'
    },
    {
      icon: <FiFileText className="text-4xl" />,
      title: 'Document Conversion',
      description: 'Convert between PDF, Word, Excel, PowerPoint, and more',
      color: 'from-purple-500 to-purple-600'
    },
    {
      icon: <FiUsers className="text-4xl" />,
      title: 'Enterprise Workflows',
      description: 'Multi-step approval chains with routing and escalation',
      color: 'from-green-500 to-green-600'
    },
    {
      icon: <FiShield className="text-4xl" />,
      title: 'Enterprise Security',
      description: 'MFA, RBAC, audit logging, and AES-256 encryption',
      color: 'from-red-500 to-red-600'
    },
    {
      icon: <FiTrendingUp className="text-4xl" />,
      title: 'Real-time Analytics',
      description: 'Dashboard with live metrics and activity monitoring',
      color: 'from-orange-500 to-orange-600'
    },
    {
      icon: <FiClock className="text-4xl" />,
      title: 'High Performance',
      description: 'Process 1M documents/day with 10K concurrent users',
      color: 'from-pink-500 to-pink-600'
    },
  ]

  const stats = [
    { value: '10GB', label: 'Max File Size' },
    { value: '10K', label: 'Concurrent Users' },
    { value: '1M', label: 'Docs/Day' },
    { value: '99.9%', label: 'Uptime' }
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section with Glassmorphism */}
      <section className="relative min-h-screen flex items-center bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 overflow-hidden">
        {/* Animated Background Elements */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-20 left-10 w-72 h-72 bg-blue-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
          <div className="absolute top-40 right-10 w-72 h-72 bg-purple-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
          <div className="absolute bottom-20 left-1/2 w-72 h-72 bg-pink-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            <motion.div
              initial={{ scale: 0.9 }}
              animate={{ scale: 1 }}
              transition={{ duration: 0.5 }}
              className="inline-block mb-6"
            >
              <span className="px-6 py-3 rounded-full bg-gradient-to-r from-blue-600 to-purple-600 text-white text-sm font-semibold shadow-lg">
                ✨ World-Class Enterprise Platform
              </span>
            </motion.div>

            <h1 className="text-6xl md:text-7xl font-bold mb-6">
              <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                Betimes Enterprise
              </span>
              <br />
              <span className="text-gray-900">Document Processing</span>
            </h1>

            <p className="text-2xl text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed">
              Process millions of documents with enterprise-grade security, workflows, and performance.
              Built for scale, designed for excellence.
            </p>

            <div className="flex flex-col sm:flex-row gap-6 justify-center mb-16">
              <Link
                to="/register"
                className="group px-10 py-5 bg-gradient-to-r from-blue-600 to-purple-600 text-white text-lg font-semibold rounded-2xl shadow-2xl hover:shadow-3xl transform hover:scale-105 transition-all duration-300"
              >
                Get Started Free
                <span className="ml-2 group-hover:translate-x-1 inline-block transition-transform">→</span>
              </Link>
              <Link
                to="/dashboard"
                className="px-10 py-5 backdrop-blur-xl bg-white/70 text-gray-900 text-lg font-semibold rounded-2xl border-2 border-white/20 hover:bg-white/90 shadow-xl transition-all duration-300"
              >
                View Dashboard
              </Link>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
              {stats.map((stat, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 + index * 0.1 }}
                  className="backdrop-blur-xl bg-white/60 rounded-2xl p-6 border border-white/20 shadow-lg"
                >
                  <p className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
                    {stat.value}
                  </p>
                  <p className="text-sm text-gray-600 font-medium">{stat.label}</p>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section with Glassmorphism */}
      <section className="py-24 bg-gradient-to-br from-gray-50 to-blue-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-5xl font-bold text-gray-900 mb-4">
              Enterprise Features
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Everything you need for world-class document processing at enterprise scale
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                whileHover={{ y: -10, scale: 1.02 }}
                className="backdrop-blur-xl bg-white/70 rounded-3xl p-8 border border-white/20 shadow-xl hover:shadow-2xl transition-all duration-300"
              >
                <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${feature.color} flex items-center justify-center text-white mb-6 shadow-lg`}>
                  {feature.icon}
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-3">
                  {feature.title}
                </h3>
                <p className="text-gray-600 leading-relaxed">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section with Glassmorphism */}
      <section className="relative py-24 bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 overflow-hidden">
        <div className="absolute inset-0 bg-black/10"></div>
        <div className="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-5xl font-bold text-white mb-6">
              Ready to Transform Your Document Processing?
            </h2>
            <p className="text-2xl text-white/90 mb-12 leading-relaxed">
              Join enterprises worldwide who trust Betimes for mission-critical document workflows
            </p>
            <div className="flex flex-col sm:flex-row gap-6 justify-center">
              <Link
                to="/register"
                className="px-10 py-5 bg-white text-purple-600 text-lg font-bold rounded-2xl shadow-2xl hover:shadow-3xl transform hover:scale-105 transition-all duration-300"
              >
                Start Free Trial
              </Link>
              <Link
                to="/workflows"
                className="px-10 py-5 backdrop-blur-xl bg-white/20 text-white text-lg font-bold rounded-2xl border-2 border-white/30 hover:bg-white/30 shadow-xl transition-all duration-300"
              >
                Explore Workflows
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}

export default Home
