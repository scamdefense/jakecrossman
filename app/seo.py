# app/seo.py
"""SEO utilities and configuration for Jake Crossman's acting portfolio."""

from flask import request
from typing import Any, Dict, List


class SEOConfig:
    """Central SEO configuration for the website."""

    # Primary website information
    SITE_NAME = "Jake Crossman - Professional Actor"
    SITE_URL = "https://jakecrossman.com"
    DEFAULT_TITLE = "Jake Crossman - Actor"
    DEFAULT_DESCRIPTION = (
        "Professional Actor based in Los Angeles, CA. "
        "ESPN+ star, TikTok influencer with 1M+ followers, and versatile "
        "performer specializing in comedy, drama, and digital content creation."
    )
    DEFAULT_KEYWORDS = [
        "Jake Crossman",
        "Jacob Crossman",
        "actor",
        "performer",
        "Los Angeles actor",
        "Virginia actor",
        "ESPN",
        "TikTok",
        "demo reel",
        "acting portfolio",
        "comedy",
        "drama",
        "digital influencer",
        "content creator",
    ]

    # 2025 SEO Enhancement Configuration
    CORE_WEB_VITALS = {
        "largest_contentful_paint": "2.5s",
        "first_input_delay": "100ms",
        "cumulative_layout_shift": "0.1",
    }
    # Enhanced social media profiles
    PROFESSIONAL_PROFILES = {
        "backstage": "https://www.backstage.com/u/jake-crossman/",
        "casting_networks": (
            "https://www.app.castingnetworks.com/talent/" "public-profile/jake-crossman"
        ),
        "actors_access": "https://resumes.actorsaccess.com/jake-crossman",
    }

    # Social media and contact
    SOCIAL_PROFILES = {
        "tiktok": "https://tiktok.com/@usamedical",
        "instagram": "https://instagram.com/jakecrossman",
        "imdb": "https://www.imdb.com/name/nm16569161/",
        "email": "crossmantv@outlook.com",
        "phone": "814-403-0835",
    }

    # Professional information
    PERSON_INFO = {
        "name": "Jacob Crossman",
        "alternateName": "Jake Crossman",
        "jobTitle": "Professional Actor",
        "description": (
            "Dynamic actor and digital influencer with athletic prowess "
            "and comedic flair"
        ),
        "address": {
            "addressLocality": "Los Angeles",
            "addressRegion": "CA",
            "addressCountry": "US",
        },
        "height": "5'10\"",
        "eyeColor": "Blue",
        "hairColor": "Dusty Blonde",
    }
    # Key achievements for rich snippets
    ACHIEVEMENTS = [
        "1M+ TikTok Followers",
        "250M+ Content Views",
        "ESPN+ Sketch Comedy Series Star",
        "Erie Community Theater Best Lead Actor Award",
        "Emmy Award-winning Production Contributor",
    ]

    # Enhanced technical SEO configuration
    PERFORMANCE_CONFIG = {
        "enable_compression": True,
        "cache_headers": True,
        "preload_critical_resources": True,
        "lazy_load_images": True,
        "optimize_fonts": True,
    }

    # Local SEO configuration
    LOCAL_SEO = {
        "primary_market": {
            "city": "Los Angeles",
            "state": "California",
            "region": "CA",
            "country": "United States",
            "latitude": "34.0522",
            "longitude": "-118.2437",
        },
        "secondary_market": {
            "city": "Lynchburg",
            "state": "Virginia",
            "region": "VA",
            "country": "United States",
            "latitude": "37.4138",
            "longitude": "-79.1422",
        },
    }


