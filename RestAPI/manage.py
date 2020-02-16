""" Migrate Script """

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from run import app
from api.users.models import DB

migrate = Migrate(app, DB)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
