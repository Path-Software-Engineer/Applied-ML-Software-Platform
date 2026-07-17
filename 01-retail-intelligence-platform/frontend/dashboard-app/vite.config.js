import { defineConfig } from "vite";

const localApiProxy = {
  "/api": "http://127.0.0.1:8000",
};

export default defineConfig({
  resolve: {
    preserveSymlinks: true,
  },
  server: {
    host: "127.0.0.1",
    port: 5173,
    strictPort: true,
    proxy: localApiProxy,
  },
  preview: {
    host: "127.0.0.1",
    port: 4173,
    strictPort: true,
    proxy: localApiProxy,
  },
});
