from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mysqldb import MySQL
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_mail import Mail
from . import glblvars

db = SQLAlchemy()

# For profile pictures
images = UploadSet('images', IMAGES)

# For password reset
mail = Mail()

def create_app():
    app = Flask(__name__)
    mysql = MySQL(app)

    MYSQL_HOST = glblvars.DB_HOST
    MYSQL_USER = glblvars.DB_USER
    MYSQL_PASSWORD = glblvars.DB_PASS
    SECRET_KEY = glblvars.SECRET_KEY
    MYSQL_PORT = glblvars.DB_PORT
    MYSQL_NAME = glblvars.DB_NAME

    app.config['SECRET_KEY'] = SECRET_KEY
    uri = "mysql+mysqldb://"+ MYSQL_USER + ":" + MYSQL_PASSWORD + "@" + MYSQL_HOST + ":" + MYSQL_PORT + "/" + MYSQL_NAME \
    
    # MySQL-Python
    # mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    
    db.init_app(app)

    # Configure app to handle image upload
    app.config["UPLOADED_IMAGES_DEST"] = "website/static/uploads"
    configure_uploads(app, images)

    # Configure app for email to allow users to reset passwords
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = "eleventhhouresports@gmail.com"
    app.config['MAIL_PASSWORD'] = "cjscyascqlysncvs"
    mail = Mail(app)

    from .views import views
    from .auth import auth
    from .logic import logic
    
    # Register blueprints for Flask
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(logic, url_prefix='/')
    
    from .models import User
    
    # with app.app_context():
    #     db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
