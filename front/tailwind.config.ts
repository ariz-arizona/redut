import type { Config } from 'tailwindcss'
import colors from 'tailwindcss/colors'
import _fontFamily from 'tailwindcss/'
import typography from '@tailwindcss/typography'
import forms from '@tailwindcss/forms';

export default <Partial<Config>>{
    theme: {
        extend: {
            colors: {
                primary: {
                    ...colors.cyan,
                    DEFAULT: colors.cyan[500],
                }
            },
            fontFamily: {
                // Bleu Empire (serif)
                'bleu': ['SangBleuEmpire', 'serif'],

                // Euclid Square (sans-serif)
                'euclid': ['EuclidSquare', 'sans-serif'],
            },
        }
    },
    plugins: [typography, forms]
}