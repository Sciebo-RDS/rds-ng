/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}", "./node_modules/primevue/**/*.{vue,js,ts,jsx,tsx}", "../common/web/**/*.{vue,js,ts,jsx,tsx}"],
    theme: {
        extend: {}
    },
    plugins: [require("@tailwindcss/typography")]
};
