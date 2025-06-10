import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    
    # MySQL Database Configuration for Laragon
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_PORT = os.environ.get('MYSQL_PORT') or 3306
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or ''  # Default Laragon MySQL password is empty
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or 'quiz_game_db'
    
    # SQLAlchemy Database URI
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@"
        f"{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # For Azure deployment, fallback to SQLite if MySQL not available
    if os.environ.get('WEBSITE_SITE_NAME'):
        basedir = '/home/site/wwwroot'
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'quiz_game.db')

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 