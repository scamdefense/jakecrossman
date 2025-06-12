import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app
import logging

logger = logging.getLogger(__name__)


def send_contact_email(form_data):
    try:
        smtp_server = current_app.config.get("SMTP_SERVER")
        smtp_port = current_app.config.get("SMTP_PORT")
        username = current_app.config.get("MAIL_USERNAME")
        password = current_app.config.get("MAIL_PASSWORD")
        from_email = current_app.config.get("EMAIL_FROM")
        to_email = current_app.config.get("EMAIL_TO")

        if not all([smtp_server, smtp_port, username, password, from_email, to_email]):
            logger.error("Missing email configuration")
            return False

        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg[
            "Subject"
        ] = f"New Contact Form Submission from {form_data.get('name', 'Unknown')}"

        body = create_email_body(form_data)
        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)

        logger.info(
            f"Contact email sent successfully from {form_data.get('email', 'unknown')}"
        )
        return True

    except Exception as e:
        logger.error(f"Failed to send contact email: {str(e)}")
        return False


def create_email_body(form_data):
    name = form_data.get("name", "Not provided")
    email = form_data.get("email", "Not provided")
    production = form_data.get("production", "Not provided")
    role = form_data.get("role", "Not provided")
    timeline = form_data.get("timeline", "Not provided")
    message = form_data.get("message", "Not provided")
    resume_attach = form_data.get("resume_attach", False)

    html_body = f"""
    <h2>New Contact Form Submission</h2>
    <p><strong>Name:</strong> {name}</p>
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Production/Project:</strong> {production}</p>
    <p><strong>Role/Opportunity:</strong> {role}</p>
    <p><strong>Timeline:</strong> {timeline}</p>
    <p><strong>Message:</strong> {message}</p>
    {f'<p><strong>Professional Materials Package Requested:</strong> '
     f'"Yes</p>' if resume_attach else ''}
    """

    return html_body
