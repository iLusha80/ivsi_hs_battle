from flask import Blueprint

def register_routes(app):
    from .main import main_bp
    from .admin import admin_bp
    from .add_game import add_game_bp
    from .games import games_bp
    from .statistic import statistics_bp
    from .for_test import for_test_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(add_game_bp)
    app.register_blueprint(games_bp)
    app.register_blueprint(statistics_bp)
    app.register_blueprint(for_test_bp)
