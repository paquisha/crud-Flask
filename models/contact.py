from models.database import get_db
from models.user import User
import re

class Contact:
    def __init__(self, id=None, user_id=None, nombre=None, correo=None, telefono=None, detalle=None, fecha_creacion=None):
        self.id = id
        self.user_id = user_id
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.detalle = detalle
        self.fecha_creacion = fecha_creacion
    
    @staticmethod
    def validate_email(email):
        """Validar formato de email (opcional)"""
        if not email:
            return True
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate(self):
        """Validar datos del contacto"""
        errors = []
        
        if not self.nombre or not self.nombre.strip():
            errors.append("El nombre es obligatorio")
        
        if self.correo and not self.validate_email(self.correo):
            errors.append("El email no tiene un formato válido")
        
        return errors
    
    @staticmethod
    def get_by_id(contact_id, user_id):
        """Obtener contacto por ID (solo si pertenece al usuario)"""
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute('''
            SELECT * FROM contactos 
            WHERE id = %s AND user_id = %s
        ''', (contact_id, user_id))
        contact_data = cursor.fetchone()
        cursor.close()
        
        if contact_data:
            return Contact(**contact_data)
        return None
    
    @staticmethod
    def get_all_by_user(user_id):
        """Obtener todos los contactos de un usuario"""
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute('''
            SELECT * FROM contactos 
            WHERE user_id = %s 
            ORDER BY nombre
        ''', (user_id,))
        contacts_data = cursor.fetchall()
        cursor.close()
        
        contacts = []
        for data in contacts_data:
            contacts.append(Contact(**data))
        return contacts
    
    def save(self):
        """Guardar contacto (crear o actualizar)"""
        errors = self.validate()
        if errors:
            return False, errors
        
        db = get_db()
        cursor = db.cursor()
        
        if self.id:
            # Actualizar contacto existente
            cursor.execute('''
                UPDATE contactos 
                SET nombre = %s, correo = %s, telefono = %s, detalle = %s
                WHERE id = %s AND user_id = %s
            ''', (self.nombre, self.correo, self.telefono, self.detalle, self.id, self.user_id))
        else:
            # Crear nuevo contacto
            cursor.execute('''
                INSERT INTO contactos (user_id, nombre, correo, telefono, detalle)
                VALUES (%s, %s, %s, %s, %s)
            ''', (self.user_id, self.nombre, self.correo, self.telefono, self.detalle))
            self.id = cursor.lastrowid
        
        db.commit()
        cursor.close()
        return True, None
    
    def delete(self):
        """Eliminar contacto"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM contactos WHERE id = %s AND user_id = %s', 
                      (self.id, self.user_id))
        db.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        return affected_rows > 0
    
    def to_dict(self):
        """Convertir contacto a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'nombre': self.nombre,
            'correo': self.correo,
            'telefono': self.telefono,
            'detalle': self.detalle,
            'fecha_creacion': self.fecha_creacion
        }