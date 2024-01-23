from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from local_settings import SECRET_KEY

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/filmes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes
from app import models