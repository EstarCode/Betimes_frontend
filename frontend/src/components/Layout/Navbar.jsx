import { Link, useNavigate } from 'react-router-dom'
import { useSelector, useDispatch } from 'react-redux'
import { FiMenu, FiX, FiUser, FiLogOut, FiMoon, FiSun, FiSettings, FiShield } from 'react-icons/fi'
import { useState } from 'react'
import { logout } from '../../store/slices/authSlice'

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false)
  const [darkMode, setDarkMode] = useState(false)
  const { isAuthenticated, user } = useSelector((state) => state.auth)
  const dispatch = useDispatch()
  const navigate = useNavigate()

  const handleLogout = () => {
    dispatch(logout())
    navigate('/login')
  }

  const toggleTheme = () => {
    setDarkMode(!darkMode)
    document.documentElement.classList.toggle('dark')
  }

  return (
    <nav className="backdrop-blur-xl bg-white/80 shadow-lg border-b border-white/20 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                <span className="text-white font-bold text-xl">B</span>
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Betimes Enterprise
              </span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-6">
            {isAuthenticated ? (
              <>
                <Link to="/dashboard" className="text-gray-700 hover:text-blue-600 transition-colors font-medium">
                  Dashboard
                </Link>
                <Link to="/compress" className="text-gray-700 hover:text-blue-600 transition-colors font-medium">
                  Compress
                </Link>
                <Link to="/convert" className="text-gray-700 hover:text-blue-600 transition-colors font-medium">
                  Convert
                </Link>
                <Link to="/workflows" className="text-gray-700 hover:text-blue-600 transition-colors font-medium">
                  Workflows
                </Link>
                {(user?.role === 'Super_Admin' || user?.role === 'Admin') && (
                  <Link to="/admin" className="text-gray-700 hover:text-blue-600 transition-colors font-medium">
                    Admin
                  </Link>
                )}
                
                <button
                  onClick={toggleTheme}
                  className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                  title="Toggle Theme"
                >
                  {darkMode ? <FiSun className="text-gray-700" /> : <FiMoon className="text-gray-700" />}
                </button>

                <div className="flex items-center space-x-3 pl-3 border-l border-gray-200">
                  <div className="flex items-center space-x-2">
                    <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
                      <FiUser className="text-white text-sm" />
                    </div>
                    <div className="text-sm">
                      <p className="font-medium text-gray-900">{user?.first_name || 'User'}</p>
                      <p className="text-xs text-gray-500">{user?.role || 'User'}</p>
                    </div>
                  </div>
                  <button
                    onClick={handleLogout}
                    className="p-2 rounded-lg hover:bg-red-50 text-gray-700 hover:text-red-600 transition-colors"
                    title="Logout"
                  >
                    <FiLogOut />
                  </button>
                </div>
              </>
            ) : (
              <>
                <Link to="/login" className="text-gray-700 hover:text-blue-600 transition-colors font-medium">
                  Login
                </Link>
                <Link to="/register" className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-2 rounded-lg font-medium hover:shadow-lg transition-all">
                  Get Started
                </Link>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center space-x-2">
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              {darkMode ? <FiSun className="text-gray-700" /> : <FiMoon className="text-gray-700" />}
            </button>
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-gray-700 hover:text-blue-600"
            >
              {isOpen ? <FiX size={24} /> : <FiMenu size={24} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isOpen && (
        <div className="md:hidden border-t border-white/20 backdrop-blur-xl bg-white/90">
          <div className="px-4 pt-2 pb-4 space-y-2">
            {isAuthenticated ? (
              <>
                <Link
                  to="/dashboard"
                  className="block px-4 py-3 rounded-lg text-gray-700 hover:bg-blue-50 hover:text-blue-600 font-medium transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  Dashboard
                </Link>
                <Link
                  to="/compress"
                  className="block px-4 py-3 rounded-lg text-gray-700 hover:bg-blue-50 hover:text-blue-600 font-medium transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  Compress
                </Link>
                <Link
                  to="/convert"
                  className="block px-4 py-3 rounded-lg text-gray-700 hover:bg-blue-50 hover:text-blue-600 font-medium transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  Convert
                </Link>
                <Link
                  to="/workflows"
                  className="block px-4 py-3 rounded-lg text-gray-700 hover:bg-blue-50 hover:text-blue-600 font-medium transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  Workflows
                </Link>
                {(user?.role === 'Super_Admin' || user?.role === 'Admin') && (
                  <Link
                    to="/admin"
                    className="block px-4 py-3 rounded-lg text-gray-700 hover:bg-blue-50 hover:text-blue-600 font-medium transition-colors"
                    onClick={() => setIsOpen(false)}
                  >
                    Admin Panel
                  </Link>
                )}
                <Link
                  to="/mfa-setup"
                  className="block px-4 py-3 rounded-lg text-gray-700 hover:bg-blue-50 hover:text-blue-600 font-medium transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  <FiShield className="inline mr-2" />
                  MFA Setup
                </Link>
                <button
                  onClick={() => {
                    handleLogout()
                    setIsOpen(false)
                  }}
                  className="w-full text-left px-4 py-3 rounded-lg text-red-600 hover:bg-red-50 font-medium transition-colors"
                >
                  <FiLogOut className="inline mr-2" />
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="block px-4 py-3 rounded-lg text-gray-700 hover:bg-blue-50 hover:text-blue-600 font-medium transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="block px-4 py-3 rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 text-white font-medium hover:shadow-lg transition-all"
                  onClick={() => setIsOpen(false)}
                >
                  Get Started
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </nav>
  )
}

export default Navbar
