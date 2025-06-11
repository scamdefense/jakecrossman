from flask import render_template, current_app, request, Response
from app.main import bp
import os


@bp.route("/")
@bp.route("/index")
def index():
    """Homepage route."""
    return render_template("index.html", title="Jake Crossman - Actor")


@bp.route("/about")
def about():
    """About page route."""
    return render_template("about.html", title="About Jake Crossman")


@bp.route("/reel")
def reel():
    """Demo reel page route."""
    return render_template("reel.html", title="Demo Reel")


@bp.route("/resume")
def resume():
    """Resume page route."""
    return render_template("resume.html", title="Resume")


@bp.route("/gallery")
def gallery():
    """Gallery page route."""
    return render_template("gallery.html", title="Gallery")


@bp.route("/news")
def news():
    """News and updates page route."""
    return render_template("news.html", title="News & Updates")


@bp.route("/contact")
def contact():
    """Contact page route."""
    return render_template("contact.html", title="Contact")


@bp.route("/video/<filename>")
def serve_video(filename):
    """Serve video files with proper range request support for streaming."""
    video_dir = os.path.join(current_app.static_folder, "videos")
    file_path = os.path.join(video_dir, filename)

    if not os.path.exists(file_path):
        return "Video not found", 404

    file_size = os.path.getsize(file_path)

    # Handle range requests for proper video streaming
    range_header = request.headers.get("Range", None)
    if range_header:
        # Parse range header more robustly
        try:
            byte_start = 0
            byte_end = file_size - 1

            # Extract byte range from header
            range_match = range_header.replace("bytes=", "").split("-")
            if range_match[0]:
                byte_start = int(range_match[0])
            if range_match[1]:
                byte_end = min(int(range_match[1]), file_size - 1)

            # Ensure we don't exceed file boundaries
            byte_start = max(0, byte_start)
            byte_end = min(byte_end, file_size - 1)
            content_length = byte_end - byte_start + 1

            # Read the requested chunk
            with open(file_path, "rb") as f:
                f.seek(byte_start)
                chunk = f.read(content_length)

            # Create proper 206 Partial Content response
            response = Response(
                chunk,
                206,  # Partial Content
                headers={
                    "Content-Range": f"bytes {byte_start}-{byte_end}/{file_size}",
                    "Accept-Ranges": "bytes",
                    "Content-Length": str(content_length),
                    "Content-Type": "video/mp4",
                    "Cache-Control": "public, max-age=3600",
                },
            )
            return response

        except (ValueError, IndexError) as e:
            # If range parsing fails, fall back to full file
            current_app.logger.warning(f"Range parsing error: {e}")
            range_header = None

    if not range_header:
        # Regular request - serve the entire file with proper headers
        def generate():
            with open(file_path, "rb") as f:
                # Stream in 1MB chunks for better performance
                while True:
                    chunk = f.read(1048576)  # 1MB chunks
                    if not chunk:
                        break
                    yield chunk

        response = Response(
            generate(),
            200,
            headers={
                "Content-Type": "video/mp4",
                "Content-Length": str(file_size),
                "Accept-Ranges": "bytes",
                "Cache-Control": "public, max-age=3600",
            },
        )
        return response


def smart_image_url(image_name, formats=None):
    """
    Generate URLs for multiple image formats with fallback support.

    Args:
        image_name: Base name of the image (without extension)
        ['webp', 'jpg', 'jpeg', 'png']

    Returns:
        Dictionary with available format URLs and fallback URL
    """
    if formats is None:
        formats = ["webp", "jpg", "jpeg", "png"]

    image_dir = os.path.join(current_app.static_folder, "images")
    available_formats = {}
    fallback_url = None

    for format_ext in formats:
        file_path = os.path.join(image_dir, f"{image_name}.{format_ext}")
        if os.path.exists(file_path):
            from flask import url_for

            url = url_for("static", filename=f"images/{image_name}.{format_ext}")
            available_formats[format_ext] = url
            if fallback_url is None or format_ext in ["jpg", "jpeg", "png"]:
                fallback_url = url

    return {
        "formats": available_formats,
        "fallback": fallback_url,
        "has_webp": "webp" in available_formats,
        "has_jpg": any(fmt in available_formats for fmt in ["jpg", "jpeg"]),
        "has_png": "png" in available_formats,
    }


# Make the function available in templates
@bp.app_template_global()
def smart_img(image_name, formats=None):
    """Template function for smart image handling"""
    return smart_image_url(image_name, formats)
