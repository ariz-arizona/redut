// types/pageData.ts

interface Image {
    id: number;
    image: string;
    alt_text: string | null;
    url: string | null;
    title: string | null;
    text: string | null;
}
type BlockType = 'text' | 'text_right' | 'gallery' | 'slider'
interface Block {
    content: string;
    content_rendered: string;
    id: number;
    images: Image[];
    order: number;
    page: number;
    title: string;
    sub_title: string | null;
    menu_title: string | null;
    slug: string;
    type: BlockType;
    link: null | string
    external_link: null | string
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