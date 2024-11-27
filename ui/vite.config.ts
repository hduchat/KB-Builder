import { fileURLToPath, URL } from 'node:url'
import type { ProxyOptions } from 'vite'
import { defineConfig, loadEnv } from 'vite'

import vue from '@vitejs/plugin-vue'
import DefineOptions from 'unplugin-vue-define-options/vite'

const envDir = './env'
// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const ENV = loadEnv(mode, envDir)
  const proxyConf: Record<string, string | ProxyOptions> = {}
  proxyConf['/api'] = {
    //http://192.168.30.238:8088
    //http://127.0.0.1:8088
    target: ENV.VITE_SERVER_PATH,
    changeOrigin: true,
    rewrite: (path) => path.replace(ENV.VITE_BASE_PATH, '/')
  }
  return {
    preflight: false,
    lintOnSave: false,
    base: ENV.VITE_BASE_PATH,
    envDir: envDir,
    plugins: [vue(), DefineOptions()],
    server: {
      cors: true,
      host: '0.0.0.0',
      port: Number(ENV.VITE_APP_PORT),
      strictPort: true,
      proxy: proxyConf
    },
    build: {
      outDir: 'dist/ui'
    },
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    }
  }
})
