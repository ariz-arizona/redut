// types/pageData.ts

interface Image {
    id: number;
    image: string;
    alt_text: string | null;
    title: string | null;
    text: string | null;
    link: string | null; // Внутренняя ссылка (опционально)
    external_link: string | null; // Внешняя ссылка (опционально)
    btn_title: string | null;
    text: string | null
    text_rendered: string | null
}
type BlockType = 'text' | 'lead' | 'gallery' | 'slider' | 'full_image' | 'feedback' | 'category' | 'calc';

interface SmallCategory {
    title: string; // Название категории
    slug: string;  // Уникальный идентификатор категории
}
interface Block {
    content_md: string; // Markdown-контент
    content: string; // Отрендеренный HTML
    id: number; // ID блока
    images: Image[]; // Массив изображений (если применимо)
    order: number; // Порядок отображения
    page: number; // ID страницы, к которой привязан блок
    title: string; // Заголовок блока
    sub_title: string | null; // Подзаголовок (опционально)
    btn_title: string | null;
    slug: string; // Уникальный идентификатор блока
    type: BlockType; // Тип блока
    link: string | null; // Внутренняя ссылка (опционально)
    external_link: string | null; // Внешняя ссылка (опционально)
    is_text_right: boolean; // Флаг для расположения текста справа (true) или слева (false)
    is_text_styled: boolean;
    category: SmallCategory
    color_scheme: 'dark' | 'light'
    menu_title: string | null
}

interface PageData {
    blocks: Block[];
    id: number;
    is_homepage: boolean;
    meta_description: string;
    meta_title: string | null;
    slug: string;
    title: string;
    created_at: string
    updated_at: string
    preview_image: string
    preview_text: string
}
interface CategoryData {
    id: number; // Уникальный идентификатор категории
    title: string; // Заголовок категории
    slug: string; // Slug для URL
    meta_description: string;
    meta_title: string | null;
    blocks: Block[]; // Массив связанных страниц (может быть пустым)
    preview_image: string
}
interface Document {
    id: number; // Уникальный идентификатор документа
    title: string; // Название документа
    file: string; // Путь к файлу документа
    description: string | null; // Описание документа (может быть null)
    uploaded_at: string; // Дата загрузки документа (ISO формат, например, "2023-10-01T12:34:56Z")
}

// Интерфейс для TopItem
interface TopItem {
    id: number; // Уникальный идентификатор элемента
    type: "page" | "category"; // Тип элемента: страница или категория
    slug: string; // Slug страницы или категории
    block: string; // Slug блока
    title: string; // Заголовок элемента
    order: number; // Порядок элемента
}

// Общий интерфейс для ContentObject
interface ContentObject {
    id: number; // Уникальный идентификатор объекта
    title: string; // Заголовок объекта
    slug?: string; // Slug (необязательно, зависит от типа объекта)
    description?: string; // Описание (необязательно, зависит от типа объекта)
}

interface SiteSettings {
    id: number; // Уникальный идентификатор
    name: string;
    phone_number: string; // Номер телефона
    logo: string | null; // Логотип (путь к файлу или null)
    favicon: string | null;
    footer_text: string; // Текст футера
    is_enabled: boolean; // Флаг активности
    allow_in_robots_txt: boolean; // Разрешено ли в robots.txt
    documents: Document[]; // Массив связанных документов
    top_items: TopItem[]; // Массив топовых элементов
    overlay_opacity: number
}

interface Pagination {
    count: number;
    next: string | null;
    previous: string | null;
}
interface PaginatedResponse<T> extends Pagination {
    results: T[];
}
interface AdditionalService {
    id: number
    name: string
    label: string
    description: string
    rate_increase: string
    is_active: boolean
}

interface Range {
    name: string
    label: string
    min_value: string
    max_value: string
    default_value: string
    description: string
    data_type: 'decimal' | 'integer' | 'percent'
    is_active: boolean
}

interface CalcConfig {
    ranges: Range[]
    services: AdditionalService[]
    base_rate: number
}