import type { Config } from 'tailwindcss'
import colors from 'tailwindcss/colors'
import tailwindTypography from '@tailwindcss/typography';

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
                ruberoid: ['Ruberoid', 'sans-serif']
            }

        }
    },
    plugins: [tailwindTypography]
}