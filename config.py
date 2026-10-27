import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base application configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'hotel_management_secret_key_mca_2026_dev')
    
    # Database configuration
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/hotel_management')
    MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', 'hotel_management')
    
    # Cloudinary Cloud Storage Configuration
    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME', '')
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY', '')
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET', '')
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload limit
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'pdf'}
    
    # GST Rate (18%)
    GST_RATE = 0.18
    
    # Flask-WTF CSRF Setting
    WTF_CSRF_ENABLED = True
