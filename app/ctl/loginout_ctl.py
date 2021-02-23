#login.def
from flask import Blueprint, render_template, flash, redirect, url_for
from flask import session, request
from flask import current_app as app
from flask import jsonify
from flask_ssl import *
from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user, login_required
import json

from app.model.user import User
from app.model.user import USERS

from app.service.user_service import UserService
from app.service.blacklisttoken_service import \
    BlacklistTokenService as BLService
from app.model.blacklisttoken import BlacklistToken
from app.model.blacklisttoken_response import BlacklistTokenResponse


user_service = UserService()
bl_service = BLService()


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
def add_user():
    userid = request.json['userid']
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    ret = user_service.add_user(userid, username, email, password)
    if ret == False:
        json_res = {'ok': False, 'error': 'user <%s> already exists' % userid}
    else:
        json_res = {'ok': True, 'msg': 'user <%s> added' % userid}
    return jsonify(json_res)


@ssl_require
@loginout_ctl.route("/get_user", methods=['POST'])
def get_user():
    userid = request.json['userid']
    ret, user = user_service.get_user(userid)
    if ret == False:
        json_res = {'ok': False, 'error': 'user <%s> does not exist' % userid}
    else:
        json_res = {'ok': True, 'info': '<%s>' % str(user)}
    return jsonify(json_res)


@ssl_require
@loginout_ctl.route("/del_user", methods=['POST'])
def del_user():
    userid = request.json['userid']
    ret = user_service.del_user(userid)
    if ret == False:
        json_res = {'ok': False, 'error': 'user <%s> does not exist' % userid}
    else:
        json_res = {'ok': True, 'msg': 'user <%s> is deleted' % userid}
    return jsonify(json_res)


def create_jwt_token(user: User, user_passwd: str) -> str:
    new_jwt_token = user.login(user_passwd)
    print(f'refresh_jwt_token : type={type(new_jwt_token)}')
    if new_jwt_token != None:
        user.authenticated = False
        user.token = new_jwt_token
        user_service.update_token(user.userid, new_jwt_token)
        login_user(user, remember=True)
        json_res={'ok': True, \
                  'msg': 'user <%s> refreshed' % user.userid,\
                  'token': new_jwt_token.decode('utf-8')}
    else:
        json_res = {'ok': False, 'error': 'Error : invalid password'}
    return json_res


@ssl_require
@loginout_ctl.route('/login', methods=['POST'])
def login():
    userid = request.json['userid']
    user_passwd = request.json['password']

    if 'token' in request.json:
        login_token = request.json['token']
    else:
        login_token = None

    if login_token == None:
        ret, user = user_service.get_user(userid, True)
        if ret == False:
            json_res={'ok': False, 'error': 'Error : not found user'}
        else:
            json_res = create_jwt_token(user, user_passwd)
    else:
        result, userid_sub = User.decode_auth_token(login_token)
        if result == True:
            if bl_service.is_blacklist(login_token):
                json_res={'ok': False, 'msg': 'user <%s> is blocked' %\
                          userid_sub}
            else:
                json_res={'ok': True, 'msg': 'user <%s> logined' % userid_sub}
        else:
            json_res={'ok': False, 'msg': 'user <%s> invalid token' % userid}

    print(f'{json_res}')
    return jsonify(json_res)


@ssl_require
@loginout_ctl.route('/logout', methods=['POST'])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    print(f'logout => userid={user.userid}, token={user.token}')
    ret = bl_service.add_blacklist(user.token)
    user.token = ''
    json_res = {'ok': True, 'msg': 'user <%s> logout' % user.userid}
    logout_user()
    print(f'{json_res}')
    return jsonify(json_res)


@ssl_require
@loginout_ctl.route("/add_blacklist", methods=['POST'])
def add_blacklist():
    token = request.json['token']
    ret = bl_service.add_blacklist(token)
    if ret == False:
        json_res = {'ok': False, 'error': 'token <%s> already exists' % token}
    else:
        json_res = {'ok': True, 'msg': 'token <%s> added' % token}
    return jsonify(json_res)


@ssl_require
@loginout_ctl.route("/is_blacklist", methods=['POST'])
def is_balcklist():
    token = request.json['token']
    ret = bl_service.is_blacklist(token)
    if ret == False:
        json_res = {'ok': False, 'error': 'token <%s> does not exist' % token}
    else:
        json_res = {'ok': True, 'msg': 'token <%s> is registered' % str(token)}
    return jsonify(json_res)


@ssl_require
@loginout_ctl.route("/del_blacklist", methods=['POST'])
def del_blacklist():
    token = request.json['token']
    ret = bl_service.del_blacklist(token)
    if ret == False:
        json_res = {'ok': False, 'error': 'token <%s> does not exist' % token}
    else:
        json_res = {'ok': True, 'msg': 'token <%s> is deleted' % token}
    return jsonify(json_res)


@ssl_require
@loginout_ctl.route("/get_all_blacklist", methods=['POST'])
def get_all_blacklist():
    ret, lists = bl_service.get_all_blacklist()
    if ret == False:
        return jsonify({'ok': False, 'error': 'does not have registered token'})

    return BlacklistTokenResponse(ret, lists).toJson()
