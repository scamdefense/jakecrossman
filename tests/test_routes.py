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


def test_unknown_page(client):
    """Requesting an unknown page should return custom 404 template."""
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    assert b"Page Not Found" in response.data
