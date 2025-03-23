// types/pageData.ts

interface Image {
    id: number;
    image: string;
    alt_text: string | null;
    url: string | null;
    title: string | null;
}

interface Block {
    content: string;
    content_rendered: string;
    id: number;
    images: Image[];
    order: number;
    page: number;
    title: string;
    type: string;
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