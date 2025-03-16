# Стадия 1: Сборка приложения
FROM node:23-alpine AS builder

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости через npm
RUN npm install

# Копируем остальной код приложения
COPY . .

# Генерируем статический сайт
RUN npm run build && npm run generate

# Стадия 2: Запуск приложения через Nginx
FROM nginx:alpine

# Копируем сгенерированные файлы из стадии сборки в директорию Nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Открываем порт 80 для подключения
EXPOSE 80

# Запускаем Nginx
CMD ["nginx", "-g", "daemon off;"]