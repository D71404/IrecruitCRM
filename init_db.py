from flask_migrate import Migrate, init, migrate, upgrade
from models.db_models import app, db
import os

def init_database():
    # Ensure migrations directory exists
    if not os.path.exists('migrations'):
        print("Initializing migrations directory...")
        with app.app_context():
            init()
    
    print("Creating new migration...")
    with app.app_context():
        migrate(message='Initial database setup')
    
    print("Applying migration...")
    with app.app_context():
        upgrade()

if __name__ == '__main__':
    init_database()
