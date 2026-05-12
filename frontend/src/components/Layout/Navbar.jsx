import { Link, useNavigate } from 'react-router-dom'
import { useSelector, useDispatch } from 'react-redux'
import { FiMenu, FiX, FiUser, FiLogOut } from 'react-icons/fi'
import { useState } from 'react'
import { logout } from '../../store/slices/authSlice'

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false)
  const { isAuthenticated, user } = useSelector((state) => state.auth)
  const dispatch = useDispatch()
  const navigate = useNavigate()

  const handleLogout = () => {
    dispatch(logout())
    navigate('/login')
  }

  return (
    <nav className="bg-white shadow-sm border-b border-secondary-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">P</span>
              </div>
              <span className="text-xl font-bold text-secondary-900">PDF Utility</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {isAuthenticated ? (
              <>
                <Link to="/dashboard" className="text-secondary-700 hover:text-primary transition-colors">
                  Dashboard
                </Link>
                <Link to="/compress" className="text-secondary-700 hover:text-primary transition-colors">
                  Compress
                </Link>
                <Link to="/convert" className="text-secondary-700 hover:text-primary transition-colors">
                  Convert
                </Link>
                <div className="flex items-center space-x-4">
                  <span className="text-sm text-secondary-600">{user?.email}</span>
                  <button
                    onClick={handleLogout}
                    className="flex items-center space-x-2 text-secondary-700 hover:text-primary transition-colors"
                  >
                    <FiLogOut />
                    <span>Logout</span>
                  </button>
                </div>
              </>
            ) : (
              <>
                <Link to="/login" className="text-secondary-700 hover:text-primary transition-colors">
                  Login
                </Link>
                <Link to="/register" className="btn-primary">
                  Get Started
                </Link>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-secondary-700 hover:text-primary"
            >
              {isOpen ? <FiX size={24} /> : <FiMenu size={24} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isOpen && (
        <div className="md:hidden border-t border-secondary-200">
          <div className="px-4 pt-2 pb-4 space-y-2">
            {isAuthenticated ? (
              <>
                <Link
                  to="/dashboard"
                  className="block px-3 py-2 rounded-md text-secondary-700 hover:bg-secondary-50"
                  onClick={() => setIsOpen(false)}
                >
                  Dashboard
                </Link>
                <Link
                  to="/compress"
                  className="block px-3 py-2 rounded-md text-secondary-700 hover:bg-secondary-50"
                  onClick={() => setIsOpen(false)}
                >
                  Compress
                </Link>
                <Link
                  to="/convert"
                  className="block px-3 py-2 rounded-md text-secondary-700 hover:bg-secondary-50"
                  onClick={() => setIsOpen(false)}
                >
                  Convert
                </Link>
                <button
                  onClick={() => {
                    handleLogout()
                    setIsOpen(false)
                  }}
                  className="w-full text-left px-3 py-2 rounded-md text-secondary-700 hover:bg-secondary-50"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="block px-3 py-2 rounded-md text-secondary-700 hover:bg-secondary-50"
                  onClick={() => setIsOpen(false)}
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="block px-3 py-2 rounded-md bg-primary text-white hover:bg-primary-600"
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
