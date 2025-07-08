/** @type {import("tailwindcss").Config} */
const primeui = require("tailwindcss-primeui");

export default {
    content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}", "../common/web/**/*.{vue,js,ts,jsx,tsx}"],
    plugins: [primeui],
    theme: {
        fontFamily: {
            sans: ["ui-sans-serif", "system-ui", "sans-serif", "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"]
        }
    }
};
