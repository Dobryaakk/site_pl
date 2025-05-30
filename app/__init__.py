from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect

mongo = PyMongo()
login_manager = LoginManager()
limiter = Limiter(key_func=get_remote_address)
csrf = CSRFProtect()

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    mongo.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)
    csrf.init_app(app)
    
    # Set up login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    from app.models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.get_user(mongo, user_id)
    
    # Register blueprints
    from app.routes import auth, blog, admin, main
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(main.bp)
    
    return app 