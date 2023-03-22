import os
from app import create_app
from flask_script import Manager
from app.extensions import db, migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
db.init_app(app)
migrate.init_app(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
if __name__ == '__main__':
	manager.run()
