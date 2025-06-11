#!/usr/bin/env python3
"""
Image Optimization Script for Jake Crossman Website (Windows Compatible)
Automatically creates optimized WebP versions of images using Python libraries.
"""

import os
import sys
from pathlib import Path
import shutil
from datetime import datetime

try:
    from PIL import Image, ImageOps

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class ImageOptimizer:
    def __init__(self, base_dir=None):
        """Initialize the optimizer with paths."""
        if base_dir is None:
            base_dir = Path(__file__).parent

        self.base_dir = Path(base_dir)
        self.images_dir = self.base_dir / "app" / "static" / "images"
        self.optimized_dir = self.images_dir / "optimized"

        # Supported input formats
        self.input_extensions = [".jpg", ".jpeg", ".png"]

        # Optimization settings
        self.webp_quality = 85
        self.jpeg_quality = 85
        self.png_optimize = True

    def check_dependencies(self):
        """Check if required Python libraries are available."""
        if not PIL_AVAILABLE:
            print("Missing required Python library: Pillow")
            print("\nInstallation instructions:")
            print("  pip install Pillow")
            print("  or")
            print("  pip install Pillow[webp]  # for better WebP support")
            return False

        # Check WebP support in PIL
        try:
            # Test WebP support
            test_img = Image.new("RGB", (1, 1), color="red")
            test_img.save("test.webp", "WebP")
            os.remove("test.webp")
            print("✓ WebP support available")
        except Exception as e:
            print(f"⚠ WebP support limited: {e}")
            print("Consider installing: pip install Pillow[webp]")

        return True

    def ensure_optimized_folder(self):
        """Create optimized folder if it doesn't exist."""
        if not self.optimized_dir.exists():
            print(f"Creating optimized folder: {self.optimized_dir}")
            self.optimized_dir.mkdir(parents=True, exist_ok=True)
            return True
        else:
            print(f"Optimized folder already exists: {self.optimized_dir}")
            return False

    def get_image_files(self):
        """Get all image files that need optimization."""
        image_files = []

        for ext in self.input_extensions:
            # Case-insensitive search
            image_files.extend(self.images_dir.glob(f"*{ext}"))
            image_files.extend(self.images_dir.glob(f"*{ext.upper()}"))

        # Filter out files already in optimized folder
        image_files = [f for f in image_files if "optimized" not in str(f)]

        return sorted(image_files)

    def optimize_to_webp(self, input_path, output_path):
        """Convert image to WebP format using PIL."""
        try:
            with Image.open(input_path) as img:
                # Convert RGBA to RGB if necessary for WebP
                if img.mode in ("RGBA", "LA", "P"):
                    # Create white background
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    if img.mode == "P":
                        img = img.convert("RGBA")
                    background.paste(
                        img,
                        mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None,
                    )
                    img = background
                elif img.mode != "RGB":
                    img = img.convert("RGB")

                # Auto-orient the image
                img = ImageOps.exif_transpose(img)

                # Save as WebP
                img.save(
                    output_path,
                    "WebP",
                    quality=self.webp_quality,
                    optimize=True,
                    method=6,  # Higher compression method
                )
            return True, None
        except Exception as e:
            return False, str(e)

    def optimize_jpeg(self, input_path, output_path):
        """Optimize JPEG image using PIL."""
        try:
            with Image.open(input_path) as img:
                # Auto-orient the image
                img = ImageOps.exif_transpose(img)

                # Convert to RGB if necessary
                if img.mode != "RGB":
                    img = img.convert("RGB")

                # Save optimized JPEG
                img.save(
                    output_path,
                    "JPEG",
                    quality=self.jpeg_quality,
                    optimize=True,
                    progressive=True,
                )
            return True, None
        except Exception as e:
            return False, str(e)

    def optimize_png(self, input_path, output_path):
        """Optimize PNG image using PIL."""
        try:
            with Image.open(input_path) as img:
                # Auto-orient the image
                img = ImageOps.exif_transpose(img)

                # Save optimized PNG
                img.save(
                    output_path,
                    "PNG",
                    optimize=self.png_optimize,
                    compress_level=9,  # Maximum compression
                )
            return True, None
        except Exception as e:
            return False, str(e)

    def get_file_size_mb(self, file_path):
        """Get file size in MB."""
        return file_path.stat().st_size / (1024 * 1024)

    def calculate_savings(self, original_size, optimized_size):
        """Calculate percentage savings."""
        if original_size == 0:
            return 0
        return ((original_size - optimized_size) / original_size) * 100

    def optimize_image(self, image_file):
        """Optimize a single image file."""
        print(f"\nProcessing: {image_file.name}")

        # Generate output filenames
        base_name = image_file.stem
        original_ext = image_file.suffix.lower()

        webp_output = self.optimized_dir / f"{base_name}.webp"
        optimized_original = self.optimized_dir / f"{base_name}{original_ext}"

        results = {
            "original_size": self.get_file_size_mb(image_file),
            "webp_created": False,
            "original_optimized": False,
            "webp_size": 0,
            "optimized_size": 0,
            "errors": [],
        }

        # Create WebP version
        if not webp_output.exists():
            print(f"  Creating WebP: {webp_output.name}")
            success, error = self.optimize_to_webp(image_file, webp_output)
            if success:
                results["webp_created"] = True
                results["webp_size"] = self.get_file_size_mb(webp_output)
                webp_savings = self.calculate_savings(
                    results["original_size"], results["webp_size"]
                )
                print(f"    ✓ WebP created ({webp_savings:.1f}% smaller)")
            else:
                results["errors"].append(f"WebP conversion failed: {error}")
                print(f"    ✗ WebP conversion failed: {error}")
        else:
            print(f"  WebP already exists: {webp_output.name}")
            results["webp_size"] = self.get_file_size_mb(webp_output)

        # Optimize original format
        if not optimized_original.exists():
            print(f"  Optimizing original: {optimized_original.name}")

            if original_ext in [".jpg", ".jpeg"]:
                success, error = self.optimize_jpeg(image_file, optimized_original)
            elif original_ext == ".png":
                success, error = self.optimize_png(image_file, optimized_original)
            else:
                # For unsupported formats, just copy
                shutil.copy2(image_file, optimized_original)
                success, error = True, None

            if success:
                results["original_optimized"] = True
                results["optimized_size"] = self.get_file_size_mb(optimized_original)
                opt_savings = self.calculate_savings(
                    results["original_size"], results["optimized_size"]
                )
                print(f"    ✓ Original optimized ({opt_savings:.1f}% smaller)")
            else:
                results["errors"].append(f"Original optimization failed: {error}")
                print(f"    ✗ Original optimization failed: {error}")
        else:
            print(f"  Optimized original already exists: {optimized_original.name}")
            results["optimized_size"] = self.get_file_size_mb(optimized_original)

        return results

    def create_usage_examples(self):
        """Create example usage file."""
        examples_file = self.optimized_dir / "USAGE_EXAMPLES.md"

        content = """# Optimized Images Usage Examples

## Template Usage

### Gallery Images:
```html
{% from "macros.html" import gallery_image %}
{{ gallery_image('image-name', 'Alt text description') }}
```

### Highlight Images:
```html
{% from "macros.html" import highlight_image %}
{{ highlight_image('image-name', 'Alt text description') }}
```

### Custom Usage:
```html
{% from "macros.html" import smart_image %}
{{ smart_image('image-name', 'Alt text', class="custom-class", style="width: 100%;") }}
```

## File Structure
```
/app/static/images/
├── image-name.jpg          (original)
├── image-name.png          (original)
└── optimized/
    ├── image-name.webp     (modern browsers)
    ├── image-name.jpg      (optimized fallback)
    └── image-name.png      (optimized fallback)
```

## Performance Benefits
- WebP images are typically 25-35% smaller than JPEG
- Optimized originals provide better compression
- Automatic format selection based on browser support
- Lazy loading for improved page speed

## Generated by Image Optimization Script
This folder contains automatically optimized versions of your images.
Run `python image_optimization.py` to update when you add new images.
"""

        with open(examples_file, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Created usage examples: {examples_file}")

    def run_optimization(self):
        """Run the complete optimization process."""
        print("=== Image Optimization Script (Windows Compatible) ===")
        print(f"Base directory: {self.base_dir}")
        print(f"Images directory: {self.images_dir}")
        print(f"Optimized directory: {self.optimized_dir}")

        # Check if images directory exists
        if not self.images_dir.exists():
            print(f"Error: Images directory not found at {self.images_dir}")
            sys.exit(1)

        # Check dependencies
        if not self.check_dependencies():
            print("\nRequired Python libraries not available. Exiting.")
            sys.exit(1)

        # Get all image files
        image_files = self.get_image_files()

        if not image_files:
            print("No image files found to optimize.")
            return

        print(f"\nFound {len(image_files)} image(s) to process:")
        for img in image_files:
            size_mb = self.get_file_size_mb(img)
            print(f"  - {img.name} ({size_mb:.2f} MB)")

        # Ask for confirmation
        print("\nProceed with optimization? (y/n): ", end="")
        if input().lower() not in ["y", "yes"]:
            print("Optimization cancelled.")
            return

        # Process each image
        total_original_size = 0
        total_webp_size = 0
        total_optimized_size = 0
        webp_count = 0
        optimized_count = 0
        error_count = 0

        start_time = datetime.now()

        for image_file in image_files:
            results = self.optimize_image(image_file)

            total_original_size += results["original_size"]
            total_webp_size += results["webp_size"]
            total_optimized_size += results["optimized_size"]

            if results["webp_created"]:
                webp_count += 1

            if results["original_optimized"]:
                optimized_count += 1

            if results["errors"]:
                error_count += 1

        # Create usage examples
        self.create_usage_examples()

        # Print summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        print("\n" + "=" * 60)
        print("OPTIMIZATION SUMMARY")
        print("=" * 60)
        print(f"Processing time: {duration:.2f} seconds")
        print(f"Images processed: {len(image_files)}")
        print(f"WebP files created: {webp_count}")
        print(f"Original files optimized: {optimized_count}")
        print(f"Errors encountered: {error_count}")

        if total_original_size > 0:
            print("\nFile Size Summary:")
            print(f"Original total: {total_original_size:.2f} MB")
            if total_webp_size > 0:
                print(
                    f"WebP total: {total_webp_size:.2f} MB "
                    "({total_webp_savings:.1f}% savings)"
                )
            if total_optimized_size > 0:
                print(
                    f"Optimized total: {total_optimized_size:.2f} MB "
                    "({total_opt_savings:.1f}% savings)"
                )

        print(f"\nOptimized files location: {self.optimized_dir}")
        print("✓ Your website will now automatically serve optimized images!")


def main():
    """Main function."""
    optimizer = ImageOptimizer()
    optimizer.run_optimization()


if __name__ == "__main__":
    main()
