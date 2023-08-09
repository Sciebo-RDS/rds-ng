import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        vue(),
    ],
    publicDir: "static",
    resolve: {
        alias: {
            "@": fileURLToPath(new URL("./src", import.meta.url)),
            "@common": fileURLToPath(new URL("../common/web", import.meta.url)),
            "@assets": fileURLToPath(new URL("../common/assets", import.meta.url)),
        }
    },
    build: {
        minify: false,  // Set to "esbuild" to enable minification
    }
});
