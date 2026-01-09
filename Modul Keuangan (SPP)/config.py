import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""

    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'

    # Database configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///billing.db')

    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG

    # Webhook security
    WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'webhook-secret-key')

    # Scheduler configuration
    SCHEDULER_TIMEZONE = os.getenv('SCHEDULER_TIMEZONE', 'Asia/Jakarta')

    # Application settings
    BILLING_PROGRAMS = {
        'Teknik': 5000000,  # 5 million IDR
        'Ekonomi': 4000000  # 4 million IDR
    }

    # Semester start months (1-based)
    SEMESTER_START_MONTHS = [1, 7]  # January and July
