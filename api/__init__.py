from flask import Flask
from flask_restx import Api
from flask_cors import CORS
# from flask_migrate import Migrate
from .request_checking.views import accia_namespace
#from .analytics.views import analytics_namespace
from .request_augmentation.views import request_augmentation_namespace
from .explain.views import explain_namespace
from .auth.views import auth_namespace
from .definition.views import definition_namespace
from .config.config import config_dict
from .utils import db
from .models.users import User
from .models.requests import Request
from flask_jwt_extended import JWTManager

def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    app.config.from_object(config)

    api = Api(app)

    api.add_namespace(accia_namespace)
    api.add_namespace(request_augmentation_namespace, path='/Checking')
    api.add_namespace(explain_namespace, path='/ModelAnalysis')
    api.add_namespace(definition_namespace, path='/Definition')
    api.add_namespace(auth_namespace, path='/auth')
    
    #api.add_namespace(analytics_namespace, path='/analytics')
    CORS(app)
    db.init_app(app)
    # migrate = Migrate(app, db)
    
    jwt = JWTManager(app)

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'user': User,
            'request': Request
        }

    return app