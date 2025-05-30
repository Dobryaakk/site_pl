from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

class User(UserMixin):
    def __init__(self, user_data):
        self.user_data = user_data
        
    def get_id(self):
        return str(self.user_data.get('_id'))
    
    @property
    def is_admin(self):
        return self.user_data.get('role') == 'admin'
    
    @staticmethod
    def create_user(mongo, username, password, role='user'):
        user = {
            'username': username,
            'password': generate_password_hash(password),
            'role': role
        }
        return mongo.db.users.insert_one(user)
    
    @staticmethod
    def get_user(mongo, user_id):
        user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        return User(user_data) if user_data else None
    
    @staticmethod
    def validate_login(mongo, username, password):
        user_data = mongo.db.users.find_one({'username': username})
        if user_data and check_password_hash(user_data['password'], password):
            return User(user_data)
        return None 