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
