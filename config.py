import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    password = quote_plus(os.getenv('DB_PASS'))
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
