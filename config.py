import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'generate-a-secure-key-here')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/topstaff')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Security settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Rate limiting
    RATELIMIT_DEFAULT = "100 per day"
    RATELIMIT_STORAGE_URL = "memory://"
    
    # CSRF Protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hour
