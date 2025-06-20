import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app, render_template
from concurrent.futures import ThreadPoolExecutor
import logging
from typing import Any, Dict, cast

logger = logging.getLogger(__name__)

# ThreadPoolExecutor to offload SMTP calls
executor = ThreadPoolExecutor(max_workers=2)


def _send_email_task(
    form_data: Dict[str, Any],
    smtp_server: str,
    smtp_port: int,
    username: str,
    password: str,
    from_email: str,
    to_email: str,
) -> None:
    """Send the email synchronously. Intended to run in a worker thread."""
    try:
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
            "Contact email sent successfully from %s",
            form_data.get("email", "unknown"),
        )
    except Exception as exc:  # pragma: no cover - log unexpected exceptions
        logger.error("Failed to send contact email: %s", exc)


def send_contact_email(form_data: Dict[str, Any]) -> bool:
    """Schedule contact email sending in a background thread."""
    try:
        smtp_server = cast(str, current_app.config.get("SMTP_SERVER"))
        smtp_port = cast(int, current_app.config.get("SMTP_PORT"))
        username = cast(str, current_app.config.get("MAIL_USERNAME"))
        password = cast(str, current_app.config.get("MAIL_PASSWORD"))
        from_email = cast(str, current_app.config.get("EMAIL_FROM"))
        to_email = cast(str, current_app.config.get("EMAIL_TO"))

        if not all([smtp_server, smtp_port, username, password, from_email, to_email]):
            logger.error("Missing email configuration")
            return False

        # Offload the SMTP call to a worker thread
        executor.submit(
            _send_email_task,
            form_data,
            smtp_server,
            smtp_port,
            username,
            password,
            from_email,
            to_email,
        )

        return True

    except Exception as exc:
        logger.error("Failed to schedule contact email: %s", exc)
        return False


def create_email_body(form_data: Dict[str, Any]) -> str:
    name = form_data.get("name", "Not provided")
    email = form_data.get("email", "Not provided")
    production = form_data.get("production", "Not provided")
    role = form_data.get("role", "Not provided")
    timeline = form_data.get("timeline", "Not provided")
    message = form_data.get("message", "Not provided")
    resume_attach = form_data.get("resume_attach", False)

    return render_template(
        "email/contact_email.html",
        name=name,
        email=email,
        production=production,
        role=role,
        timeline=timeline,
        message=message,
        resume_attach=resume_attach,
    )
