import mysql.connector
from mysql.connector import Error
from flask import g, current_app
import logging
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db():
    """Obtener conexión a la base de datos"""
    if 'db' not in g:
        try:
            # Usar configuración de Flask primero, luego variables de entorno, luego defaults
            # Nota: Usar 'in' para password porque puede ser string vacío (válido para XAMPP)
            host = current_app.config.get('MYSQL_HOST') or os.environ.get('MYSQL_HOST', 'localhost')
            user = current_app.config.get('MYSQL_USER') or os.environ.get('MYSQL_USER', 'root')
            password = current_app.config.get('MYSQL_PASSWORD') if 'MYSQL_PASSWORD' in current_app.config else os.environ.get('MYSQL_PASSWORD', '')
            database = current_app.config.get('MYSQL_DATABASE') or os.environ.get('MYSQL_DATABASE', 'contacts_db')
            port = current_app.config.get('MYSQL_PORT') or int(os.environ.get('MYSQL_PORT', 3306))
        
            
            g.db = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port,
                autocommit=True
            )
            logger.info(f"Conexión a MySQL establecida exitosamente (database: {database})")
        except Error as e:
            logger.error(f"Error conectando a MySQL: {e}")
            # Información útil para debugging
            logger.info(f"Intentando conectar con: host={host}, user={user}, database={database}")
            
            # Intentar conexión sin base de datos primero (para crearla)
            try:
                temp_db = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    port=port
                )
                logger.info("Conexión exitosa sin base de datos específica")
                g.db = temp_db
            except Error as e2:
                logger.error(f"No se pudo conectar a MySQL: {e2}")
                raise
    return g.db

def close_db(e=None):
    """Cerrar conexión a la base de datos"""
    db = g.pop('db', None)
    if db is not None:
        db.close()
        logger.info("Conexión a MySQL cerrada")

def init_db(app):
    """Inicializar la base de datos"""
    with app.app_context():
        # Obtener nombre de la base de datos de la configuración
        database = app.config.get('MYSQL_DATABASE') or os.environ.get('MYSQL_DATABASE', 'contacts_db')
        
        # Conectar sin especificar base de datos primero
        host = app.config.get('MYSQL_HOST') or os.environ.get('MYSQL_HOST', 'localhost')
        user = app.config.get('MYSQL_USER') or os.environ.get('MYSQL_USER', 'root')
        password = app.config.get('MYSQL_PASSWORD') if 'MYSQL_PASSWORD' in app.config else os.environ.get('MYSQL_PASSWORD', '')
        port = app.config.get('MYSQL_PORT') or int(os.environ.get('MYSQL_PORT', 3306))
        
        # Crear base de datos si no existe
        try:
            temp_db = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                port=port
            )
            cursor = temp_db.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            temp_db.commit()
            cursor.close()
            temp_db.close()
            logger.info(f"Base de datos '{database}' creada/verificada")
        except Error as e:
            logger.error(f"Error creando base de datos: {e}")
            raise
        
        # Ahora obtener la conexión con la base de datos
        db = get_db()
        cursor = db.cursor()
        
        # Seleccionar la base de datos
        cursor.execute(f"USE {database}")
        
        # Crear tabla de usuarios si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Crear tabla de contactos si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contactos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                correo VARCHAR(100),
                telefono VARCHAR(20),
                detalle TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                INDEX idx_user_id (user_id)
            )
        ''')
        
        db.commit()
        cursor.close()
        logger.info("Tablas creadas/existentes verificadas")