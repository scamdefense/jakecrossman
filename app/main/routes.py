from flask import (
    render_template,
    current_app,
    request,
    Response,
    make_response,
    url_for,
    flash,
    redirect,
    jsonify,
)
from app.main import bp
from app.seo import get_page_seo_data, SEOConfig
from app.email_utils import send_contact_email
import os
import xml.etree.ElementTree as ET
from datetime import datetime


@bp.route("/")
@bp.route("/index")
def index():
    """Homepage route."""
    seo_data = get_page_seo_data("index")
    return render_template(
        "index.html",
        title="Jake Crossman - Professional Actor | Los Angeles, CA",
        seo_data=seo_data,
    )


@bp.route("/about")
def about():
    """About page route."""
    seo_data = get_page_seo_data("about")
    return render_template(
        "about.html",
        title="About Jake Crossman - Professional Actor Bio & Background",
        seo_data=seo_data,
    )


@bp.route("/reel")
def reel():
    """Demo reel page route."""
    seo_data = get_page_seo_data("reel")
    return render_template(
        "reel.html",
        title="Jake Crossman Demo Reel - Professional Acting Showcase",
        seo_data=seo_data,
    )


@bp.route("/resume")
def resume():
    """Resume page route."""
    seo_data = get_page_seo_data("resume")
    return render_template(
        "resume.html",
        title="Jake Crossman Acting Resume - Credits & Experience",
        seo_data=seo_data,
    )


@bp.route("/gallery")
def gallery():
    """Gallery page route."""
    # Get list of gallery images for schema
    gallery_images = [
        f"{SEOConfig.SITE_URL}/static/images/headshot-{i}.jpg" for i in range(1, 9)
    ]
    seo_data = get_page_seo_data("gallery", images=gallery_images)
    return render_template(
        "gallery.html",
        title="Jake Crossman Gallery - Professional Headshots",
        seo_data=seo_data,
    )


@bp.route("/news")
def news():
    """News and updates page route."""
    seo_data = get_page_seo_data("news")
    return render_template(
        "news.html",
        title="Jake Crossman News & Updates - Latest Projects & Blog",
        seo_data=seo_data,
    )


@bp.route("/contact", methods=["GET", "POST"])
def contact():
    """Contact page route."""
    if request.method == "POST":
        # Handle AJAX form submission
        if request.is_json:
            form_data = request.get_json()
        else:
            # Handle regular form submission
            form_data = request.form.to_dict()

        # Basic validation
        required_fields = ["name", "email", "message"]
        missing_fields = [
            field for field in required_fields if not form_data.get(field)
        ]

        if missing_fields:
            if request.is_json:
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": (
                                f"Missing required fields: "
                                f'{", ".join(missing_fields)}'
                            ),
                        }
                    ),
                    400,
                )
            else:
                flash("Please fill in all required fields.", "error")
                return redirect(url_for("main.contact"))

        # Validate email format (basic)
        email = form_data.get("email", "")
        if "@" not in email or "." not in email:
            if request.is_json:
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "Please enter a valid email address.",
                        }
                    ),
                    400,
                )
            else:
                flash("Please enter a valid email address.", "error")
                return redirect(url_for("main.contact"))

        # Try to send email
        email_sent = send_contact_email(form_data)

        if email_sent:
            if request.is_json:
                return jsonify(
                    {
                        "success": True,
                        "message": (
                            "Thank you for your message! "
                            "I will get back to you soon."
                        ),
                    }
                )
            else:
                flash(
                    "Thank you for your message! I will get back to you soon.",
                    "success",
                )
                return redirect(url_for("main.contact"))
        else:
            if request.is_json:
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": (
                                "Sorry, there was an error sending your message. "
                                "Please try again or contact me directly."
                            ),
                        }
                    ),
                    500,
                )
            else:
                flash(
                    (
                        "Sorry, there was an error sending your message. "
                        "Please try again or contact me directly."
                    ),
                    "error",
                )
                return redirect(url_for("main.contact"))

    # GET request - show contact form
    seo_data = get_page_seo_data("contact")
    return render_template(
        "contact.html",
        title="Contact Jake Crossman - Professional Actor Representation",
        seo_data=seo_data,
    )


