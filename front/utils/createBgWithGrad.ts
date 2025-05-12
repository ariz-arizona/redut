export default (
    imageUrl: string,
    color: string = 'var(--image-overlay-color)',
    startOpacity: string = 'var(--image-overlay-opacity)',
    endOpacity: string = 'var(--image-overlay-opacity)',
    gradientDirection: 'to right' | 'to left' | 'to top' | 'to bottom' | string = 'to bottom',
) => {
    const startColor = `rgba(${color} / ${startOpacity})`;
    const endColor = `rgba(${color} / ${endOpacity})`;

    return `linear-gradient(${gradientDirection}, ${startColor}, ${endColor}), url("${imageUrl}")`;
};