/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}",
        "../web-common/**/*.{vue,js,ts,jsx,tsx}",
        "../../common/web/**/*.{vue,js,ts,jsx,tsx}"
    ],
    theme: {
        extend: {},
    },
    plugins: []
}
