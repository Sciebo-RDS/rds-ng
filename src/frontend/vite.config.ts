import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    publicDir: "static",
    resolve: {
        alias: {
            "@": fileURLToPath(new URL("./src", import.meta.url)),
            "@common": fileURLToPath(new URL("../common/web", import.meta.url)),
            "@assets": fileURLToPath(new URL("../common/assets", import.meta.url))
        }
    },
    build: {
        minify: "esbuild",
        sourcemap: false,
        chunkSizeWarningLimit: 1000,
        rollupOptions: {
            output: {
                manualChunks(id) {
                    if (id.includes('node_modules')) {
                        return 'vendor';
                    }
                }
            }
        }
    },
    server: {
        allowedHosts: true
    },
    envPrefix: "RDS_"
});
