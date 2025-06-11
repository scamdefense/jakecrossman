from flask import Flask


def create_app(config_name="default"):
    """Application factory pattern."""
    app = Flask(__name__)

    # Configure for better video/audio serving
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0  # Disable caching for development
    app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100MB max file size

    # Register blueprints
    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    return app
