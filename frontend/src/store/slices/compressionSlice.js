import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  jobs: [],
  currentJob: null,
  loading: false,
  error: null,
}

const compressionSlice = createSlice({
  name: 'compression',
  initialState,
  reducers: {
    setJobs: (state, action) => {
      state.jobs = action.payload
    },
    addJob: (state, action) => {
      state.jobs.unshift(action.payload)
    },
    updateJob: (state, action) => {
      const index = state.jobs.findIndex(job => job.id === action.payload.id)
      if (index !== -1) {
        state.jobs[index] = action.payload
      }
    },
    setCurrentJob: (state, action) => {
      state.currentJob = action.payload
    },
    setLoading: (state, action) => {
      state.loading = action.payload
    },
    setError: (state, action) => {
      state.error = action.payload
    },
  },
})

export const { setJobs, addJob, updateJob, setCurrentJob, setLoading, setError } = compressionSlice.actions
export default compressionSlice.reducer
