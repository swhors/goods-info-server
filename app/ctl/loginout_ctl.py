#login.def
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app
from flask import jsonify
from flask_ssl import *
from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user, login_required
import json

from app.model.user import User
from app.model.user import USERS

loginout_ctl=Blueprint('loginout_ctl', __name__, url_prefix='/auth')


@ssl_require
@loginout_ctl.route("/auth_func", methods=['POST'])
@login_required
def auth_func():
    user = current_user
    json_res = {'ok': True, 'msg': 'auth_func(%s),user_id=%s'
                                   % (request.json, user.user_id)}
    return jsonify(json_res)


@ssl_require
@loginout_ctl.route("/notauth_func", methods=['POST'])
def notauth_func():
    json_res = {'ok': True, 'msg': 'notauth_func(%s)'
                                   % request.json}
    return jsonify(json_res)


@ssl_require
@loginout_ctl.route("/add_user", methods=['POST'])
def addUser():
    user_id = request.json['user_id']
    passwd_hash = request.json['passwd_hash']
    if user_id in USERS:
        json_res = {'ok': False, 'error': 'user <%s> already exists' % user_id}
    else:
        user = User(user_id, passwd_hash)
        USERS[user_id] = user
        json_res = {'ok': True, 'msg': 'user <%s> added' % user_id}
    return jsonify(json_res)


@ssl_require
@loginout_ctl.route('/login', methods=['POST'])
def login():
    user_id = request.json['user_id']
    passwd_hash = request.json['passwd_hash']
    if user_id not in USERS:
        json_res={'ok': False, 'error': 'Error : not found user'}
    elif not USERS[user_id].can_login(passwd_hash):
        json_res = {'ok': False, 'error': 'Error : invalid password'}
    else:
        json_res={'ok': True, 'msg': 'user <%s> logined' % user_id}

        USERS[user_id].authenticated = True
        login_user(USERS[user_id], remember=True)
    print(f'{json_res}')
    return jsonify(json_res)


@ssl_require
@loginout_ctl.route('/logout', methods=['POST'])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    json_res = {'ok': True, 'msg': 'user <%s> logout' % user.user_id}
    logout_user()
    print(f'{json_res}')
    return jsonify(json_res)
