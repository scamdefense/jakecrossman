import pytest
from app.seo import generate_meta_tags, generate_page_schema, SEOConfig


def test_generate_meta_tags_defaults(app):
    with app.test_request_context('/'):
        tags = generate_meta_tags({})
    assert tags["title"] == SEOConfig.DEFAULT_TITLE
    assert tags["description"] == SEOConfig.DEFAULT_DESCRIPTION
    # canonical should use request URL
    assert tags["canonical_url"].endswith('/')
    for key in ["og_title", "twitter_title", "robots"]:
        assert key in tags


def test_generate_meta_tags_custom(app):
    page_data = {
        "title": "Custom Title",
        "description": "Custom desc",
        "keywords": ["one", "two"],
        "canonical_url": "https://example.com/page",
        "og_type": "article",
    }
    with app.test_request_context('/custom'):
        tags = generate_meta_tags(page_data)
    assert tags["title"] == "Custom Title"
    assert tags["description"] == "Custom desc"
    assert tags["keywords"] == "one, two"
    assert tags["canonical_url"] == "https://example.com/page"
    assert tags["og_type"] == "article"
    assert tags["twitter_title"] == "Custom Title"


def test_generate_page_schema_homepage():
    schema = generate_page_schema("homepage")
    assert "WebSite" in schema["@type"]
    assert "potentialAction" in schema
    assert schema["@context"] == "https://schema.org"


def test_generate_page_schema_about():
    schema = generate_page_schema("about")
    assert "knowsAbout" in schema
    assert "award" in schema
    assert SEOConfig.PERSON_INFO["name"] == schema["name"]
