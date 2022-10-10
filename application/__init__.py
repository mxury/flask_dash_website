from flask import Flask


def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile('../config.py')

    with app.app_context():
        from . import routes

        from application.dash.dashboard import create_dashboard
        app = create_dashboard(app)

        return app