@bp.route("/sitemap.xml")
def sitemap():
    """Generate enhanced dynamic sitemap.xml with images and videos."""

    # Define pages with their priorities and change frequencies
    pages = [
        {
            "loc": "/",
            "priority": "1.0",
            "changefreq": "weekly",
            "images": [f"headshot-{i}" for i in range(1, 9)],
            "videos": [],
        },
        {
            "loc": "/about",
            "priority": "0.9",
            "changefreq": "monthly",
            "images": ["headshot-1", "headshot-2"],
            "videos": [],
        },
        {
            "loc": "/reel",
            "priority": "0.9",
            "changefreq": "monthly",
            "images": ["demo-reel-thumbnail"],
            "videos": ["demo-reel.mp4"],
        },
        {
            "loc": "/resume",
            "priority": "0.8",
            "changefreq": "monthly",
            "images": [],
            "videos": [],
        },
        {
            "loc": "/gallery",
            "priority": "0.7",
            "changefreq": "weekly",
            "images": [f"headshot-{i}" for i in range(1, 9)]
            + ["espn-fuse-highlight", "tiktok-highlight", "continue-to-win-highlight"],
            "videos": [],
        },
        {
            "loc": "/news",
            "priority": "0.8",
            "changefreq": "weekly",
            "images": ["headshot-1"],
            "videos": [],
        },
        {
            "loc": "/contact",
            "priority": "0.6",
            "changefreq": "monthly",
            "images": [],
            "videos": [],
        },
    ]

    # Create XML structure with namespaces
    urlset = ET.Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    urlset.set("xmlns:image", "http://www.google.com/schemas/sitemap-image/1.1")
    urlset.set("xmlns:video", "http://www.google.com/schemas/sitemap-video/1.1")
    urlset.set("xmlns:news", "http://www.google.com/schemas/sitemap-news/0.9")

    for page in pages:
        url_elem = ET.SubElement(urlset, "url")

        # Location
        loc = ET.SubElement(url_elem, "loc")
        loc.text = f"{SEOConfig.SITE_URL}{page['loc']}"

        # Last modified (use current date for now, could be dynamic)
        lastmod = ET.SubElement(url_elem, "lastmod")
        lastmod.text = datetime.now().strftime("%Y-%m-%d")

        # Change frequency
        changefreq = ET.SubElement(url_elem, "changefreq")
        changefreq.text = page["changefreq"]

        # Priority
        priority = ET.SubElement(url_elem, "priority")
        priority.text = page["priority"]

        # Add image references
        for image_name in page.get("images", []):
            image = ET.SubElement(url_elem, "image:image")

            # Image location (check for WebP and fallback)
            image_loc = ET.SubElement(image, "image:loc")
            if os.path.exists(
                os.path.join(current_app.static_folder, "images", f"{image_name}.webp")
            ):
                image_loc.text = f"{SEOConfig.SITE_URL}/static/images/{image_name}.webp"
            elif os.path.exists(
                os.path.join(current_app.static_folder, "images", f"{image_name}.jpg")
            ):
                image_loc.text = f"{SEOConfig.SITE_URL}/static/images/{image_name}.jpg"
            elif os.path.exists(
                os.path.join(current_app.static_folder, "images", f"{image_name}.png")
            ):
                image_loc.text = f"{SEOConfig.SITE_URL}/static/images/{image_name}.png"

            # Image caption
            image_caption = ET.SubElement(image, "image:caption")
            if "headshot" in image_name:
                image_caption.text = (
                    f"Jake Crossman Professional Headshot - "
                    f"{image_name.replace('headshot-', 'Photo ')}"
                )
            elif image_name == "demo-reel-thumbnail":
                image_caption.text = "Jake Crossman Demo Reel Thumbnail"
            elif "highlight" in image_name:
                highlight_name = (
                    image_name.replace("-highlight", "").replace("-", " ").title()
                )
                image_caption.text = f"Jake Crossman {highlight_name} Production Photo"
            else:
                image_caption.text = (
                    f"Jake Crossman {image_name.replace('-', ' ').title()}"
                )

            # Image title
            image_title = ET.SubElement(image, "image:title")
            image_title.text = image_caption.text

            # Image license (optional)
            image_license = ET.SubElement(image, "image:license")
            image_license.text = f"{SEOConfig.SITE_URL}/license"

        # Add video references
        for video_name in page.get("videos", []):
            video = ET.SubElement(url_elem, "video:video")

            # Video thumbnail
            video_thumbnail = ET.SubElement(video, "video:thumbnail_loc")
            video_thumbnail.text = (
                f"{SEOConfig.SITE_URL}/static/images/demo-reel-thumbnail.jpg"
            )

            # Video title
            video_title = ET.SubElement(video, "video:title")
            video_title.text = "Jake Crossman Professional Acting Demo Reel"

            # Video description
            video_desc = ET.SubElement(video, "video:description")
            video_desc.text = (
                "Professional acting demo reel showcasing Jake Crossman's "
                "versatility across comedy, drama, and commercial work. "
                "Features performances from ESPN+, independent films, "
                "and theater productions."
            )

            # Video content location
            video_content = ET.SubElement(video, "video:content_loc")
            video_content.text = f"{SEOConfig.SITE_URL}/static/videos/{video_name}"

            # Video player location
            video_player = ET.SubElement(video, "video:player_loc")
            video_player.text = f"{SEOConfig.SITE_URL}/reel"

            # Video duration (in seconds)
            video_duration = ET.SubElement(video, "video:duration")
            video_duration.text = "180"  # 3 minutes

            # Publication date
            video_pub_date = ET.SubElement(video, "video:publication_date")
            video_pub_date.text = "2025-01-01T00:00:00+00:00"

            # Video category
            video_category = ET.SubElement(video, "video:category")
            video_category.text = "Entertainment"

            # Video tags
            video_tag = ET.SubElement(video, "video:tag")
            video_tag.text = "acting, demo reel, Jake Crossman, actor, professional"

            # Family friendly
            video_family = ET.SubElement(video, "video:family_friendly")
            video_family.text = "yes"

            # Video rating
            video_rating = ET.SubElement(video, "video:rating")
            video_rating.text = "5.0"

    # Generate XML string
    xml_str = ET.tostring(urlset, encoding="unicode", method="xml")

    # Add XML declaration
    xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_str = xml_declaration + xml_str

    # Create response with proper headers
    response = make_response(xml_str)
    response.headers["Content-Type"] = "application/xml"
    response.headers["Cache-Control"] = "public, max-age=3600"

    return response


