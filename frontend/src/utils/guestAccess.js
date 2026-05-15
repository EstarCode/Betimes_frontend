/**
 * Guest Access Management
 * Tracks document processing for non-authenticated users
 * Allows 3 free document processes before prompting signup
 */

const GUEST_LIMIT = 3
const STORAGE_KEY = 'guest_document_count'

export const guestAccess = {
  /**
   * Get current guest document count
   */
  getCount: () => {
    const count = localStorage.getItem(STORAGE_KEY)
    return count ? parseInt(count) : 0
  },

  /**
   * Increment guest document count
   */
  incrementCount: () => {
    const currentCount = guestAccess.getCount()
    const newCount = currentCount + 1
    localStorage.setItem(STORAGE_KEY, newCount.toString())
    return newCount
  },

  /**
   * Check if guest has reached limit
   */
  hasReachedLimit: () => {
    return guestAccess.getCount() >= GUEST_LIMIT
  },

  /**
   * Get remaining free documents
   */
  getRemainingCount: () => {
    const remaining = GUEST_LIMIT - guestAccess.getCount()
    return remaining > 0 ? remaining : 0
  },

  /**
   * Reset count (called after user signs up/logs in)
   */
  resetCount: () => {
    localStorage.removeItem(STORAGE_KEY)
  },

  /**
   * Check if user can process document
   * Returns { allowed: boolean, remaining: number, message: string }
   */
  canProcess: () => {
    const isAuthenticated = !!localStorage.getItem('token')
    
    if (isAuthenticated) {
      return {
        allowed: true,
        remaining: -1, // Unlimited for authenticated users
        message: 'Authenticated user'
      }
    }

    const remaining = guestAccess.getRemainingCount()
    
    if (remaining > 0) {
      return {
        allowed: true,
        remaining,
        message: `${remaining} free document${remaining > 1 ? 's' : ''} remaining`
      }
    }

    return {
      allowed: false,
      remaining: 0,
      message: 'Free limit reached. Please sign up to continue.'
    }
  }
}
