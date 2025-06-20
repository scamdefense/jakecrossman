def test_index_page(client):
    """Test homepage loads correctly."""
    response = client.get("/")
    assert response.status_code == 200
    assert b'JACOB "JAKE" CROSSMAN' in response.data


def test_about_page(client):
    """Test about page loads correctly."""
    response = client.get("/about")
    assert response.status_code == 200
    assert b"About Jake Crossman" in response.data


def test_contact_page(client):
    """Test contact page loads correctly."""
    response = client.get("/contact")
    assert response.status_code == 200
    assert b"Get In Touch" in response.data
    assert b'name="csrf_token"' in response.data


def test_contact_post_json_success(client, monkeypatch):
    """Posting valid JSON should schedule an email and return success."""

    called = {}

    def fake_submit(func, *args, **kwargs):
        called["submitted"] = True
        # execute synchronously for test determinism
        func(*args, **kwargs)

    monkeypatch.setattr("app.email_utils.executor.submit", fake_submit)

    # provide minimal email configuration on the flask app
    client.application.config.update(
        {
            "SMTP_SERVER": "smtp.test",
            "SMTP_PORT": 587,
            "MAIL_USERNAME": "user",
            "MAIL_PASSWORD": "pass",
            "EMAIL_FROM": "from@test",
            "EMAIL_TO": "to@test",
        }
    )

    payload = {"name": "Test", "email": "a@b.com", "message": "hi"}
    response = client.post("/contact", json=payload)

    assert response.status_code == 200
    assert response.get_json()["success"] is True
    assert called.get("submitted") is True


def test_contact_post_json_missing(client):
    """Missing required fields should return 400."""

    payload = {"name": "Test", "email": "", "message": ""}
    response = client.post("/contact", json=payload)
    assert response.status_code == 400
    assert response.get_json()["success"] is False


def test_contact_post_json_invalid_email(client):
    """Invalid email format should be rejected."""

    payload = {"name": "Test", "email": "invalid", "message": "hi"}
    response = client.post("/contact", json=payload)
    assert response.status_code == 400
    assert response.get_json()["success"] is False


def test_video_valid(client):
    """Valid video request should return the file."""
    response = client.get("/video/demo-reel.mp4")
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("video/")


def test_video_path_traversal(client):
    """Path traversal attempts should be blocked."""
    response = client.get("/video/../../etc/passwd")
    assert response.status_code == 404


def test_video_encoded_traversal(client):
    """Encoded path traversal should also be blocked."""
    response = client.get("/video/..%2F..%2Fetc/passwd")
    assert response.status_code == 404


def test_sitemap_xml(client):
    """Ensure the main sitemap is reachable and XML is returned."""
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/xml")


def test_news_sitemap_xml(client):
    """Ensure the news sitemap endpoint returns XML."""
    response = client.get("/news-sitemap.xml")
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/xml")


def test_gallery_page_dynamic(client):
    """Gallery page should include loaded markdown title."""
    response = client.get("/gallery")
    assert response.status_code == 200
    assert b"Professional Headshot 1" in response.data


def test_news_page_dynamic(client):
    """News page should include loaded markdown entry."""
    response = client.get("/news")
    assert response.status_code == 200
    assert b"Cardistry Consultant on F1 The Movie" in response.data


def test_image_sitemap_xml(client):
    """Ensure the image sitemap endpoint returns XML."""
    response = client.get("/image-sitemap.xml")
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/xml")


def test_video_sitemap_xml(client):
    """Ensure the video sitemap endpoint returns XML."""
    response = client.get("/video-sitemap.xml")
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/xml")


def test_robots_txt(client):
    """Ensure robots.txt is served with plain text content."""
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("text/plain")


def test_unknown_page(client):
    """Requesting an unknown page should return custom 404 template."""
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    assert b"Page Not Found" in response.data


def test_static_cache_headers(client):
    """Static files should include cache headers when enabled."""
    client.application.config.update({
        "ENABLE_CACHE_HEADERS": True,
        "STATIC_CACHE_TIMEOUT": 123,
    })
    response = client.get("/static/robots.txt")
    assert response.status_code == 200
    assert response.headers["Cache-Control"] == "public, max-age=123"
