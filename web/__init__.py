import os
from flask import Flask, render_template
from pony.flask import Pony
from .config import Config
from flask_login import current_user, LoginManager, UserMixin, logout_user
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

    # a simple page that says hello
    @app.route('/hello/')
    @app.route('/hello/<name>')
    def hello(name=None):
        return render_template('hello.html', name=name)

    from web.user_management import user_management
    app.register_blueprint(user_management)

    return app
