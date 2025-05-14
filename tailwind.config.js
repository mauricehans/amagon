/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        amazon: {
          blue: {
            DEFAULT: '#232F3E',
            light: '#37475A',
            dark: '#131921',
          },
          orange: {
            DEFAULT: '#FF9900',
            hover: '#FA8900',
          },
          yellow: {
            DEFAULT: '#FEBD69',
            hover: '#F3A847',
          },
          green: {
            DEFAULT: '#00A8E1',
          },
          teal: '#00A8E1',
          success: '#067D62',
          warning: '#FFD814',
          error: '#B12704',
          gray: {
            light: '#F3F3F3',
            medium: '#DDDDDD',
            dark: '#767676',
          },
        },
      },
      fontFamily: {
        sans: ['"Amazon Ember"', 'Arial', 'sans-serif'],
      },
      boxShadow: {
        'product': '0 2px 5px 0 rgba(213, 217, 217, .5)',
        'button': '0 2px 5px 0 rgba(213, 217, 217, .5)',
        'header': '0 1px 3px rgba(0, 0, 0, 0.1)',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
};