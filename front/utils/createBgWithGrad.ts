// utils/backgroundUtils.js

/**
 * Функция для создания фонового изображения с полупрозрачным градиентом.
 * @param {string} imageUrl - URL фонового изображения.
 * @param {string} gradientColor - Цвет градиента в формате rgba (например, 'rgba(0, 0, 0, 0.2)').
 * @returns {string} - Строка для свойства background-image.
 */
export default (imageUrl: string, gradientColor = 'rgba(0, 0, 0, 0.5)') => {
    return `linear-gradient(${gradientColor}, ${gradientColor}), url("${imageUrl}")`;
}