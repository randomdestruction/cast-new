from flask import Flask
from config import config
from app.extensions import bootstrap, login_manager, moment

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])

	# Register our blueprints
	from .cast import cast as cast_blueprint
	from .auth import auth as auth_blueprint
	from .api_1_0 import api as api_blueprint
	app.register_blueprint(cast_blueprint)
	app.register_blueprint(auth_blueprint, url_prefix='/auth')
	app.register_blueprint(api_blueprint, url_prefix='/api/1.0')

	# Initialize any extensions we are using
	bootstrap.init_app(app)
	login_manager.init_app(app)
	moment.init_app(app)

	return app