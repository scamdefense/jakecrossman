from flask import Flask, render_template, request
from flask_wtf import CSRFProtect
from flask_caching import Cache
import os
from dotenv import load_dotenv

# Load environment variables so configuration classes can access them
load_dotenv()

csrf = CSRFProtect()
cache = Cache()


class BaseConfig:
    """Base configuration with common settings."""

    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
    ENABLE_CACHE_HEADERS = os.getenv("ENABLE_CACHE_HEADERS", "True") == "True"
    STATIC_CACHE_TIMEOUT = int(os.getenv("STATIC_CACHE_TIMEOUT", 3600))
    SEND_FILE_MAX_AGE_DEFAULT = STATIC_CACHE_TIMEOUT if ENABLE_CACHE_HEADERS else 0
    CACHE_TYPE = os.getenv("CACHE_TYPE", "SimpleCache")
    CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", 300))
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
    cache.init_app(app)

    # Register blueprints
    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    @app.errorhandler(404)
    def page_not_found(error):
        """Render custom 404 page."""
        return render_template("404.html"), 404

    @app.after_request
    def add_static_cache_headers(response):
        """Add Cache-Control headers for static files if enabled."""
        if app.config.get("ENABLE_CACHE_HEADERS") and request.path.startswith(
            "/static"
        ):
            max_age = app.config.get("STATIC_CACHE_TIMEOUT", 3600)
            response.headers["Cache-Control"] = f"public, max-age={max_age}"
        return response

    return app
