from werkzeug.security import generate_password_hash, check_password_hash
from models.database import get_db
import re

class User:
    def __init__(self, id=None, nombre=None, email=None, password_hash=None, fecha_creacion=None):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password_hash = password_hash
        self.fecha_creacion = fecha_creacion
    
    @staticmethod
    def validate_email(email):
        """Validar formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password):
        """Validar contraseña (mínimo 8 caracteres)"""
        return len(password) >= 8
    
    def set_password(self, password):
        """Generar hash de contraseña"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verificar contraseña"""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def get_by_id(user_id):
        """Obtener usuario por ID"""
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE id = %s', (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        
        if user_data:
            return User(**user_data)
        return None
    
    @staticmethod
    def get_by_email(email):
        """Obtener usuario por email"""
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        user_data = cursor.fetchone()
        cursor.close()
        
        if user_data:
            return User(**user_data)
        return None
    
    @staticmethod
    def create(nombre, email, password):
        """Crear nuevo usuario"""
        if not User.validate_email(email):
            return None, "Email inválido"
        
        if not User.validate_password(password):
            return None, "La contraseña debe tener al menos 8 caracteres"
        
        # Verificar si el email ya existe
        if User.get_by_email(email):
            return None, "El email ya está registrado"
        
        user = User()
        user.nombre = nombre
        user.email = email
        user.set_password(password)
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO usuarios (nombre, email, password_hash)
            VALUES (%s, %s, %s)
        ''', (user.nombre, user.email, user.password_hash))
        
        user.id = cursor.lastrowid
        db.commit()
        cursor.close()
        
        return user, None
    
    def to_dict(self):
        """Convertir usuario a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'fecha_creacion': self.fecha_creacion
        }