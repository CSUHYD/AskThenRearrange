import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Override with PREFQUEST_BACKEND_URL env var if backend is on a non-default port/host.
// Use 127.0.0.1 (not 'localhost') so Node doesn't try IPv6 first and time out
// when uvicorn is bound to IPv4 only.
const BACKEND = process.env.PREFQUEST_BACKEND_URL ?? 'http://127.0.0.1:8000'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/sessions': BACKEND,
      '/dialogue': BACKEND,
      '/logs': BACKEND,
      '/health': BACKEND,
      '/voice': BACKEND,
    },
  },
})
