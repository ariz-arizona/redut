import type { Config } from 'tailwindcss'
import colors from 'tailwindcss/colors'

export default <Partial<Config>>{
    theme: {
        extend: {
            colors: {
                primary: {
                    ...colors.emerald,
                    DEFAULT: colors.emerald[500],
                }
            }
        }
    }
}