def generate_page_schema(page_type: str, **kwargs: Any) -> Dict[str, Any]:
    """Generate JSON-LD schema markup for different page types."""

    base_schema = {
        "@context": "https://schema.org",
        "@type": ["Person", "PerformingArtist"],
        "name": SEOConfig.PERSON_INFO["name"],
        "alternateName": SEOConfig.PERSON_INFO["alternateName"],
        "jobTitle": SEOConfig.PERSON_INFO["jobTitle"],
        "description": SEOConfig.PERSON_INFO["description"],
        "url": SEOConfig.SITE_URL,
        "sameAs": list(SEOConfig.SOCIAL_PROFILES.values()),
        "address": {
            "@type": "PostalAddress",
            **SEOConfig.PERSON_INFO["address"],  # type: ignore[dict-item]
        },
        "contactPoint": {
            "@type": "ContactPoint",
            "email": SEOConfig.SOCIAL_PROFILES["email"],
            "telephone": SEOConfig.SOCIAL_PROFILES["phone"],
        },
    }

    if page_type == "homepage":
        base_schema.update(
            {
                "@type": ["Person", "PerformingArtist", "WebSite"],
                "potentialAction": {
                    "@type": "SearchAction",
                    "target": f"{SEOConfig.SITE_URL}/search?q={{search_term_string}}",
                    "query-input": "required name=search_term_string",
                },
            }
        )

    elif page_type == "about":
        base_schema.update(
            {
                "knowsAbout": [
                    "Acting",
                    "Comedy",
                    "Drama",
                    "Digital Content Creation",
                    "Social Media",
                ],
                "award": SEOConfig.ACHIEVEMENTS,
            }
        )

    elif page_type == "resume":
        base_schema.update(
            {
                "@type": ["Person", "PerformingArtist", "Resume"],
                "hasCredential": [
                    {  # type: ignore[list-item]
                        "@type": "EducationalOccupationalCredential",
                        "credentialCategory": "degree",
                        "educationalLevel": "Bachelor's",
                        "recognizedBy": "Gannon University & Liberty University",
                    }
                ],
            }
        )

    elif page_type == "gallery":
        if kwargs.get("images"):
            base_schema["image"] = kwargs["images"]

    elif page_type == "contact":
        base_schema.update(
            {
                "@type": ["Person", "ContactPage"],
                "availableService": {
                    "@type": "Service",
                    "name": "Acting Services",
                    "description": (
                        "Professional acting for film, television, theater, "
                        "and digital content"
                    ),
                },
            }
        )

    elif page_type == "news":
        base_schema.update(
            {"@type": ["Person", "Blog"], "blogPost": kwargs.get("blog_posts", [])}
        )

    elif page_type == "reel":
        base_schema.update(
            {
                "@type": ["Person", "VideoObject"],
                "video": {
                    "@type": "VideoObject",
                    "name": "Jake Crossman Demo Reel",
                    "description": (
                        "Professional acting demo reel showcasing range "
                        "and versatility"
                    ),
                    "uploadDate": "2025-01-01",
                    "duration": "PT3M",
                },
            }
        )

    return base_schema


