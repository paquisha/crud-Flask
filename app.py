from flask import Flask
from flask_session import Session
from controllers import auth_controller, contact_controller
import os
import sys

# Configuración básica para evitar el error de sesión
class BaseConfig:
    # Asegurar que SECRET_KEY sea siempre string, nunca bytes
    SECRET_KEY = str(os.environ.get('SECRET_KEY', 'dev-key-segura-para-flask-session-2024'))
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = False  # Deshabilitado temporalmente para evitar error de bytes
    SESSION_KEY_PREFIX = 'contactos_'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hora en segundos
    # Configuración adicional para evitar problemas con bytes
    SESSION_COOKIE_NAME = 'session'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configuración de MySQL (ajusta según tu instalación)
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''  # Para XAMPP/WAMP normalmente vacío
    MYSQL_DATABASE = 'contactos_app'
    MYSQL_PORT = 3306

def create_app():
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Cargar configuración básica primero
    app.config.from_object(BaseConfig)
    
    # Intentar cargar configuración personalizada si existe
    try:
        from config_auto import Config as AutoConfig
        app.config.from_object(AutoConfig)
        print("✅ Usando configuración automática")
    except ImportError:
        try:
            from config import Config as FileConfig
            app.config.from_object(FileConfig)
            print("✅ Usando configuración del archivo")
        except ImportError:
            print("⚠️  Usando configuración básica")
            print("💡 Para configuración personalizada, ejecuta: python setup_database.py")
    
    # Asegurar que SECRET_KEY sea siempre string (nunca bytes)
    if isinstance(app.config.get('SECRET_KEY'), bytes):
        app.config['SECRET_KEY'] = app.config['SECRET_KEY'].decode('utf-8')
    elif app.config.get('SECRET_KEY') is None:
        app.config['SECRET_KEY'] = 'dev-key-segura-para-flask-session-2024'
    else:
        app.config['SECRET_KEY'] = str(app.config['SECRET_KEY'])
    
    # Mostrar configuración
    print(f"\n🔧 Configuración MySQL:")
    print(f"   Host: {app.config.get('MYSQL_HOST')}")
    print(f"   Usuario: {app.config.get('MYSQL_USER')}")
    print(f"   Base de datos: {app.config.get('MYSQL_DATABASE')}")
    
    # Configurar Flask-Session ANTES de inicializar la base de datos
    # Esto es clave para evitar el error
    Session(app)
    
    # Importar después de configurar la sesión
    from models.database import init_db
    
    try:
        # Inicializar base de datos
        init_db(app)
        print("✅ Base de datos inicializada correctamente")
    except Exception as e:
        print(f"\n❌ Error inicializando base de datos: {e}")
        print("\n💡 SOLUCIONES:")
        print("1. Asegúrate que MySQL esté corriendo")
        print("2. Ejecuta: python setup_database.py")
        print("3. Verifica credenciales")
        raise
    
    # Registrar blueprints
    app.register_blueprint(auth_controller.bp)
    app.register_blueprint(contact_controller.bp)
    
    # Ruta principal
    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('auth.login'))
    
    return app

if __name__ == '__main__':
    app = create_app()
    print(f"\n🚀 Aplicación Flask iniciada")
    print("   🌐 Local: http://localhost:5000")
    print("   👤 Login: http://localhost:5000/auth/login")
    app.run(host='0.0.0.0', port=5000, debug=False)  # debug=False para evitar problemas