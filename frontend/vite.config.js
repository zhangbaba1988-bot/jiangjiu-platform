import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  // GitHub Pages 部署在 /jiangjiu-platform/ 子路径，base 必须与之匹配，否则 /assets/* 404 白屏
  base: process.env.VITE_BASE || '/jiangjiu-platform/',
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@use "@/styles/variables.scss" as *;`
      }
    }
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          echarts: ['echarts'],
          elementPlus: ['element-plus'],
          vendor: ['vue', 'vue-router', 'pinia', 'axios', 'vant']
        }
      }
    }
  },
  server: {
    port: 3001,
    open: false,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
