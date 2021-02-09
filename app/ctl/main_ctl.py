# app/main/main.py

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app

main_ctl=Blueprint('main_ctl', __name__, url_prefix='/main')

@main_ctl.route('/', methods=['GET'])
def index():
    return render_template('/main/index.html')

@main_ctl.route('/about', methods=['GET'])
def about():
    return 'Hello Goods V0.1'
