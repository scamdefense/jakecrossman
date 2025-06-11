#!/usr/bin/env python3
"""
Image Conversion Script for Jake Crossman Website
Converts existing JPEG/PNG images to WebP format for better performance.
"""

import subprocess
import sys
from pathlib import Path


def check_webp_support():
    """Check if cwebp command is available."""
    try:
        subprocess.run(["cwebp", "-version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def convert_to_webp(input_path, output_path, quality=85):
    """Convert an image to WebP format."""
    try:
        cmd = ["cwebp", "-q", str(quality), str(input_path), "-o", str(output_path)]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr


def main():
    """Main conversion function."""
    # Path to images directory
    images_dir = Path(__file__).parent / "app" / "static" / "images"

    if not images_dir.exists():
        print(f"Error: Images directory not found at {images_dir}")
        sys.exit(1)

    # Check if cwebp is available
    if not check_webp_support():
        print("Error: cwebp command not found.")
        print("Please install WebP tools:")
        print("  Ubuntu/Debian: sudo apt install webp")
        print("  macOS: brew install webp")
        print(
            "  Windows: Download from https://developers.google.com/speed/webp/download"
        )
        sys.exit(1)

    # Find all JPEG and PNG files
    image_extensions = ["*.jpg", "*.jpeg", "*.png"]
    image_files = []

    for ext in image_extensions:
        image_files.extend(images_dir.glob(ext))
        image_files.extend(images_dir.glob(ext.upper()))

    if not image_files:
        print("No JPEG or PNG files found in the images directory.")
        return

    print(f"Found {len(image_files)} image(s) to convert:")

    converted_count = 0
    skipped_count = 0
    error_count = 0

    for image_file in image_files:
        # Generate WebP filename
        webp_file = image_file.with_suffix(".webp")

        # Skip if WebP already exists
        if webp_file.exists():
            print(f"  Skipping {image_file.name} (WebP already exists)")
            skipped_count += 1
            continue

        print(f"  Converting {image_file.name} -> {webp_file.name}...")

        # Convert to WebP
        success, message = convert_to_webp(image_file, webp_file)

        if success:
            # Compare file sizes
            original_size = image_file.stat().st_size
            webp_size = webp_file.stat().st_size

            savings = (1 - webp_size / original_size) * 100
            print(
                f"    ✓ Success! "
                f"Saved {savings:.1f}% ({original_size:,} -> {webp_size:,} bytes)"
            )
            converted_count += 1
        else:
            print(f"    ✗ Error: {message}")
            error_count += 1

    print("\nConversion complete:")
    print(f"  Converted: {converted_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Errors: {error_count}")

    if converted_count > 0:
        print(
            "\n✓ Your website will now automatically serve "
            "WebP images to supported browsers!"
        )
        print("  Original JPEG/PNG files are kept as fallbacks for older browsers.")


if __name__ == "__main__":
    main()
