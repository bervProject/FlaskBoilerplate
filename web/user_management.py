from flask import Blueprint, request, render_template, redirect, current_app, flash
from flask_login import login_user, logout_user, login_required
from pony.orm import flush
from datetime import datetime
from web.model import db

user_management = Blueprint('user_management', __name__, template_folder='templates')

@user_management.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      possible_user = db.User.get(login=username)
      if not possible_user:
        flash('Wrong username')
        return redirect('/login')
      if possible_user.password == password:
        possible_user.last_login = datetime.now()
        login_user(possible_user)
        return redirect('/')
      flash('Wrong password')
      return redirect('/login')
  else:
      return render_template('login.html')

@user_management.route('/reg', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    exist = db.User.get(login=username)
    if exist:
      flash('Username %s is already taken, choose another one' % username)
      return redirect('/reg')

    user = db.User(login=username, password=password)
    user.last_login = datetime.now()
    flush()
    login_user(user)
    flash('Successfully registered')
    return redirect('/')
  else:
    return render_template('reg.html')

@user_management.route('/logout')
@login_required
def logout():
  logout_user()
  flash('Logged out')
  return redirect('/')
