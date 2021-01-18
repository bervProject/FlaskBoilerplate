import os
from flask import Flask, render_template, request, redirect, flash
from pony.flask import Pony
from pony.orm import flush
from .config import Config
from flask_login import current_user, LoginManager, UserMixin, login_user, login_required, logout_user
from datetime import datetime
from web.model import db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'random-key')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(Config)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.bind(**app.config['PONY'])
    db.generate_mapping(create_tables=True)

    Pony(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return db.User.get(id=user_id)

    @app.route('/')
    def index():
        users = db.User.select()
        return render_template('index.html', user=current_user, users=users)

    @app.route('/login', methods=['GET', 'POST'])
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

    @app.route('/reg', methods=['GET', 'POST'])
    def reg():
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

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Logged out')
        return redirect('/')

    # a simple page that says hello
    @app.route('/hello/')
    @app.route('/hello/<name>')
    def hello(name=None):
        return render_template('hello.html', name=name)

    return app
