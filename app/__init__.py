from ntpath import join
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO


basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI']  = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config[' SQLALCHEMY_TRACK_MODIFICATIONS']  = False
app.config['UPLOAD_FOLDER'] = basedir +'/src/images'
app.config['UPLOADED_IMAGES_DEST'] = basedir +'/src/images'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
socketio = SocketIO(app, cors_allowed_origins="*")


login = LoginManager(app)
login.login_view = 'login'



from app import routes,models