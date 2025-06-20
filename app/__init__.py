from flask import Flask
from flask_wtf import CSRFProtect
import os
from dotenv import load_dotenv

csrf = CSRFProtect()


def create_app(config_name="default"):
    """Application factory pattern."""
    # Load environment variables from .env file
    load_dotenv()

    app = Flask(__name__)  # Load configuration from environment variables
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "fallback-secret-key")
    csrf.init_app(app)
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024

    # Email Configuration
    app.config["SMTP_SERVER"] = os.getenv("SMTP_SERVER")
    app.config["SMTP_PORT"] = int(os.getenv("SMTP_PORT", 587))
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["EMAIL_FROM"] = os.getenv("EMAIL_FROM")
    app.config["EMAIL_TO"] = os.getenv("EMAIL_TO")

    # Analytics Configuration
    app.config["GOOGLE_ANALYTICS_ID"] = os.getenv("GOOGLE_ANALYTICS_ID")
    app.config["GOOGLE_TAG_MANAGER_ID"] = os.getenv("GOOGLE_TAG_MANAGER_ID")
    app.config["CLARITY_PROJECT_ID"] = os.getenv("CLARITY_PROJECT_ID")
    app.config["FACEBOOK_PIXEL_ID"] = os.getenv("FACEBOOK_PIXEL_ID")

    # Search Engine Verification
    app.config["GOOGLE_SEARCH_CONSOLE_VERIFICATION"] = os.getenv(
        "GOOGLE_SEARCH_CONSOLE_VERIFICATION"
    )
    app.config["BING_VERIFICATION"] = os.getenv("BING_VERIFICATION")
    app.config["YANDEX_VERIFICATION"] = os.getenv("YANDEX_VERIFICATION")
    app.config["PINTEREST_VERIFICATION"] = os.getenv("PINTEREST_VERIFICATION")

    # Register blueprints
    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    return app
