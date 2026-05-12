import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'

const NotFound = () => {
  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center bg-secondary-50">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <h1 className="text-9xl font-bold text-primary mb-4">404</h1>
        <h2 className="text-3xl font-bold text-secondary-900 mb-4">Page Not Found</h2>
        <p className="text-xl text-secondary-600 mb-8">
          The page you're looking for doesn't exist.
        </p>
        <Link to="/" className="btn-primary">
          Go Home
        </Link>
      </motion.div>
    </div>
  )
}

export default NotFound
