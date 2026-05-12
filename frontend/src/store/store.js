import { configureStore } from '@reduxjs/toolkit'
import authReducer from './slices/authSlice'
import compressionReducer from './slices/compressionSlice'

export const store = configureStore({
  reducer: {
    auth: authReducer,
    compression: compressionReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,
    }),
})
