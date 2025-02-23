from flask import Blueprint, render_template
from flask import request, session, redirect

from .. import config

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['POST'])
def login():
    if request.form.get('password') == config.admin_password:
        session['logged_in'] = True
    return redirect('/')

@admin_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')
