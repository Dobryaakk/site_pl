import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'hui')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/topstaff')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    RATELIMIT_DEFAULT = "100 per day"
    RATELIMIT_STORAGE_URL = "memory://"
    
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
