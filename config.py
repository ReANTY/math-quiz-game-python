import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    
    # MySQL Database Configuration for Laragon (Local Development)
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_PORT = os.environ.get('MYSQL_PORT') or 3306
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or ''  # Default Laragon MySQL password is empty
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or 'quiz_game_db'
    
    # SQLAlchemy Database URI for local MySQL
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@"
        f"{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    )

class ProductionConfig(Config):
    DEBUG = False
    
    # Check if Azure Database for MySQL is configured
    azure_mysql_host = os.environ.get('AZURE_MYSQL_HOST')
    azure_mysql_user = os.environ.get('AZURE_MYSQL_USER') 
    azure_mysql_password = os.environ.get('AZURE_MYSQL_PASSWORD')
    azure_mysql_database = os.environ.get('AZURE_MYSQL_DATABASE')
    
    if azure_mysql_host and azure_mysql_user and azure_mysql_password:
        # Use Azure Database for MySQL
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{azure_mysql_user}:{azure_mysql_password}@"
            f"{azure_mysql_host}:3306/{azure_mysql_database}?charset=utf8mb4"
        )
    else:
        # Fallback to SQLite for Azure App Service (if MySQL not configured)
        basedir = '/home/site/wwwroot'
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'quiz_game.db')

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 