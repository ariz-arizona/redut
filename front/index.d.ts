// types/pageData.ts

interface Image {
    id: number;
    image: string;
    alt_text: string | null;
    url: string | null;
    title: string | null;
    text: string | null;
}
type BlockType = 'text' | 'lead' | 'gallery' | 'slider' | 'feedback';

interface Block {
    content: string; // Markdown-контент
    content_rendered: string; // Отрендеренный HTML
    id: number; // ID блока
    images: Image[]; // Массив изображений (если применимо)
    order: number; // Порядок отображения
    page: number; // ID страницы, к которой привязан блок
    title: string; // Заголовок блока
    sub_title: string | null; // Подзаголовок (опционально)
    menu_title: string | null; // Заголовок для меню (опционально)
    slug: string; // Уникальный идентификатор блока
    type: BlockType; // Тип блока
    link: string | null; // Внутренняя ссылка (опционально)
    external_link: string | null; // Внешняя ссылка (опционально)
    is_text_right: boolean; // Флаг для расположения текста справа (true) или слева (false)
}

interface PageData {
    blocks: Block[];
    id: number;
    is_homepage: boolean;
    meta_description: string;
    meta_title: string | null;
    slug: string;
    title: string;
}
interface SiteSettings {
    id: number; // Уникальный идентификатор
    phone_number: string; // Номер телефона
    logo: string | null; // Логотип (путь к файлу или null)
    footer_text: string; // Текст футера
    is_enabled: boolean; // Флаг активности
}