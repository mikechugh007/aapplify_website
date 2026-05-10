/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.{html,js}",  // Add this to scan HTML and JS files in templates directory
    "./static/**/*.{html,js}",     // Add this to scan files in static directory
  ],
  theme: {
    extend: {
        screens: {
            xs: '520px',
            sm: '576px',
            md: '768px',
            lg: '991px',
            xl: '1200px',
            xxl: '1400px',
        },
        colors: {
            primary_c: "#2B50AA",
            secondary_c: "#E9D758",
            neural_c: "#FF8552",
            white: "#FFFFFF",
            light_white: "#F7F6F8",
            black: "#272727",
        },
        fontFamily: {
            plus: ['DM Sans', 'sans-serif'],
        }
    },
},
plugins: [
    /**
     * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
     * for forms. If you don't like it or have own styling for forms,
     * comment the line below to disable '@tailwindcss/forms'.
     */
    // require('@tailwindcss/forms'),
    // require('@tailwindcss/typography'),
    // require('@tailwindcss/aspect-ratio'),
],
}
