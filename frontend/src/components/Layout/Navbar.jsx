import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useState } from 'react'
import { FiMenu, FiX, FiUser, FiLogOut, FiScissors, FiLayers, FiLock, FiUnlock, FiDroplet, FiGrid, FiFileText, FiTrendingUp, FiChevronDown } from 'react-icons/fi'
import { motion, AnimatePresence } from 'framer-motion'

const Navbar = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [pdfToolsOpen, setPdfToolsOpen] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()
  
  // Check if user is logged in
  const isAuthenticated = localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user') || '{}')

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('user')
    navigate('/login')
  }

  const pdfTools = [
    { name: 'Merge PDF', icon: FiLayers, link: '/pdf-tools/merge' },
    { name: 'Split PDF', icon: FiScissors, link: '/pdf-tools/split' },
    { name: 'Compress PDF', icon: FiTrendingUp, link: '/compress' },
    { name: 'Convert PDF', icon: FiFileText, link: '/convert' },
    { name: 'Protect PDF', icon: FiLock, link: '/pdf-tools/protect' },
    { name: 'Unlock PDF', icon: FiUnlock, link: '/pdf-tools/unlock' },
    { name: 'Watermark PDF', icon: FiDroplet, link: '/pdf-tools/watermark' },
    { name: 'Organize PDF', icon: FiGrid, link: '/pdf-tools/organize' },
  ]

  const isActive = (path) => location.pathname === path

  return (
    <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-200 shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-gradient-to-br from-teal-600 to-purple-600 rounded-lg flex items-center justify-center">
              <FiFileText className="text-white text-xl" />
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-teal-600 to-purple-600 bg-clip-text text-transparent">
              Betimes
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-1">
            <Link
              to="/"
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                isActive('/') ? 'bg-teal-50 text-teal-600' : 'text-gray-700 hover:bg-gray-50'
              }`}
            >
              Home
            </Link>

            {/* PDF Tools Dropdown */}
            <div className="relative">
              <button
                onMouseEnter={() => setPdfToolsOpen(true)}
                onMouseLeave={() => setPdfToolsOpen(false)}
                className="px-4 py-2 rounded-lg font-medium text-gray-700 hover:bg-gray-50 transition-all flex items-center"
              >
                PDF Tools
                <FiChevronDown className={`ml-1 transition-transform ${pdfToolsOpen ? 'rotate-180' : ''}`} />
              </button>

              <AnimatePresence>
                {pdfToolsOpen && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    transition={{ duration: 0.2 }}
                    onMouseEnter={() => setPdfToolsOpen(true)}
                    onMouseLeave={() => setPdfToolsOpen(false)}
                    className="absolute top-full left-0 mt-2 w-64 bg-white rounded-xl shadow-2xl border border-gray-100 py-2"
                  >
                    {pdfTools.map((tool) => (
                      <Link
                        key={tool.name}
                        to={tool.link}
                        className="flex items-center px-4 py-3 hover:bg-teal-50 transition-colors"
                      >
                        <tool.icon className="text-teal-600 mr-3" />
                        <span className="text-gray-700 font-medium">{tool.name}</span>
                      </Link>
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {isAuthenticated ? (
              <>
                <Link
                  to="/dashboard"
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    isActive('/dashboard') ? 'bg-teal-50 text-teal-600' : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  Dashboard
                </Link>
                <div className="flex items-center space-x-2 ml-4">
                  <div className="px-3 py-1 bg-gradient-to-r from-teal-600 to-purple-600 text-white rounded-lg text-sm">
                    {user.email}
                  </div>
                  <button
                    onClick={handleLogout}
                    className="px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg font-medium transition-all flex items-center"
                  >
                    <FiLogOut className="mr-2" />
                    Logout
                  </button>
                </div>
              </>
            ) : (
              <div className="flex items-center space-x-2 ml-4">
                <Link
                  to="/login"
                  className="px-4 py-2 text-gray-700 hover:bg-gray-50 rounded-lg font-medium transition-all"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="px-6 py-2 bg-gradient-to-r from-teal-600 to-purple-600 text-white rounded-lg font-medium hover:shadow-lg transition-all"
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 text-gray-700 hover:bg-gray-100 rounded-lg"
          >
            {mobileMenuOpen ? <FiX size={24} /> : <FiMenu size={24} />}
          </button>
        </div>

        {/* Mobile Menu */}
        <AnimatePresence>
          {mobileMenuOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="md:hidden py-4 border-t border-gray-200"
            >
              <Link
                to="/"
                className="block px-4 py-3 text-gray-700 hover:bg-gray-50 rounded-lg font-medium"
                onClick={() => setMobileMenuOpen(false)}
              >
                Home
              </Link>

              <div className="px-4 py-2 text-sm font-semibold text-gray-500 uppercase">PDF Tools</div>
              {pdfTools.map((tool) => (
                <Link
                  key={tool.name}
                  to={tool.link}
                  className="flex items-center px-4 py-3 text-gray-700 hover:bg-gray-50 rounded-lg"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  <tool.icon className="mr-3 text-teal-600" />
                  {tool.name}
                </Link>
              ))}

              {isAuthenticated ? (
                <>
                  <Link
                    to="/dashboard"
                    className="block px-4 py-3 text-gray-700 hover:bg-gray-50 rounded-lg font-medium mt-4"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    Dashboard
                  </Link>
                  <button
                    onClick={() => {
                      handleLogout()
                      setMobileMenuOpen(false)
                    }}
                    className="w-full text-left px-4 py-3 text-red-600 hover:bg-red-50 rounded-lg font-medium flex items-center"
                  >
                    <FiLogOut className="mr-2" />
                    Logout
                  </button>
                </>
              ) : (
                <div className="mt-4 space-y-2">
                  <Link
                    to="/login"
                    className="block px-4 py-3 text-center text-gray-700 hover:bg-gray-50 rounded-lg font-medium border border-gray-200"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    Login
                  </Link>
                  <Link
                    to="/register"
                    className="block px-4 py-3 text-center bg-gradient-to-r from-teal-600 to-purple-600 text-white rounded-lg font-medium"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    Sign Up
                  </Link>
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </nav>
  )
}

export default Navbar
