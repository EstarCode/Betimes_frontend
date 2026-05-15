import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { FiZap, FiShield, FiClock, FiCheck, FiUploadCloud, FiFileText, FiUsers, FiTrendingUp, FiScissors, FiLayers, FiLock, FiUnlock, FiDroplet, FiGrid } from 'react-icons/fi'

const Home = () => {
  const pdfTools = [
    { name: 'Merge PDF', icon: FiLayers, desc: 'Combine multiple PDFs into one', link: '/pdf-tools/merge', color: 'from-blue-500 to-cyan-500' },
    { name: 'Split PDF', icon: FiScissors, desc: 'Split PDF into separate pages', link: '/pdf-tools/split', color: 'from-purple-500 to-pink-500' },
    { name: 'Compress PDF', icon: FiTrendingUp, desc: 'Reduce PDF file size', link: '/compress', color: 'from-green-500 to-emerald-500' },
    { name: 'Convert PDF', icon: FiFileText, desc: 'Convert PDF to other formats', link: '/convert', color: 'from-orange-500 to-red-500' },
    { name: 'Protect PDF', icon: FiLock, desc: 'Add password protection', link: '/pdf-tools/protect', color: 'from-indigo-500 to-blue-500' },
    { name: 'Unlock PDF', icon: FiUnlock, desc: 'Remove PDF password', link: '/pdf-tools/unlock', color: 'from-yellow-500 to-orange-500' },
    { name: 'Watermark PDF', icon: FiDroplet, desc: 'Add watermark to PDF', link: '/pdf-tools/watermark', color: 'from-teal-500 to-cyan-500' },
    { name: 'Organize PDF', icon: FiGrid, desc: 'Reorder PDF pages', link: '/pdf-tools/organize', color: 'from-rose-500 to-pink-500' },
  ]

  const features = [
    { icon: FiZap, title: 'Lightning Fast', desc: 'Process documents in seconds with our optimized engine' },
    { icon: FiShield, title: 'Secure & Private', desc: 'Your files are encrypted and automatically deleted after processing' },
    { icon: FiClock, title: 'No Signup Required', desc: 'Process up to 3 documents for free without creating an account' },
    { icon: FiUsers, title: 'User Friendly', desc: 'Simple drag-and-drop interface that anyone can use' },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-20 pb-32">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-600/10 via-purple-600/10 to-pink-600/10"></div>
        <div className="container mx-auto px-4 relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center max-w-4xl mx-auto"
          >
            <h1 className="text-5xl md:text-7xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent mb-6">
              Professional PDF Tools
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 mb-8">
              Merge, split, compress, and convert PDFs instantly. No signup required for your first 3 documents!
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/pdf-tools/merge"
                className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold hover:shadow-2xl hover:scale-105 transition-all duration-300"
              >
                <FiUploadCloud className="inline mr-2" />
                Start Processing
              </Link>
              <Link
                to="/register"
                className="px-8 py-4 bg-white text-gray-800 rounded-xl font-semibold hover:shadow-xl hover:scale-105 transition-all duration-300 border-2 border-gray-200"
              >
                Create Free Account
              </Link>
            </div>
            <p className="mt-6 text-sm text-gray-500">
              <FiCheck className="inline text-green-500 mr-1" />
              No credit card required • Process 3 documents free
            </p>
          </motion.div>
        </div>
      </section>

      {/* PDF Tools Grid */}
      <section className="py-20 bg-white/50 backdrop-blur-sm">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold text-gray-800 mb-4">All PDF Tools</h2>
            <p className="text-gray-600 text-lg">Everything you need to work with PDFs</p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {pdfTools.map((tool, index) => (
              <motion.div
                key={tool.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
              >
                <Link
                  to={tool.link}
                  className="block p-6 bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 border border-gray-100"
                >
                  <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${tool.color} flex items-center justify-center mb-4`}>
                    <tool.icon className="text-white text-2xl" />
                  </div>
                  <h3 className="text-xl font-bold text-gray-800 mb-2">{tool.name}</h3>
                  <p className="text-gray-600 text-sm">{tool.desc}</p>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold text-gray-800 mb-4">Why Choose Betimes?</h2>
            <p className="text-gray-600 text-lg">Fast, secure, and easy to use</p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="text-center p-6"
              >
                <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
                  <feature.icon className="text-white text-2xl" />
                </div>
                <h3 className="text-xl font-bold text-gray-800 mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600">
        <div className="container mx-auto px-4 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold text-white mb-6">Ready to Get Started?</h2>
            <p className="text-xl text-white/90 mb-8">Process your first 3 documents absolutely free!</p>
            <Link
              to="/pdf-tools/merge"
              className="inline-block px-8 py-4 bg-white text-purple-600 rounded-xl font-semibold hover:shadow-2xl hover:scale-105 transition-all duration-300"
            >
              Start Now - No Signup Required
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  )
}

export default Home
