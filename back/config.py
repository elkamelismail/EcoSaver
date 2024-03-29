from dotenv import load_dotenv
import os
import redis

load_dotenv()

class ApplicationConfig:
    """
    Application configuration class
    """
    
    SECRET_KEY = os.getenv('SECRET_KEY')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = r'sqlite:///./db.sqlite'

    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url(os.getenv('REDIS_URL'))
