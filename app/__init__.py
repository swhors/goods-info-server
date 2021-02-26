# app/__init__.py
import os

from flask import Flask
from flask_login import LoginManager
# from flask_jwt import JWT, jwt_required

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from app.model.user import User, USERS

from app.ctl.main_ctl import main_ctl
from app.ctl.goods_ctl import goods_ctl
from app.ctl.category_ctl import category_ctl
from app.ctl.loginout_ctl import loginout_ctl
from app.service.user_service import UserService

from config import Config


app=Flask(__name__)

app.secret_key = os.urandom(24)
app.config['JWT_SECRET_KEY'] = Config.jwt_key

jwt_manager = JWTManager(app)

app.register_blueprint(category_ctl)
app.register_blueprint(goods_ctl)
app.register_blueprint(main_ctl)
app.register_blueprint(loginout_ctl)

login_manager = LoginManager()
login_manager.init_app(app)

from app.ctl.loginout_ctl import user_service

@login_manager.user_loader
def user_loader(user_id) -> User:
    ret, user = user_service.get_user(user_id)
    return user
