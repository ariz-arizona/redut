import type { Config } from 'tailwindcss'
import colors from 'tailwindcss/colors'
import _fontFamily from 'tailwindcss/'
import typography from '@tailwindcss/typography'
import forms from '@tailwindcss/forms';

const new_colors = {
    'midnight': {
        '50': '#f6f7f9',
        '100': '#ebeff3',
        '200': '#d3dbe4',
        '300': '#adbccc',
        '400': '#8098b0',
        '500': '#607c97',
        '600': '#4c637d',
        '700': '#3e5166',
        '800': '#364556',
        '900': '#313c49',
        '950': '#181d24',
    },
    'provincial-pink': {
        '50': '#fbf7f5',
        '100': '#f9f0ec',
        '200': '#f2dfd6',
        '300': '#e9c7b8',
        '400': '#daa68f',
        '500': '#c9876a',
        '600': '#b46d4e',
        '700': '#965a3f',
        '800': '#7d4d37',
        '900': '#694433',
        '950': '#382117',
    },

}

export default <Partial<Config>>{
    theme: {
        extend: {
            colors: {
                ...new_colors,
                primary: {
                    ...new_colors.midnight,
                    DEFAULT: new_colors.midnight[500],
                }
            },
            fontFamily: {
                // Bleu Empire (serif)
                'bleu': ['SangBleuEmpire', 'serif'],

                // Euclid Square (sans-serif)
                'euclid': ['EuclidSquare', 'sans-serif'],
                'wonder': ['WonderGardenScript']
            },
        }
    },
    plugins: [typography, forms]
}