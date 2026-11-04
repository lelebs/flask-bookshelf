from flask import Flask

def register_blueprints(app: Flask) -> None:
    from .health import health_bp
    from .authors import authors_bp
    from .books import books_bp

    for bp in (health_bp, authors_bp, books_bp):
        app.register_blueprint(bp)