def generate_meta_tags(page_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate comprehensive meta tags for a page with 2025 best practices."""

    title = page_data.get("title", SEOConfig.DEFAULT_TITLE)
    description = page_data.get("description", SEOConfig.DEFAULT_DESCRIPTION)
    keywords = page_data.get("keywords", SEOConfig.DEFAULT_KEYWORDS)
    image = page_data.get("image", f"{SEOConfig.SITE_URL}/static/images/headshot-1.jpg")
    canonical_url = page_data.get(
        "canonical_url", request.url if request else SEOConfig.SITE_URL
    )

    return {
        # Basic meta tags
        "title": title,
        "description": description,
        "keywords": (", ".join(keywords) if isinstance(keywords, list) else keywords),
        "author": SEOConfig.PERSON_INFO["name"],
        "canonical_url": canonical_url,
        "robots": page_data.get(
            "robots",
            ("index, follow, max-snippet:-1, max-image-preview:large"),
        ),
        # Enhanced meta tags for 2025
        "language": "en-US",
        "content_language": "en",
        "geo_region": "US-CA",
        "geo_placename": "Los Angeles, California",
        "geo_position": "34.0522;-118.2437",
        "ICBM": "34.0522, -118.2437",
        # Security and privacy
        "referrer": "strict-origin-when-cross-origin",
        "permissions_policy": "camera=(), microphone=(), geolocation=()",
        # Performance hints
        "dns_prefetch": [
            "//fonts.googleapis.com",
            "//fonts.gstatic.com",
            "//cdnjs.cloudflare.com",
        ],
        "preconnect": ["https://fonts.googleapis.com", "https://fonts.gstatic.com"],
        # Open Graph tags (enhanced)
        "og_title": title,
        "og_description": description,
        "og_image": image,
        "og_image_width": "1200",
        "og_image_height": "630",
        "og_image_alt": (f'{SEOConfig.PERSON_INFO["name"]} - Professional Actor'),
        "og_url": canonical_url,
        "og_type": page_data.get("og_type", "website"),
        "og_site_name": SEOConfig.SITE_NAME,
        "og_locale": "en_US",
        "og_video": page_data.get("og_video", ""),
        # Twitter Card tags (enhanced)
        "twitter_card": "summary_large_image",
        "twitter_site": "@jakecrossman",
        "twitter_creator": "@jakecrossman",
        "twitter_title": title,
        "twitter_description": description,
        "twitter_image": image,
        "twitter_image_alt": (f'{SEOConfig.PERSON_INFO["name"]} - Professional Actor'),
        "twitter_player": page_data.get("twitter_player", ""),
        # Mobile & App Meta Tags (enhanced)
        "viewport": (
            "width=device-width, initial-scale=1.0, maximum-scale=5.0, "
            "user-scalable=yes"
        ),
        "theme_color": "#ffd700",
        "color_scheme": "dark light",
        "apple_mobile_web_app_capable": "yes",
        "apple_mobile_web_app_status_bar_style": "black-translucent",
        "apple_mobile_web_app_title": "Jake Crossman",
        "apple_touch_fullscreen": "yes",
        "mobile_web_app_capable": "yes",
        "msapplication_TileColor": "#ffd700",
        "msapplication_TileImage": (
            f"{SEOConfig.SITE_URL}/static/favicon/mstile-144x144.png"
        ),
        "msapplication_config": (
            f"{SEOConfig.SITE_URL}/static/favicon/browserconfig.xml"
        ),
        # Additional structured data hints
        "article_author": SEOConfig.PERSON_INFO["name"],
        "article_publisher": SEOConfig.SITE_NAME,
        "article_section": page_data.get("section", "Entertainment"),
        "article_tag": (
            ", ".join(keywords) if isinstance(keywords, list) else keywords
        ),
        # 2025 Entertainment Industry Meta Tags
        "industry": "Entertainment",
        "profession": "Actor",
        "specialization": "Comedy, Drama, Digital Content",
        "experience_level": "Professional",
        "union_status": "Non-Union",
        "representation_status": "Available",
        "casting_type": "Lead, Supporting, Commercial",
        "age_range": "25-35",
        "type_casting": "Athletic, Comedic, Digital Native",
        # Casting Director Specific Tags
        "contact_preference": "Email",
        "response_time": "24 hours",
        "travel_radius": "Unlimited",
        "equipment_access": "Self-tape capable",
        # Performance Specialties
        "performance_skills": "Improv, Stage Combat, Sports, Digital Content",
        "accent_skills": "General American, Southern, French, Russian",
        "athletic_skills": "Football, Baseball, Basketball, Swimming",
        "music_skills": "Piano, Guitar, Vocals",
        # Link prefetching for performance
        "prefetch": page_data.get("prefetch_urls", []),
        "preload": page_data.get("preload_resources", []),
        # Accessibility
        "color_scheme": "dark light",
        "reduced_motion": "reduce",
    }


def generate_breadcrumb_schema(breadcrumbs: List[Dict[str, str]]) -> Dict[str, Any]:
    """Generate breadcrumb schema markup."""
    item_list: List[Dict[str, Any]] = []
    breadcrumb_list = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": item_list,
    }

    for i, crumb in enumerate(breadcrumbs):
        item_list.append(
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": crumb["name"],
                "item": crumb["url"],
            }
        )

    return breadcrumb_list


def generate_organization_schema() -> Dict[str, Any]:
    """Generate organization schema for the website."""

    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": SEOConfig.SITE_NAME,
        "url": SEOConfig.SITE_URL,
        "founder": {"@type": "Person", "name": SEOConfig.PERSON_INFO["name"]},
        "sameAs": list(SEOConfig.SOCIAL_PROFILES.values()),
        "contactPoint": {
            "@type": "ContactPoint",
            "email": SEOConfig.SOCIAL_PROFILES["email"],
            "telephone": SEOConfig.SOCIAL_PROFILES["phone"],
            "contactType": "business inquiry",
        },
    }


def generate_local_business_schema() -> Dict[str, Any]:
    """Generate LocalBusiness schema markup for acting services."""

    return {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": SEOConfig.SITE_NAME,
        "description": "Professional acting services in Los Angeles and Virginia",
        "url": SEOConfig.SITE_URL,
        "telephone": SEOConfig.SOCIAL_PROFILES["phone"],
        "email": SEOConfig.SOCIAL_PROFILES["email"],
        "address": [
            {
                "@type": "PostalAddress",
                "addressLocality": SEOConfig.LOCAL_SEO["primary_market"]["city"],
                "addressRegion": SEOConfig.LOCAL_SEO["primary_market"]["region"],
                "addressCountry": SEOConfig.LOCAL_SEO["primary_market"]["country"],
            },
            {
                "@type": "PostalAddress",
                "addressLocality": SEOConfig.LOCAL_SEO["secondary_market"]["city"],
                "addressRegion": SEOConfig.LOCAL_SEO["secondary_market"]["region"],
                "addressCountry": SEOConfig.LOCAL_SEO["secondary_market"]["country"],
            },
        ],
        "geo": [
            {
                "@type": "GeoCoordinates",
                "latitude": SEOConfig.LOCAL_SEO["primary_market"]["latitude"],
                "longitude": SEOConfig.LOCAL_SEO["primary_market"]["longitude"],
            },
            {
                "@type": "GeoCoordinates",
                "latitude": SEOConfig.LOCAL_SEO["secondary_market"]["latitude"],
                "longitude": SEOConfig.LOCAL_SEO["secondary_market"]["longitude"],
            },
        ],
        "serviceArea": [
            {"@type": "State", "name": "California"},
            {"@type": "State", "name": "Virginia"},
        ],
        "priceRange": "$$",
        "openingHours": "Mo-Su 09:00-18:00",
        "sameAs": list(SEOConfig.SOCIAL_PROFILES.values())
        + list(SEOConfig.PROFESSIONAL_PROFILES.values()),
    }


def generate_creative_work_schema(
    work_type: str, work_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate schema for creative works (films, shows, etc.)."""

    base_schema = {
        "@context": "https://schema.org",
        "@type": work_type,
        "name": work_data.get("name", ""),
        "description": work_data.get("description", ""),
        "dateCreated": work_data.get("date", ""),
        "creator": {"@type": "Person", "name": SEOConfig.PERSON_INFO["name"]},
        "actor": {
            "@type": "Person",
            "name": SEOConfig.PERSON_INFO["name"],
            "url": SEOConfig.SITE_URL,
        },
    }

    if work_data.get("image"):
        base_schema["image"] = work_data["image"]

    if work_data.get("video"):
        base_schema["video"] = work_data["video"]

    return base_schema


def generate_faq_schema(faqs: List[Dict[str, str]]) -> Dict[str, Any]:
    """Generate FAQ schema markup."""

    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq["question"],
                "acceptedAnswer": {"@type": "Answer", "text": faq["answer"]},
            }
            for faq in faqs
        ],
    }


