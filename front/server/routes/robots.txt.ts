// server/routes/robots.get.ts
export default defineEventHandler(async (event) => {
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase

    // Устанавливаем правильный Content-Type
    event.node.res.setHeader('Content-Type', 'text/plain')

    try {
        const res = await fetch(`${apiBase}/api/site-settings`)
        const data = await res.json()

        const allowIndexing = Boolean(data.allow_in_robots_txt)

        const rules = []

        rules.push('User-agent: *')

        if (allowIndexing) {
            rules.push('Disallow:')
        } else {
            rules.push('Disallow: /')
        }

        // Всегда запрещаем /admin
        rules.push('Disallow: /admin')

        return rules.join('\n')
    } catch (error) {
        console.error('Ошибка при генерации robots.txt:', error)
        return ['User-agent: *', 'Disallow: /'].join('\n')
    }
})