@bp.route("/robots.txt")
def robots():
    """Serve enhanced robots.txt file with multiple sitemaps."""
    response = make_response(
        f"""User-agent: *
Allow: /

# Primary Sitemap
Sitemap: {SEOConfig.SITE_URL}/sitemap.xml

# Specialized Sitemaps
Sitemap: {SEOConfig.SITE_URL}/news-sitemap.xml
Sitemap: {SEOConfig.SITE_URL}/image-sitemap.xml
Sitemap: {SEOConfig.SITE_URL}/video-sitemap.xml

# Search Engine Specific Directives
User-agent: Googlebot
Allow: /
Crawl-delay: 1

User-agent: Bingbot
Allow: /
Crawl-delay: 1

User-agent: facebookexternalhit
Allow: /

User-agent: Twitterbot
Allow: /

User-agent: LinkedInBot
Allow: /

User-agent: PinterestBot
Allow: /

User-agent: InstagramBot
Allow: /

User-agent: TikTokBot
Allow: /

# Block administrative and system directories
Disallow: /admin/
Disallow: /private/
Disallow: /.git/
Disallow: /app/
Disallow: /__pycache__/
Disallow: /.env
Disallow: /config/
Disallow: /logs/
Disallow: /tmp/
Disallow: /test/
Disallow: /tests/

# Allow static assets and important resources
Allow: /static/css/
Allow: /static/js/
Allow: /static/images/
Allow: /static/videos/
Allow: /static/favicon/
Allow: /static/fonts/

# Performance and courtesy settings
Crawl-delay: 1
Request-rate: 1/1s
Host: {SEOConfig.SITE_URL.replace('https://', '').replace('http://', '')}

# Cache directive for this file
# Cache-Control: public, max-age=86400"""
    )
    response.headers["Content-Type"] = "text/plain"
    response.headers["Cache-Control"] = "public, max-age=86400"
    return response


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


