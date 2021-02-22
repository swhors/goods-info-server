# app/__init__.py

from flask import Flask
from flask_login import LoginManager
import os


from app.model.data.user import User
from app.model.data.user import USERS

from app.ctl.main_ctl import main_ctl
from app.ctl.goods_ctl import goods_ctl
from app.ctl.category_ctl import category_ctl
from app.ctl.loginout_ctl import loginout_ctl

from app.model.user_model import UserModel

app=Flask(__name__)

app.secret_key = os.urandom(24)

app.register_blueprint(category_ctl)
app.register_blueprint(goods_ctl)
app.register_blueprint(main_ctl)
app.register_blueprint(loginout_ctl)

login_manager = LoginManager()
login_manager.init_app(app)

user_model = UserModel()

@login_manager.user_loader
def user_loader(user_id) -> User:
    return user_model.get_user(user_id)
