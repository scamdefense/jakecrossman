from app.email_utils import create_email_body


def test_create_email_body_with_resume(app):
    data = {
        "name": "Tester",
        "email": "tester@example.com",
        "production": "Prod",
        "role": "Actor",
        "timeline": "Soon",
        "message": "Hello",
        "resume_attach": True,
    }
    with app.app_context():
        body = create_email_body(data)
    expected = '<p><strong>Professional Materials Package Requested:</strong> "Yes"</p>'
    assert expected in body


def test_create_email_body_without_resume(app):
    data = {
        "name": "Tester",
        "email": "tester@example.com",
        "production": "Prod",
        "role": "Actor",
        "timeline": "Soon",
        "message": "Hello",
        "resume_attach": False,
    }
    with app.app_context():
        body = create_email_body(data)
    assert 'Professional Materials Package Requested' not in body


def test_create_email_body_includes_fields(app):
    data = {
        "name": "Tester",
        "email": "tester@example.com",
        "production": "Prod",
        "role": "Actor",
        "timeline": "Soon",
        "message": "Hello",
        "resume_attach": False,
    }
    with app.app_context():
        body = create_email_body(data)
    assert "<p><strong>Name:</strong> Tester</p>" in body
    assert "<p><strong>Email:</strong> tester@example.com</p>" in body
    assert "<p><strong>Production/Project:</strong> Prod</p>" in body
    assert "<p><strong>Role/Opportunity:</strong> Actor</p>" in body
    assert "<p><strong>Timeline:</strong> Soon</p>" in body
    assert "<p><strong>Message:</strong> Hello</p>" in body
