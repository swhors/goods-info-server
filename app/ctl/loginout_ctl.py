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
    json_res = {'ok': True, 'msg': 'auth_func(%s),userid=%s'
                                   % (request.json, user.userid)}
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
    userid = request.json['userid']
    passwd_hash = request.json['passwd_hash']
    if userid in USERS:
        json_res = {'ok': False, 'error': 'user <%s> already exists' % userid}
    else:
        user = User(userid, passwd_hash)
        USERS[userid] = user
        json_res = {'ok': True, 'msg': 'user <%s> added' % userid}
    return jsonify(json_res)


@ssl_require
@loginout_ctl.route('/login', methods=['POST'])
def login():
    userid = request.json['userid']
    passwd_hash = request.json['passwd_hash']
    if userid not in USERS:
        json_res={'ok': False, 'error': 'Error : not found user'}
    elif not USERS[userid].can_login(passwd_hash):
        json_res = {'ok': False, 'error': 'Error : invalid password'}
    else:
        json_res={'ok': True, 'msg': 'user <%s> logined' % userid}

        USERS[userid].authenticated = True
        login_user(USERS[userid], remember=True)
    print(f'{json_res}')
    return jsonify(json_res)


@ssl_require
@loginout_ctl.route('/logout', methods=['POST'])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    json_res = {'ok': True, 'msg': 'user <%s> logout' % user.userid}
    logout_user()
    print(f'{json_res}')
    return jsonify(json_res)
