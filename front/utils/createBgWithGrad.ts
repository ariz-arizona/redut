export default (
    imageUrl: string,
    startColor: string = 'rgba(0, 0, 0, 0.5)',
    endColor: string = 'rgba(0, 0, 0, 0.5)',
    gradientDirection: 'to right' | 'to left' | 'to top' | 'to bottom' | string = 'to bottom',
) => {
    return `linear-gradient(${gradientDirection}, ${startColor}, ${endColor}), url("${imageUrl}")`;
};