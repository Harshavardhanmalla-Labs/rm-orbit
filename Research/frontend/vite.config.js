import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    host: '0.0.0.0',
    port: 10007,
    strictPort: true,
    allowedHosts: ['research.freedomlabs.in'],
    proxy: {
      '/api': {
        target: 'http://localhost:6420',
        changeOrigin: true,
        ws: true,
        rewrite: (path) => {
          const rewritten = path.replace(/^\/api/, '/api')
          return rewritten.endsWith('/') ? rewritten : rewritten + '/'
        },
      },
    },
  },
})
