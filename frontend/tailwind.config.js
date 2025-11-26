/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
        './src/components/**/*.{js,ts,jsx,tsx,mdx}',
        './src/app/**/*.{js,ts,jsx,tsx,mdx}',
    ],
    theme: {
        extend: {
            colors: {
                cyber: {
                    black: '#0a0a0a',
                    dark: '#111111',
                    gray: '#222222',
                    neon: '#00ff9d',
                    pink: '#ff00ff',
                    blue: '#00ffff',
                },
            },
            fontFamily: {
                mono: ['monospace'],
            },
        },
    },
    plugins: [],
}
