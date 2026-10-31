from flask import Flask

def register_blueprints(app: Flask) -> None:
    from .health import health_bp

    app.register_blueprint(health_bp)