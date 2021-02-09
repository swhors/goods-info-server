# app/__init__.py

from flask import Flask
from app.ctl.main_ctl import main_ctl
from app.ctl.goods_ctl import goods_ctl

app=Flask(__name__)
print("name =", __name__)

app.register_blueprint(goods_ctl)
app.register_blueprint(main_ctl)
