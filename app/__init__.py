import os
from flask import Flask
from instance.config import app_config
from .api import v1_blueprint
from flask_jwt_extended import JWTManager
from functools import wraps
from manage import create_tables
from .api.models import Blacklist



def create_app(config_name):
    """
    This function wraps the creation of a new Flask object
    and ModuleNotFoundError: No module named 'app' returns it after it's loaded up with configuration settings
    using 'app.config' and connected to DB using 'create_tables()'
    """
    app = Flask(__name__, instance_relative_config=True)
    create_tables()
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SECRET_KEY'] = "sweet_secret"
    app.config['JWT_SECRET_KEY'] = "jwt_sweet_secret"
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app.config['APP_SETTINGS'] = "development"
    jwt = JWTManager(app)

    # create user claims
    @jwt.user_claims_loader
    def add_claims_to_access_token(identity):
        return {
            'is_admin': identity
        }

    # check if token exists blacklist table
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        if Blacklist.search(jti):
            return True

    # register blueprint
    app.register_blueprint(v1_blueprint)

    return app
