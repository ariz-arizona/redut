import { useRuntimeConfig, useFetch, createError } from '#imports'

export function useApiFetch() {
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase
    
    const fetchData = <T>(path: string, queryParams: Record<string, any> = {}, global = false) => {
        const headers = new Headers()
        headers.set('Content-Type', 'application/json')
        console.log(`${apiBase}/api/${path}/`)

        return useFetch<T>(`${apiBase}/api/${path}/`, {
            headers,
            query: queryParams, 
            onResponseError({ response }) {
                console.log(response.status)
                console.log(response.url)
                window.location.pathname = '/404'
                throw createError({
                    statusCode: 404,
                    fatal: true
                })
            },
        })
    }

    return {
        fetchData
    }
}