import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
export default defineConfig({
  plugins: [react()],
  resolve: { alias: { '@': path.resolve(__dirname, './src') } },
  server: {
    host: '0.0.0.0', port: 6201, strictPort: true,
    allowedHosts: ['.freedomlabs.in', 'localhost'],
    proxy: { '/api': { target: 'http://localhost:6200', changeOrigin: true } },
  },
  preview: { host: '0.0.0.0', port: 6201, strictPort: true },
});
