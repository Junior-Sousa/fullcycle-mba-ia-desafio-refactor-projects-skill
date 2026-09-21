import os

class Settings:
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key-123')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///tasks.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_USER = os.getenv('SMTP_USER', 'taskmanager@gmail.com')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', 'senha123')

settings = Settings()
