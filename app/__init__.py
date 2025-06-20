from flask import Flask, render_template
from flask_wtf import CSRFProtect
import os
from dotenv import load_dotenv

# Load environment variables so configuration classes can access them
load_dotenv()

csrf = CSRFProtect()


class BaseConfig:
    """Base configuration with common settings."""

    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
    SEND_FILE_MAX_AGE_DEFAULT = 0
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024

    # Email Configuration
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    EMAIL_FROM = os.getenv("EMAIL_FROM")
    EMAIL_TO = os.getenv("EMAIL_TO")

    # Analytics Configuration
    GOOGLE_ANALYTICS_ID = os.getenv("GOOGLE_ANALYTICS_ID")
    GOOGLE_TAG_MANAGER_ID = os.getenv("GOOGLE_TAG_MANAGER_ID")
    CLARITY_PROJECT_ID = os.getenv("CLARITY_PROJECT_ID")
    FACEBOOK_PIXEL_ID = os.getenv("FACEBOOK_PIXEL_ID")

    # Search Engine Verification
    GOOGLE_SEARCH_CONSOLE_VERIFICATION = os.getenv("GOOGLE_SEARCH_CONSOLE_VERIFICATION")
    BING_VERIFICATION = os.getenv("BING_VERIFICATION")
    YANDEX_VERIFICATION = os.getenv("YANDEX_VERIFICATION")
    PINTEREST_VERIFICATION = os.getenv("PINTEREST_VERIFICATION")


class DevelopmentConfig(BaseConfig):
    """Configuration for local development."""

    DEBUG = True


class TestingConfig(BaseConfig):
    """Configuration used during tests."""

    TESTING = True


class ProductionConfig(BaseConfig):
    """Configuration for deployed environments."""

    DEBUG = False


def create_app(config_name="development"):
    """Application factory pattern."""
    load_dotenv()

    app = Flask(__name__)

    # Map config names to classes
    config_map = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
        "default": DevelopmentConfig,
    }

    config_class = config_map.get(config_name, DevelopmentConfig)
    app.config.from_object(config_class)
    csrf.init_app(app)

    # Register blueprints
    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    @app.errorhandler(404)
    def page_not_found(error):
        """Render custom 404 page."""
        return render_template("404.html"), 404

    return app
