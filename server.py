from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
from flask import request
from flask.json import jsonify
import json
from flask_cors import CORS
from flask_marshmallow import Marshmallow


app= Flask(__name__) 

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

@app.route("/")
def home():
    return "Server Working"
