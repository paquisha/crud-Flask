#!/usr/bin/env python3
"""
Script para ejecutar la aplicación Flask y exponerla con ngrok
"""

from flask import Flask
from pyngrok import ngrok
import threading
import time
import os
import sys

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_ngrok_tunnel(port=5000):
    """
    Crear un túnel ngrok para la aplicación Flask
    
    Args:
        port (int): Puerto donde corre la aplicación Flask
        
    Returns:
        str: URL pública de ngrok
    """
    try:
        # Configurar ngrok (opcional: agregar token de autenticación)
        # ngrok.set_auth_token("tu_token_ngrok")
        
        # Crear el túnel
        print(f"🚀 Iniciando túnel ngrok en puerto {port}...")
        public_url = ngrok.connect(port).public_url
        print(f"✅ Túnel ngrok creado exitosamente!")
        print(f"🌐 URL pública: {public_url}")
        print(f"🔗 URL local: http://localhost:{port}")
        print("\n📋 Información del túnel:")
        print(f"   • Usa {public_url}/auth/login para acceder a la aplicación")
        print(f"   • Para detener: Ctrl + C")
        print("=" * 50)
        
        return public_url
    except Exception as e:
        print(f"❌ Error al crear túnel ngrok: {e}")
        return None

def run_flask_app():
    """
    Ejecutar la aplicación Flask
    """
    try:
        from app import create_app
        
        app = create_app()
        
        # Configurar para que Flask se ejecute en el puerto correcto
        print("🚀 Iniciando aplicación Flask...")
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,  # False para producción con ngrok
            threaded=True
        )
    except Exception as e:
        print(f"❌ Error al ejecutar Flask: {e}")

def main():
    """
    Función principal que ejecuta Flask y ngrok simultáneamente
    """
    print("=" * 50)
    print("🔧 CONFIGURACIÓN DE APLICACIÓN FLASK CON NGROK")
    print("=" * 50)
    
    # Verificar dependencias
    try:
        import flask
        import mysql.connector
        from werkzeug.security import generate_password_hash
        print("✅ Todas las dependencias están instaladas")
    except ImportError as e:
        print(f"❌ Faltan dependencias: {e}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return
    
    # Crear hilo para Flask
    flask_thread = threading.Thread(target=run_flask_app, daemon=True)
    flask_thread.start()
    
    # Esperar a que Flask se inicie
    print("⏳ Esperando que Flask se inicie...")
    time.sleep(3)
    
    # Crear túnel ngrok
    ngrok_url = create_ngrok_tunnel(5000)
    
    if not ngrok_url:
        print("❌ No se pudo crear el túnel ngrok")
        return
    
    try:
        # Mantener el script ejecutándose
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Deteniendo aplicación...")
        ngrok.kill()
        print("✅ Aplicación detenida correctamente")
        sys.exit(0)

if __name__ == "__main__":
    # Verificar si pyngrok está instalado
    try:
        from pyngrok import ngrok
    except ImportError:
        print("❌ pyngrok no está instalado")
        print("💡 Instálalo con: pip install pyngrok")
        print("\n💡 Alternativa: Ejecuta solo Flask con: python app.py")
        
        # Preguntar si quiere instalar pyngrok
        respuesta = input("\n¿Quieres instalar pyngrok ahora? (s/n): ")
        if respuesta.lower() == 's':
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyngrok"])
            print("\n✅ pyngrok instalado. Reinicia este script.")
        else:
            print("\n💡 Para ejecutar solo Flask: python app.py")
        sys.exit(1)
    
    main()