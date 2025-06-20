from app.email_utils import create_email_body


def test_create_email_body_with_resume():
    data = {
        "name": "Tester",
        "email": "tester@example.com",
        "production": "Prod",
        "role": "Actor",
        "timeline": "Soon",
        "message": "Hello",
        "resume_attach": True,
    }
    body = create_email_body(data)
    expected = '<p><strong>Professional Materials Package Requested:</strong> "Yes"</p>'
    assert expected in body


def test_create_email_body_without_resume():
    data = {
        "name": "Tester",
        "email": "tester@example.com",
        "production": "Prod",
        "role": "Actor",
        "timeline": "Soon",
        "message": "Hello",
        "resume_attach": False,
    }
    body = create_email_body(data)
    assert "Professional Materials Package Requested" not in body