def generate_review_schema(reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate review/testimonial schema markup."""

    return {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": SEOConfig.PERSON_INFO["name"],
        "review": [
            {
                "@type": "Review",
                "author": {"@type": "Person", "name": review["author"]},
                "reviewBody": review["text"],
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": review.get("rating", 5),
                    "bestRating": 5,
                },
                "datePublished": review.get("date", ""),
            }
            for review in reviews
        ],
    }


def generate_video_schema(video_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate VideoObject schema for demo reels and acting clips."""

    return {
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "name": video_data.get("name", "Jake Crossman Demo Reel"),
        "description": video_data.get(
            "description",
            "Professional acting demo reel showcasing versatility and range",
        ),
        "thumbnailUrl": video_data.get(
            "thumbnail", f"{SEOConfig.SITE_URL}/static/images/demo-reel-thumbnail.jpg"
        ),
        "uploadDate": video_data.get("upload_date", "2025-01-01"),
        "duration": video_data.get("duration", "PT3M"),
        "contentUrl": video_data.get(
            "content_url", f"{SEOConfig.SITE_URL}/static/videos/demo-reel.mp4"
        ),
        "embedUrl": video_data.get("embed_url", ""),
        "creator": {
            "@type": "Person",
            "name": SEOConfig.PERSON_INFO["name"],
            "url": SEOConfig.SITE_URL,
        },
        "keywords": [
            "acting",
            "demo reel",
            "Jake Crossman",
            "actor showcase",
            "performance",
        ],
        "genre": ["Drama", "Comedy", "Commercial"],
        "inLanguage": "en-US",
    }


def generate_article_schema(article_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate Article schema for blog posts/news."""

    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article_data.get("title", ""),
        "description": article_data.get("description", ""),
        "image": article_data.get(
            "image", f"{SEOConfig.SITE_URL}/static/images/headshot-1.jpg"
        ),
        "author": {
            "@type": "Person",
            "name": SEOConfig.PERSON_INFO["name"],
            "url": SEOConfig.SITE_URL,
        },
        "publisher": {
            "@type": "Organization",
            "name": SEOConfig.SITE_NAME,
            "url": SEOConfig.SITE_URL,
            "logo": {
                "@type": "ImageObject",
                "url": f"{SEOConfig.SITE_URL}/static/images/headshot-1.jpg",
            },
        },
        "datePublished": article_data.get("date_published", ""),
        "dateModified": article_data.get("date_modified", ""),
        "mainEntityOfPage": {"@type": "WebPage", "@id": article_data.get("url", "")},
    }


def get_page_seo_data(page_name: str, **kwargs: Any) -> Dict[str, Any]:
    """Get complete SEO data for a specific page."""
    page_configs: Dict[str, Dict[str, Any]] = {
        "index": {
            "title": ("Jake Crossman - Professional Actor | " "Los Angeles & Virginia"),
            "description": (
                "Professional Actor Jake Crossman brings dynamic energy to "
                "every role. ESPN+ star, TikTok influencer with 1M+ followers. "
                "Based in Los Angeles, CA."
            ),
            "keywords": [
                "Jake Crossman actor",
                "Jacob Crossman",
                "Los Angeles actor",
                "Virginia actor",
                "ESPN actor",
                "TikTok actor",
                "professional actor",
                "demo reel",
            ],
            "schema_type": "homepage",
            "og_type": "profile",
            "section": "Acting Portfolio",
            "prefetch_urls": ["/about", "/reel", "/resume"],
            "preload_resources": ["/static/css/main.css", "/static/js/main.js"],
        },
        "about": {
            "title": "About Jake Crossman - Professional Actor Bio & Background",
            "description": (
                "Learn about Jake Crossman's journey from athlete to actor. "
                "Training, skills, and achievements including ESPN+ series, "
                "TikTok success, and theater awards."
            ),
            "keywords": [
                "Jake Crossman bio",
                "actor biography",
                "Jake Crossman background",
                "ESPN FUSE",
                "actor training",
                "athletic actor",
            ],
            "schema_type": "about",
            "og_type": "profile",
            "section": "Biography",
            "prefetch_urls": ["/reel", "/resume", "/gallery"],
            "robots": "index, follow, max-image-preview:large",
        },
        "resume": {
            "title": "Jake Crossman Acting Resume - Credits & Experience",
            "description": (
                "Professional acting resume for Jake Crossman featuring film, "
                "television, theater credits, training, and special skills. "
                "Available for hire in LA & Virginia."
            ),
            "keywords": [
                "Jake Crossman resume",
                "acting resume",
                "actor credits",
                "professional experience",
                "hiring actor",
            ],
            "schema_type": "resume",
            "og_type": "profile",
            "section": "Professional Experience",
            "prefetch_urls": ["/contact", "/reel"],
            "robots": "index, follow, max-snippet:-1",
        },
        "reel": {
            "title": "Jake Crossman Demo Reel - Professional Acting Showcase",
            "description": (
                "Watch Jake Crossman's professional acting demo reel "
                "showcasing range in comedy, drama, and commercial work. "
                "High-quality performance samples."
            ),
            "keywords": [
                "Jake Crossman demo reel",
                "acting reel",
                "actor showcase",
                "professional reel",
                "casting reel",
            ],
            "schema_type": "reel",
            "og_type": "video.other",
            "section": "Demo Reel",
            "og_video": f"{SEOConfig.SITE_URL}/static/videos/demo-reel.mp4",
            "twitter_player": f"{SEOConfig.SITE_URL}/reel",
            "prefetch_urls": ["/gallery", "/contact"],
            "robots": "index, follow, max-video-preview:-1",
        },
        "gallery": {
            "title": (
                "Jake Crossman Photo Gallery - Professional Headshots & " "Portfolio"
            ),
            "description": (
                "Professional headshots and behind-the-scenes photos of "
                "Jake Crossman. High-resolution images for casting directors "
                "and media use."
            ),
            "keywords": [
                "Jake Crossman photos",
                "professional headshots",
                "actor photos",
                "portfolio gallery",
                "casting photos",
            ],
            "schema_type": "gallery",
            "og_type": "website",
            "section": "Photo Gallery",
            "prefetch_urls": ["/about", "/contact"],
            "robots": "index, follow, max-image-preview:large",
        },
        "news": {
            "title": "Jake Crossman News & Updates - Latest Projects & Blog",
            "description": (
                "Latest news, updates, and blog posts from Jake Crossman. "
                "Current projects, industry insights, and behind-the-scenes "
                "content."
            ),
            "keywords": [
                "Jake Crossman news",
                "actor blog",
                "latest projects",
                "industry updates",
                "behind the scenes",
            ],
            "schema_type": "news",
            "og_type": "blog",
            "section": "News & Blog",
            "prefetch_urls": ["/about", "/reel"],
            "robots": "index, follow, max-snippet:-1, max-image-preview:large",
        },
        "contact": {
            "title": "Contact Jake Crossman - Professional Actor Representation",
            "description": (
                "Contact Jake Crossman for professional acting opportunities. "
                "Available for film, television, theater, and commercial work "
                "in LA & Virginia."
            ),
            "keywords": [
                "contact Jake Crossman",
                "hire actor",
                "actor representation",
                "casting contact",
                "professional inquiry",
            ],
            "schema_type": "contact",
            "og_type": "website",
            "section": "Contact",
            "prefetch_urls": ["/resume", "/reel"],
            "robots": "index, follow, noarchive",
            "faq_data": [
                {
                    "question": "What is Jake's availability for projects?",
                    "answer": (
                        "Jake is available for projects year-round and can "
                        "travel anywhere for the right opportunity. He's based "
                        "between Los Angeles, CA and Virginia."
                    ),
                },
                {
                    "question": (
                        "Does Jake work with smaller/independent productions?"
                    ),
                    "answer": (
                        "Absolutely! Jake is passionate about storytelling at "
                        "every level and has experience with both major network "
                        "content and independent projects."
                    ),
                },
                {
                    "question": (
                        "Can Jake help with content creation and social media?"
                    ),
                    "answer": (
                        "Yes! With 1M+ TikTok followers and extensive digital "
                        "media experience, Jake can contribute to both "
                        "performance and promotional aspects of projects."
                    ),
                },
                {
                    "question": "What about athletic/physical roles?",
                    "answer": (
                        "Athletic performance is one of Jake's strongest "
                        "assets. He has extensive sports background and is "
                        "comfortable with physical comedy, action sequences, "
                        "and sports-related content."
                    ),
                },
            ],
        },
    }

    page_config = page_configs.get(page_name, {})

    # Generate meta tags
    meta_tags = generate_meta_tags(page_config)

    # Generate schema
    schema_markup = generate_page_schema(
        page_config.get("schema_type", "webpage"), **kwargs
    )
    # Generate breadcrumbs
    breadcrumbs = []
    if page_name != "index":
        breadcrumbs = [
            {"name": "Home", "url": SEOConfig.SITE_URL},
            {
                "name": page_config.get("title", page_name.title()),
                "url": request.url if request else SEOConfig.SITE_URL,
            },
        ]
        breadcrumb_schema = generate_breadcrumb_schema(breadcrumbs)
    else:
        breadcrumb_schema = None

    return {
        "meta_tags": meta_tags,
        "schema_markup": schema_markup,
        "breadcrumb_schema": breadcrumb_schema,
        "organization_schema": generate_organization_schema(),
        "local_business_schema": generate_local_business_schema(),
        "actor_profession_schema": generate_actor_profession_schema(),
        "entertainment_organization_schema": (
            generate_entertainment_organization_schema()
        ),
        "video_schema": (generate_video_schema({}) if page_name == "reel" else None),
        "faq_schema": (
            generate_faq_schema(page_config.get("faq_data", []))
            if page_config.get("faq_data")
            else None
        ),
        "performance_hints": {
            "critical_resources": page_config.get("preload_resources", []),
            "prefetch_urls": page_config.get("prefetch_urls", []),
            "dns_prefetch": [
                "fonts.googleapis.com",
                "fonts.gstatic.com",
                "cdnjs.cloudflare.com",
            ],
        },
    }


def generate_actor_profession_schema() -> Dict[str, Any]:
    """Generate advanced actor profession schema for 2025 entertainment industry SEO."""

    return {
        "@context": "https://schema.org",
        "@type": ["Person", "PerformingArtist", "Actor"],
        "name": SEOConfig.PERSON_INFO["name"],
        "alternateName": SEOConfig.PERSON_INFO["alternateName"],
        "jobTitle": "Professional Actor",
        "hasOccupation": {
            "@type": "Occupation",
            "name": "Actor",
            "occupationLocation": [
                {
                    "@type": "City",
                    "name": "Los Angeles",
                    "containedInPlace": {"@type": "State", "name": "California"},
                },
                {
                    "@type": "City",
                    "name": "Lynchburg",
                    "containedInPlace": {"@type": "State", "name": "Virginia"},
                },
            ],
            "skills": [
                "Drama",
                "Comedy",
                "Sketch Comedy",
                "Improv",
                "Stage Combat",
                "Voiceover",
                "On-Camera Hosting",
                "Teleprompter",
                "Sports Commentary",
                "Digital Content Creation",
                "Social Media",
                "Athletic Performance",
            ],
            "experienceRequirements": "Professional",
            "responsibilities": [
                "Character development and portrayal",
                "Script analysis and memorization",
                "Collaboration with directors and cast",
                "Physical and vocal performance",
                "Digital content creation",
            ],
        },
        "knowsAbout": [
            "Method Acting",
            "Meisner Technique",
            "Athletic Performance",
            "Digital Marketing",
            "Content Creation",
            "Sports Commentary",
            "Health and Wellness",
            "Social Media Strategy",
        ],
        "award": SEOConfig.ACHIEVEMENTS,
        "memberOf": [
            {
                "@type": "Organization",
                "name": "Erie Community Theater",
                "description": "Local theater company",
            }
        ],
        "hasCredential": [
            {
                "@type": "EducationalOccupationalCredential",
                "credentialCategory": "degree",
                "educationalLevel": "Bachelor's Degree",
                "about": "Digital Media (Video Production)",
                "recognizedBy": ["Gannon University", "Liberty University"],
            },
            {
                "@type": "EducationalOccupationalCredential",
                "credentialCategory": "certification",
                "about": "NASM Certified Nutritionist",
                "dateCreated": "2022",
                "expires": "2026",
            },
        ],
        "performerIn": [
            {
                "@type": "TVSeries",
                "name": "Fuse",
                "description": "ESPN+ sports comedy sketch series",
                "datePublished": "2023",
                "productionCompany": "ESPN+",
            },
            {
                "@type": "Movie",
                "name": "Continue to Win",
                "description": "Independent pilot directed by Lester Speight",
                "datePublished": "2025",
                "genre": ["Drama", "Sports"],
            },
            {
                "@type": "Movie",
                "name": "F1 The Movie",
                "description": "Feature film directed by Joseph Kosinski",
                "datePublished": "2025",
                "genre": ["Action", "Sports"],
            },
        ],
    }


def generate_entertainment_organization_schema() -> Dict[str, Any]:
    """Generate entertainment industry organization schema."""

    return {
        "@context": "https://schema.org",
        "@type": "EntertainmentBusiness",
        "name": SEOConfig.SITE_NAME,
        "description": "Professional acting services and digital content creation",
        "url": SEOConfig.SITE_URL,
        "founder": {"@type": "Person", "name": SEOConfig.PERSON_INFO["name"]},
        "serviceType": [
            "Acting Services",
            "Digital Content Creation",
            "Social Media Marketing",
            "Voice Over",
            "Commercial Performance",
        ],
        "areaServed": [
            {"@type": "State", "name": "California"},
            {"@type": "State", "name": "Virginia"},
            {"@type": "Country", "name": "United States"},
        ],
        "paymentAccepted": ["Cash", "Check", "Wire Transfer"],
        "currenciesAccepted": "USD",
    }
