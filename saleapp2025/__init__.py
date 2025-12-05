from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import cloudinary

app = Flask(__name__)

app.secret_key="longyeuthuratnhieuoklanha"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:5225@localhost/sale2025db?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 3

db = SQLAlchemy(app)

login_manager = LoginManager(app)

cloudinary.config(cloud_name="dmia4sdki",
                  api_key="595166767185712",
                  api_secret="nBO01bBlqslGGoI_nJuswVIxj-I",)