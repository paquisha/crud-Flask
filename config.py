import os
from datetime import timedelta

class Config:
    # Configuración básica - IMPORTANTE: Usar string, no bytes
    # Asegurar que siempre sea string, incluso si viene de variable de entorno
    _secret_key = os.environ.get('SECRET_KEY') or 'dev-secret-key-flask-2024-string-not-bytes'
    SECRET_KEY = str(_secret_key) if _secret_key else 'dev-secret-key-flask-2024-string-not-bytes'
    
    # Configuración de Flask-Session
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = False  # Deshabilitado temporalmente para evitar error de bytes
    SESSION_KEY_PREFIX = 'contactos_'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    # Configuración adicional para evitar problemas con bytes
    SESSION_COOKIE_NAME = 'session'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configuración de MySQL
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '1234567890')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'contacts_db')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    
    # Configuración de la aplicación
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'