@bp.route("/news-sitemap.xml")
def news_sitemap():
    """Generate news sitemap for the blog/news section."""

    # Sample news articles - in production, this would come from a database
    news_articles = [
        {
            "url": "/news#f1-the-movie",
            "title": "Cardistry Consultant on F1 The Movie",
            "publication_date": "2025-09-01T00:00:00Z",
            "keywords": (
                "Jake Crossman, F1 The Movie, cardistry consultant, Joseph Kosinski"
            ),
        },
        {
            "url": "/news#continue-to-win",
            "title": "Continue to Win Pilot Wraps Production",
            "publication_date": "2025-06-01T00:00:00Z",
            "keywords": (
                "Jake Crossman, Continue to Win, independent film, "
                "acting, Trent Harlen"
            ),
        },
        {
            "url": "/news#espn-fuse",
            "title": "ESPN+ FUSE Sketch Comedy Series Launch",
            "publication_date": "2019-08-01T00:00:00Z",
            "keywords": (
                "Jake Crossman, ESPN, FUSE, sketch comedy, " "executive producer"
            ),
        },
        {
            "url": "/news#tiktok-milestone",
            "title": "Reaching 1 Million TikTok Followers",
            "publication_date": "2024-03-01T00:00:00Z",
            "keywords": (
                "Jake Crossman, TikTok, social media, digital content, "
                "1 million followers"
            ),
        },
    ]

    # Create XML structure
    urlset = ET.Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    urlset.set("xmlns:news", "http://www.google.com/schemas/sitemap-news/0.9")

    for article in news_articles:
        url_elem = ET.SubElement(urlset, "url")

        # Location
        loc = ET.SubElement(url_elem, "loc")
        loc.text = f"{SEOConfig.SITE_URL}{article['url']}"

        # News element
        news_elem = ET.SubElement(url_elem, "news:news")

        # Publication
        publication = ET.SubElement(news_elem, "news:publication")
        pub_name = ET.SubElement(publication, "news:name")
        pub_name.text = SEOConfig.SITE_NAME
        pub_language = ET.SubElement(publication, "news:language")
        pub_language.text = "en"

        # Publication date
        pub_date = ET.SubElement(news_elem, "news:publication_date")
        pub_date.text = article["publication_date"]

        # Title
        title = ET.SubElement(news_elem, "news:title")
        title.text = article["title"]

        # Keywords
        keywords = ET.SubElement(news_elem, "news:keywords")
        keywords.text = article["keywords"]

    # Generate XML string
    xml_str = ET.tostring(urlset, encoding="unicode", method="xml")

    # Add XML declaration
    xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_str = xml_declaration + xml_str

    # Create response
    response = make_response(xml_str)
    response.headers["Content-Type"] = "application/xml"
    response.headers["Cache-Control"] = "public, max-age=1800"  # 30 minutes for news

    return response


@bp.route("/image-sitemap.xml")
def image_sitemap():
    """Generate dedicated image sitemap."""

    # Define all images with metadata
    images = [
        {
            "url": f"/static/images/headshot-{i}.jpg",
            "caption": f"Jake Crossman Professional Headshot {i}",
            "title": f"Professional Actor Headshot {i}",
            "location": "/" if i <= 3 else "/gallery",
        }
        for i in range(1, 9)
    ] + [
        {
            "url": "/static/images/espn-fuse-highlight.jpg",
            "caption": "Jake Crossman in ESPN+ FUSE Sketch Comedy Series",
            "title": "ESPN FUSE Production Photo",
            "location": "/gallery",
        },
        {
            "url": "/static/images/tiktok-highlight.jpg",
            "caption": "Jake Crossman TikTok Content Creation",
            "title": "Social Media Content Photo",
            "location": "/gallery",
        },
        {
            "url": "/static/images/continue-to-win-highlight.jpg",
            "caption": ("Jake Crossman in Continue to Win Independent Pilot"),
            "title": "Continue to Win Production Photo",
            "location": "/gallery",
        },
        {
            "url": "/static/images/demo-reel-thumbnail.jpg",
            "caption": "Jake Crossman Demo Reel Thumbnail",
            "title": "Acting Demo Reel Preview",
            "location": "/reel",
        },
    ]

    # Create XML structure
    urlset = ET.Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    urlset.set("xmlns:image", "http://www.google.com/schemas/sitemap-image/1.1")

    # Group images by page location
    pages = {}
    for image in images:
        location = image["location"]
        if location not in pages:
            pages[location] = []
        pages[location].append(image)

    for location, page_images in pages.items():
        url_elem = ET.SubElement(urlset, "url")

        # Page location
        loc = ET.SubElement(url_elem, "loc")
        loc.text = f"{SEOConfig.SITE_URL}{location}"

        # Add all images for this page
        for image in page_images:
            image_elem = ET.SubElement(url_elem, "image:image")

            # Image location
            image_loc = ET.SubElement(image_elem, "image:loc")
            image_loc.text = f"{SEOConfig.SITE_URL}{image['url']}"

            # Image caption
            image_caption = ET.SubElement(image_elem, "image:caption")
            image_caption.text = image["caption"]

            # Image title
            image_title = ET.SubElement(image_elem, "image:title")
            image_title.text = image["title"]

            # Geo location (optional)
            if (
                "los angeles" in image["caption"].lower()
                or "headshot" in image["caption"].lower()
            ):
                image_geo = ET.SubElement(image_elem, "image:geo_location")
                image_geo.text = "Los Angeles, CA, USA"

            # License
            image_license = ET.SubElement(image_elem, "image:license")
            image_license.text = f"{SEOConfig.SITE_URL}/license"

    # Generate XML
    xml_str = ET.tostring(urlset, encoding="unicode", method="xml")
    xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_str = xml_declaration + xml_str

    response = make_response(xml_str)
    response.headers["Content-Type"] = "application/xml"
    response.headers["Cache-Control"] = "public, max-age=7200"  # 2 hours

    return response


