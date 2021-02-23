# app/__init__.py
import os

from flask import Flask
from flask_login import LoginManager
# from flask_jwt import JWT, jwt_required
from flask_jwt_extended import (
    JWTManager, jwt_required, jwt_optional, create_access_token, get_jwt_identity, get_jwt_claims)

from app.model.user import User, USERS

from app.ctl.main_ctl import main_ctl
from app.ctl.goods_ctl import goods_ctl
from app.ctl.category_ctl import category_ctl
from app.ctl.loginout_ctl import loginout_ctl
from app.service.user_service import UserService

from config import Config


app=Flask(__name__)

app.secret_key = os.urandom(24)

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

# def authenticate(username, password):
#     ret, user = user_service.get_user(user_id)
#
#     if user and safe_str_cmp(user.password, password):
#         return user
#
# def identity(payload):
#     user_id = payload['identity']
#     ret, user = user_service.get_user(user_id)
#     return user

# jwt = JWT(app, authenticate, identity)
app.config['JWT_SECRET_KEY'] = Config.jwt_key
jwt = JWTManager(app)
