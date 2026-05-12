import { Routes, Route, Navigate } from 'react-router-dom'
import { useSelector } from 'react-redux'
import Layout from './components/Layout/Layout'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Compress from './pages/Compress'
import Convert from './pages/Convert'
import NotFound from './pages/NotFound'

function App() {
  const { isAuthenticated } = useSelector((state) => state.auth)

  const PrivateRoute = ({ children }) => {
    return isAuthenticated ? children : <Navigate to="/login" />
  }

  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="login" element={<Login />} />
        <Route path="register" element={<Register />} />
        <Route
          path="dashboard"
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          }
        />
        <Route
          path="compress"
          element={
            <PrivateRoute>
              <Compress />
            </PrivateRoute>
          }
        />
        <Route
          path="convert"
          element={
            <PrivateRoute>
              <Convert />
            </PrivateRoute>
          }
        />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  )
}

export default App