@bp.route("/video-sitemap.xml")
def video_sitemap():
    """Generate video sitemap for demo reel and other video content."""

    videos = [
        {
            "page_url": "/reel",
            "content_url": "/static/videos/demo-reel.mp4",
            "thumbnail_url": "/static/images/demo-reel-thumbnail.jpg",
            "title": "Jake Crossman Professional Acting Demo Reel",
            "description": (
                "Professional acting demo reel showcasing Jake Crossman's "
                "versatility across comedy, drama, and commercial work. "
                "Features performances from ESPN+, independent films, "
                "and theater productions."
            ),
            "duration": 180,  # seconds
            "publication_date": "2025-01-01T00:00:00Z",
            "tags": [
                "acting",
                "demo reel",
                "Jake Crossman",
                "actor",
                "professional",
                "comedy",
                "drama",
            ],
            "category": "Entertainment",
            "rating": 5.0,
            "view_count": 1000,
            "family_friendly": True,
        }
    ]

    # Create XML structure
    urlset = ET.Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    urlset.set("xmlns:video", "http://www.google.com/schemas/sitemap-video/1.1")

    for video in videos:
        url_elem = ET.SubElement(urlset, "url")

        # Page location
        loc = ET.SubElement(url_elem, "loc")
        loc.text = f"{SEOConfig.SITE_URL}{video['page_url']}"

        # Video element
        video_elem = ET.SubElement(url_elem, "video:video")

        # Thumbnail
        thumbnail = ET.SubElement(video_elem, "video:thumbnail_loc")
        thumbnail.text = f"{SEOConfig.SITE_URL}{video['thumbnail_url']}"

        # Title
        title = ET.SubElement(video_elem, "video:title")
        title.text = video["title"]

        # Description
        description = ET.SubElement(video_elem, "video:description")
        description.text = video["description"]

        # Content location
        content_loc = ET.SubElement(video_elem, "video:content_loc")
        content_loc.text = f"{SEOConfig.SITE_URL}{video['content_url']}"

        # Player location
        player_loc = ET.SubElement(video_elem, "video:player_loc")
        player_loc.text = f"{SEOConfig.SITE_URL}{video['page_url']}"

        # Duration
        duration = ET.SubElement(video_elem, "video:duration")
        duration.text = str(video["duration"])

        # Publication date
        pub_date = ET.SubElement(video_elem, "video:publication_date")
        pub_date.text = video["publication_date"]

        # Tags
        for tag in video["tags"]:
            tag_elem = ET.SubElement(video_elem, "video:tag")
            tag_elem.text = tag

        # Category
        category = ET.SubElement(video_elem, "video:category")
        category.text = video["category"]

        # Rating
        rating = ET.SubElement(video_elem, "video:rating")
        rating.text = str(video["rating"])

        # View count
        view_count = ET.SubElement(video_elem, "video:view_count")
        view_count.text = str(video["view_count"])

        # Family friendly
        family_friendly = ET.SubElement(video_elem, "video:family_friendly")
        family_friendly.text = "yes" if video["family_friendly"] else "no"

        # Uploader
        uploader = ET.SubElement(video_elem, "video:uploader")
        uploader.text = SEOConfig.PERSON_INFO["name"]
        uploader.set("info", SEOConfig.SITE_URL)

    # Generate XML
    xml_str = ET.tostring(urlset, encoding="unicode", method="xml")
    xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_str = xml_declaration + xml_str

    response = make_response(xml_str)
    response.headers["Content-Type"] = "application/xml"
    response.headers["Cache-Control"] = "public, max-age=3600"

    return response
