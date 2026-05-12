import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { FiZap, FiShield, FiClock, FiCheck } from 'react-icons/fi'

const Home = () => {
  const features = [
    {
      icon: <FiZap className="text-3xl" />,
      title: 'Lightning Fast',
      description: 'Process PDFs in seconds with our optimized compression engine',
    },
    {
      icon: <FiShield className="text-3xl" />,
      title: 'Secure & Private',
      description: 'Your files are encrypted and automatically deleted after processing',
    },
    {
      icon: <FiClock className="text-3xl" />,
      title: 'Save Time',
      description: 'Batch process multiple files and automate your workflow',
    },
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-50 via-white to-accent-50 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center"
          >
            <h1 className="text-5xl md:text-6xl font-bold text-secondary-900 mb-6">
              Compress & Convert PDFs
              <span className="block text-primary mt-2">In Seconds</span>
            </h1>
            <p className="text-xl text-secondary-600 mb-8 max-w-2xl mx-auto">
              Professional PDF compression and conversion platform. 
              Reduce file sizes by up to 90% while maintaining quality.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/register" className="btn-primary text-lg px-8 py-4">
                Get Started Free
              </Link>
              <Link to="/compress" className="btn-secondary text-lg px-8 py-4">
                Try Compression
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-secondary-900 mb-4">
              Why Choose PDF Utility?
            </h2>
            <p className="text-xl text-secondary-600">
              Built for professionals who value quality and efficiency
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="card hover:shadow-lg transition-shadow duration-200"
              >
                <div className="w-16 h-16 bg-primary-100 rounded-lg flex items-center justify-center text-primary mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-secondary-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-secondary-600">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-primary text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold mb-6">
            Ready to Get Started?
          </h2>
          <p className="text-xl mb-8 text-primary-100">
            Join thousands of users who trust PDF Utility for their document needs
          </p>
          <Link
            to="/register"
            className="inline-block px-8 py-4 bg-white text-primary rounded-lg font-semibold hover:bg-primary-50 transition-colors"
          >
            Create Free Account
          </Link>
        </div>
      </section>
    </div>
  )
}

export default Home
