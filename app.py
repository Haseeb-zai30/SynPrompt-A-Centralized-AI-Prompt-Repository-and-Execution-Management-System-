from flask import Flask

from config import Config
from extensions import mysql, bcrypt

# Import Blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.prompt import prompt_bp
from routes.project import project_bp
from routes.favorite import favorite_bp
from routes.execution import execution_bp
from routes.search import search_bp


def create_app():

    app = Flask(__name__)

    # Load Configuration
    app.config.from_object(Config)

    # Initialize Extensions
    mysql.init_app(app)
    bcrypt.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(prompt_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(favorite_bp)
    app.register_blueprint(execution_bp)
    app.register_blueprint(search_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)