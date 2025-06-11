# Multi-Format Image Support Documentation

## Overview

This website now supports automatic multi-format image handling with WebP optimization and fallbacks. The system automatically detects available image formats and serves the most appropriate one based on browser support.

## How It Works

### 1. Smart Image Function
The `smart_img()` function in Flask automatically:
- Checks for multiple image formats (WebP, JPG, JPEG, PNG)
- Returns available formats and fallback URLs
- Provides browser compatibility information

### 2. Template Macros
Three convenient macros are available in `macros.html`:

#### `smart_image(image_name, alt_text, class="", style="", loading="lazy", formats=None)`
Basic smart image with full control over attributes.

#### `gallery_image(image_name, alt_text, class="gallery-item", loading="lazy")`
Pre-configured for gallery items with proper styling.

#### `highlight_image(image_name, alt_text, class="highlight-image")`
Pre-configured for highlight cards on the homepage.

### 3. Browser Support
- **WebP**: Modern browsers get smaller, higher-quality WebP images
- **JPEG/PNG**: Fallback for older browsers
- **Automatic Detection**: JavaScript detects WebP support and adds CSS classes

## Adding Images

### 1. File Naming Convention
For an image called "headshot-1", create these files in `/app/static/images/`:
```
headshot-1.webp    (recommended - smallest file size)
headshot-1.jpg     (fallback for older browsers)
headshot-1.png     (if transparency is needed)
```

### 2. Template Usage

#### In Gallery Pages:
```html
{% from "macros.html" import gallery_image %}
{{ gallery_image('headshot-1', 'Jake Crossman Professional Headshot 1') }}
```

#### In Highlight Cards:
```html
{% from "macros.html" import highlight_image %}
{{ highlight_image('project-image', 'Project Description') }}
```

#### Custom Usage:
```html
{% from "macros.html" import smart_image %}
{{ smart_image('custom-image', 'Description', class="custom-class", style="width: 50%;") }}
```

## Image Optimization Recommendations

### 1. Format Priority
1. **WebP**: Best compression, modern browser support
2. **JPEG**: Good compression for photos, universal support
3. **PNG**: For images requiring transparency

### 2. Optimization Commands

#### Create WebP from JPEG:
```bash
cwebp -q 85 input.jpg -o output.webp
```

#### Create optimized JPEG:
```bash
jpegoptim --max=85 --strip-all input.jpg
```

#### Create optimized PNG:
```bash
optipng -o7 input.png
```

### 3. Batch Conversion Script
Create a batch file for converting all images:

```bash
# Convert all JPGs to WebP
for file in *.jpg; do
    cwebp -q 85 "$file" -o "${file%.jpg}.webp"
done

# Convert all PNGs to WebP
for file in *.png; do
    cwebp -q 85 "$file" -o "${file%.png}.webp"
done
```

## Browser Compatibility

### Supported Formats by Browser:
- **WebP**: Chrome 23+, Firefox 65+, Safari 14+, Edge 18+
- **JPEG**: All browsers
- **PNG**: All browsers

### Fallback Strategy:
1. Browser loads WebP if supported
2. Falls back to JPEG/PNG if WebP not supported
3. Shows placeholder if no image files found

## Performance Benefits

### 1. File Size Reduction
- WebP typically 25-35% smaller than equivalent JPEG
- Faster page load times
- Reduced bandwidth usage

### 2. Progressive Enhancement
- Modern browsers get optimized experience
- Older browsers still work perfectly
- No JavaScript required for basic functionality

### 3. Lazy Loading
- Images load only when needed
- Improves initial page load speed
- Smooth fade-in animations

## CSS Classes Added

### Browser Detection:
- `.webp-supported`: Added when browser supports WebP
- `.webp-not-supported`: Added when browser doesn't support WebP

### Image States:
- `.smart-picture`: Container for multi-format images
- `.loaded`: Added when lazy-loaded image is visible

## Migration Guide

### For Existing Images:
1. Keep existing JPG/PNG files
2. Add WebP versions using the same base name
3. Update templates to use new macros
4. Test in multiple browsers

### Example Migration:
```html
<!-- OLD -->
<img src="{{ url_for('static', filename='images/headshot-1.jpg') }}" alt="Headshot">

<!-- NEW -->
{{ gallery_image('headshot-1', 'Jake Crossman Professional Headshot 1') }}
```

## Troubleshooting

### Image Not Loading?
1. Check file exists in `/app/static/images/`
2. Verify file naming matches template usage
3. Check browser console for errors
4. Ensure at least one supported format exists

### Performance Issues?
1. Optimize image file sizes
2. Enable server-side compression (gzip)
3. Consider CDN for image delivery
4. Monitor Core Web Vitals

## Future Enhancements

### Potential Additions:
- AVIF format support
- Responsive image sizes
- Automatic image compression
- Progressive JPEG support
- Art direction with different crops
