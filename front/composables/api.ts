import { useRuntimeConfig, useFetch, createError } from '#imports'

export function useApiFetch() {
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase

    const fetchData = <T>(path: string,
        method: 'get' | 'post' = 'get',
        queryParams: Record<string, any> = {},
        body: Record<string, any> | null = null) => {
        const headers = new Headers()
        headers.set('Content-Type', 'application/json')

        // Логирование URL для отладки
        // console.log(`${apiBase}/api/${path}${path.indexOf('?') !== -1 ? '' : '/'}`)

        return useFetch<T>(`${apiBase}/api/${path}${path.indexOf('?') !== -1 ? '' : '/'}`, {
            method: method as any,
            headers,
            query: queryParams,
            body: body ? JSON.stringify(body) : undefined,
            onResponseError({ response }) {
                console.log('Ошибка:', response.status)
                console.log('URL:', response.url)
            },
        })
    }

    return {
        fetchData
    }
}