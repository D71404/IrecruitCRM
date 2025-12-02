from flask_migrate import Migrate, upgrade
from models.db_models import app, db

migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        upgrade()