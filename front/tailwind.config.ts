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
    'sandal': {
        '50': '#f8f6f2',
        '100': '#ece5d9',
        '200': '#d7c9b0',
        '300': '#c3ac86',
        '400': '#b5946a',
        '500': '#ac835e',
        '600': '#94674b',
        '700': '#7c5241',
        '800': '#674339',
        '900': '#563831',
        '950': '#2f1e19',
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