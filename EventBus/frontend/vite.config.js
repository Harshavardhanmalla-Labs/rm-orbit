import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

const allowedHosts = ['.freedomlabs.in', 'localhost', '127.0.0.1'];

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5179,
    strictPort: true,
    allowedHosts,
  },
  preview: {
    host: '0.0.0.0',
    port: 5179,
    strictPort: true,
    allowedHosts,
  }
});
