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
