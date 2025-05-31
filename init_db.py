from app import create_app, mongo
from app.models.user import User
from config import Config

def init_db():
    app = create_app(Config)
    with app.app_context():
        if not mongo.db.users.find_one({'username': 'admin'}):
            User.create_user(mongo, 'admin', 'admin123', role='admin')
            print("Admin user created successfully!")
        else:
            print("Admin user already exists!")

if __name__ == '__main__':
    init_db() 
