import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { FiShield, FiSmartphone, FiKey } from 'react-icons/fi'
import axios from 'axios'

const MFASetup = () => {
  const [step, setStep] = useState(1)
  const [qrCode, setQrCode] = useState('')
  const [secret, setSecret] = useState('')
  const [backupCodes, setBackupCodes] = useState([])
  const [verificationCode, setVerificationCode] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    initializeMFA()
  }, [])

  const initializeMFA = async () => {
    try {
      const response = await axios.post('/api/v1/auth/mfa/setup/')
      setQrCode(response.data.qr_code)
      setSecret(response.data.secret)
    } catch (error) {
      console.error('Failed to initialize MFA:', error)
    }
  }

  const handleVerify = async () => {
    setLoading(true)
    try {
      const response = await axios.post('/api/v1/auth/mfa/verify/', {
        code: verificationCode
      })
      setBackupCodes(response.data.backup_codes)
      setStep(3)
    } catch (error) {
      console.error('Verification failed:', error)
      alert('Invalid code. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const downloadBackupCodes = () => {
    const text = backupCodes.join('\n')
    const blob = new Blob([text], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'betimes-backup-codes.txt'
    a.click()
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12">
      <div className="max-w-2xl mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl shadow-xl p-8"
        >
          {/* Header */}
          <div className="text-center mb-8">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <FiShield className="text-3xl text-blue-600" />
            </div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Enable Two-Factor Authentication
            </h1>
            <p className="text-gray-600">
              Add an extra layer of security to your account
            </p>
          </div>

          {/* Progress Steps */}
          <div className="flex items-center justify-center mb-8">
            {[1, 2, 3].map((s) => (
              <div key={s} className="flex items-center">
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold ${
                    step >= s
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-200 text-gray-500'
                  }`}
                >
                  {s}
                </div>
                {s < 3 && (
                  <div
                    className={`w-16 h-1 ${
                      step > s ? 'bg-blue-600' : 'bg-gray-200'
                    }`}
                  />
                )}
              </div>
            ))}
          </div>

          {/* Step 1: Scan QR Code */}
          {step === 1 && (
            <div className="text-center">
              <FiSmartphone className="text-5xl text-blue-600 mx-auto mb-4" />
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Scan QR Code
              </h2>
              <p className="text-gray-600 mb-6">
                Use an authenticator app like Google Authenticator or Authy to scan this QR code
              </p>
              {qrCode && (
                <div className="bg-white p-4 rounded-lg inline-block mb-4">
                  <img src={qrCode} alt="QR Code" className="w-64 h-64" />
                </div>
              )}
              <div className="bg-gray-50 p-4 rounded-lg mb-6">
                <p className="text-sm text-gray-600 mb-2">Or enter this code manually:</p>
                <code className="text-lg font-mono text-gray-900">{secret}</code>
              </div>
              <button
                onClick={() => setStep(2)}
                className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700"
              >
                Continue
              </button>
            </div>
          )}

          {/* Step 2: Verify Code */}
          {step === 2 && (
            <div className="text-center">
              <FiKey className="text-5xl text-blue-600 mx-auto mb-4" />
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Verify Your Code
              </h2>
              <p className="text-gray-600 mb-6">
                Enter the 6-digit code from your authenticator app
              </p>
              <input
                type="text"
                value={verificationCode}
                onChange={(e) => setVerificationCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                placeholder="000000"
                className="w-full text-center text-3xl font-mono tracking-widest border-2 border-gray-300 rounded-lg py-4 mb-6 focus:border-blue-500 focus:outline-none"
                maxLength={6}
              />
              <button
                onClick={handleVerify}
                disabled={verificationCode.length !== 6 || loading}
                className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Verifying...' : 'Verify & Enable'}
              </button>
            </div>
          )}

          {/* Step 3: Backup Codes */}
          {step === 3 && (
            <div className="text-center">
              <FiCheck className="text-5xl text-green-600 mx-auto mb-4" />
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Save Your Backup Codes
              </h2>
              <p className="text-gray-600 mb-6">
                Store these codes in a safe place. You can use them to access your account if you lose your device.
              </p>
              <div className="bg-gray-50 p-6 rounded-lg mb-6">
                <div className="grid grid-cols-2 gap-3">
                  {backupCodes.map((code, index) => (
                    <div
                      key={index}
                      className="bg-white p-3 rounded border border-gray-200"
                    >
                      <code className="text-sm font-mono text-gray-900">{code}</code>
                    </div>
                  ))}
                </div>
              </div>
              <div className="space-y-3">
                <button
                  onClick={downloadBackupCodes}
                  className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700"
                >
                  Download Backup Codes
                </button>
                <button
                  onClick={() => window.location.href = '/dashboard'}
                  className="w-full bg-gray-200 text-gray-700 py-3 rounded-lg font-medium hover:bg-gray-300"
                >
                  Done
                </button>
              </div>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  )
}

export default MFASetup
