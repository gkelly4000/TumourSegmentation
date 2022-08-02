import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin


from keras.models import load_model


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config['SECRET_KEY'] = "MYSECRETKEY"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.db"

app.debug = True

db = SQLAlchemy(app)

model = load_model("app/MLmodels/dice65", compile=False)

admin = Admin(app)

from app import routes
